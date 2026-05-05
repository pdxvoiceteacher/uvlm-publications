"""Phase 6 Atlas memory candidate classifier.

This module intentionally produces only a non-authoritative retrieval candidate
packet. It reads the Phase 6 handoff and Sophia adjudication artifacts to carry
forward the request identity, but it does not authorize an Atlas memory write and
it does not alter retrieval behavior.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCHEMA = "atlas.phase6_memory_candidate.v1"
CANDIDATE_STATUS = "shadow_only"
ALLOWED_USE = "retrieval_candidate"
REASON_CODES = [
    "not_truth_certification",
    "human_review_required",
    "cross_domain_validation_pending",
]
GUARDRAILS = {
    "not_authoritative_memory": True,
    "does_not_override_source": True,
    "human_review_required": True,
}
REQUEST_ID_KEYS = (
    "request_id",
    "requestId",
    "phase6_request_id",
    "phase6RequestId",
    "triadic_request_id",
    "triadicRequestId",
)


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return payload


def _find_first_value(payload: Any, keys: tuple[str, ...]) -> Any:
    if isinstance(payload, dict):
        for key in keys:
            value = payload.get(key)
            if value not in (None, ""):
                return value
        for value in payload.values():
            found = _find_first_value(value, keys)
            if found not in (None, ""):
                return found
    elif isinstance(payload, list):
        for value in payload:
            found = _find_first_value(value, keys)
            if found not in (None, ""):
                return found
    return None


def _request_id(
    handoff_request: dict[str, Any], sophia_adjudication: dict[str, Any]
) -> str | None:
    for payload in (handoff_request, sophia_adjudication):
        found = _find_first_value(payload, REQUEST_ID_KEYS)
        if found not in (None, ""):
            return str(found)
    return None


def build_phase6_memory_candidate_packet(
    handoff_request: dict[str, Any], sophia_adjudication: dict[str, Any]
) -> dict[str, Any]:
    """Build a shadow-only Phase 6 memory candidate packet.

    The classifier is deliberately conservative: the candidate may be used only
    as a retrieval candidate, and human review remains required before any
    authoritative memory write could be considered by a separate workflow.
    """

    return {
        "schema": SCHEMA,
        "request_id": _request_id(handoff_request, sophia_adjudication),
        "candidate_status": CANDIDATE_STATUS,
        "allowed_use": ALLOWED_USE,
        "memory_write_authorized": False,
        "reason_codes": list(REASON_CODES),
        "artifact_refs": [],
        "artifact_sha256s": {},
        "guardrails": dict(GUARDRAILS),
    }


def write_phase6_memory_candidate_packet(
    handoff_request_path: Path, sophia_adjudication_path: Path, out_path: Path
) -> dict[str, Any]:
    handoff_request = _read_json(handoff_request_path)
    sophia_adjudication = _read_json(sophia_adjudication_path)
    packet = build_phase6_memory_candidate_packet(handoff_request, sophia_adjudication)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    return packet


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classify a Phase 6 Atlas memory candidate packet."
    )
    parser.add_argument("--handoff-request", required=True, type=Path)
    parser.add_argument("--sophia-adjudication", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    write_phase6_memory_candidate_packet(
        args.handoff_request, args.sophia_adjudication, args.out
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
