"""Loopback-only, file-bound human decision capture for sealed Atlas reviews."""
from __future__ import annotations

import argparse
import hashlib
import html
import ipaddress
import json
import os
import secrets
import socket
import uuid
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from urllib.parse import parse_qs

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn


class HumanReviewError(ValueError):
    """A bounded structural error that never includes sealed content."""


REQUIRED = ("request.json", "grounding/manifest.json", "candidate_packet.json",
            "sophia_audit_packet.json", "atlas_posture_packet.json", "final_review.html",
            "run_manifest.json", "checksums.sha256")
AUTH = ("truth_certification", "final_answer_authority", "memory_write_authority",
        "pmr_write_authority", "canonization", "publication", "doi_mutation",
        "crossref_deposit", "catalog_mutation", "knowledge_graph_mutation", "deployment",
        "release", "model_invocation", "candidate_alteration", "sophia_alteration",
        "atlas_posture_alteration", "external_action_authority", "automatic_phase_advance")
EFFECTS = ("network_access_beyond_loopback", "model_invocation_performed",
           "candidate_mutation_performed", "sophia_mutation_performed",
           "atlas_posture_mutation_performed", "sealed_run_mutation_performed",
           "memory_write_performed", "pmr_write_performed", "canonization_performed",
           "publication_performed", "doi_mutated", "crossref_deposit_performed",
           "catalog_mutated", "knowledge_graph_mutated", "deployment_performed", "release_performed")
HEADERS = {"Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'; frame-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'", "X-Content-Type-Options": "nosniff", "Referrer-Policy": "no-referrer", "Cache-Control": "no-store"}


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise HumanReviewError("sealed JSON artifact is invalid") from error
    if not isinstance(value, dict):
        raise HumanReviewError("sealed JSON artifact is invalid")
    return value


def _safe_root(value: str | Path) -> Path:
    original = Path(value)
    if not original.is_absolute() or original.is_symlink() or original == Path(original.anchor):
        raise HumanReviewError("run root must be an absolute, non-root, non-symlink directory")
    root = original.resolve()
    if not root.is_dir():
        raise HumanReviewError("run root must be an existing directory")
    return root


def _inputs(root: Path) -> dict[str, bytes]:
    values: dict[str, bytes] = {}
    for name in REQUIRED:
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise HumanReviewError("sealed required artifact is missing or unsafe")
        try:
            path.resolve().relative_to(root)
        except ValueError as error:
            raise HumanReviewError("sealed required artifact is outside run root") from error
        values[name] = path.read_bytes()
    return values


def _verify_checksums(files: dict[str, bytes]) -> None:
    try:
        lines = files["checksums.sha256"].decode("utf-8").splitlines()
    except UnicodeDecodeError as error:
        raise HumanReviewError("checksum file is invalid") from error
    expected = {line.split(maxsplit=1)[1].lstrip(" *"): line.split(maxsplit=1)[0]
                for line in lines if len(line.split(maxsplit=1)) == 2}
    required = set(REQUIRED) - {"checksums.sha256"}
    if not required <= expected.keys() or any(expected[name] != _sha(files[name]) for name in required):
        raise HumanReviewError("sealed checksum verification failed")


def load_sealed_run(run_root: str | Path) -> dict[str, Any]:
    root = _safe_root(run_root); files = _inputs(root); _verify_checksums(files)
    request, manifest, candidate, sophia, atlas, run = (_json(root / n) for n in REQUIRED[:5] + ("run_manifest.json",))
    ids = [(x.get("run_id"), x.get("logical_time")) for x in (request, candidate, sophia, atlas, run)]
    if not all(pair == ids[0] for pair in ids) or not all(ids[0]):
        raise HumanReviewError("sealed run identity mismatch")
    if sophia.get("disposition") not in {"PASS", "HOLD", "REJECT"} or atlas.get("requires_human_review") is not True or atlas.get("human_decision") != "PENDING":
        raise HumanReviewError("sealed review is not eligible for a human decision")
    return {"root": root, "files": files, "hashes": {n: _sha(v) for n, v in files.items()},
            "request": request, "manifest": manifest, "candidate": candidate, "sophia": sophia, "atlas": atlas}


def _decision_root(sealed: dict[str, Any], value: str | Path | None) -> Path:
    root = sealed["root"]; parent = root.parent
    candidate = (Path(value) if value else parent / "human_decisions")
    if not candidate.is_absolute() or candidate.is_symlink():
        raise HumanReviewError("decision root must be a safe absolute directory")
    resolved = candidate.resolve()
    try: resolved.relative_to(parent)
    except ValueError as error: raise HumanReviewError("decision root must remain below artifact parent") from error
    if resolved == root: raise HumanReviewError("decision root cannot be sealed run root")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def _existing(decision_root: Path, run_id: str) -> Path | None:
    for packet in decision_root.glob("*/human_review_decision.json"):
        try:
            if _json(packet).get("run_id") == run_id: return packet.parent
        except HumanReviewError: continue
    return None


