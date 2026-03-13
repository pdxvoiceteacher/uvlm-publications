# Universal PDE Grammar Implementation

Below are the key code components to turn the universal PDE grammar into a runnable pipeline. It includes:

- Typed AST classes for operators/expressions (no free-form strings)
- An operator registry with metadata (inputs, locality, type, etc.)
- A revised corridor update that applies contributions from each operator
- Enforcement of derived-field recomputation and governance at compile/runtime

These Python snippets illustrate the structure of the grammar engine. (You would of course integrate them into the existing bridge modules.)

```python
# File: python/src/coherence/bridge/pde_grammar.py

from dataclasses import dataclass
from typing import List, Dict, Union

# --- AST Node Classes ---

@dataclass
class Expr:
    """Base class for expression AST nodes."""
    pass

@dataclass
class FieldExpr(Expr):
    field: str

@dataclass
class ConstExpr(Expr):
    value: float

@dataclass
class AddExpr(Expr):
    left: Expr
    right: Expr

@dataclass
class MulExpr(Expr):
    left: Expr
    right: Expr

@dataclass
class DivExpr(Expr):
    left: Expr
    right: Expr

# Example: Psi = E * T expressed as AST
psi_expr = MulExpr(FieldExpr("E"), FieldExpr("T"))


# --- Operator Registry and Metadata ---

@dataclass
class OperatorSpec:
    name: str
    inputs: List[str]         # e.g. ["C"]
    outputs: List[str]        # e.g. ["C"]
    locality: str            # e.g. "edge-local", "node-local", "global"
    op_type: str             # e.g. "diffusion", "advection", "source", "sink"
    governance: str          # e.g. "safe", "risky"
    # Additional flags as needed...

# Example registry of built-in operators
OPERATOR_REGISTRY: Dict[str, OperatorSpec] = {
    "graph_diffusion": OperatorSpec(
        name="graph_diffusion",
        inputs=["C"], outputs=["C"],
        locality="edge-local",
        op_type="diffusion",
        governance="safe"
    ),
    "advective_flux": OperatorSpec(
        name="advective_flux",
        inputs=["C","Theta"], outputs=["C"],
        locality="edge-local",
        op_type="advection",
        governance="safe"
    ),
    "gradient_source": OperatorSpec(
        name="gradient_source",
        inputs=["Theta"], outputs=["C"],
        locality="edge-local",
        op_type="source",
        governance="safe"
    ),
    "theta_time_source": OperatorSpec(
        name="theta_time_source",
        inputs=["Theta_dot"], outputs=["C"],
        locality="node-local",
        op_type="source",
        governance="safe"
    ),
    # ... add other operators like sinks, coupling, etc.
}


# --- PDE Grammar Executor (Simplified) ---

def apply_operator(spec: OperatorSpec, state: Dict[str, Dict[str,float]]) -> Dict[str, Dict[str,float]]:
    """
    Apply one operator to the entire graph field state.
    Returns contributions to the output fields.
    """
    contributions = {field: {} for field in spec.outputs}
    # For demonstration, handle each op_type explicitly:
    if spec.op_type == "diffusion":
        # e.g. graph Laplacian on field C -> delta C
        C = state["C"]
        adj = state["adjacency"]  # WeightedGraph adjacency
        lap = {}
        for i, nbrs in adj.items():
            c_val = C.get(i, 0.0)
            # Compute graph Laplacian L*C
            deg = sum(w for (_, w) in nbrs)
            s = deg * c_val
            for (j, w) in nbrs:
                s -= w * C.get(j, 0.0)
            lap[i] = s
        contributions["C"] = lap

    elif spec.op_type == "advection":
        # e.g. -div(C * grad Theta)
        Theta = state["Theta"]
        C = state["C"]
        adj = state["adjacency"]
        div_flux = {}
        for i, nbrs in adj.items():
            s = 0.0
            Ci = C.get(i, 0.0)
            for (j, w) in nbrs:
                Cj = C.get(j, 0.0)
                avg_c = 0.5 * (Ci + Cj)
                diff = Theta.get(j, 0.0) - Theta.get(i, 0.0)
                flux = w * avg_c * diff
                s += flux
            div_flux[i] = -s  # note the negative sign for divergence term
        contributions["C"] = div_flux

    elif spec.op_type == "source":
        # e.g. |∇Theta|^2
        Theta = state["Theta"]
        adj = state["adjacency"]
        src = {}
        for i, nbrs in adj.items():
            sum_sq = 0.0
            for (j, w) in nbrs:
                diff = Theta.get(j, 0.0) - Theta.get(i, 0.0)
                sum_sq += w * (diff * diff)
            src[i] = sum_sq
        contributions["C"] = src

    elif spec.op_type == "time_deriv":
        # e.g. Theta_dot contribution
        Theta_dot = state["Theta_dot"]
        contrib = {}
        for i, val in Theta_dot.items():
            contrib[i] = max(val, 0.0)  # positive part
        contributions["C"] = contrib

    # (Add other operator implementations as needed...)

    return contributions


def step_pde(state: Dict[str, Dict[str,float]], dt: float, weights: Dict[str,float]) -> Dict[str, Dict[str,float]]:
    """
    Perform one PDE step: sum contributions, apply Euler update, and enforce governance.
    'weights' contains coefficients like D, alpha, beta, mu, nu, chi, etc.
    """
    # Collect contributions
    total_deltas = {field: {} for field in state["fields"].keys()}
    for name, spec in OPERATOR_REGISTRY.items():
        contribs = apply_operator(spec, state)
        coeff = 1.0
        if name == "graph_diffusion":
            coeff = weights["D"]
        elif name == "advective_flux":
            coeff = 1.0
        elif name == "gradient_source":
            coeff = weights["alpha"]
        elif name == "theta_time_source":
            coeff = weights["beta"]
        # ... match operators to coefficients ...

        # Accumulate
        for field, delta_map in contribs.items():
            for node, delta in delta_map.items():
                total_deltas[field][node] = total_deltas[field].get(node, 0.0) + coeff * delta

    # Apply damping sinks (as negative contributions)
    C = state["C"]
    deltaS = state.get("DeltaS", {})
    Lambda = state.get("Lambda", {})
    mu = weights["mu"]; nu = weights["nu"]; chi = weights["chi"]
    for i, Ci in C.items():
        decay = mu * Ci
        suppress = nu * (max(deltaS.get(i,0),0) + max(Lambda.get(i,0),0)) * Ci
        saturation = chi * (Ci**3)
        total = total_deltas.setdefault("C", {})
        total[i] = total.get(i, 0.0) - (decay + suppress + saturation)

    # Euler integrate and clamp [0,1]
    newC = {}
    for i, Ci in C.items():
        dC = total_deltas["C"].get(i, 0.0)
        Ci_new = max(0.0, min(1.0, Ci + dt * dC))
        newC[i] = Ci_new

    # Assemble new state
    new_state = state.copy()
    new_state["C"] = newC

    # Governance projection: clamp any forbidden fields (example)
    # (In practice this should use UCC/audit logic)
    # e.g., ensure C remains [0,1], etc.

    return new_state
```

## Explanation of key parts

- AST classes (`FieldExpr`, `MulExpr`, etc.) ensure derived-field formulas are structured, not raw strings.
- The operator registry (`OPERATOR_REGISTRY`) lists named operators with their input/output fields, locality, type, and governance class.
- `apply_operator` computes each operator’s contribution. Here we implemented diffusion (`graph_diffusion`), advection (`advective_flux`), gradient-source, and time-derivative source as examples.
- `step_pde` sums weighted contributions, applies sinks (decay/entropy), integrates with Euler, and clamps to `[0,1]`. After integration, a governance step (`Π_UCC/audit`) should enforce admissibility.

This skeleton demonstrates the kernel compiler and execution engine in action.

A real implementation would:

- Use these operator specs to parse and validate a JSON PDE spec (reject forbidden combos, check derived fields).
- Recompute derived fields (like `Ψ`, etc.) after each step (so they aren’t directly edited by operators).
- Support additional operators (reversible Hamiltonian, nonlocal coupling, etc.) per the meta-kernel grammar.
- Perform a canonicalization pass (hashing, normalization of the operator graph).

## Summary

With these code components, the triadic brain can instantiate arbitrary admissible PDEs by composing operators from the registry rather than writing raw formulas, achieving the “universal grammar” vision.
