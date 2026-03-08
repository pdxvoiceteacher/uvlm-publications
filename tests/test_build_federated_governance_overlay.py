from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_federated_governance_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class FederatedGovernanceOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-ar.0', 'producerCommits': ['ar123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'federated_governance_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'fg-1', 'federatedGovernanceAuditState': 'verified'}]})
        write_json(self.bridge / 'federated_governance_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'fg-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x'], 'mitigationRequirement': 'high'},
            {'reviewId': 'fg-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y'], 'mitigationRequirement': 'monitor'},
            {'reviewId': 'fg-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z'], 'mitigationRequirement': 'low'},
        ]})
        write_json(self.bridge / 'stewardship_node_map.json', {'provenance': prov, 'entries': [{'reviewId': 'fg-1', 'nodeClass': 'distributed'}]})
        write_json(self.bridge / 'federation_coherence_report.json', {'provenance': prov, 'entries': [{'reviewId': 'fg-1', 'federationStatus': 'coherent'}]})
        write_json(self.bridge / 'cross_node_dissent_map.json', {'provenance': prov, 'entries': [{'reviewId': 'fg-1', 'dissentPortability': 'portable'}]})
        write_json(self.bridge / 'commons_capture_risk_report.json', {'provenance': prov, 'entries': [{'reviewId': 'fg-1', 'captureRisk': 'elevated', 'captureRiskScore': 0.62, 'legitimacySignal': 'strained'}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'social_entropy_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'value_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'architecture_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--federated-governance-audit', str(self.bridge / 'federated_governance_audit.json'),
            '--federated-governance-recommendations', str(self.bridge / 'federated_governance_recommendations.json'),
            '--stewardship-node-map', str(self.bridge / 'stewardship_node_map.json'),
            '--federation-coherence-report', str(self.bridge / 'federation_coherence_report.json'),
            '--cross-node-dissent-map', str(self.bridge / 'cross_node_dissent_map.json'),
            '--commons-capture-risk-report', str(self.bridge / 'commons_capture_risk_report.json'),
            '--social-entropy-dashboard', str(self.registry / 'social_entropy_dashboard.json'),
            '--value-dashboard', str(self.registry / 'value_dashboard.json'),
            '--architecture-dashboard', str(self.registry / 'architecture_dashboard.json'),
            '--out-federation-dashboard', str(self.registry / 'federation_dashboard.json'),
            '--out-stewardship-registry', str(self.registry / 'stewardship_registry.json'),
            '--out-capture-watchlist', str(self.registry / 'capture_watchlist.json'),
            '--out-federation-annotations', str(self.registry / 'federation_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'federation_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'stewardship_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'capture_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['fg-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['fg-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['fg-2'])

    def test_guardrails_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'federation_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noAutomaticCentralization'))
        self.assertTrue(ann.get('noCommunityRanking'))
        self.assertTrue(ann.get('noSovereigntyClaims'))
        self.assertTrue(ann.get('noGovernanceRightsMutation'))

    def test_invalid_numeric_values_default_to_zero(self) -> None:
        payload = json.loads((self.bridge / 'commons_capture_risk_report.json').read_text(encoding='utf-8'))
        payload['entries'][0]['captureRiskScore'] = 'bad-number'
        write_json(self.bridge / 'commons_capture_risk_report.json', payload)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'federation_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['captureRiskScore'], 0.0)

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'federated_governance_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'federated_governance_audit.json', payload)

        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
