#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = "pdxvoiceteacher/uvlm-publications"
SOURCE_REPOS = [
    "pdxvoiceteacher/CoherenceLattice",
    "pdxvoiceteacher/Sophia",
    "pdxvoiceteacher/uvlm-publications",
]
GENERATED_AT = None
ACCEPTED_PHASES = [
    {
        "phase_id": "EXP-SUITE-REGISTRY-01",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "experiment_suite_registry",
        "primary_artifacts": ["experiments/experiment_suite_registry.json"],
        "reproduction_command_summary": "Inspect experiments/experiment_suite_registry.json and rebuild the suite repro pack.",
        "claim_allowed": "Accepted/partial/blocked/planned phase registry is reviewable.",
        "claims_blocked": ["registry is not deployment authority", "route is not authorization"],
        "reviewer_caution": "Registry status is a claim-boundary map, not a product launch.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "EXP-SUITE-REPRO-01",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "reproducibility_pack",
        "primary_artifacts": [
            "experiment_suite_repro_pack.json",
            "acceptance_matrix.csv",
            "artifact_manifest.json",
            "experiment_suite_reproducibility_report.md",
        ],
        "reproduction_command_summary": "python -m coherence.tools.build_experiment_suite_repro_pack --registry experiments/experiment_suite_registry.json --artifacts-root artifacts --out-dir artifacts/experiment_suite_repro_pack --zip",
        "claim_allowed": "Reproducibility receipts and artifact manifests can be inspected.",
        "claims_blocked": ["reproducibility pack is not deployment authority", "receipt is not truth certification"],
        "reviewer_caution": "A receipt records checks; it does not certify truth.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "WAVE-FAMILY-CLOSEOUT-01",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "gold_physics_calibration",
        "primary_artifacts": ["waveform_gold_physics_family_acceptance_packet.json"],
        "reproduction_command_summary": "python -m coherence.waveform.family_acceptance --bridge-root artifacts/wave_gold_physics_family",
        "claim_allowed": "Closed-form waveform metric calibration across WAVE-00R through WAVE-03R.",
        "claims_blocked": ["WAVE calibration is not universal ontology", "WAVE Gold-Physics is not psychoacoustic proof"],
        "reviewer_caution": "High coherence is not necessarily constructive or safe.",
        "publication_status": "PUB-WAVE-ROSETTA-01 drafted",
    },
    {
        "phase_id": "SONYA-INGRESS-HARDEN-03",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "sonya_membrane_acceptance",
        "primary_artifacts": [
            "sonya_aegis_smoke_02_acceptance_report.json",
            "human_review bundle",
            "auto route bundle",
        ],
        "reproduction_command_summary": "experiments/Run-SONYA-AEGIS-SMOKE02-Acceptance.ps1 -CiMode",
        "claim_allowed": "Direct-call blocking and local Sonya membrane evidence are inspectable.",
        "claims_blocked": ["Sonya local membrane is not federation", "candidate is not answer"],
        "reviewer_caution": "Local fixture only; no recursive Sonya federation is implied.",
        "publication_status": "PUB-GOV-ARTIFACT-COG-01 drafted",
    },
    {
        "phase_id": "SOPHIA-UCC-ROUTE-01",
        "repo": "pdxvoiceteacher/Sophia",
        "status": "accepted",
        "evidence_type": "route_control",
        "primary_artifacts": ["sophia_ucc_route_acceptance_packet.json"],
        "reproduction_command_summary": "python -m pytest -q python/tests/integration/test_sophia_ucc_route.py",
        "claim_allowed": "Sophia/UCC route controls can classify admissibility posture.",
        "claims_blocked": ["route is not authorization", "no live Sophia calls"],
        "reviewer_caution": "Route disposition is governance posture, not final authority.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "PUB-GOV-ARTIFACT-COG-01",
        "repo": REPO,
        "status": "accepted",
        "evidence_type": "publication_draft",
        "primary_artifacts": [
            "papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md",
            "papers/governed_artifact_cognition/reviewer_quickstart.md",
            "papers/governed_artifact_cognition/status.json",
        ],
        "reproduction_command_summary": "python tools/validate_publication_claims.py --paper papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md --quickstart papers/governed_artifact_cognition/reviewer_quickstart.md --status papers/governed_artifact_cognition/status.json",
        "claim_allowed": "Governed artifact cognition paper is available as an internal preprint draft.",
        "claims_blocked": ["not truth certification", "not deployment authority", "not final answer release"],
        "reviewer_caution": "Draft requires external peer review.",
        "publication_status": "drafted",
    },
    {
        "phase_id": "PUB-WAVE-ROSETTA-01",
        "repo": REPO,
        "status": "accepted",
        "evidence_type": "publication_draft",
        "primary_artifacts": [
            "papers/waveform_rosetta/PUB_WAVE_ROSETTA_01.md",
            "papers/waveform_rosetta/reviewer_quickstart.md",
            "papers/waveform_rosetta/status.json",
        ],
        "reproduction_command_summary": "python tools/validate_publication_claims.py --paper papers/waveform_rosetta/PUB_WAVE_ROSETTA_01.md --quickstart papers/waveform_rosetta/reviewer_quickstart.md --status papers/waveform_rosetta/status.json",
        "claim_allowed": "Waveform Rosetta methods paper is available as an internal preprint draft.",
        "claims_blocked": ["not universal ontology", "not psychoacoustic effect", "not truth certification"],
        "reviewer_caution": "Closed-form calibration is not deployment evidence.",
        "publication_status": "drafted",
    },
    {
        "phase_id": "UNI-02D-SONYA-GATE-01",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "safe_portability_fixture",
        "primary_artifacts": [
            "uni02d_sonya_gate_acceptance_report.json",
            "semantic_term_quarantine_packet.json",
            "runtime_profile_leakage_packet.json",
            "uni02d_prior_origin_provenance_packet.json",
            "uni02d_prior_quarantine_packet.json",
        ],
        "reproduction_command_summary": "python -m pytest -q python/tests/integration/test_uni02d_sonya_gate_acceptance.py",
        "claim_allowed": "A Sonya-gated safe portability fixture can be inspected.",
        "claims_blocked": ["UNI-02D safe portability fixture is not universal portability proof", "prior quarantine is not prior canonization"],
        "reviewer_caution": "Scan selected_priors and matches[*].prior shapes for quarantine/provenance posture.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "RETRO-LANE-00",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "retrosynthesis_admission_lanes",
        "primary_artifacts": [
            "retrosynthesis_admission_packet.json",
            "retrosynthesis_admission_review_packet.json",
            "retro_lane_00_acceptance_receipt.json",
        ],
        "reproduction_command_summary": "python -m pytest -q python/tests/integration/test_retro_lane_00_acceptance.py",
        "claim_allowed": "sandbox_auto, review_required, and blocked admission lanes can be reviewed.",
        "claims_blocked": ["Retrosynthesis admission is not retrosynthesis execution", "hallucination telemetry is not evidence"],
        "reviewer_caution": "Admission is not execution; hallucination is telemetry, not evidence.",
        "publication_status": "dashboard_indexed",
    },
]
PARTIAL_PHASES = [
    {"phase_id": "TIMBRE-SPECTRAL-METRIC-TIER-02", "status": "planned_partial", "reason": "spectral-complexity tier remains future work"},
]
BLOCKED_PHASES = [
    {"phase_id": "DEPLOYMENT-CLAIM", "status": "blocked", "reason": "dashboard is not deployment authority"},
]
PLANNED_PHASES = [
    "PSYCHOACOUSTIC-SAFETY-TIER-03",
    "MODEL-INTERPRETATION-ORACLE-TIER-03",
    "Raw-model comparison baselines",
]
BOUNDARIES = [
    "Route is not authorization.",
    "Receipt is not truth certification.",
    "Model candidate is not answer.",
    "Publisher candidate is not final answer.",
    "Memory intent is not memory write.",
    "Sonya local membrane is not federation.",
    "WAVE calibration is not universal ontology.",
    "UNI-02D safe portability fixture is not universal portability proof.",
    "Retrosynthesis admission is not retrosynthesis execution.",
    "Admission is not execution.",
    "Reproducibility pack is not deployment authority.",
    "Dashboard is not deployment authority.",
]
GLOBAL_NON_CLAIMS = [
    "not truth certification",
    "not deployment authority",
    "not final answer release",
    "local fixture only",
    "requires external peer review",
    "not AI consciousness",
    "not universal ontology",
    "not recursive Sonya federation",
    "not live Atlas memory writes",
    "not live Sophia calls",
    "not retrosynthesis runtime",
    "not Omega detection",
    "not Publisher finalization",
]


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _assert_safe_dashboard(dashboard: dict[str, Any]) -> None:
    for key in ("deployment_ready", "truth_certified", "final_answer_release"):
        if dashboard.get(key) is True:
            raise ValueError(f"{key} must not be true")
    if any(not phase.get("claims_blocked") for phase in ACCEPTED_PHASES):
        raise ValueError("accepted phases must include claim boundaries")


