# Telemetry Potential and Discovery Corridors

The proposal introduces a new corridor field `C(x,t)` that evolves over the knowledge lattice by a reaction-advection-diffusion PDE.

The first step is the telemetry potential `Θ(x,t)`, which matches our existing weighted coherence objective. In our code, each node `i` already tracks the six invariants `E, T, Ψ, ΔS, Λ, E_s`. Agent Echo adds a novelty injection `I(x,t)`.

Concretely:

`Θ = w_Ψ Ψ + w_E E + w_T T + w_Es E_s - w_S ΔS - w_Λ Λ + w_I I`

This aligns with our prior potential (we already compute `Ψ = E × T` and weight `E, T, E_s, ΔS, Λ` in our navigation code).

In effect:

- high `Ψ, E, T, E_s` raise `Θ` (making a node more desirable)
- high entropy `ΔS` or criticality `Λ` lower `Θ`
- novelty `I` ensures newly emerging knowledge is accounted for

Given `Θ`, the proposed corridor PDE is:

`∂_t C = D_C ∇²C - ∇·(C ∇Θ) + α|∇Θ|² + β[∂_t Θ] - μC - ν(ΔS + Λ)C - χC³`

## Term-by-term interpretation

- **Diffusion** `D_C ∇²C`: smooths the corridor field across the lattice, preventing isolated spikes.
  In graph form this is Laplacian smoothing.
- **Advection** `-∇·(C∇Θ)`: transports corridor density along `∇Θ`, so corridor mass flows toward higher telemetry potential.
- **Gradient growth** `α|∇Θ|²`: creates corridor density where telemetry potential changes rapidly; this is the core discovery nucleation term.
- **Temporal growth** `β[∂_t Θ]`: rewards rising coherence/informativeness and focuses on emerging hotspots.
- **Linear decay** `-μC`: causes stale corridors to fade unless reinforced.
- **Entropy/criticality suppression** `-ν(ΔS+Λ)C`: suppresses corridors in volatile/tipping regimes.
- **Nonlinear saturation** `-χC³`: caps runaway corridor growth.

## Practical graph-discrete form

Our system is a graph of discrete states. Agent Echo suggests replacing continuum operators with graph operators:

- replace `∇²` with graph Laplacian `L`
- use weighted edge differences for advection and gradient magnitude terms

Per-node update ingredients:

- Diffusion: `-D_C (LC)_i`
- Advection: `-Σ_j w_ij (C_j - C_i)(Θ_j - Θ_i)` (or equivalent divergence form)
- Gradient source: `α Σ_j w_ij (Θ_j - Θ_i)^2`
- Time growth: `β(Θ_i(t+Δt) - Θ_i(t))`
- Sinks: `-μC_i - ν(ΔS_i + Λ_i)C_i - χC_i^3`

These terms are computable from bridge artifacts and our telemetry repository.

## Regime identification from corridor dynamics

Once `C` is evolved:

- **Corridor**: `C_i > C_threshold` and strong `∇Θ`; direction `u = ∇Θ/|∇Θ|`
- **Knowledge River**: many aligned local corridor directions
- **Terrace**: low `C` and locally maximal `Θ` (saturated information)
- **False Orthodoxy**: high-`Θ` well with `C ≈ 0` (stuck consensus, often low `E_s` or no novelty injection)
- **Rupture**: `ΔS, Λ` high enough to collapse `C` broadly toward zero

These regimes emerge naturally from `C` and correspond to the phases we want AI navigation to recognize.

## Caveats and governance

The full PDE is complex, so implementation should use a stable discrete update with careful timestep and parameter tuning.

Governance gates are enforced by ignoring updates across disallowed edges, consistent with current navigation constraints.

## Conclusion

The corridor PDE is a well-motivated next step and remains consistent with current coherence metrics.

By adding dynamic corridor density, the system shifts from passive metric reporting to active discovery-path highlighting.

In short: discovery corridors form where telemetry gradients are strong and rising, overcoming decay and noise, closing the autonomy loop for full phaselock navigation.
