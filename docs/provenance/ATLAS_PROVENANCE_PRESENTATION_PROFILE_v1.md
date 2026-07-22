# Atlas Provenance Presentation and Decision Apprentice Profile v1

**Role:** Posture, presentation, human decision, retention boundary, and publication-boundary lineage.

## Required habits

- Bind posture to exact CoherenceLattice candidate and Sophia audit artifacts.
- Keep file-byte and canonical-content digests distinct; neither digest establishes correctness or authority.
- Render evidence without changing its source bytes. Polished presentation is not evidence that inputs were valid.
- Keep presentation quality, posture, and evidentiary quality separate.
- Keep the mutable human-review state separate from one immutable human-decision receipt bound to one sealed run.
- Record authority and side-effect ceilings.
- Treat retention, PMR, canonization, publication, deployment, and release as separate gates.

## Decision and posture boundaries

APPROVE, HOLD, and REJECT are bounded human decisions for the sealed run; they do not certify universal truth or authorize memory, PMR, canonization, DOI, Crossref, catalog, graph, publication, deployment, or release.

A blocking Atlas posture or decision HOLD must identify an observed failure, affected invariant/security/privacy property/authority boundary, plausible consequence, owner, exact exit test, and retirement condition. Otherwise classify the work as PROCEED, PROCEED_WITH_DEBT, or REPAIR_IN_CURRENT_WORK_UNIT.

Accepted predecessor evidence is inherited until an Atlas changed surface can plausibly affect it. A production-path review or decision claim needs sensitivity evidence: its test must fail when the claimed production path is deliberately disabled. A validation-driver defect invalidates its evidence segment; it does not establish a product defect.

## Lifecycle and authority boundaries

Invalidation, supersession, and revocation append downstream review effects; they do not rewrite candidate, audit, posture, or decision history. Retention is consent-bounded inspectability, not PMR execution or canon. Review is not DOI, Crossref, catalog, graph, publication, deployment, or release authority. Atlas has no side effect or authority beyond this presentation and bounded decision lineage.

## Apprentice exit demonstration

Trace candidate → Sophia audit → Atlas posture → human decision. Explain the source bytes and canonical content digests, what APPROVE permits, what remains prohibited, and how a revocation changes downstream review without laundering a polished presentation into valid evidence.
