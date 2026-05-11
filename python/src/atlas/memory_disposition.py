"""Atlas memory-intent disposition intake.

Atlas receives bounded memory-intent candidates and emits deterministic posture
only. This module never promotes candidates, never certifies truth, and never
changes retrieval or publication state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "atlas.memory_disposition_packet.v1"
SOURCE_SCHEMA = "uvlm.atlas_memory_intent_packet.v1"
ROUTE_TRACE_SCHEMA = "uvlm.atlas_memory_intent_route_trace.v1"

STATUS_VALUES = {
    "pending_human_review",
    "retrieval_candidate",
    "quarantine",
    "reject",
    "needs_more_evidence",
    "ltm_candidate_review_required",
}
ALLOWED_USE_VALUES = {
    "retrieval_candidate",
    "shadow_only",
    "context_only",
    "quarantine_only",
    "rejected",
}
REQUIRED_STRING_FIELDS = (
    "audit_pass_id",
    "submission_id",
    "sonya_ingress_id",
    "aegis_trace_id",
    "request_envelope_id",
    "analysis_profile_id",
    "semantic_taxonomy_id",
)
REQUIRED_ARRAY_FIELDS = (
    "grounding_refs",
    "tel_refs",
    "coherence_metric_refs",
)
CANDIDATE_ROUTE_FALSE_FIELDS = (
    "atlas_memory_write_authorized",
    "atlas_prior_canonized",
    "truth_certified",
    "deployment_authorized",
)
SOURCE_BOUNDARY_FALSE_FIELDS = (
    "live_atlas_call_performed",
    "model_call_performed",
    "network_call_performed",
)
GUARDRAIL_TRUE_FIELDS = (
    "intent_not_memory_write_authorization",
    "intent_not_prior_canonization",
    "intent_not_truth_certification",
    "intent_not_deployment_authority",
    "intent_not_final_answer",
)
BASE_REASON_CODES = (
    "candidate_only",
    "atlas_disposition_required",
    "human_review_required",
    "not_memory_write",
    "not_prior_canonization",
    "not_truth_certification",
)


class AtlasMemoryDispositionValidationError(ValueError):
    """Raised when an Atlas memory-intent candidate violates intake bounds."""


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise AtlasMemoryDispositionValidationError(f"Expected JSON object in {path}")
    return payload


def _require_dict(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise AtlasMemoryDispositionValidationError(f"{key} must be an object")
    return value


def _require_non_empty_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise AtlasMemoryDispositionValidationError(f"{key} must be a non-empty string")
    return value


def _require_array(payload: dict[str, Any], key: str) -> list[Any]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise AtlasMemoryDispositionValidationError(f"{key} must be an array")
    return list(value)


def _require_const_false(payload: dict[str, Any], key: str) -> None:
    if payload.get(key) is not False:
        raise AtlasMemoryDispositionValidationError(f"{key} must be false")


def _require_const_true(payload: dict[str, Any], key: str) -> None:
    if payload.get(key) is not True:
        raise AtlasMemoryDispositionValidationError(f"{key} must be true")


def _canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def atlas_memory_disposition_id(memory_intent_id: str, *parts: str) -> str:
    """Return a deterministic disposition ID for a memory-intent candidate."""

    base = "|".join([memory_intent_id, *parts])
    digest = hashlib.sha256(base.encode("utf-8")).hexdigest()[:24]
    return f"atlas-memory-disposition-{digest}"


def _validate_memory_intent_packet(
    memory_intent_packet: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    if memory_intent_packet.get("schema") != SOURCE_SCHEMA:
        raise AtlasMemoryDispositionValidationError(
            f"schema must be {SOURCE_SCHEMA}"
        )

    memory_intent = _require_dict(memory_intent_packet, "memory_intent")
    candidate_routes = _require_dict(memory_intent_packet, "candidate_routes")
    source_boundary = _require_dict(memory_intent_packet, "source_boundary")

    _require_non_empty_string(memory_intent, "memory_intent_id")
    for key in REQUIRED_STRING_FIELDS:
        _require_non_empty_string(memory_intent_packet, key)
    for key in REQUIRED_ARRAY_FIELDS:
        _require_array(memory_intent_packet, key)

    _require_const_true(memory_intent, "requires_atlas_disposition")
    for key in CANDIDATE_ROUTE_FALSE_FIELDS:
        _require_const_false(candidate_routes, key)
    for key in SOURCE_BOUNDARY_FALSE_FIELDS:
        _require_const_false(source_boundary, key)
    for key in GUARDRAIL_TRUE_FIELDS:
        _require_const_true(memory_intent_packet, key)

    return memory_intent, candidate_routes, source_boundary


def _validate_route_trace(route_trace: dict[str, Any] | None, memory_intent_id: str) -> None:
    if route_trace is None:
        return
    if route_trace.get("schema") != ROUTE_TRACE_SCHEMA:
        raise AtlasMemoryDispositionValidationError(
            f"route trace schema must be {ROUTE_TRACE_SCHEMA}"
        )
    if route_trace.get("memory_intent_id") != memory_intent_id:
        raise AtlasMemoryDispositionValidationError(
            "route trace memory_intent_id must match memory intent"
        )
    _require_const_false(route_trace, "atlas_memory_write_performed")
    _require_const_false(route_trace, "live_atlas_call_performed")


def _retention_band(
    memory_intent_packet: dict[str, Any], memory_intent: dict[str, Any]
) -> str:
    return str(
        memory_intent.get("retention_band_hint")
        or memory_intent_packet.get("retention_band_hint")
        or "mtm"
    )


def _status_for_retention(retention_band: str) -> str:
    if retention_band == "ltm_candidate":
        return "ltm_candidate_review_required"
    return "pending_human_review"


def build_atlas_memory_disposition_packet(
    memory_intent_packet: dict[str, Any], route_trace: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Build a deterministic non-authoritative Atlas disposition packet."""

    memory_intent, _candidate_routes, _source_boundary = _validate_memory_intent_packet(
        memory_intent_packet
    )
    memory_intent_id = _require_non_empty_string(memory_intent, "memory_intent_id")
    _validate_route_trace(route_trace, memory_intent_id)

    retention_band = _retention_band(memory_intent_packet, memory_intent)
    status = _status_for_retention(retention_band)
    if status not in STATUS_VALUES:
        raise AtlasMemoryDispositionValidationError(f"invalid status {status}")

    allowed_use = "retrieval_candidate"
    disposition_id = atlas_memory_disposition_id(
        memory_intent_id,
        memory_intent_packet["audit_pass_id"],
        memory_intent_packet["submission_id"],
        _canonical_json(route_trace or {}),
    )

    return {
        "schema": SCHEMA,
        "disposition_id": disposition_id,
        "memory_intent_id": memory_intent_id,
        "source_packet_schema": SOURCE_SCHEMA,
        "audit_pass_id": memory_intent_packet["audit_pass_id"],
        "submission_id": memory_intent_packet["submission_id"],
        "sonya_ingress_id": memory_intent_packet["sonya_ingress_id"],
        "aegis_trace_id": memory_intent_packet["aegis_trace_id"],
        "request_envelope_id": memory_intent_packet["request_envelope_id"],
        "analysis_profile_id": memory_intent_packet["analysis_profile_id"],
        "semantic_taxonomy_id": memory_intent_packet["semantic_taxonomy_id"],
        "grounding_refs": list(memory_intent_packet["grounding_refs"]),
        "tel_refs": list(memory_intent_packet["tel_refs"]),
        "coherence_metric_refs": list(memory_intent_packet["coherence_metric_refs"]),
        "coherence_escrow_status": str(
            memory_intent.get("coherence_escrow_status") or "review_escrow"
        ),
        "reversibility_index": str(memory_intent.get("reversibility_index") or "R2"),
        "disposition": {
            "status": status,
            "allowed_use": allowed_use,
            "retention_band": retention_band,
            "sensitivity_class": str(memory_intent.get("sensitivity_class") or "internal"),
            "reason_codes": list(BASE_REASON_CODES),
        },
        "review_requirements": {
            "requires_human_review": True,
            "requires_ltm_review": retention_band == "ltm_candidate",
            "requires_prior_canonization_review": True,
            "requires_source_lineage_review": True,
        },
        "authority_boundary": {
            "memory_write_authorized": False,
            "prior_canonized": False,
            "truth_certified": False,
            "deployment_authorized": False,
            "publisher_finalized": False,
            "canonical_publication_mutated": False,
        },
        "runtime_boundary": {
            "live_atlas_call_performed": False,
            "network_call_performed": False,
            "model_call_performed": False,
            "live_sophia_call_performed": False,
            "live_sonya_call_performed": False,
        },
        "created_at": None,
        "meta": {},
    }


def write_atlas_memory_disposition_packet(
    memory_intent_path: Path, out_path: Path, route_trace_path: Path | None = None
) -> dict[str, Any]:
    memory_intent_packet = _read_json(memory_intent_path)
    route_trace = _read_json(route_trace_path) if route_trace_path else None
    packet = build_atlas_memory_disposition_packet(memory_intent_packet, route_trace)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    return packet


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an Atlas memory-intent disposition packet."
    )
    parser.add_argument("--memory-intent", required=True, type=Path)
    parser.add_argument("--route-trace", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    write_atlas_memory_disposition_packet(
        args.memory_intent, args.out, route_trace_path=args.route_trace
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
