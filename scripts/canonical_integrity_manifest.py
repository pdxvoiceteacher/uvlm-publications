"""Canonical integrity manifest helper for bridge/registry artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

REQUIRED_MANIFEST_FIELDS = (
    "originProject",
    "canonicalPhaselock",
    "modificationDisclosureRequired",
    "ethicalBoundaryNotice",
    "commonsIntegrityNotice",
    "constraintSignatureVersion",
    "constraintSignatureSha256",
)


def load_manifest(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in canonical integrity manifest {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"Canonical integrity manifest at {path} must be a JSON object")
    return payload


def immutable_constraint_payload(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "originProject": manifest.get("originProject"),
        "canonicalPhaselock": manifest.get("canonicalPhaselock"),
        "modificationDisclosureRequired": bool(manifest.get("modificationDisclosureRequired", False)),
        "ethicalBoundaryNotice": manifest.get("ethicalBoundaryNotice"),
        "commonsIntegrityNotice": manifest.get("commonsIntegrityNotice"),
        "constraintSignatureVersion": manifest.get("constraintSignatureVersion"),
    }


def compute_constraint_signature_sha256(manifest: dict[str, Any]) -> str:
    payload = immutable_constraint_payload(manifest)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _has_required_fields(manifest: dict[str, Any]) -> bool:
    return all(field in manifest for field in REQUIRED_MANIFEST_FIELDS)


def _is_valid_manifest(manifest: dict[str, Any]) -> bool:
    if not _has_required_fields(manifest):
        return False
    expected = compute_constraint_signature_sha256(manifest)
    given = str(manifest.get("constraintSignatureSha256", "")).lower().strip()
    return bool(given) and expected == given


def evaluate_manifest_pair(
    bridge_manifest: dict[str, Any] | None,
    registry_manifest: dict[str, Any] | None,
) -> dict[str, Any]:
    bridge_valid = isinstance(bridge_manifest, dict) and _is_valid_manifest(bridge_manifest)
    registry_valid = isinstance(registry_manifest, dict) and _is_valid_manifest(registry_manifest)

    manifests_present = isinstance(bridge_manifest, dict) and isinstance(registry_manifest, dict)
    same_signature = False
    if bridge_valid and registry_valid:
        same_signature = (
            str(bridge_manifest.get("constraintSignatureVersion")) == str(registry_manifest.get("constraintSignatureVersion"))
            and str(bridge_manifest.get("constraintSignatureSha256")).lower() == str(registry_manifest.get("constraintSignatureSha256")).lower()
        )

    canonical_integrity_verified = bool(manifests_present and bridge_valid and registry_valid and same_signature)

    modification_disclosure_required = bool(
        (bridge_manifest or {}).get("modificationDisclosureRequired", False)
        or (registry_manifest or {}).get("modificationDisclosureRequired", False)
    )
    modification_disclosure_missing = bool(modification_disclosure_required and not canonical_integrity_verified)

    trust_presentation_degraded = not canonical_integrity_verified

    selected = bridge_manifest if isinstance(bridge_manifest, dict) else (registry_manifest if isinstance(registry_manifest, dict) else {})
    return {
        "canonicalIntegrityVerified": canonical_integrity_verified,
        "modificationDisclosureMissing": modification_disclosure_missing,
        "trustPresentationDegraded": trust_presentation_degraded,
        "originProject": selected.get("originProject", "unknown"),
        "canonicalPhaselock": selected.get("canonicalPhaselock", "unknown"),
        "ethicalBoundaryNotice": selected.get("ethicalBoundaryNotice", "unknown"),
        "commonsIntegrityNotice": selected.get("commonsIntegrityNotice", "unknown"),
        "constraintSignatureVersion": selected.get("constraintSignatureVersion", "unknown"),
        "constraintSignatureSha256": selected.get("constraintSignatureSha256", "unknown"),
    }