def dashboard_payload() -> dict[str, Any]:
    dashboard = {
        "schema": "uvlm.public_experiment_suite_dashboard.v1",
        "repo": REPO,
        "source_repos": SOURCE_REPOS,
        "dashboard_status": "draft_public_review",
        "generated_at": GENERATED_AT,
        "accepted_phase_count": len(ACCEPTED_PHASES),
        "partial_phase_count": len(PARTIAL_PHASES),
        "blocked_phase_count": len(BLOCKED_PHASES),
        "planned_phase_count": len(PLANNED_PHASES),
        "accepted_phases": ACCEPTED_PHASES,
        "partial_phases": PARTIAL_PHASES,
        "blocked_phases": BLOCKED_PHASES,
        "planned_phases": PLANNED_PHASES,
        "evidence_packages": [
            "experiment_suite_repro_pack.json",
            "waveform_gold_physics_family_acceptance_packet.json",
            "sonya_aegis_smoke_02_acceptance_report.json",
        ],
        "publication_drafts": [
            "papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md",
            "papers/waveform_rosetta/PUB_WAVE_ROSETTA_01.md",
        ],
        "global_non_claims": GLOBAL_NON_CLAIMS,
        "reviewer_quickstart_paths": [
            "docs/experiment-suite/reviewer-quickstart.md",
            "papers/governed_artifact_cognition/reviewer_quickstart.md",
            "papers/waveform_rosetta/reviewer_quickstart.md",
        ],
        "requires_external_peer_review": True,
        "not_truth_certification": True,
        "not_deployment_authority": True,
        "not_final_answer_release": True,
        "not_ai_consciousness_claim": True,
        "not_universal_ontology_claim": True,
    }
    _assert_safe_dashboard(dashboard)
    return dashboard


