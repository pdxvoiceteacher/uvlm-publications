#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PAPER_ID = "PUB-GOV-ARTIFACT-COG-01"
REQUIRED_FILES = (
    "PUB_GOV_ARTIFACT_COG_01.md",
    "reproducibility_appendix.md",
    "claim_boundary_table.md",
    "artifact_table.md",
    "reviewer_quickstart.md",
    "status.json",
)
REQUIRED_PHRASES = (
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
)
FORBIDDEN_OVERCLAIMS = (
    "proves universal intelligence",
    "certifies truth",
    "deployment ready",
    "ai consciousness proven",
    "final answer authority",
    "universal wisdom machine",
    "recursive sonya federation demonstrated",
    "retrosynthesis runtime demonstrated",
    "omega detection demonstrated",
)
STATUS_REQUIRED = {
    "paper_id": PAPER_ID,
    "repo": "pdxvoiceteacher/uvlm-publications",
    "status": "drafted",
    "claim_level": "internal_preprint_draft",
    "requires_external_peer_review": True,
    "not_truth_certification": True,
    "not_deployment_authority": True,
    "not_final_answer_release": True,
    "not_ai_consciousness_claim": True,
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
    window = normalized_text[max(0, start - 80) : start]
    return any(marker in window for marker in NEGATION_MARKERS)


def _forbidden_hits(normalized_text: str) -> list[str]:
    hits: list[str] = []
    for phrase in FORBIDDEN_OVERCLAIMS:
        search_from = 0
        while True:
            index = normalized_text.find(phrase, search_from)
            if index == -1:
                break
            if not _is_negated(normalized_text, index):
                hits.append(phrase)
                break
            search_from = index + len(phrase)
    return hits


def _resolve_paths(args: argparse.Namespace) -> dict[str, Path]:
    paper = args.paper.resolve()
    root = paper.parent
    return {
        "paper": paper,
        "appendix": (args.appendix or root / "reproducibility_appendix.md").resolve(),
        "quickstart": (args.quickstart or root / "reviewer_quickstart.md").resolve(),
        "status": (args.status or root / "status.json").resolve(),
        "claim_boundary": (root / "claim_boundary_table.md").resolve(),
        "artifact_table": (root / "artifact_table.md").resolve(),
    }


def validate_publication_claims(
    paper: Path,
    appendix: Path | None = None,
    quickstart: Path | None = None,
    status: Path | None = None,
) -> dict[str, Any]:
    root = paper.parent
    paths = {
        "paper": paper,
        "appendix": appendix or root / "reproducibility_appendix.md",
        "quickstart": quickstart or root / "reviewer_quickstart.md",
        "status": status or root / "status.json",
        "claim_boundary": root / "claim_boundary_table.md",
        "artifact_table": root / "artifact_table.md",
    }

    required_file_paths = [root / name for name in REQUIRED_FILES]
    missing_files = [str(path) for path in required_file_paths if not path.exists()]
    required_files_present = not missing_files

    text_paths = [
        paths["paper"],
        paths["appendix"],
        paths["quickstart"],
        paths["claim_boundary"],
        paths["artifact_table"],
    ]
    combined_text = "\n".join(_read_text(path) for path in text_paths if path.exists())
    normalized_text = _normalize(combined_text)

    required_phrases_present = [
        phrase for phrase in REQUIRED_PHRASES if phrase in normalized_text
    ]
    missing_required_phrases = [
        phrase for phrase in REQUIRED_PHRASES if phrase not in normalized_text
    ]
    forbidden_overclaims_found = _forbidden_hits(normalized_text)

    status_json_valid = False
    status_errors: list[str] = []
    try:
        status_payload = json.loads(paths["status"].read_text(encoding="utf-8"))
        status_json_valid = all(
            status_payload.get(key) == expected
            for key, expected in STATUS_REQUIRED.items()
        )
        if not status_json_valid:
            status_errors = [
                key
                for key, expected in STATUS_REQUIRED.items()
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
        "paper_id": PAPER_ID,
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
        description="Validate publication claim boundaries for PUB-GOV-ARTIFACT-COG-01."
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
        appendix=paths["appendix"],
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
