# v3 Kernel: Three-Plane Architecture and Hardening Summary

Kernel (Thomas) = Lawful PDE engine: Compiler + engine with typed AST, operator registry, and rich FieldSpec registry. Implements deterministic integration, phase transitions, and governance.

Consent Layer (Joe) = PatternDonation interface: Narrative/acoustic artifacts with explicit consent metadata. All "pattern donations" are advisory only, subject to compile-time checks and no direct mutation of derived/governance fields.

Audit/Overlay Plane (Sophia/Atlas): Telemetry and audit outputs, watch/docket records, hashed state snapshots, and reset-safe visual overlays.

This braid realizes a deterministic "coherence-field compiler" under strict ethics: Joe’s rules become admissibility constraints; Thomas’s math becomes the executable substrate; and the system logs an auditable trail rather than opaque control.

## 1. Field Registry as Constitutional Core

- `FieldSpec` (new dataclass) holds `name`, `role`, `locality`, `bounds`, `governanceClass`, `shape`, `derived_from`, `dtype`, `conserved`, `writable`, etc.
- Enforces at compile-time: derived fields are immutable, locality rules, bounded ranges.
- Allows per-field projection rules (clip, reflect, no-saturation for specified fields).
- Example:

```python
@dataclass(frozen=True)
class FieldSpec:
    name: str
    role: Literal["primitive","derived","observable"]
    locality: Literal["node","edge","global"]
    bounds: Tuple[Optional[float],Optional[float]] = (0.0,1.0)
    governance: str           # e.g. "open", "sensitive"
    shape: Literal["scalar","vector","tensor"] = "scalar"
    conserved: bool = False
    derived_from: Tuple[str,...] = ()
    writable: bool = True
    dtype: Literal["float","bool","int","complex"] = "float"
```

- `OperatorSpec` (refined) is typed and includes `inputs`, `outputs`, `params`, `apply` function, etc., so the compiler knows each operator’s signature explicitly.

## 2. Typed AST and Operator Registry

- AST nodes (e.g. `FieldExpr`, `ConstExpr`, `AddExpr`, etc.) remain pure algebraic (no graph ops). Complex ops like Laplacian or divergence stay in operator implementations.
- Example AST class:

```python
@dataclass(frozen=True)
class FieldExpr(Expr):
    field: str
    def eval(self, state): return state[self.field]
# ... AddExpr, MulExpr, etc. ...
```

- `OperatorRegistry` maps operator names to implementations. For each operator (diffusion, advection, source, sink, etc.), store an `OperatorSpec`.
- Operators output `FieldContribution` records instead of mutating state directly:

```python
@dataclass(frozen=True)
class FieldContribution:
    field: str
    locality: str
    value: float
```

- Upon execution, operators return contributions which are validated against the `FieldRegistry` before aggregation.

## 3. Compiler Pipeline (Phase-aligned)

1. Parse JSON spec → AST: read unified spec schema (with `operators` list). Build ASTs for derived-field formulas under pattern donations.
2. Normalize and validate.
3. Apply compile-time governance: reject unknown ops, disallowed derived targets, missing consent tags.
4. Ensure `FieldSpec` consistency (e.g. no operator writes a derived field).
5. Lower to operator graph plan: flatten AST into a list of operator calls with parameters.
6. Canonicalize and hash: normalize ordering (e.g. sort operators), compute hash of the plan for provenance tracking.

## 4. Evolution Engine and Integration

- Generic engine: a single `step_kernel(state, ops, dt)` method. Corridor, river, terrace all use this base.
- Contribution aggregation: initialize empty `deltas: Dict[str, float]`. For each operator, call `contribs = op.apply(state, ...)` then merge into `deltas` (sum contributions). Validate each contribution’s field/locality.
- Integrate fields: for each primitive field `f`:

```text
new_val = state[f] + dt * deltas[f]
```

Then apply field-specific projection (clamp/bound) according to `FieldSpec.bounds`.

