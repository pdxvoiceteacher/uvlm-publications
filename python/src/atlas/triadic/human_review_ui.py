"""Loopback-only, transaction-bound local human-review decision capture."""
from __future__ import annotations
import argparse, hashlib, html, ipaddress, json, os, secrets, socket, uuid, webbrowser
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from urllib.parse import parse_qs
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
class HumanReviewError(ValueError): pass
REQUIRED=("request.json","grounding/manifest.json","candidate_packet.json","sophia_audit_packet.json","atlas_posture_packet.json","final_review.html","run_manifest.json","checksums.sha256")
AUTH=("truth_certification","final_answer_authority","memory_write_authority","pmr_write_authority","canonization","publication","doi_mutation","crossref_deposit","catalog_mutation","knowledge_graph_mutation","deployment","release","model_invocation","candidate_alteration","sophia_alteration","atlas_posture_alteration","external_action_authority","automatic_phase_advance")
EFFECTS=("network_access_beyond_loopback","model_invocation_performed","candidate_mutation_performed","sophia_mutation_performed","atlas_posture_mutation_performed","sealed_run_mutation_performed","memory_write_performed","pmr_write_performed","canonization_performed","publication_performed","doi_mutated","crossref_deposit_performed","catalog_mutated","knowledge_graph_mutated","deployment_performed","release_performed")
HEADERS={"Content-Security-Policy":"default-src 'none'; style-src 'unsafe-inline'; frame-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'","X-Content-Type-Options":"nosniff","Referrer-Policy":"no-referrer","Cache-Control":"no-store"}
def _sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def _pairs(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError
  d[k]=v
 return d
def _constant(v):raise ValueError
def _json(p:Path)->dict:
 try:
  raw=p.read_bytes()
  if b'\0' in raw:raise ValueError
  obj=json.loads(raw.decode('utf-8'),object_pairs_hook=_pairs,parse_constant=_constant)
 except (OSError,UnicodeDecodeError,json.JSONDecodeError,ValueError) as e:raise HumanReviewError('sealed JSON artifact is invalid') from e
 if not isinstance(obj,dict):raise HumanReviewError('sealed JSON artifact is invalid')
 return obj
def _root(v):
 p=Path(v)
 if not p.is_absolute() or p.is_symlink() or p==Path(p.anchor):raise HumanReviewError('run root is invalid')
 p=p.resolve()
 if not p.is_dir():raise HumanReviewError('run root is invalid')
 return p
def _files(root):
 out={}
 for n in REQUIRED:
  p=root/n
  if p.is_symlink() or not p.is_file():raise HumanReviewError('sealed required artifact is invalid')
  try:p.resolve().relative_to(root)
  except ValueError as e:raise HumanReviewError('sealed required artifact is invalid') from e
  out[n]=p.read_bytes()
 return out
def _checks(files):
 try:lines=files['checksums.sha256'].decode().splitlines()
 except UnicodeDecodeError as e:raise HumanReviewError('checksum file is invalid') from e
 got={}
 for line in lines:
  parts=line.split(maxsplit=1)
  if len(parts)!=2 or len(parts[0])!=64 or parts[1].lstrip(' *') in got:raise HumanReviewError('checksum file is invalid')
  got[parts[1].lstrip(' *')]=parts[0]
 names=set(REQUIRED)-{'checksums.sha256'}
 if set(got)!=names or any(got[n]!=_sha(files[n]) for n in names):raise HumanReviewError('sealed checksum verification failed')
def load_sealed_run(v):
 root=_root(v); files=_files(root);_checks(files); req,man,cand,sop,atlas,run=(_json(root/n) for n in REQUIRED[:5]+('run_manifest.json',))
 ids=[(x.get('run_id'),x.get('logical_time')) for x in (req,cand,sop,atlas,run)]
 if not all(x==ids[0] for x in ids) or not all(ids[0]):raise HumanReviewError('sealed run identity mismatch')
 if sop.get('disposition') not in {'PASS','HOLD','REJECT'} or atlas.get('requires_human_review') is not True or atlas.get('human_decision')!='PENDING':raise HumanReviewError('sealed review is not eligible')
 return {'root':root,'files':files,'hashes':{n:_sha(b) for n,b in files.items()},'request':req,'manifest':man,'candidate':cand,'sophia':sop,'atlas':atlas}
def _decision_root(s,v):
 p=Path(v) if v else s['root'].parent/'human_decisions'
 if not p.is_absolute() or p.is_symlink():raise HumanReviewError('decision root is invalid')
 p=p.resolve()
 try:p.relative_to(s['root'].parent)
 except ValueError as e:raise HumanReviewError('decision root is invalid') from e
 if p==s['root']:raise HumanReviewError('decision root is invalid')
 p.mkdir(parents=True,exist_ok=True);return p
def _existing(out,rid):
 found=[]
 for p in out.glob('*/human_review_decision.json'):
  d=_json(p); side=p.with_suffix('.json.sha256'); receipt=p.with_name('human_review_decision_receipt.html')
  if not side.is_file() or not receipt.is_file() or side.read_text(encoding='utf-8')!=f'{_sha(p.read_bytes())}  human_review_decision.json\n':raise HumanReviewError('existing decision is invalid')
  if d.get('run_id')==rid:found.append(p.parent)
 if len(found)>1:raise HumanReviewError('existing decision conflict')
 return found[0] if found else None
def _esc(x):return html.escape(str(x),quote=True)
def _response(body,status=200):return HTMLResponse('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Atlas human review</title></head><body>'+body+'</body></html>',status_code=status,headers=HEADERS)
def _host(host):
 if host.startswith('['):
  if ']' not in host:return None
  return host[1:host.index(']')]
 return host.rsplit(':',1)[0] if host.count(':')==1 else host
def _loop(v):
 try:return bool(v) and all(ipaddress.ip_address(x[4][0]).is_loopback for x in socket.getaddrinfo(v,None,type=socket.SOCK_STREAM))
 except (ValueError,socket.gaierror):return False
def _form(req):return {k:v[-1] for k,v in parse_qs(req.scope['_body'].decode(),keep_blank_values=True).items()}
def create_app(run_root,decision_root=None):
 s=load_sealed_run(run_root);out=_decision_root(s,decision_root);csrf=secrets.token_urlsafe(32);pending=None;used=set();app=FastAPI(docs_url=None,redoc_url=None,openapi_url=None)
 def reject(msg,status):return _response(f'<h1 tabindex="-1">Request rejected</h1><p>{msg}</p>',status)
 def guard(req,form=None):
  host=_host(req.headers.get('host','')); client=req.client.host if req.client else None
  if not _loop(host) or (client is not None and not ipaddress.ip_address(client).is_loopback):raise PermissionError
  origin=req.headers.get('origin');site=req.headers.get('sec-fetch-site')
  if origin not in (None,'',f'http://{req.headers.get("host")}') or site not in (None,'','none','same-origin'):raise PermissionError
  if form is not None and not secrets.compare_digest(form.get('csrf',''),csrf):raise PermissionError
 @app.middleware('http')
 async def boundary(req,call):
  try:
   if req.method=='POST':req.scope['_body']=await req.body()
   guard(req);return await call(req)
  except PermissionError:return reject('The local request was not authorized.',403)
  except HumanReviewError:return reject('The local review request could not be accepted.',409)
 def review(errors=(),values={}):
  c=s['candidate'];so=s['sophia'];a=s['atlas']; claims=''.join(f'<li>{_esc(x.get("claim_id"))}: {_esc(x.get("text"))}; {_esc(x.get("uncertainty"))}; {_esc(x.get("support_status"))}; {_esc(x.get("candidate_maturity"))}<ul>'+''.join(f'<li>{_esc(y.get("segment_id"))}: {_esc(y.get("segment_sha256"))}; {_esc(y.get("source_ordinal"))}; {_esc(y.get("exact_excerpt"))}</li>' for y in x.get('citations',[]) if isinstance(y,dict))+'</ul></li>' for x in c.get('claims',[]) if isinstance(x,dict)); findings=''.join(f'<li>{_esc(x)}</li>' for x in so.get('claim_findings',[])); err='' if not errors else '<div id="errors" tabindex="-1"><h2>Correct these fields</h2>'+''.join(f'<p>{_esc(x)}</p>' for x in errors)+'</div>'
  return f'<h1>Local human review decision</h1>{err}<p>Run { _esc(s["request"]["run_id"]) } | logical time { _esc(s["request"]["logical_time"]) }</p><p>Question: {_esc(s["request"].get("question"))}<br>Model provenance: {_esc(s["request"].get("model_id"))}<br>Candidate: {_esc(c.get("answer"))}<br>Uncertainty: {_esc(c.get("uncertainty"))}</p><h2>Claims and citations</h2><ul>{claims}</ul><h2>Sophia</h2><p>{_esc(so.get("disposition"))}: {_esc(", ".join(so.get("reason_codes",[])))}</p><ul>{findings}</ul><h2>Atlas</h2><p>{_esc(a.get("retention_posture"))}; {_esc(a.get("publication_posture"))}; {_esc(a.get("expiry_posture"))}; {_esc(a.get("revocation_posture"))}; human decision PENDING</p><p><a href="/sealed-review">Open exact sealed review</a></p><form method="post" action="/review/preview"><input type="hidden" name="csrf" value="{_esc(csrf)}"><fieldset><legend>Decision (required)</legend><label><input required type="radio" name="decision" value="APPROVE"> APPROVE: accept bounded output.</label><label><input required type="radio" name="decision" value="HOLD"> HOLD: correction is required.</label><label><input required type="radio" name="decision" value="REJECT"> REJECT: output is not accepted.</label></fieldset><label for="reviewer">Reviewer display name (required)</label><input id="reviewer" name="reviewer" required aria-invalid="{"true" if "Reviewer" in " ".join(errors) else "false"}"><label for="note">Decision note (required for HOLD or REJECT)</label><textarea id="note" name="note"></textarea><button>Preview decision</button></form>'
 @app.get('/review')
 async def get_review():
  if _existing(out,s['request']['run_id']):return _response('<h1 tabindex="-1">Decision already recorded</h1><p>This run is read-only.</p>',409)
  return _response(review())
 @app.get('/sealed-review')
 async def sealed():return HTMLResponse(s['files']['final_review.html'],headers=HEADERS)
 @app.post('/review/preview')
 async def preview(req:Request):
  nonlocal pending
  f=_form(req)
  try:guard(req,f)
  except PermissionError:return reject('The local request was not authorized.',403)
  d=f.get('decision','');r=f.get('reviewer','').strip();n=f.get('note','').strip();errors=[]
  if d not in {'APPROVE','HOLD','REJECT'}:errors.append('Choose APPROVE, HOLD, or REJECT.')
  if not r:errors.append('Reviewer display name is required.')
  if d in {'HOLD','REJECT'} and not n:errors.append('A decision note is required for HOLD or REJECT.')
  if errors:return _response(review(errors,f),400)
  token=secrets.token_urlsafe(32);pending={'token':token,'decision':d,'reviewer':r,'note':n,'run_id':s['request']['run_id'],'logical_time':s['request']['logical_time'],'evidence_bindings':s['hashes'],'sophia_disposition':s['sophia']['disposition'],'atlas_retention_posture':s['atlas'].get('retention_posture'),'atlas_publication_posture':s['atlas'].get('publication_posture')}
  rows=''.join(f'<li>{_esc(k)}: {_esc(v)}</li>' for k,v in pending.items() if k!='token')
  return _response(f'<h1>Confirm decision</h1><ul>{rows}</ul><form method="post" action="/review/commit"><input type="hidden" name="csrf" value="{_esc(csrf)}"><input type="hidden" name="confirmation_token" value="{_esc(token)}"><button>Confirm decision</button></form>')
 @app.post('/review/commit')
 async def commit(req:Request):
  nonlocal pending
  f=_form(req)
  try:guard(req,f)
  except PermissionError:return reject('The local request was not authorized.',403)
  token=f.get('confirmation_token','')
  if not pending or token in used or not secrets.compare_digest(token,pending.get('token','')):return reject('The decision confirmation conflicts with this session.',409)
  record=pending;pending=None;used.add(token)
  try:
   if _existing(out,record['run_id']):return reject('A decision already exists for this run.',409)
   if _files(s['root'])!=s['files']:raise HumanReviewError
   did=str(uuid.uuid4());packet={'schema_id':'uvlm.human_review_decision.v1','schema_version':'1.0','packet_type':'human_review_decision','decision_id':did,'generated_at_utc':datetime.now(timezone.utc).isoformat(),'reviewer':{'display_name':record['reviewer'],'identity_assurance':'local_assertion_only','cryptographic_signature_present':False},'decision':record['decision'],'decision_note':record['note'],'source':{'interface':'atlas_local_human_review_ui','loopback_only':True},'requires_human_review':True,'authority_boundary':dict.fromkeys(AUTH,False),'side_effects':dict.fromkeys(EFFECTS,False),'nonauthority':'This receipt records a bounded human decision only.'}|{k:v for k,v in record.items() if k!='token'};data=json.dumps(packet,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()+b'\n'
   with TemporaryDirectory(dir=out,prefix='.pending-') as temp:
    t=Path(temp);(t/'human_review_decision.json').write_bytes(data);(t/'human_review_decision.json.sha256').write_text(f'{_sha(data)}  human_review_decision.json\n');bindings=''.join(f'<li>{_esc(k)}: {_esc(v)}</li>' for k,v in record['evidence_bindings'].items());(t/'human_review_decision_receipt.html').write_text(f'<!doctype html><html><body><h1>Human decision receipt</h1><p>This receipt records a human decision. It does not certify truth. It does not authorize memory or PMR write, canonization or publication, DOI, Crossref, catalog, or graph mutation, deployment, release, or automatic phase advance.</p><p>ID: {_esc(did)}; decision: {_esc(record["decision"])}; reviewer: {_esc(record["reviewer"])}; note: {_esc(record["note"])}; run: {_esc(record["run_id"])}; logical time: {_esc(record["logical_time"])}; timestamp: {_esc(packet["generated_at_utc"])}</p><p>Sophia: {_esc(record["sophia_disposition"])}; Atlas: {_esc(record["atlas_retention_posture"])} / {_esc(record["atlas_publication_posture"])}; identity assurance local_assertion_only; cryptographic signature absent.</p><ul>{bindings}</ul></body></html>',encoding='utf-8');os.replace(t,out/did)
   if _files(s['root'])!=s['files']:raise HumanReviewError
  except HumanReviewError:return reject('The sealed review transaction conflicts.',409)
  return _response('<h1 tabindex="-1">Decision recorded</h1><p>The immutable bounded decision receipt was written outside the sealed run root.</p>')
 return app
def main():
 p=argparse.ArgumentParser();p.add_argument('--run-root',required=True);p.add_argument('--decision-root');p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=8765);p.add_argument('--no-browser',action='store_true');a=p.parse_args()
 if not _loop(a.host):raise SystemExit('host must resolve only to loopback')
 if not a.no_browser:webbrowser.open(f'http://{a.host}:{a.port}/review')
 uvicorn.run(create_app(a.run_root,a.decision_root),host=a.host,port=a.port)
if __name__=='__main__':main()
