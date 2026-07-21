from __future__ import annotations
import hashlib
import json
import re
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'python' / 'src'))
from atlas.triadic.governed_posture import assign_governed_posture
from atlas.triadic.human_review_ui import HumanReviewError, create_app, load_sealed_run
from test_atlas_governed_posture import run

def sealed(root: Path) -> Path:
    run(root); assign_governed_posture(root)
    (root / 'run_manifest.json').write_text('{"logical_time":"t1","run_id":"r1"}\n')
    (root / 'grounding' / 'source.md').write_text('source\n')
    (root / 'grounding' / 'conversion_report.json').write_text('{}\n')
    (root / 'lifecycle_events.jsonl').write_text('{\"event\":\"review\"}\n')
    names = sorted(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file())
    (root / 'checksums.sha256').write_text(''.join(f'{hashlib.sha256((root/n).read_bytes()).hexdigest()}  {n}\n' for n in names))
    return root

def fields(body: str) -> dict[str,str]:
    return dict(re.findall(r'name="([^"]+)" value="([^"]*)"', body))

def loopback_app(app):
    async def wrapper(scope, receive, send):
        scope = dict(scope); scope['client'] = ('127.0.0.1', 1)
        await app(scope, receive, send)
    return wrapper

def client(root): return TestClient(loopback_app(create_app(root)), base_url='http://127.0.0.1')

def test_review_preview_commit_packet_and_receipt(tmp_path):
    root = sealed(tmp_path/'artifacts'/'run'); before = {p:p.read_bytes() for p in root.rglob('*') if p.is_file()}
    c = client(root); review = c.get('/review'); assert review.status_code == 200
    assert review.text.count('<h1>') == 1 and '<fieldset>' in review.text and 'required type="radio"' in review.text
    assert 'Claims and citations' in review.text and 'Sophia' in review.text and review.headers['cache-control'] == 'no-store'
    csrf = fields(review.text)['csrf']
    preview = c.post('/review/preview', data={'csrf':csrf,'decision':'APPROVE','reviewer':'<Tom>','note':'<note>'})
    assert preview.status_code == 200; form = fields(preview.text); assert set(form) == {'csrf','confirmation_token'}
    committed = c.post('/review/commit', data={**form,'decision':'REJECT','reviewer':'evil','note':'evil'})
    assert committed.status_code == 200
    packet_path = next((root.parent/'human_decisions').glob('*/human_review_decision.json')); packet = json.loads(packet_path.read_text())
    assert packet['decision'] == 'APPROVE' and packet['reviewer']['display_name'] == '<Tom>' and 'note' not in packet
    assert hashlib.sha256(packet_path.read_bytes()).hexdigest() in packet_path.with_suffix('.json.sha256').read_text()
    receipt = packet_path.with_name('human_review_decision_receipt.html').read_text(); assert '&lt;Tom&gt;' in receipt and 'logical time' in receipt and 'Sophia:' in receipt
    assert before == {p:p.read_bytes() for p in before}; assert c.get('/review').status_code == 409

def test_rejections_are_bounded_and_no_packet_is_published(tmp_path):
    root = sealed(tmp_path/'artifacts'/'run'); before = {p:p.read_bytes() for p in root.rglob('*') if p.is_file()}
    ordinary = TestClient(create_app(root), base_url='http://127.0.0.1'); assert ordinary.get('/review').status_code == 403
    c = client(root); csrf = fields(c.get('/review').text)['csrf']
    for data, status in [({'decision':'APPROVE','reviewer':'a','note':''},403), ({'csrf':csrf,'decision':'HOLD','reviewer':'a','note':''},400), ({'csrf':csrf,'confirmation_token':'unknown'},409)]:
        response = c.post('/review/commit' if 'confirmation_token' in data else '/review/preview', data=data)
        assert response.status_code == status
        if status == 400:
            assert 'Correct these fields' in response.text
        else:
            assert 'Request rejected' in response.text and csrf not in response.text
    assert not list((root.parent/'human_decisions').glob('*/human_review_decision.json')) and before == {p:p.read_bytes() for p in before}
    with pytest.raises(HumanReviewError): load_sealed_run('relative')


@pytest.mark.parametrize('decision,note', [('HOLD', 'needs correction'), ('REJECT', 'not accepted')])
def test_hold_and_reject_preview_with_required_note(tmp_path, decision, note):
    root = sealed(tmp_path / 'artifacts' / 'run')
    c = client(root)
    csrf = fields(c.get('/review').text)['csrf']
    response = c.post('/review/preview', data={'csrf': csrf, 'decision': decision, 'reviewer': 'Reviewer', 'note': note})
    assert response.status_code == 200
    confirm = fields(response.text)
    committed = c.post('/review/commit', data=confirm)
    assert committed.status_code == 200
    packet = json.loads(next((root.parent/'human_decisions').glob('*/human_review_decision.json')).read_text())
    assert packet['decision'] == decision


def test_input_and_decision_root_bounds(tmp_path):
    root = sealed(tmp_path / 'artifacts' / 'run')
    with pytest.raises(HumanReviewError):
        create_app(root, root)
    with pytest.raises(HumanReviewError):
        create_app(root, root / 'human_decisions')
    c = client(root)
    csrf = fields(c.get('/review').text)['csrf']
    response = c.post('/review/preview', data={'csrf': csrf, 'decision': 'APPROVE', 'reviewer': 'x' * 201, 'note': ''})
    assert response.status_code == 400


@pytest.mark.parametrize('target', ['grounding/source.md', 'grounding/segments.jsonl', 'lifecycle_events.jsonl'])
def test_complete_eleven_target_ledger_rejects_supplemental_changes(tmp_path, target):
    root = sealed(tmp_path / 'artifacts' / 'run')
    assert len((root / 'checksums.sha256').read_text().splitlines()) == 11
    (root / target).write_text('altered\n')
    with pytest.raises(HumanReviewError):
        load_sealed_run(root)


def test_complete_ledger_rejects_an_unlisted_artifact(tmp_path):
    root = sealed(tmp_path / 'artifacts' / 'run')
    (root / 'unlisted.txt').write_text('not ledgered\n')
    with pytest.raises(HumanReviewError):
        load_sealed_run(root)
