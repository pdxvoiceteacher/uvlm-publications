from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from atlas.triadic import governed_posture as posture
from atlas.triadic.governed_posture import assign_governed_posture
from atlas.triadic.governed_posture_explain import (
    GovernedPostureExplanationError,
    build_atlas_explanation,
    load_atlas_explanation,
)
from atlas.triadic.human_review_ui import HumanReviewError, create_app
from test_atlas_governed_posture import run


def sealed(root: Path, disposition: str = "PASS") -> Path:
    run(root, disposition)
    assign_governed_posture(root)
    (root / "run_manifest.json").write_text('{"logical_time":"t1","run_id":"r1"}\n')
    (root / "grounding" / "source.md").write_text("source\n")
    (root / "grounding" / "conversion_report.json").write_text("{}\n")
    (root / "lifecycle_events.jsonl").write_text('{"event":"review"}\n')
    names = sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())
    (root / "checksums.sha256").write_text("".join(f"{hashlib.sha256((root / name).read_bytes()).hexdigest()}  {name}\n" for name in names))
    return root


def sophia_explanation(root: Path, output: Path, *, repairable: bool = True) -> Path:
    candidate = json.loads((root / "candidate_packet.json").read_text())
    audit = json.loads((root / "sophia_audit_packet.json").read_text())
    packet = {
        "schema_id": "uvlm.sophia.explanation_packet.v1", "schema_version": "1.0", "packet_type": "sophia_explanation",
        "run_id": "r1", "logical_time": "t1", "producer_repository": "pdxvoiceteacher/Sophia",
        "parents": [
            {"artifact_type": "candidate_packet", "path": "candidate_packet.json", "file_sha256": hashlib.sha256((root / "candidate_packet.json").read_bytes()).hexdigest(), "canonical_sha256": hashlib.sha256(posture._canon(candidate)).hexdigest()},
            {"artifact_type": "sophia_audit_packet", "path": "sophia_audit_packet.json", "file_sha256": hashlib.sha256((root / "sophia_audit_packet.json").read_bytes()).hexdigest(), "canonical_sha256": hashlib.sha256(posture._canon(audit)).hexdigest()},
        ],
        "disposition": audit["disposition"], "overall_reason": "Sophia evaluated bounded evidence without certifying truth.",
        "claim_explanations": [{"claim_id": "c1", "evidence_status": "supported", "maturity_status": "draft", "uncertainty_status": "partial", "reason_codes": ["a"], "plain_language_reason": "The cited segment supports this draft claim.", "evidence_refs": ["seg"], "repair_constraints": [{"code": "ADD_SUPPORT", "instruction": "Add bounded support."}]}],
        "repairable": repairable, "authority_boundary": dict.fromkeys(posture.SOPHIA_NONAUTH, False), "side_effects": dict.fromkeys(posture.SOPHIA_EFFECTS, False), "nonauthority": "No authority is granted.",
    }
    output.write_bytes(posture._canon(packet) + b"\n")
    return output


def loopback(app):
    async def wrapped(scope, receive, send):
        scope = dict(scope); scope["client"] = ("127.0.0.1", 1)
        await app(scope, receive, send)
    return wrapped