def accepted_phase_matrix() -> dict[str, Any]:
    return {"schema": "uvlm.accepted_phase_matrix.v1", "entries": ACCEPTED_PHASES}


def reproducibility_index() -> dict[str, Any]:
    return {
        "schema": "uvlm.reproducibility_index.v1",
        "commands": {
            "CoherenceLattice": [
                {"name": "SONYA-AEGIS-SMOKE-02 harness", "command": "experiments/Run-SONYA-AEGIS-SMOKE02-Acceptance.ps1 -CiMode"},
                {"name": "WAVE family acceptance", "command": "python -m coherence.waveform.family_acceptance --bridge-root artifacts/wave_gold_physics_family"},
                {"name": "UNI-02D Sonya gate acceptance", "command": "python -m pytest -q python/tests/integration/test_uni02d_sonya_gate_acceptance.py"},
                {"name": "RETRO-LANE-00 acceptance", "command": "python -m pytest -q python/tests/integration/test_retro_lane_00_acceptance.py"},
                {"name": "experiment suite repro pack builder", "command": "python -m coherence.tools.build_experiment_suite_repro_pack --registry experiments/experiment_suite_registry.json --artifacts-root artifacts --out-dir artifacts/experiment_suite_repro_pack --zip"},
            ],
            "Sophia": [
                {"name": "UCC route test command", "command": "python -m pytest -q python/tests/integration/test_sophia_ucc_route.py"},
            ],
            "uvlm-publications": [
                {"name": "governed artifact cognition validator", "command": "python tools/validate_publication_claims.py --paper papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md --quickstart papers/governed_artifact_cognition/reviewer_quickstart.md --status papers/governed_artifact_cognition/status.json"},
                {"name": "waveform Rosetta validator", "command": "python tools/validate_publication_claims.py --paper papers/waveform_rosetta/PUB_WAVE_ROSETTA_01.md --quickstart papers/waveform_rosetta/reviewer_quickstart.md --status papers/waveform_rosetta/status.json"},
                {"name": "dashboard validator", "command": "python tools/validate_public_repro_dashboard.py --dashboard registry/experiment_suite_dashboard.json --docs-dir docs/experiment-suite"},
            ],
        },
        "not_deployment_authority": True,
    }


