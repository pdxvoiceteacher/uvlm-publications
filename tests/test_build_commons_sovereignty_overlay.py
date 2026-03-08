from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_commons_sovereignty_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class CommonsSovereigntyOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-au.0', 'producerCommits': ['au123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'commons_sovereignty_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'cs-1', 'commonsSovereigntyAuditState': 'verified'}]})
        write_json(self.bridge / 'commons_sovereignty_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'cs-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x'], 'sovereigntyStatus': 'priority-review'},
            {'reviewId': 'cs-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y'], 'sovereigntyStatus': 'monitor'},
            {'reviewId': 'cs-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z'], 'sovereigntyStatus': 'hold'},
        ]})
        write_json(self.bridge / 'commons_sovereignty_map.json', {'provenance': prov, 'entries': [{'reviewId': 'cs-1', 'commonsIntegrity': 'resilient'}]})
        write_json(self.bridge / 'institutional_capture_risk_report.json', {'provenance': prov, 'entries': [{'reviewId': 'cs-1', 'institutionalCaptureRisk': 'elevated', 'institutionalCaptureRiskScore': 0.7}]})
        write_json(self.bridge / 'public_trust_signal_map.json', {'provenance': prov, 'entries': [{'reviewId': 'cs-1', 'publicTrustStability': 'fragile'}]})
        write_json(self.bridge / 'civilizational_integrity_report.json', {'provenance': prov, 'entries': [{'reviewId': 'cs-1', 'epistemicDiversity': 'high', 'dissentPortability': 'portable'}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'federation_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'social_entropy_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'value_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'architecture_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--commons-sovereignty-audit', str(self.bridge / 'commons_sovereignty_audit.json'),
            '--commons-sovereignty-recommendations', str(self.bridge / 'commons_sovereignty_recommendations.json'),
            '--commons-sovereignty-map', str(self.bridge / 'commons_sovereignty_map.json'),
            '--institutional-capture-risk-report', str(self.bridge / 'institutional_capture_risk_report.json'),
            '--public-trust-signal-map', str(self.bridge / 'public_trust_signal_map.json'),
            '--civilizational-integrity-report', str(self.bridge / 'civilizational_integrity_report.json'),
            '--federation-dashboard', str(self.registry / 'federation_dashboard.json'),
            '--social-entropy-dashboard', str(self.registry / 'social_entropy_dashboard.json'),
            '--value-dashboard', str(self.registry / 'value_dashboard.json'),
            '--architecture-dashboard', str(self.registry / 'architecture_dashboard.json'),
            '--out-commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--out-institutional-capture-registry', str(self.registry / 'institutional_capture_registry.json'),
            '--out-public-trust-watchlist', str(self.registry / 'public_trust_watchlist.json'),
            '--out-civilizational-integrity-annotations', str(self.registry / 'civilizational_integrity_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'commons_sovereignty_dashboard.json').read_text(encoding='utf-8'))
        capture = json.loads((self.registry / 'institutional_capture_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'public_trust_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['cs-1'])
        self.assertEqual([e['reviewId'] for e in capture['entries']], ['cs-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['cs-2'])

    def test_guardrails_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'civilizational_integrity_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noTheoryStatusMutation'))
        self.assertTrue(ann.get('noGovernanceRightsMutation'))
        self.assertTrue(ann.get('noCommunityRanking'))
        self.assertTrue(ann.get('noSovereigntyClaims'))

    def test_invalid_numeric_values_default_to_zero(self) -> None:
        payload = json.loads((self.bridge / 'institutional_capture_risk_report.json').read_text(encoding='utf-8'))
        payload['entries'][0]['institutionalCaptureRiskScore'] = 'bad-number'
        write_json(self.bridge / 'institutional_capture_risk_report.json', payload)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'commons_sovereignty_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['institutionalCaptureRiskScore'], 0.0)

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'commons_sovereignty_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'commons_sovereignty_audit.json', payload)

        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
