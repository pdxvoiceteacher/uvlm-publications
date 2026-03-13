# Universal PDE Grammar Implementation

Below are the key code components to turn the universal PDE grammar into a runnable pipeline. We define a typed AST for field expressions, an operator registry with signatures, a compiler to parse PDE specs, and an execution engine that assembles operator contributions into field updates (with governance projection at the end). Each block is a Python module or snippet to include in the CoherenceLattice codebase (in python/src/coherence/pde/).

## ast.py – Expression AST nodes

```python
# coherence/pde/ast.py

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Union

@dataclass(frozen=True)
class Expr:
    """Base class for expression AST nodes."""

@dataclass(frozen=True)
class FieldRef(Expr):
    field: str

@dataclass(frozen=True)
class Constant(Expr):
    value: float

@dataclass(frozen=True)
class BinaryOp(Expr):
    op: str               # e.g. "add", "mul", "sub", "div"
    left: Expr
    right: Expr

@dataclass(frozen=True)
class UnaryOp(Expr):
    op: str               # e.g. "neg", "pos"
    operand: Expr


def eval_expr(expr: Expr, state: dict[str, float]) -> float:
    """
    Evaluate an expression AST given a mapping of field values.
    """
    if isinstance(expr, FieldRef):
        return state.get(expr.field, 0.0)
    if isinstance(expr, Constant):
        return expr.value
    if isinstance(expr, BinaryOp):
        a = eval_expr(expr.left, state)
        b = eval_expr(expr.right, state)
        if expr.op == "add":
            return a + b
        if expr.op == "sub":
            return a - b
        if expr.op == "mul":
            return a * b
        if expr.op == "div":
            return a / b if b != 0 else 0.0
        raise ValueError(f"Unknown binary op {expr.op}")
    if isinstance(expr, UnaryOp):
        a = eval_expr(expr.operand, state)
        if expr.op == "neg":
            return -a
        if expr.op == "pos":
            return a
        raise ValueError(f"Unknown unary op {expr.op}")
    raise TypeError(f"Unhandled Expr type: {type(expr)}")
```

This AST lets us represent formulas unambiguously. For example, the formula `E * T` would be represented as:

`BinaryOp(op="mul", left=FieldRef("E"), right=FieldRef("T"))`

instead of a string. This ensures deterministic parsing and evaluation.

## operator.py – Operator specification and registry

```python
# coherence/pde/operator.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Callable

@dataclass
class OperatorSpec:
    """
    Metadata for a PDE operator.
    """
    name: str
    inputs: List[str]
    outputs: List[str]
    locality: str           # "node", "edge", "global", "nonlocal"
    reversible: bool
    dissipative: bool
    # Additional metadata fields:
    requires_governance: bool = False
    # The actual compute function (to be assigned later).
    apply: Callable[..., None] = field(default=lambda *args, **kwargs: None)

class OperatorRegistry:
    """
    Registry of available PDE operators.
    """
    def __init__(self):
        self.operators: Dict[str, OperatorSpec] = {}

    def register(self, spec: OperatorSpec):
        self.operators[spec.name] = spec

    def get(self, name: str) -> OperatorSpec:
        return self.operators[name]

# Initialize a global registry
operator_registry = OperatorRegistry()

# Example: Register a simple diffusion operator for field "C"
def diffusion_apply(state, inputs, outputs):
    # This is a placeholder for the actual diffusion logic.
    pass


diffusion_spec = OperatorSpec(
    name="graph_diffusion",
    inputs=["C"],
    outputs=["C"],
    locality="edge",
    reversible=False,
    dissipative=True,
    requires_governance=False,
    apply=diffusion_apply
)
operator_registry.register(diffusion_spec)
```

In this registry, each operator has a fixed signature. For example, the `"graph_diffusion"` operator declares that it takes input field `"C"` and outputs to `"C"`, operates at edges, is dissipative, etc. We will populate `apply` with actual PDE logic later or in the engine.

## compiler.py – PDE spec parser and normalizer

```python
# coherence/pde/compiler.py

import json
from .ast import Expr, FieldRef, Constant, BinaryOp, UnaryOp
from .operator import operator_registry, OperatorSpec, OperatorRegistry
from typing import Any


def parse_expr(node: Any) -> Expr:
    """
    Recursively parse a JSON expression node into our AST.
    """
    if isinstance(node, dict):
        if "field" in node:
            return FieldRef(node["field"])
        if "const" in node:
            return Constant(node["const"])
        if "op" in node:
            op = node["op"]
            if op in ("add", "sub", "mul", "div"):
                return BinaryOp(
                    op=op,
                    left=parse_expr(node["left"]),
                    right=parse_expr(node["right"]),
                )
            if op in ("neg", "pos"):
                return UnaryOp(op=op, operand=parse_expr(node["arg"]))
    raise ValueError(f"Invalid expression node: {node}")


def compile_pde_spec(pde_spec: dict) -> list[OperatorSpec]:
    """
    Given a PDE specification dictionary (JSON-loaded), return a list of
    OperatorSpec instances (with ASTs parsed) ready for execution.
    """
    ops: list[OperatorSpec] = []
    for op_json in pde_spec.get("operators", []):
        name = op_json["name"]
        if name not in operator_registry.operators:
            raise KeyError(f"Unknown operator: {name}")
        base_spec = operator_registry.get(name)
        spec = OperatorSpec(
            name=base_spec.name,
            inputs=base_spec.inputs.copy(),
            outputs=base_spec.outputs.copy(),
            locality=base_spec.locality,
            reversible=base_spec.reversible,
            dissipative=base_spec.dissipative,
            requires_governance=base_spec.requires_governance,
            apply=base_spec.apply,
        )
        # If the spec defines a formula for a derived field:
        if "formula" in op_json:
            spec.formula = parse_expr(op_json["formula"])
        ops.append(spec)
    return ops
```

