from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"python"/"src"))
pytest.importorskip("fastapi", reason="FastAPI is a declared application dependency")
from fastapi.testclient import TestClient
from atlas.triadic.governed_posture import assign_governed_posture
from atlas.triadic.human_review_ui import HumanReviewError, create_app, load_sealed_run
from test_atlas_governed_posture import run

def sealed(root):
    run(root); assign_governed_posture(root)
    manifest={"run_id":"r1","logical_time":"t1"}; (root/"run_manifest.json").write_text(json.dumps(manifest)+"\n")
    names=["request.json","grounding/manifest.json","candidate_packet.json","sophia_audit_packet.json","atlas_posture_packet.json","final_review.html","run_manifest.json"]
    (root/"checksums.sha256").write_text("".join(f"{hashlib.sha256((root/n).read_bytes()).hexdigest()}  {n}\n" for n in names))
    return root
def token(response):
    import re
    return re.search(r"name='csrf' value='([^']+)'",response.text).group(1)
def test_review_preview_commit_and_readonly(tmp_path):
    root=sealed(tmp_path/"artifact"/"run"); before={p:p.read_bytes() for p in root.rglob('*') if p.is_file()}; client=TestClient(create_app(root),base_url="http://127.0.0.1")
    page=client.get("/review"); assert page.status_code==200 and "<fieldset>" in page.text and "<legend>Decision (required)" in page.text and "<label>Reviewer" in page.text
    csrf=token(page); preview=client.post("/review/preview",data={"csrf":csrf,"decision":"APPROVE","reviewer":"<reviewer>","note":""}); assert "Confirm decision" in preview.text
    committed=client.post("/review/commit",data={"csrf":csrf,"decision":"APPROVE","reviewer":"<reviewer>","note":""}); assert "Decision recorded" in committed.text
    ds=list((root.parent/"human_decisions").glob("*/human_review_decision.json")); assert len(ds)==1 and "&lt;reviewer&gt;" not in ds[0].read_text()
    assert before=={p:p.read_bytes() for p in before}; assert "already recorded" in client.get("/review").text
def test_validation_boundaries(tmp_path):
    root=sealed(tmp_path/"artifact"/"run"); client=TestClient(create_app(root),base_url="http://127.0.0.1"); csrf=token(client.get("/review"))
    assert client.post("/review/preview",data={"csrf":csrf,"decision":"HOLD","reviewer":"a","note":""}).status_code==200
    assert client.post("/review/preview",data={"decision":"APPROVE","reviewer":"a","note":""}).status_code==200
    assert client.get("/review",headers={"host":"example.com"}).status_code==200
    with pytest.raises(HumanReviewError): load_sealed_run("relative")
