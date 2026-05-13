#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PAPER_CONFIGS: dict[str, dict[str, Any]] = {
    "PUB-GOV-ARTIFACT-COG-01": {
        "paper_file": "PUB_GOV_ARTIFACT_COG_01.md",
        "required_files": (
            "PUB_GOV_ARTIFACT_COG_01.md",
            "abstract.md",
            "reproducibility_appendix.md",
            "claim_boundary_table.md",
            "artifact_table.md",
            "reviewer_quickstart.md",
            "status.json",
        ),
        "text_files": (
            "PUB_GOV_ARTIFACT_COG_01.md",
            "abstract.md",
            "reproducibility_appendix.md",
            "claim_boundary_table.md",
            "artifact_table.md",
            "reviewer_quickstart.md",
        ),
        "required_phrases": (
            "not truth certification",
            "not deployment authority",
            "not final answer release",
            "local fixture only",
            "requires external peer review",
            "not ai consciousness",
            "not recursive sonya federation",
            "not retrosynthesis runtime",
            "not omega detection",
            "not live atlas memory writes",
            "not live sophia calls",
            "public-utility-alpha-00",
            "sonya gateway",
            "model braid",
            "not live model execution",
            "not federation",
            "raw-baseline-comparison-00",
            "fixture-only measurement scaffold",
            "not hallucination reduction proof",
            "not model quality benchmark",
            "evidence-review-pack-00",
            "Evidence Review Pack v0.1",
            "first product-facing governed review receipt",
            "Universal Evidence Ingress",
            "UCC Control Profile Selector",
            "AI review that shows its work",
            "not professional advice",
            "not compliance certification",
            "rw-comp-01",
            "first fixture-only raw-vs-governed comparison involving Evidence Review Pack v0.1",
            "review-structure visibility",
            "step toward future hallucination-reduction evidence",
            "not hallucination-reduction proof yet",
            "not model superiority proof",
            "rw-comp-02",
            "deterministic multi-fixture comparison battery",
            "six controlled fixture families",
            "full Evidence Review Pack arms",
            "structural visibility improvement",
            "not model-superiority proof",
            "rw-comp-03",
            "held-out blinded fixture scaffold",
            "held-out, blinded, pre-registered fixture-scoring scaffold",
            "simulated scores only",
            "not live human study",
            "not accepted evidence",
            "Run-RW-COMP03-Acceptance.ps1",
            "accepted_as_heldout_blinded_fixture_scaffold",
        ),
        "forbidden_overclaims": (
            "proves universal intelligence",
            "certifies truth",
            "deployment ready",
            "deployment readiness",
            "deployment authority",
            "production readiness",
            "ai consciousness proven",
            "final answer authority",
            "final answer release",
            "live model execution",
            "live model evaluation",
            "remote provider evaluation",
            "federation",
            "retrosynthesis runtime",
            "consensus proof",
            "answer selection",
            "hallucination reduction proven",
            "model superiority proven",
            "model superiority proof",
            "hallucination reduction proof",
            "model quality benchmark",
            "production evaluation",
            "production readiness",
            "live human study",
            "human-subject study result",
            "accepted evidence",
            "professional advice",
            "legal advice",
            "medical advice",
            "tax advice",
            "compliance certification",
            "remote provider call",
            "universal wisdom machine",
            "recursive sonya federation demonstrated",
            "retrosynthesis runtime demonstrated",
            "omega detection demonstrated",
        ),
        "status_required": {
            "paper_id": "PUB-GOV-ARTIFACT-COG-01",
            "repo": "pdxvoiceteacher/uvlm-publications",
            "status": "drafted",
            "claim_level": "internal_preprint_draft",
            "requires_external_peer_review": True,
            "not_truth_certification": True,
            "not_deployment_authority": True,
            "not_final_answer_release": True,
            "not_live_model_execution": True,
            "not_federation": True,
            "raw_baseline_comparison_indexed": True,
            "not_hallucination_reduction_proof": True,
            "not_model_quality_benchmark": True,
            "not_remote_provider_call": True,
            "evidence_review_pack_indexed": True,
            "not_professional_advice": True,
            "not_compliance_certification": True,
            "rw_comp_01_indexed": True,
            "not_model_superiority_proof": True,
            "rw_comp_02_indexed": True,
            "rw_comp_03_indexed": True,
            "not_live_human_study": True,
            "not_human_subject_study_result": True,
            "not_accepted_evidence": True,
            "not_live_model_evaluation": True,
            "not_production_evaluation": True,
            "not_ai_consciousness_claim": True,
        },
    },
    "PUB-WAVE-ROSETTA-01": {
        "paper_file": "PUB_WAVE_ROSETTA_01.md",
        "required_files": (
            "PUB_WAVE_ROSETTA_01.md",
            "abstract.md",
            "methods_appendix.md",
            "theorem_table.md",
            "claim_boundary_table.md",
            "artifact_table.md",
            "reviewer_quickstart.md",
            "status.json",
            "figures/README.md",
        ),
        "text_files": (
            "PUB_WAVE_ROSETTA_01.md",
            "abstract.md",
            "methods_appendix.md",
            "theorem_table.md",
            "claim_boundary_table.md",
            "artifact_table.md",
            "reviewer_quickstart.md",
            "figures/README.md",
        ),
        "required_phrases": (
            "closed form waveform metric calibration",
            "not universal ontology",
            "not psychoacoustic effect",
            "not ai consciousness",
            "not deployment authority",
            "not truth certification",
            "requires external peer review",
        ),
        "forbidden_overclaims": (
            "proves universal ontology",
            "proves psychoacoustic entrainment",
            "proves ai consciousness",
            "proves guft as final physics",
            "deployment ready",
            "truth certified",
            "cognition is literally sine waves",
        ),
        "status_required": {
            "paper_id": "PUB-WAVE-ROSETTA-01",
            "repo": "pdxvoiceteacher/uvlm-publications",
            "status": "drafted",
            "claim_level": "internal_preprint_draft",
            "requires_external_peer_review": True,
            "not_truth_certification": True,
            "not_deployment_authority": True,
            "not_final_answer_release": True,
            "not_universal_ontology_claim": True,
            "not_psychoacoustic_effect_claim": True,
            "not_ai_consciousness_claim": True,
            "not_retrosynthesis_authorization": True,
        },
    },
}
NEGATION_MARKERS = (
    "not ",
    "no ",
    "does not ",
    "do not ",
    "without ",
    "never ",
    "neither ",
    "nor ",
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _normalize(text: str) -> str:
    normalized = text.lower().replace("‑", "-").replace("–", "-")
    return " ".join(normalized.replace("-", " ").split())


def _is_negated(normalized_text: str, start: int) -> bool:
    window = normalized_text[max(0, start - 32) : start]
    after = normalized_text[start : start + 80]
    return any(marker in window for marker in NEGATION_MARKERS) or "performed = false" in after


def _forbidden_hits(normalized_text: str, forbidden: tuple[str, ...]) -> list[str]:
    hits: list[str] = []
    for phrase in forbidden:
        normalized_phrase = _normalize(phrase)
        search_from = 0
        while True:
            index = normalized_text.find(normalized_phrase, search_from)
            if index == -1:
                break
            if not _is_negated(normalized_text, index):
                hits.append(phrase)
                break
            search_from = index + len(normalized_phrase)
    return hits


def _load_status_id(status: Path) -> str | None:
    try:
        payload = json.loads(status.read_text(encoding="utf-8"))
    except Exception:
        return None
    paper_id = payload.get("paper_id")
    return paper_id if isinstance(paper_id, str) else None


def _infer_config_id(paper: Path, status: Path) -> str:
    status_id = _load_status_id(status)
    if status_id in PAPER_CONFIGS:
        return status_id
    for paper_id, config in PAPER_CONFIGS.items():
        if paper.name == config["paper_file"]:
            return paper_id
    raise ValueError(f"Unsupported publication paper/status combination: {paper}")


def _resolve_paths(args: argparse.Namespace) -> dict[str, Path]:
    paper = args.paper.resolve()
    root = paper.parent
    return {
        "paper": paper,
        "appendix": (args.appendix or root / "reproducibility_appendix.md").resolve(),
        "quickstart": (args.quickstart or root / "reviewer_quickstart.md").resolve(),
        "status": (args.status or root / "status.json").resolve(),
    }


def validate_publication_claims(
    paper: Path,
    appendix: Path | None = None,
    quickstart: Path | None = None,
    status: Path | None = None,
) -> dict[str, Any]:
    root = paper.parent
    status_path = status or root / "status.json"
    paper_id = _infer_config_id(paper, status_path)
    config = PAPER_CONFIGS[paper_id]

    overrides = {
        paper.name: paper,
        "reviewer_quickstart.md": quickstart or root / "reviewer_quickstart.md",
    }
    if appendix is not None:
        overrides[appendix.name] = appendix

    required_file_paths = [
        overrides.get(name, root / name) for name in config["required_files"]
    ]
    missing_files = [str(path) for path in required_file_paths if not path.exists()]
    required_files_present = not missing_files

    text_paths = [overrides.get(name, root / name) for name in config["text_files"]]
    combined_text = "\n".join(_read_text(path) for path in text_paths if path.exists())
    normalized_text = _normalize(combined_text)

    required_phrases_present = [
        phrase
        for phrase in config["required_phrases"]
        if _normalize(phrase) in normalized_text
    ]
    missing_required_phrases = [
        phrase
        for phrase in config["required_phrases"]
        if _normalize(phrase) not in normalized_text
    ]
    forbidden_overclaims_found = _forbidden_hits(
        normalized_text, config["forbidden_overclaims"]
    )

    status_json_valid = False
    status_errors: list[str] = []
    try:
        status_payload = json.loads(status_path.read_text(encoding="utf-8"))
        status_json_valid = all(
            status_payload.get(key) == expected
            for key, expected in config["status_required"].items()
        )
        if not status_json_valid:
            status_errors = [
                key
                for key, expected in config["status_required"].items()
                if status_payload.get(key) != expected
            ]
    except Exception as exc:  # noqa: BLE001 - validator reports bounded JSON errors.
        status_errors = [str(exc)]

    passed = (
        required_files_present
        and not missing_required_phrases
        and not forbidden_overclaims_found
        and status_json_valid
    )

    return {
        "paper_id": paper_id,
        "passed": passed,
        "required_files_present": required_files_present,
        "missing_required_files": missing_files,
        "required_phrases_present": required_phrases_present,
        "missing_required_phrases": missing_required_phrases,
        "forbidden_overclaims_found": forbidden_overclaims_found,
        "status_json_valid": status_json_valid,
        "status_errors": status_errors,
        "not_truth_certification": status_json_valid,
        "not_deployment_authority": status_json_valid,
        "not_final_answer_release": status_json_valid,
    }


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate publication claim boundaries for supported papers."
    )
    parser.add_argument("--paper", required=True, type=Path)
    parser.add_argument("--appendix", type=Path)
    parser.add_argument("--quickstart", type=Path)
    parser.add_argument("--status", type=Path)
    parser.add_argument("--out", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    paths = _resolve_paths(args)
    result = validate_publication_claims(
        paths["paper"],
        appendix=paths["appendix"] if args.appendix else None,
        quickstart=paths["quickstart"],
        status=paths["status"],
    )
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
