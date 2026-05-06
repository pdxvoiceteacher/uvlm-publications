"""Phase 6 Atlas memory candidate classifier.

This module intentionally produces only a non-authoritative retrieval candidate
packet. It reads the Phase 6 handoff and Sophia adjudication artifacts to carry
forward the request identity and source artifact bindings, but it does not
authorize an Atlas memory write and it does not alter retrieval behavior.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "atlas.phase6_memory_candidate.v1"
CANDIDATE_STATUS = "shadow_only"
ALLOWED_USE = "retrieval_candidate"
BASE_REASON_CODES = [
    "not_truth_certification",
    "human_review_required",
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
SOURCE_POSTURE_KEYS = (
    "metrics_consistency_passed",
    "ready_for_retrosynthesis_seed",
    "application_portability_status",
    "domain_boundedness_status",
    "cross_domain_validation_status",
    "universal_claim_status",
)


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return payload


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def _string_dict(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {
        str(key): str(item)
        for key, item in value.items()
        if item not in (None, "")
    }


def _dict_value(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    return {}


def _artifact_ref_bindings(
    handoff_request: dict[str, Any],
) -> tuple[list[str], dict[str, str]]:
    raw_refs = _find_first_value(handoff_request, ("artifact_refs", "artifactRefs"))
    explicit_refs_by_key = _string_dict(
        _find_first_value(
            handoff_request, ("artifact_refs_by_key", "artifactRefsByKey")
        )
    )

    refs: list[str] = []
    refs_by_key: dict[str, str] = {}

    if isinstance(raw_refs, dict):
        refs_by_key = _string_dict(raw_refs)
        refs = list(refs_by_key.values())
    elif isinstance(raw_refs, list):
        for item in raw_refs:
            if isinstance(item, str):
                refs.append(item)
            elif isinstance(item, dict):
                item_refs_by_key = _string_dict(item)
                refs.extend(item_refs_by_key.values())
                refs_by_key.update(item_refs_by_key)
            elif item not in (None, ""):
                refs.append(str(item))
    elif raw_refs not in (None, ""):
        refs.append(str(raw_refs))

    if explicit_refs_by_key:
        refs_by_key = explicit_refs_by_key
    if not refs and refs_by_key:
        refs = list(refs_by_key.values())

    return refs, refs_by_key


def _artifact_sha256_bindings(
    handoff_request: dict[str, Any], refs_by_key: dict[str, str]
) -> tuple[dict[str, str], dict[str, str]]:
    raw_sha256s = _string_dict(
        _find_first_value(handoff_request, ("artifact_sha256s", "artifactSha256s"))
    )
    explicit_sha256s_by_key = _string_dict(
        _find_first_value(
            handoff_request, ("artifact_sha256s_by_key", "artifactSha256sByKey")
        )
    )

    path_keyed: dict[str, str] = {}
    role_keyed = dict(explicit_sha256s_by_key)

    for key, sha256 in raw_sha256s.items():
        if key in refs_by_key:
            path_keyed[refs_by_key[key]] = sha256
            role_keyed.setdefault(key, sha256)
        else:
            path_keyed[key] = sha256

    for role, sha256 in explicit_sha256s_by_key.items():
        ref = refs_by_key.get(role)
        if ref:
            path_keyed.setdefault(ref, sha256)

    for role, ref in refs_by_key.items():
        if ref in path_keyed:
            role_keyed.setdefault(role, path_keyed[ref])

    return path_keyed, role_keyed


def _source_posture(handoff_request: dict[str, Any]) -> dict[str, Any]:
    posture = _dict_value(
        _find_first_value(handoff_request, ("source_posture", "sourcePosture"))
    )
    return {
        key: posture.get(key)
        if key in posture
        else _find_first_value(handoff_request, (key, _camel_case(key)))
        for key in SOURCE_POSTURE_KEYS
    }


def _camel_case(value: str) -> str:
    first, *rest = value.split("_")
    return first + "".join(part.capitalize() for part in rest)


def _sophia_blocks_authoritative_memory_write(
    sophia_adjudication: dict[str, Any],
) -> bool:
    blocked = _find_first_value(
        sophia_adjudication,
        (
            "authoritative_memory_write_blocked",
            "authoritativeMemoryWriteBlocked",
        ),
    )
    if blocked is True:
        return True

    authorized = _find_first_value(
        sophia_adjudication,
        (
            "authoritative_memory_write",
            "authoritativeMemoryWrite",
            "memory_write_authorized",
            "memoryWriteAuthorized",
        ),
    )
    if authorized is False:
        return True
    if isinstance(authorized, str) and authorized.lower() in {
        "blocked",
        "deny",
        "denied",
        "false",
        "no",
    }:
        return True

    directive = _find_first_value(
        sophia_adjudication, ("sophia_directive", "sophiaDirective", "directive")
    )
    return (
        isinstance(directive, str)
        and "authoritative_memory_write" in directive
        and "block" in directive.lower()
    )


def _reason_codes(
    source_posture: dict[str, Any], sophia_adjudication: dict[str, Any]
) -> list[str]:
    reason_codes = list(BASE_REASON_CODES)

    if source_posture.get("cross_domain_validation_status") in (
        None,
        "not_yet_tested",
    ):
        reason_codes.append("cross_domain_validation_pending")
    if source_posture.get("ready_for_retrosynthesis_seed") is False:
        reason_codes.append("retrosynthesis_blocked")
    if source_posture.get("metrics_consistency_passed") is True:
        reason_codes.append("metrics_consistency_passed")
    if _sophia_blocks_authoritative_memory_write(sophia_adjudication):
        reason_codes.append("authoritative_memory_write_blocked")

    return reason_codes


def build_phase6_memory_candidate_packet(
    handoff_request: dict[str, Any],
    sophia_adjudication: dict[str, Any],
    *,
    handoff_request_ref: str | None = None,
    handoff_request_sha256: str | None = None,
    sophia_adjudication_ref: str | None = None,
    sophia_adjudication_sha256: str | None = None,
) -> dict[str, Any]:
    """Build a shadow-only Phase 6 memory candidate packet.

    The classifier is deliberately conservative: the candidate may be used only
    as a retrieval candidate, and human review remains required before any
    authoritative memory write could be considered by a separate workflow.
    """

    source_posture = _source_posture(handoff_request)
    artifact_refs, artifact_refs_by_key = _artifact_ref_bindings(handoff_request)
    artifact_sha256s, artifact_sha256s_by_key = _artifact_sha256_bindings(
        handoff_request, artifact_refs_by_key
    )

    return {
        "schema": SCHEMA,
        "request_id": _request_id(handoff_request, sophia_adjudication),
        "candidate_status": CANDIDATE_STATUS,
        "allowed_use": ALLOWED_USE,
        "memory_write_authorized": False,
        "reason_codes": _reason_codes(source_posture, sophia_adjudication),
        "artifact_refs": artifact_refs,
        "artifact_refs_by_key": artifact_refs_by_key,
        "artifact_sha256s": artifact_sha256s,
        "artifact_sha256s_by_key": artifact_sha256s_by_key,
        "handoff_request_ref": handoff_request_ref
        or _find_first_value(
            handoff_request, ("handoff_request_ref", "handoffRequestRef")
        ),
        "handoff_request_sha256": handoff_request_sha256
        or _find_first_value(
            handoff_request, ("handoff_request_sha256", "handoffRequestSha256")
        ),
        "sophia_adjudication_ref": sophia_adjudication_ref
        or _find_first_value(
            sophia_adjudication,
            ("sophia_adjudication_ref", "sophiaAdjudicationRef"),
        ),
        "sophia_adjudication_sha256": sophia_adjudication_sha256
        or _find_first_value(
            sophia_adjudication,
            ("sophia_adjudication_sha256", "sophiaAdjudicationSha256"),
        ),
        "sophia_directive": _find_first_value(
            sophia_adjudication, ("sophia_directive", "sophiaDirective", "directive")
        ),
        "sophia_retrosynthesis_status": _find_first_value(
            sophia_adjudication,
            (
                "sophia_retrosynthesis_status",
                "sophiaRetrosynthesisStatus",
                "retrosynthesis_status",
                "retrosynthesisStatus",
            ),
        ),
        "source_posture": source_posture,
        "guardrails": dict(GUARDRAILS),
    }


def write_phase6_memory_candidate_packet(
    handoff_request_path: Path, sophia_adjudication_path: Path, out_path: Path
) -> dict[str, Any]:
    handoff_request = _read_json(handoff_request_path)
    sophia_adjudication = _read_json(sophia_adjudication_path)
    packet = build_phase6_memory_candidate_packet(
        handoff_request,
        sophia_adjudication,
        handoff_request_ref=str(handoff_request_path),
        handoff_request_sha256=_sha256_file(handoff_request_path),
        sophia_adjudication_ref=str(sophia_adjudication_path),
        sophia_adjudication_sha256=_sha256_file(sophia_adjudication_path),
    )

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