- Derived recompute: recompute all derived fields in topo-sorted order (using `FieldSpec.derived_from`). Emit a telemetry record `DerivedRecompute` if needed.
- Governance projection: after integration, apply governance rules: if any predicted jump violates policy, clip, queue review, or downgrade to advisory. (This is separate from numeric projection.)

## 5. New First-Class Artifacts

- `PhaseTransitionWitness`: emitted when system crosses regime boundaries. Contains `fromPhase`, `toPhase`, `targetId`, `triggerMetrics`, `kernelHash`, `supportingArtifacts`, `advisoryNote`.
- `RuntimeControlState`: captures operator-user feedback (`abort`, `downgrade`, `review`).
  - hard abort flag stops execution immediately
  - `downgradeToAdvisory` can disable scheduled ops
  - `requireHumanReview` pauses execution

All control changes should be settable via UI or API.

## 6. Execution Profiles and Modes

- Define profiles (`lean_safe`, `runtime_graph`, `research_field`, `experimental`) that restrict operators and writable fields.
- Example: `research_field` may allow stochastic novelty injections (fixed seed); `lean_safe` forbids randomness.
- Every run specifies a profile; compiler enforces profile constraints and consent/risk boundaries.

## 7. Deposit-Only Pattern Donations

- `PatternDonationSpec` (advisory-only): incoming artifact from consent layer with `donation_id`, `level`, `modality`, `content_ref`, `intended_targets`, `provenance`, `consent`, `audit_tags`, `artifact_mode`.
- Processing: compiler validates donation against profile and consent level; may convert hints into admissible operator parameters.
- Unapproved donations become logged advisories.
- Donations never directly write runtime state or derived fields; they flow through the same compiled operator pipeline.

## 8. Audit and Public Overlays

- Telemetry stream (TEL): each step emits core metrics (`kernelHash`, `ΔΨ`, `ΔS` spikes, field summaries, control flags).
- Sophia audit: emits JSONL records with severity (`info`/`warn`/`docket`/`watch`) for governance events. Records are schema-validated, deterministic (`sort_keys=True`), and contextual.
- Atlas overlays: load state from canonical artifacts (`chosen_state`, `risk_by_node`), toggles are idempotent, class clearing is centralized, and visualization is observable-only.

## 9. Repair/Rebraiding Test Harness

- Implement scenario fixtures (e.g. `tests/repair/hidden_to_exposed.json`, `tests/repair/reconciliation_arc.json`) to trigger known outcomes.
- Validate higher-order invariants such as:
  - post-rebraid `shared_memory_overlap` increases
  - `trust_legibility_overlap` remains nonzero

These tests validate polycentric/altruistic invariants across trajectories.

## 10. Remaining Hardening / Merge Gates

Before declaring this kernel final (“terrace”), ensure:

- `FieldSpec` completeness for all fields (including social fields such as `status_asymmetry`, `shared_memory_overlap`, `translation_capacity`, `trust_legibility`).
- Derived DAG surfaced as explicit runtime phase with telemetry record.
- Projection outputs separated from governance outputs in audit logs.
- Corridor and river both use the same generic `step_kernel` path.
- Golden-path CI: compile → step → telemetry → audit → overlay passes end-to-end.
- Explainability: no single “truth” voice; all outputs labeled non-authoritative with source hashes.

---

## Closing Synthesis

Developer Echo’s hardening core is the nucleus. The architecture is a two-layer, three-plane braid:

- Thomas layer (engine) enforces lawful triadic-brain dynamics.
- Joe layer (consent overlay) enforces ethics and admissibility.
- Audit layer ensures full traceability and reset-safe visualization.

This positions the PDE compiler as the execution nucleus (not a sidecar), with symbolic extensions bounded by governance.

The two most novel additions are `PhaseTransitionWitness` and `RuntimeControlState`, making each phase shift and each abort/downgrade explicit.

With these and the hardening checklist satisfied, the system reaches a terrace-grade design: a governed, auditable coherence-field compiler integrating all three perspectives.
