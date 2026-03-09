from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_theory_transfer_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class TheoryTransferOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-ak.0', 'producerCommits': ['ak123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'theory_transfer_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'tr-1', 'theoryTransferAuditState': 'verified'}]})
        write_json(self.bridge / 'theory_transfer_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'tr-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
            {'reviewId': 'tr-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
            {'reviewId': 'tr-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
        ]})
        write_json(self.bridge / 'theory_transfer_map.json', {'provenance': prov, 'entries': [{'reviewId': 'tr-1', 'transferStatus': 'conditional-transfer'}]})
        write_json(self.bridge / 'donor_target_asymmetry_report.json', {'provenance': prov, 'entries': [{'reviewId': 'tr-1', 'donorTargetAsymmetry': 'medium'}]})
        write_json(self.bridge / 'transfer_replication_gate.json', {'provenance': prov, 'entries': [{'reviewId': 'tr-1', 'replicationGateState': 'gated-open', 'prohibitedClaims': ['x']}]})
        write_json(self.bridge / 'transfer_risk_register.json', {'provenance': prov, 'entries': [{'reviewId': 'tr-1', 'riskRegisterSummary': 'bounded'}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'theory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'experiment_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'agency_mode_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--theory-transfer-audit', str(self.bridge / 'theory_transfer_audit.json'),
            '--theory-transfer-recommendations', str(self.bridge / 'theory_transfer_recommendations.json'),
            '--theory-transfer-map', str(self.bridge / 'theory_transfer_map.json'),
            '--donor-target-asymmetry-report', str(self.bridge / 'donor_target_asymmetry_report.json'),
            '--transfer-replication-gate', str(self.bridge / 'transfer_replication_gate.json'),
            '--transfer-risk-register', str(self.bridge / 'transfer_risk_register.json'),
            '--theory-dashboard', str(self.registry / 'theory_dashboard.json'),
            '--experiment-dashboard', str(self.registry / 'experiment_dashboard.json'),
            '--agency-mode-dashboard', str(self.registry / 'agency_mode_dashboard.json'),
            '--out-transfer-dashboard', str(self.registry / 'transfer_dashboard.json'),
            '--out-theory-transfer-registry', str(self.registry / 'theory_transfer_registry.json'),
            '--out-transfer-watchlist', str(self.registry / 'transfer_watchlist.json'),
            '--out-transfer-annotations', str(self.registry / 'transfer_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'transfer_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'theory_transfer_registry.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'transfer_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['tr-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['tr-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['tr-2'])

    def test_non_mutation_guarantee(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'transfer_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noAutomaticCrossDomainCertification'))
        self.assertTrue(ann.get('noCanonicalMutation'))

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'theory_transfer_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'theory_transfer_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
