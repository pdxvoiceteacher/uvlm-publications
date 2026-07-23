from __future__ import annotations
import hashlib,json
from pathlib import Path
import pytest
from atlas.triadic.governed_posture import GovernedPostureError,assign_governed_posture
from atlas.triadic import governed_posture as gp
from test_atlas_governed_posture import run

def write(p,x):p.write_bytes(gp._canon(x)+b'\n');return hashlib.sha256(p.read_bytes()).hexdigest(),hashlib.sha256(gp._canon(x)).hexdigest()
def v2(root,trust='local_loopback',egress='none',assurance='artifact_digest_verified'):
 run(root); req=json.loads((root/'request.json').read_text());req.update(provider_id='provider-a',provider_profile_sha256='e'*64,provider_trust_class=trust,data_egress=egress,external_provider_consent=True);rf,rc=write(root/'request.json',req)
 c=json.loads((root/'candidate_packet.json').read_text());
 for k in ('requested_model_id','observed_response_model','installed_model_digest','adapter_identity','real_model_invoked'):c.pop(k)
 c.update(schema_id='uvlm.coherencelattice.candidate_packet.v2',schema_version='2.0',request_sha256=rc,parents=[{'artifact_type':'request','path':'request.json','sha256':rc},c['parents'][1]],provider={'provider_id':'provider-a','adapter_id':'adapter-a','adapter_version':'1','protocol':'plugin','trust_class':trust,'data_egress':egress,'profile_sha256':'e'*64,'endpoint_sha256':'f'*64},model_identity={'requested_model_id':'model-a','observed_model_id':'model-a','assurance':assurance,'artifact_digest_sha256':'d'*64 if assurance=='artifact_digest_verified' else None,'provider_model_version':'v1' if assurance=='provider_version_reported' else None},completion={'complete':True,'finish_reason':'stop','input_tokens':1,'output_tokens':2,'time_to_first_byte_ms':3,'total_duration_ms':4,'provider_request_id_sha256':None})
 cf,cc=write(root/'candidate_packet.json',c)
 s=json.loads((root/'sophia_audit_packet.json').read_text());s.update(request_file_sha256=rf,request_canonical_sha256=rc,candidate_sha256=cf,candidate_canonical_sha256=cc,parent_list=[{'artifact_type':'request','path':'request.json','file_sha256':rf,'canonical_sha256':rc},s['parent_list'][1],{'artifact_type':'candidate_packet','path':'candidate_packet.json','file_sha256':cf,'canonical_sha256':cc}]);write(root/'sophia_audit_packet.json',s);return root
@pytest.mark.parametrize('trust,egress,assurance',[('local_loopback','none','artifact_digest_verified'),('private_network','private_network','provider_version_reported'),('external_managed','external','requested_and_observed_id_only')])
def test_v2_provider_context_and_neutral_posture(tmp_path,trust,egress,assurance):
 r=v2(tmp_path,trust,egress,assurance);p=assign_governed_posture(r);x=p['provider_context'];assert x['trust_class']==trust and x['assurance']==assurance and p['retention_posture']=='retain_for_human_review'
@pytest.mark.parametrize('change',[lambda r,c:c['provider'].update(profile_sha256='x'),lambda r,c:r.update(external_provider_consent=False),lambda r,c:c['model_identity'].update(artifact_digest_sha256=None)])
def test_v2_bad_provider_fails_closed(tmp_path,change):
 r=v2(tmp_path);c=json.loads((r/'candidate_packet.json').read_text());req=json.loads((r/'request.json').read_text());change(req,c);write(r/'request.json',req);write(r/'candidate_packet.json',c)
 with pytest.raises(GovernedPostureError):assign_governed_posture(r)
def test_v2_validator_sensitivity(tmp_path,monkeypatch):
 r=v2(tmp_path);monkeypatch.setattr(gp,'_sha',lambda v:False)
 with pytest.raises(GovernedPostureError):assign_governed_posture(r)