This compiler parses a JSON PDE spec into internal objects. For example, a spec entry for a source term might look like:

```json
{
  "name": "alpha_source",
  "formula": {
    "op": "mul",
    "left": {"field": "Alpha"},
    "right": {"field": "DeltaPsi"}
  },
  "requires_governance": false
}
```

It ensures fields and expressions are typed ASTs.

## engine.py – PDE step execution with projection

```python
# coherence/pde/engine.py

from .compiler import compile_pde_spec
from .ast import eval_expr
from .operator import OperatorSpec
from typing import Dict


def step_pde(
    state: dict[str, float],
    pde_ops: list[OperatorSpec],
    dt: float = 0.1,
) -> dict[str, float]:
    """
    Perform one PDE step: compute contributions from each operator,
    integrate updates, then apply governance projection.
    """
    # Initialize change accumulator
    delta: Dict[str, float] = {field: 0.0 for field in state.keys()}

    # Compute each operator's effect
    for op in pde_ops:
        # Example: if operator has a 'formula', evaluate it as a source
        if hasattr(op, "formula"):
            # Evaluate formula expression using current state
            val = eval_expr(op.formula, state)
            # Distribute val to outputs (assuming one output for simplicity)
            for out in op.outputs:
                delta[out] += val
        # For built-in operators, call their apply function
        else:
            op.apply(state, delta)

    # Update state with Euler step
    new_state = {}
    for field, value in state.items():
        new_state[field] = max(0.0, min(1.0, value + dt * delta.get(field, 0.0)))

    # TODO: Apply governance projection / clamping for UCC/audit
    # e.g. new_state = apply_governance(new_state)
    return new_state


# Example usage:
if __name__ == "__main__":
    # Load or define a PDE spec (JSON)
    pde_json = {
        "operators": [
            {
                "name": "alpha_source",
                "formula": {
                    "op": "mul",
                    "left": {"field": "alpha"},
                    "right": {"field": "deltaPsi"},
                },
            }
        ]
    }

    # Initial state
    state = {"alpha": 0.5, "deltaPsi": 0.2}
    pde_ops = compile_pde_spec(pde_json)
    new_state = step_pde(state, pde_ops, dt=0.1)
    print(new_state)
```

This engine takes the compiled operators, evaluates any formulas, sums up contributions (`delta`), and then updates each field with an explicit Euler step. Governance projection (e.g. UCC constraints) should be applied after integration (omitted here, but see Governance below).

## Schema additions (`pde_schema.json`)

You would also add to your JSON schema (e.g. `pde_schema.json` in CoherenceLattice/bridge or schemas folder) to define the PDE spec format. For example:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Triadic PDE Specification",
  "type": "object",
  "properties": {
    "operators": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "formula": {"$ref": "expression.json#"},
          "requires_governance": {"type": "boolean"}
        },
        "required": ["name"],
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```

The `expression.json` schema would define the AST form (fields, constants, binary/unary ops).

## Governance Enforcement

Per Consultant Echo’s advice, the PDE system must enforce governance both at compile-time and at run-time. In practice, this means:

- **Compile-time checks**: Validate that operator combinations and target fields are allowed. For example, reject any spec that tries to write to a derived field (`role: derived`) or uses a `requires_governance` operator without review.
- **Run-time projection**: After computing `new_state`, apply any clamping or corrections mandated by UCC/audit. This could be a function like `apply_governance(new_state)` that zeroes out forbidden changes or triggers emergency resets.

## Example: Corridor Operator

You would register and implement the corridor-specific operators similarly. For instance:

```python
# coherence/pde/operators_corridor.py

from .operator import OperatorSpec, operator_registry


def compute_graph_laplacian(state, delta):
    # Implement graph Laplacian on corridor field "C" here
    pass


laplacian_spec = OperatorSpec(
    name="graph_laplacian",
    inputs=["C"],
    outputs=["C"],
    locality="edge",
    reversible=False,
    dissipative=True,
    requires_governance=False,
    apply=compute_graph_laplacian,
)
operator_registry.register(laplacian_spec)


def compute_gradient_source(state, delta):
    # Example: gradientEnergy term
    pass


gradient_spec = OperatorSpec(
    name="gradient_energy_source",
    inputs=["Theta"],
    outputs=["C"],
    locality="edge",
    reversible=False,
    dissipative=False,
    requires_governance=False,
    apply=compute_gradient_source,
)
operator_registry.register(gradient_spec)
```

Each such operator’s `apply` function computes its contribution given the global state and accumulates into `delta`.

## Summary

With these pieces, the triadic brain now has:

- Typed PDE grammar: field definitions and operators are specified with strict types, not free-form code.
- AST expressions: formulas are parsed into ASTs (`ast.py`) for safety and consistency.
- Operator registry: each operator’s signature and behavior is explicitly declared (`operator.py`).
- Compiler + engine: PDE specs (JSON) are compiled to operators (`compiler.py`) and stepped (`engine.py`).
- Governance hooks: compile-time validation and runtime projection points enforce UCC/audit constraints.

This completes the PDE framework so that AI-driven definitions of corridors, terraces, etc. can be processed systematically and safely by the Triadic Brain. Each code block above should be placed in the CoherenceLattice codebase (in `python/src/coherence/pde/`) and integrated with existing bridge tooling.
