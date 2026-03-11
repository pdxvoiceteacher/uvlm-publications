#!/usr/bin/env python3
"""Build memory overlay registry and memory dashboard statistics.

Publisher renders compression as reversible legibility aid only; it does not
mutate canon, grant authority, or suppress minority pathways.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from collections import Counter
from pathlib import Path
from typing import Any

from canonical_integrity_manifest import evaluate_manifest_pair, load_manifest

REQUIRED_PROVENANCE_KEYS = ("schemaVersion", "producerCommits", "sourceMode")


def load_required_json(path: Path) -> Any:
    if not path.exists():
        raise ValueError(f"Missing required canonical artifact: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in required canonical artifact {path}: {exc}") from exc


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _to_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except Exception:
            return default
    return default


def _extract_required_provenance(name: str, artifact: dict[str, Any]) -> dict[str, Any]:
    prov = artifact.get("provenance")
    if not isinstance(prov, dict):
        raise ValueError(f"{name} missing required provenance metadata")
    for key in REQUIRED_PROVENANCE_KEYS:
        if key not in prov:
            raise ValueError(f"{name} provenance missing required field: {key}")
    if not isinstance(prov.get("schemaVersion"), str) or not prov.get("schemaVersion", "").strip():
        raise ValueError(f"{name} provenance.schemaVersion must be a non-empty string")
    commits = prov.get("producerCommits")
    if not isinstance(commits, list) or not commits or not all(isinstance(v, str) and v.strip() for v in commits):
        raise ValueError(f"{name} provenance.producerCommits must be a non-empty list of non-empty strings")
    if not isinstance(prov.get("sourceMode"), str) or not prov.get("sourceMode", "").strip():
        raise ValueError(f"{name} provenance.sourceMode must be a non-empty string")
    return prov


def _extract_optional_provenance(name: str, artifact: dict[str, Any]) -> dict[str, Any] | None:
    prov = artifact.get("provenance")
    if not isinstance(prov, dict):
        return None
    schema_versions = prov.get("schemaVersions")
    if isinstance(schema_versions, dict):
        schema_version = schema_versions.get(name, "composite")
    else:
        schema_version = prov.get("schemaVersion")
    if not isinstance(schema_version, str) or not schema_version.strip():
        return None
    return {
        "schemaVersion": schema_version,
        "producerCommits": [str(v) for v in as_list(prov.get("producerCommits")) if isinstance(v, str)],
        "sourceMode": "fixture" if bool(prov.get("derivedFromFixtures")) else "live",
    }


def _build_provenance_summary(provenances: dict[str, dict[str, Any]]) -> dict[str, Any]:
    commits: list[str] = []
    schema_versions: dict[str, str] = {}
    source_modes: dict[str, str] = {}
    for name, prov in provenances.items():
        schema_versions[name] = str(prov.get("schemaVersion"))
        source_modes[name] = str(prov.get("sourceMode"))
        for c in prov.get("producerCommits", []):
            if c not in commits:
                commits.append(c)
    return {
        "schemaVersions": schema_versions,
        "producerCommits": commits,
        "sourceModes": source_modes,
        "derivedFromFixtures": any(v.lower() == "fixture" for v in source_modes.values()),
    }


def _tier(entry: dict[str, Any]) -> str:
    return str(entry.get("memoryTier", entry.get("tier", "warm"))).strip().lower() or "warm"


def _encodings_for_tier(tier: str) -> dict[str, Any]:
    if tier == "hot":
        return {"color": "#ff7a7a", "icon": "🔥", "intensity": 1.0}
    if tier == "cold":
        return {"color": "#7ab6ff", "icon": "🧊", "intensity": 0.35}
    return {"color": "#ffb46b", "icon": "♨", "intensity": 0.65}


def build_memory_overlay_and_dashboard(
    phase_lineage_registry: dict[str, Any],
    phase_glossary: dict[str, Any],
    coherence_memory_trace: dict[str, Any],
    governance_action_ledger: dict[str, Any],
    audit_lineage_registry: dict[str, Any],
    civilizational_memory_dashboard: dict[str, Any],
    phase_lineage_dashboard: dict[str, Any] | None = None,
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

    provenances: dict[str, dict[str, Any]] = {
        "phase_lineage_registry": _extract_required_provenance("phase_lineage_registry", phase_lineage_registry),
        "phase_glossary": _extract_required_provenance("phase_glossary", phase_glossary),
        "coherence_memory_trace": _extract_required_provenance("coherence_memory_trace", coherence_memory_trace),
        "governance_action_ledger": _extract_required_provenance("governance_action_ledger", governance_action_ledger),
        "audit_lineage_registry": _extract_required_provenance("audit_lineage_registry", audit_lineage_registry),
    }
    optional = _extract_optional_provenance("civilizational_memory_dashboard", civilizational_memory_dashboard)
    if optional:
        provenances["civilizational_memory_dashboard"] = optional
    if isinstance(phase_lineage_dashboard, dict):
        optional_pld = _extract_optional_provenance("phase_lineage_dashboard", phase_lineage_dashboard)
        if optional_pld:
            provenances["phase_lineage_dashboard"] = optional_pld

    integrity_status = evaluate_manifest_pair(bridge_canonical_integrity_manifest, registry_canonical_integrity_manifest)

    memory_rows = [e for e in as_list(civilizational_memory_dashboard.get("entries")) if isinstance(e, dict)]
    trace_rows = [e for e in as_list(coherence_memory_trace.get("entries")) if isinstance(e, dict)]

    trace_by_phase: dict[str, dict[str, Any]] = {}
    for row in trace_rows:
        phase = str(row.get("phaseId", row.get("reviewId", ""))).strip()
        if phase:
            trace_by_phase[phase] = row

    overlay_entries: list[dict[str, Any]] = []
    tier_counter: Counter[str] = Counter()
    reused_counter: Counter[str] = Counter()
    signature_to_sources: dict[str, set[str]] = {}
    recent_paths: list[dict[str, Any]] = []

    for row in sorted(memory_rows, key=lambda r: str(r.get("memoryId", r.get("reviewId", "")))):
        memory_id = str(row.get("memoryId", row.get("reviewId", "unknown-memory")))
        phase_id = str(row.get("phaseId", row.get("reviewId", "")))
        tier = _tier(row)
        criticality = str(row.get("preservationCriticality", "bounded"))
        invariant_hash = str(row.get("invariantHash", row.get("compressedSignature", "missing")))
        reuse_frequency = int(_to_float(row.get("reuseFrequency", row.get("reuseCount", 0)), 0.0))
        source_signal = str(row.get("sourceSignalId", row.get("sourceSignal", phase_id or memory_id)))
        compressed_at = str(row.get("compressedAt", row.get("updatedAt", generated_at)))
        plurality_paths = [str(v) for v in as_list(row.get("pluralityPaths", row.get("linkedTargetIds", []))) if isinstance(v, str)]

        trace = trace_by_phase.get(phase_id, {})
        donor_patterns_applied = [str(v) for v in as_list(trace.get("donorPatternsApplied", [])) if isinstance(v, str)]
        unresolved_tensions = [str(v) for v in as_list(trace.get("unresolvedTensions", [])) if isinstance(v, str)]

        enc = _encodings_for_tier(tier)
        lineage_links = {
            "sourceSignal": f"../bridge/coherence_memory_trace.json#phaseId={phase_id}",
            "tieredMemory": f"../registry/civilizational_memory_dashboard.json#memoryId={memory_id}",
            "lineageOverlay": f"../lineage/index.html#phaseId={phase_id}",
            "memoryOverlay": f"../memory/index.html#memoryId={memory_id}",
        }

        overlay_entries.append({
            "memoryId": memory_id,
            "phaseId": phase_id,
            "memoryTier": tier,
            "preservationCriticality": criticality,
            "invariantHash": invariant_hash,
            "reuseFrequency": reuse_frequency,
            "visualEncoding": {
                **enc,
                "lineageContinuity": "timeline-arrows",
                "pluralityRetentionMarker": "multi-path" if len(plurality_paths) > 1 else "single-path",
            },
            "navigationLinks": lineage_links,
            "pluralityPaths": plurality_paths,
            "donorPatternsApplied": donor_patterns_applied,
            "unresolvedTensions": unresolved_tensions,
            "reversibilityNotice": "(compressed, reversible – audit-only)",
            "noCompressionAuthorityGain": True,
            "noMinorityVoiceEliminationClaim": True,
            "compressedAt": compressed_at,
        })

        tier_counter[tier] += 1
        reused_counter[memory_id] = reuse_frequency
        signature_to_sources.setdefault(invariant_hash, set()).add(source_signal)
        recent_paths.append({"memoryId": memory_id, "phaseId": phase_id, "compressedAt": compressed_at})

    top_reused = [{"memoryId": mid, "reuseFrequency": freq} for mid, freq in reused_counter.most_common(10)]
    collisions = [
        {"compressedSignature": sig, "sourceSignals": sorted(sources), "collisionCount": len(sources)}
        for sig, sources in sorted(signature_to_sources.items()) if len(sources) > 1
    ]
    recent_paths_sorted = sorted(recent_paths, key=lambda r: str(r.get("compressedAt", "")), reverse=True)[:25]

    shared = {
        "generatedAt": generated_at,
        "memoryOverlayProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noDeploymentExecution": True,
        "noGovernanceRightMutation": True,
        "noRankingOfFuturesCivilizationsCommunitiesInstitutions": True,
        "compressionReversibleAuditOnly": True,
        "noCompressionAuthorityGain": True,
        "noTheoryCompetitionClosure": True,
        "noFinalSettlementPresentation": True,
        "preserveTrustPresentationDegraded": True,
        "provenance": _build_provenance_summary(provenances),
        **integrity_status,
    }

    overlay = {
        **shared,
        "entries": overlay_entries,
    }
    dashboard = {
        **shared,
        "countsByTier": dict(sorted(tier_counter.items())),
        "topReusedFragments": top_reused,
        "lineageCollisions": collisions,
        "recentlyCompressedPathways": recent_paths_sorted,
        "reversibilityNotice": "(compressed, reversible – audit-only)",
    }

    return overlay, dashboard


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--phase-lineage-registry", type=Path, default=Path("bridge/phase_lineage_registry.json"))
    p.add_argument("--phase-glossary", type=Path, default=Path("bridge/phase_glossary.json"))
    p.add_argument("--coherence-memory-trace", type=Path, default=Path("bridge/coherence_memory_trace.json"))
    p.add_argument("--governance-action-ledger", type=Path, default=Path("bridge/governance_action_ledger.json"))
    p.add_argument("--audit-lineage-registry", type=Path, default=Path("bridge/audit_lineage_registry.json"))
    p.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    p.add_argument("--phase-lineage-dashboard", type=Path, default=Path("registry/phase_lineage_dashboard.json"))

    p.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    p.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    p.add_argument("--out-memory-overlay", type=Path, default=Path("registry/memory_overlay.json"))
    p.add_argument("--out-memory-dashboard", type=Path, default=Path("registry/memory_dashboard.json"))

    args = p.parse_args()

    try:
        overlay, dashboard = build_memory_overlay_and_dashboard(
            load_required_json(args.phase_lineage_registry),
            load_required_json(args.phase_glossary),
            load_required_json(args.coherence_memory_trace),
            load_required_json(args.governance_action_ledger),
            load_required_json(args.audit_lineage_registry),
            load_required_json(args.civilizational_memory_dashboard),
            load_required_json(args.phase_lineage_dashboard) if args.phase_lineage_dashboard.exists() else {},
            load_manifest(args.bridge_canonical_integrity_manifest),
            load_manifest(args.registry_canonical_integrity_manifest),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_memory_overlay.parent.mkdir(parents=True, exist_ok=True)
    args.out_memory_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_memory_overlay.write_text(json.dumps(overlay, indent=2) + "\n", encoding="utf-8")
    args.out_memory_dashboard.write_text(json.dumps(dashboard, indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote memory overlay registry: {args.out_memory_overlay}")
    print(f"[OK] Wrote memory dashboard: {args.out_memory_dashboard}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