def claim_boundary_index() -> dict[str, Any]:
    return {"schema": "uvlm.claim_boundary_index.v1", "boundaries": BOUNDARIES}


def artifact_index() -> dict[str, Any]:
    return {
        "schema": "uvlm.artifact_index.v1",
        "phases": {
            "SONYA-AEGIS-SMOKE-02": ["sonya_aegis_smoke_02_acceptance_report.json", "human_review bundle", "auto route bundle"],
            "WAVE": ["waveform_gold_physics_family_acceptance_packet.json"],
            "UNI-02D": ["uni02d_sonya_gate_acceptance_report.json", "semantic_term_quarantine_packet.json", "runtime_profile_leakage_packet.json", "uni02d_prior_origin_provenance_packet.json", "uni02d_prior_quarantine_packet.json"],
            "RETRO-LANE-00": ["retrosynthesis_admission_packet.json", "retrosynthesis_admission_review_packet.json", "retro_lane_00_acceptance_receipt.json"],
            "publications": ["PUB_GOV_ARTIFACT_COG_01.md", "PUB_WAVE_ROSETTA_01.md", "reviewer quickstarts", "status.json files"],
        },
    }


def status_payload() -> dict[str, Any]:
    return {
        "dashboard_id": "PUBLIC-REPRO-DASHBOARD-01",
        "repo": REPO,
        "status": "draft_public_review",
        "claim_level": "public_reviewer_orientation",
        "requires_external_peer_review": True,
        "not_truth_certification": True,
        "not_deployment_authority": True,
        "not_final_answer_release": True,
        "not_ai_consciousness_claim": True,
        "not_universal_ontology_claim": True,
    }