@pytest.mark.parametrize("disposition,retention,publication", [("PASS", "retain_for_human_review", "publication_blocked_pending_human_review"), ("HOLD", "quarantine", "do_not_publish"), ("REJECT", "rejected", "do_not_publish")])
def test_deterministic_posture_explanations_and_immutability(tmp_path: Path, disposition: str, retention: str, publication: str):
    root = sealed(tmp_path / "run", disposition); before = {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
    sophia = sophia_explanation(root, tmp_path / "sophia_explanation_packet.json")
    first = build_atlas_explanation(root, sophia, tmp_path / "external")
    second = build_atlas_explanation(root, sophia, tmp_path / "external")
    data = (tmp_path / "external" / "atlas_explanation_packet.json").read_bytes()
    assert first == second and data == posture._canon(first) + b"\n"
    assert first["posture_explanations"]["retention"].startswith("This candidate")
    assert retention in first["posture_explanations"]["retention"] or disposition == "PASS"
    assert first["decision_meanings"]["APPROVE"].startswith("accept this bounded output")
    assert first["permitted_next_actions"] == ["REQUEST_REPAIR", "RECORD_DECISION", "EXPORT_EVIDENCE"]
    assert all(value is False for value in first["authority_boundary"].values()) and all(value is False for value in first["side_effects"].values())
    assert before == {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
    assert publication in json.loads((root / "atlas_posture_packet.json").read_text())["publication_posture"]


def test_cli_ui_and_optional_explanation_receipt_binding(tmp_path: Path):
    root = sealed(tmp_path / "run"); sophia = sophia_explanation(root, tmp_path / "sophia.json"); external = tmp_path / "external"
    command = [sys.executable, "-m", "atlas.triadic.governed_posture_explain", "--run-root", str(root), "--sophia-explanation", str(sophia), "--output-root", str(external)]
    env = {**os.environ, "PYTHONPATH": "python/src"}
    assert subprocess.run(command, cwd=Path(__file__).resolve().parents[1], env=env, check=False).returncode == 0
    explanation = external / "atlas_explanation_packet.json"
    app = create_app(root, explanation_path=explanation)
    client = TestClient(loopback(app), base_url="http://127.0.0.1")
    review = client.get("/review")
    assert review.status_code == 200
    for heading in ("Why Sophia reached this disposition", "Why Atlas has this posture", "What your choices mean"):
        assert heading in review.text
    csrf = __import__("re").search(r'name="csrf" value="([^"]+)"', review.text).group(1)
    preview = client.post("/review/preview", data={"csrf": csrf, "decision": "APPROVE", "reviewer": "Reviewer", "note": ""})
    fields = dict(__import__("re").findall(r'name="([^"]+)" value="([^"]*)"', preview.text))
    assert client.post("/review/commit", data=fields).status_code == 200
    receipt = json.loads(next((root.parent / "human_decisions").glob("*/human_review_decision.json")).read_text())
    assert receipt["explanation_evidence_bindings"]["atlas_explanation_packet_file_sha256"] == hashlib.sha256(explanation.read_bytes()).hexdigest()


@pytest.mark.parametrize("mutation,code", [
    (lambda root, sophia: (root / "atlas_posture_packet.json").write_text('{"retention_posture":"unknown"}\n'), "SEALED_RUN_INVALID"),
    (lambda root, sophia: sophia.write_text('{"schema_id":"wrong"}\n'), "SOPHIA_EXPLANATION_INVALID"),
    (lambda root, sophia: sophia.write_text(sophia.read_text().replace('"run_id":"r1"', '"run_id":"wrong"')), "SOPHIA_EXPLANATION_RUN_MISMATCH"),
])
def test_invalid_inputs_fail_closed(tmp_path: Path, mutation, code: str):
    root = sealed(tmp_path / "run"); sophia = sophia_explanation(root, tmp_path / "sophia.json"); mutation(root, sophia)
    with pytest.raises(GovernedPostureExplanationError, match=code):
        build_atlas_explanation(root, sophia, tmp_path / "external")


def test_output_inside_run_and_symlink_explanation_rejected(tmp_path: Path):
    root = sealed(tmp_path / "run"); sophia = sophia_explanation(root, tmp_path / "sophia.json")
    with pytest.raises(GovernedPostureExplanationError, match="OUTPUT_INSIDE_SEALED_RUN"):
        build_atlas_explanation(root, sophia, root / "external")
    link = tmp_path / "link.json"; link.symlink_to(sophia)
    with pytest.raises(GovernedPostureExplanationError, match="SOPHIA_EXPLANATION_UNSAFE"):
        build_atlas_explanation(root, link, tmp_path / "external")


def test_production_mapping_sensitivity(tmp_path: Path, monkeypatch):
    root = sealed(tmp_path / "run"); sophia = sophia_explanation(root, tmp_path / "sophia.json")
    monkeypatch.delitem(__import__("atlas.triadic.governed_posture_explain", fromlist=["POSTURE_TEXT"]).POSTURE_TEXT["retention_posture"], "retain_for_human_review")
    with pytest.raises(GovernedPostureExplanationError, match="UNKNOWN_ATLAS_POSTURE"):
        build_atlas_explanation(root, sophia, tmp_path / "external")

@pytest.mark.parametrize("mutator,code", [
    (lambda packet: packet["parents"][0].update(file_sha256="0" * 64), "SOPHIA_EXPLANATION_PARENT_MISMATCH"),
    (lambda packet: packet.update(raw_output="forbidden"), "SOPHIA_EXPLANATION_INVALID"),
    (lambda packet: packet["authority_boundary"].update(publication=True), "SOPHIA_EXPLANATION_AUTHORITY"),
])
def test_sophia_explanation_parent_private_and_authority_boundaries(tmp_path: Path, mutator, code: str):
    root = sealed(tmp_path / "run"); sophia = sophia_explanation(root, tmp_path / "sophia.json")
    packet = json.loads(sophia.read_text()); mutator(packet); sophia.write_bytes(posture._canon(packet) + b"\n")
    with pytest.raises(GovernedPostureExplanationError, match=code):
        build_atlas_explanation(root, sophia, tmp_path / "external")


def test_unknown_posture_fails_after_valid_checksum_reseal(tmp_path: Path):
    root = sealed(tmp_path / "run"); sophia = sophia_explanation(root, tmp_path / "sophia.json")
    atlas = json.loads((root / "atlas_posture_packet.json").read_text()); atlas["retention_posture"] = "unknown"
    (root / "atlas_posture_packet.json").write_bytes(posture._canon(atlas) + b"\n")
    names = sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file() and path.name != "checksums.sha256")
    (root / "checksums.sha256").write_text("".join(f"{hashlib.sha256((root / name).read_bytes()).hexdigest()}  {name}\n" for name in names))
    with pytest.raises(GovernedPostureExplanationError, match="UNKNOWN_ATLAS_POSTURE"):
        build_atlas_explanation(root, sophia, tmp_path / "external")