def _esc(value: Any) -> str: return html.escape(str(value), quote=True)
def _page(title: str, body: str) -> HTMLResponse: return HTMLResponse(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{_esc(title)}</title><style>body{{max-width:55rem;margin:auto;font:1.1rem sans-serif;padding:1rem}}label{{display:block;padding:.5rem}}.error{{border:2px solid #900;padding:.5rem}}fieldset{{padding:1rem}}</style></head><body>{body}</body></html>", headers=HEADERS)


def _review_body(s: dict[str, Any], token: str, errors: list[str] | None = None, values: dict[str, str] | None = None) -> str:
    values = values or {}; e = "" if not errors else "<div id='errors' class='error' tabindex='-1'><h2>Correct these fields</h2><ul>" + "".join(f"<li>{_esc(x)}</li>" for x in errors) + "</ul></div>"
    r,c,so,a=s["request"],s["candidate"],s["sophia"],s["atlas"]
    claims="".join(f"<li>{_esc(x.get('claim_id',''))}: {_esc(x.get('text',''))}</li>" for x in c.get("claims",[]) if isinstance(x,dict))
    return f"<h1>Local human review decision</h1>{e}<p>Review the sealed material, then record one bounded decision. Required fields are marked required.</p><p><b>Run:</b> {_esc(r['run_id'])} | <b>Logical time:</b> {_esc(r['logical_time'])}</p><p><b>Question:</b> {_esc(r.get('question',''))}<br><b>Model provenance:</b> {_esc(r.get('model_id',''))}<br><b>Candidate:</b> {_esc(c.get('answer',''))}<br><b>Uncertainty:</b> {_esc(c.get('uncertainty',''))}</p><h2>Claims</h2><ul>{claims}</ul><p><b>Sophia:</b> {_esc(so.get('disposition',''))} — {_esc(', '.join(so.get('reason_codes',[])))}</p><p><b>Atlas:</b> {_esc(a.get('retention_posture',''))} | {_esc(a.get('publication_posture',''))}</p><p>None of these options certifies truth or authorizes memory, canonization, publication, deployment, or release.</p><p><a href='/sealed-review'>Open the exact sealed review</a></p><form method='post' action='/review/preview'><input type='hidden' name='csrf' value='{_esc(token)}'><fieldset><legend>Decision (required)</legend>{''.join(f"<label><input type='radio' name='decision' value='{d}' {'checked' if values.get('decision')==d else ''}> {d}: {_esc(desc)}</label>" for d,desc in [('APPROVE','accept this bounded output for the stated task.'),('HOLD','the route worked, but correction is required before closeout.'),('REJECT','the route worked, but the output is not accepted.')])}</fieldset><label>Reviewer display name (required)<input name='reviewer' required value='{_esc(values.get('reviewer',''))}' aria-invalid='{str(bool(errors)).lower()}'></label><label>Decision note (required for HOLD or REJECT)<textarea name='note'>{_esc(values.get('note',''))}</textarea></label><button type='submit'>Preview decision</button></form>"


def _form(request: Request) -> dict[str, str]:
    return {k: v[-1] for k,v in parse_qs(request.scope.get("_body", b"").decode("utf-8"), keep_blank_values=True).items()}


def _loopback(host: str) -> bool:
    try: return all(ipaddress.ip_address(x[4][0]).is_loopback for x in socket.getaddrinfo(host, None, type=socket.SOCK_STREAM))
    except (socket.gaierror, ValueError): return False


def create_app(run_root: str | Path, decision_root: str | Path | None = None) -> FastAPI:
    sealed = load_sealed_run(run_root); out = _decision_root(sealed, decision_root); token = secrets.token_urlsafe(32); used = False
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    def guard(request: Request, form: dict[str,str] | None = None) -> None:
        host=request.headers.get("host","").split(":")[0].strip("[]")
        if not host or not _loopback(host): raise HumanReviewError("local request boundary rejected")
        if request.headers.get("origin") not in (None, "", f"http://{request.headers.get('host')}") or request.headers.get("sec-fetch-site") not in (None,"", "same-origin", "none"): raise HumanReviewError("local request boundary rejected")
        if form is not None and not secrets.compare_digest(form.get("csrf",""),token): raise HumanReviewError("request validation failed")
    @app.middleware("http")
    async def boundary(request: Request, call_next):
        try:
            if request.method == "POST": request.scope["_body"] = await request.body()
            guard(request)
            response=await call_next(request)
        except HumanReviewError: response=_page("Request rejected", "<h1 tabindex='-1'>Request rejected</h1><p>The local review request could not be accepted.</p>")
        for k,v in HEADERS.items(): response.headers[k]=v
        return response
    @app.get("/review")
    async def review():
        existing=_existing(out,sealed["request"]["run_id"])
        if existing: return _page("Decision already recorded", "<h1 tabindex='-1'>Decision already recorded</h1><p>This run is read-only; a decision receipt already exists.</p>")
        return _page("Local human review", _review_body(sealed,token))
    @app.get("/sealed-review")
    async def sealed_review(): return HTMLResponse(sealed["files"]["final_review.html"], headers=HEADERS)
    @app.post("/review/preview")
    async def preview(request: Request):
        form=_form(request); guard(request,form); decision=form.get("decision",""); reviewer=form.get("reviewer","").strip(); note=form.get("note","").strip(); errors=[]
        if decision not in {"APPROVE","HOLD","REJECT"}: errors.append("Choose APPROVE, HOLD, or REJECT.")
        if not reviewer: errors.append("Reviewer display name is required.")
        if decision in {"HOLD","REJECT"} and not note: errors.append("A decision note is required for HOLD or REJECT.")
        if errors: return _page("Correct decision",_review_body(sealed,token,errors,form))
        data={"decision":decision,"reviewer":reviewer,"note":note}
        details="".join(f"<li>{_esc(k)}: {_esc(v)}</li>" for k,v in data.items())+"".join(f"<li>{_esc(k)}: {_esc(sealed['hashes'][k])}</li>" for k in ("candidate_packet.json","sophia_audit_packet.json","atlas_posture_packet.json","final_review.html"))
        return _page("Confirm decision",f"<h1>Confirm decision</h1><p>Review these details. This records a bounded human decision only.</p><ul>{details}</ul><form method='post' action='/review/commit'><input type='hidden' name='csrf' value='{_esc(token)}'><input type='hidden' name='decision' value='{_esc(decision)}'><input type='hidden' name='reviewer' value='{_esc(reviewer)}'><input type='hidden' name='note' value='{_esc(note)}'><button type='submit'>Confirm decision</button></form><form method='get' action='/review'><button type='submit'>Return and edit</button></form>")
    @app.post("/review/commit")
    async def commit(request: Request):
        nonlocal used
        form=_form(request); guard(request,form)
        if used or _existing(out,sealed["request"]["run_id"]): raise HumanReviewError("decision already recorded")
        decision,reviewer,note=form.get("decision",""),form.get("reviewer","").strip(),form.get("note","").strip()
        if decision not in {"APPROVE","HOLD","REJECT"} or not reviewer or (decision in {"HOLD","REJECT"} and not note): raise HumanReviewError("request validation failed")
        if _inputs(sealed["root"]) != sealed["files"]: raise HumanReviewError("sealed run changed")
        did=str(uuid.uuid4()); dest=out/did; dest.mkdir()
        packet={"schema_id":"uvlm.human_review_decision.v1","schema_version":"1.0","packet_type":"human_review_decision","decision_id":did,"run_id":sealed["request"]["run_id"],"logical_time":sealed["request"]["logical_time"],"generated_at_utc":datetime.now(timezone.utc).isoformat(),"reviewer":{"display_name":reviewer,"identity_assurance":"local_assertion_only","cryptographic_signature_present":False},"decision":decision,"decision_note":note,"source":{"interface":"atlas_local_human_review_ui","loopback_only":True},"evidence_bindings":sealed["hashes"],"sophia_disposition":sealed["sophia"]["disposition"],"atlas_retention_posture":sealed["atlas"].get("retention_posture"),"atlas_publication_posture":sealed["atlas"].get("publication_posture"),"requires_human_review":True,"authority_boundary":dict.fromkeys(AUTH,False),"side_effects":dict.fromkeys(EFFECTS,False),"nonauthority":"This receipt records a bounded human decision and grants no operational authority."}
        data=json.dumps(packet,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()+b"\n"
        for name,content in (("human_review_decision.json",data),("human_review_decision.json.sha256",(_sha(data)+"  human_review_decision.json\n").encode()),("human_review_decision_receipt.html",f"<!doctype html><html><body><h1>Human decision receipt</h1><p>This receipt records a human decision. It does not certify truth. It does not authorize memory, canonization, publication, deployment, or release.</p><p>{_esc(decision)} — {_esc(reviewer)} — {_esc(note)}</p><p>Run {_esc(packet['run_id'])}</p></body></html>".encode())):
            with NamedTemporaryFile(dir=dest,delete=False) as f: f.write(content); temp=f.name
            os.replace(temp,dest/name)
        used=True
        return _page("Decision recorded","<h1 tabindex='-1'>Decision recorded</h1><p>The immutable bounded decision receipt was written outside the sealed run root.</p>")
    return app


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--run-root",required=True); parser.add_argument("--decision-root"); parser.add_argument("--host",default="127.0.0.1"); parser.add_argument("--port",type=int,default=8765); parser.add_argument("--no-browser",action="store_true")
    args=parser.parse_args()
    if not _loopback(args.host): raise SystemExit("host must resolve only to loopback")
    app=create_app(args.run_root,args.decision_root)
    if not args.no_browser: webbrowser.open(f"http://{args.host}:{args.port}/review")
    uvicorn.run(app,host=args.host,port=args.port)
    return 0
if __name__ == "__main__": raise SystemExit(main())