def docs() -> dict[str, str]:
    phase_rows = "\n".join(
        f"| {p['phase_id']} | {p['repo']} | {p['status']} | {p['claim_allowed']} | {p['reviewer_caution']} |"
        for p in ACCEPTED_PHASES
    )
    boundaries = "\n".join(f"- {b}" for b in BOUNDARIES)
    return {
        "README.md": "# Experiment Suite Docs\n\nPublic reviewer documentation for the claim-bounded reproducibility dashboard.\n",
        "assets/README.md": "# Assets\n\nOptional static assets for the public reproducibility dashboard.\n",
        "index.md": f"# Public Experiment Suite Dashboard\n\nThis dashboard presents accepted evidence for reviewer orientation. It is not truth certification, not deployment authority, not final answer release, local fixture only, and requires external peer review.\n\n## Accepted evidence\n\n| Phase | Repo | Status | What this supports | Reviewer caution |\n| --- | --- | --- | --- | --- |\n{phase_rows}\n\n## Reviewer path\n\nStart with claim boundaries, then read the governed artifact cognition paper, WAVE Rosetta paper, SONYA-AEGIS-SMOKE-02, WAVE family, UNI-02D Sonya gate, and RETRO-LANE-00 pages.\n\n## What this proves\n\nIt proves only that accepted local fixture artifacts and draft publication materials are organized for review.\n\n## What this does not prove\n\nNo oracle posture, no deployment posture, no final-answer posture, no AI consciousness claim, and no universal ontology claim.\n\n## Phase pages\n\n- [SONYA-AEGIS-SMOKE-02](sonya-aegis-smoke-02.md)\n- [WAVE Gold-Physics](wave-gold-physics.md)\n- [UNI-02D Sonya gate](uni02d-sonya-gate.md)\n- [RETRO-LANE-00](retro-lane-00.md)\n- [Governed artifact cognition paper](governed-artifact-cognition-paper.md)\n- [Waveform Rosetta paper](waveform-rosetta-paper.md)\n",
        "claim-boundaries.md": f"# Claim Boundaries\n\n{boundaries}\n\nNo oracle posture. No deployment posture. No final-answer posture. No AI consciousness claim. No universal ontology claim.\n",
        "sonya-aegis-smoke-02.md": "# SONYA-AEGIS-SMOKE-02\n\nPurpose: inspect a local Sonya membrane and direct-call blocking fixture.\n\nRun command: `experiments/Run-SONYA-AEGIS-SMOKE02-Acceptance.ps1 -CiMode`.\n\nEvidence: `sonya_aegis_smoke_02_acceptance_report.json`, human_review bundle, auto route bundle.\n\nClaim allowed: local deterministic membrane evidence and direct-call blocking are reviewable.\n\nClaims blocked: Sonya local membrane is not federation; candidate is not answer; local fixture only.\n\nInspect direct-call blocking and Sonya membrane evidence in the acceptance report and route bundles.\n",
        "wave-gold-physics.md": "# WAVE Gold-Physics\n\nPurpose: closed-form waveform metric calibration.\n\nRun command: `python -m coherence.waveform.family_acceptance --bridge-root artifacts/wave_gold_physics_family`.\n\nEvidence: `waveform_gold_physics_family_acceptance_packet.json`.\n\nTheorem summary: constructive interference, coherent cancellation, detuning spiral, incomplete cancellation, and observability degradation.\n\nClaim allowed: WAVE calibration distinguishes waveform metric behavior.\n\nClaims blocked: WAVE calibration is not universal ontology and WAVE Gold-Physics is not psychoacoustic proof.\n\nCaution: high coherence is not necessarily constructive or safe.\n",
        "uni02d-sonya-gate.md": "# UNI-02D Sonya Gate\n\nPurpose: inspect safe portability fixture routing through Sonya-gated constraints.\n\nRun command: `python -m pytest -q python/tests/integration/test_uni02d_sonya_gate_acceptance.py`.\n\nEvidence: `uni02d_sonya_gate_acceptance_report.json`, semantic term quarantine, runtime profile leakage, prior origin provenance, and prior quarantine packets.\n\nPrior quarantine: selected priors remain bounded and must not be canonized. Review selected_priors and matches[*].prior shape scanning for provenance and quarantine posture.\n\nClaim allowed: safe portability fixture evidence can be reviewed.\n\nClaims blocked: UNI-02D safe portability fixture is not universal portability proof.\n\nCaution: safe portability fixture is not universal proof.\n",
        "retro-lane-00.md": "# RETRO-LANE-00\n\nPurpose: inspect retrosynthesis admission lanes without executing retrosynthesis.\n\nRun command: `python -m pytest -q python/tests/integration/test_retro_lane_00_acceptance.py`.\n\nEvidence: `retrosynthesis_admission_packet.json`, `retrosynthesis_admission_review_packet.json`, `retro_lane_00_acceptance_receipt.json`.\n\nLane definitions: sandbox_auto, review_required, blocked.\n\nClaim allowed: admission lane posture can be reviewed.\n\nClaims blocked: Retrosynthesis admission is not retrosynthesis execution; hallucination is telemetry not evidence.\n\nCaution: admission is not execution.\n",
        "governed-artifact-cognition-paper.md": "# Governed Artifact Cognition Paper\n\nSummary: systems paper for governed artifact cognition as a reproducible audit lab.\n\nLinks: `papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md`, reviewer quickstart, claim boundary table, status.json.\n\nClaim boundaries: not truth certification, not deployment authority, not final answer release, local fixture only, requires external peer review.\n\nValidation command: `python tools/validate_publication_claims.py --paper papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md --quickstart papers/governed_artifact_cognition/reviewer_quickstart.md --status papers/governed_artifact_cognition/status.json`.\n",
        "waveform-rosetta-paper.md": "# Waveform Rosetta Paper\n\nSummary: methods paper for closed-form WAVE Gold-Physics metric calibration.\n\nLinks: `papers/waveform_rosetta/PUB_WAVE_ROSETTA_01.md`, reviewer quickstart, theorem table, status.json.\n\nClaim boundaries: not universal ontology, not psychoacoustic effect, not AI consciousness, not deployment authority, not truth certification, requires external peer review.\n\nValidation command: `python tools/validate_publication_claims.py --paper papers/waveform_rosetta/PUB_WAVE_ROSETTA_01.md --quickstart papers/waveform_rosetta/reviewer_quickstart.md --status papers/waveform_rosetta/status.json`.\n",
        "reviewer-quickstart.md": "# Reviewer Quickstart\n\n## Read first path\n\n1. claim boundaries\n2. governed artifact cognition paper\n3. WAVE Rosetta paper\n4. SONYA-AEGIS-SMOKE-02\n5. WAVE family\n6. UNI-02D Sonya gate\n7. RETRO-LANE-00\n\n## CoherenceLattice commands\n\nPOSIX: `python -m coherence.waveform.family_acceptance --bridge-root artifacts/wave_gold_physics_family`\n\nPowerShell: `experiments/Run-SONYA-AEGIS-SMOKE02-Acceptance.ps1 -CiMode`\n\n## Sophia commands\n\n`python -m pytest -q python/tests/integration/test_sophia_ucc_route.py`\n\n## uvlm-publications commands\n\n`python tools/validate_publication_claims.py --paper papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md --quickstart papers/governed_artifact_cognition/reviewer_quickstart.md --status papers/governed_artifact_cognition/status.json`\n\n`python tools/validate_public_repro_dashboard.py --dashboard registry/experiment_suite_dashboard.json --docs-dir docs/experiment-suite`\n\nnot truth certification; not deployment authority; not final answer release; local fixture only; requires external peer review.\n",
    }


def build(out_dir: Path, docs_dir: Path) -> None:
    _write_json(out_dir / "experiment_suite_dashboard.json", dashboard_payload())
    _write_json(out_dir / "accepted_phase_matrix.json", accepted_phase_matrix())
    _write_json(out_dir / "reproducibility_index.json", reproducibility_index())
    _write_json(out_dir / "claim_boundary_index.json", claim_boundary_index())
    _write_json(out_dir / "artifact_index.json", artifact_index())
    _write_json(out_dir / "status.json", status_payload())
    for name, text in docs().items():
        _write_text(docs_dir / name, text)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build public experiment suite reproducibility dashboard.")
    parser.add_argument("--out-dir", type=Path, default=Path("registry"))
    parser.add_argument("--docs-dir", type=Path, default=Path("docs/experiment-suite"))
    parser.add_argument("--coherencelattice-repro-pack", type=Path)
    parser.add_argument("--sonya-aegis-report", type=Path)
    parser.add_argument("--wave-family-report", type=Path)
    parser.add_argument("--uni02d-report", type=Path)
    parser.add_argument("--retro-lane-report", type=Path)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    build(args.out_dir, args.docs_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
