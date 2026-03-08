from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_meta_cognition_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class MetaCognitionOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-ao.0', 'producerCommits': ['ao123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'meta_cognition_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'mc-1', 'metaCognitionAuditState': 'verified'}]})
        write_json(self.bridge / 'meta_cognition_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'mc-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
            {'reviewId': 'mc-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
            {'reviewId': 'mc-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
        ]})
        write_json(self.bridge / 'reasoning_efficiency_report.json', {'provenance': prov, 'entries': [{'reviewId': 'mc-1', 'reasoningEfficiency': 0.79}]})
        write_json(self.bridge / 'pattern_donor_reliability_report.json', {'provenance': prov, 'entries': [{'reviewId': 'mc-1', 'patternDonorReliability': 'reliable'}]})
        write_json(self.bridge / 'governance_constraint_performance_report.json', {'provenance': prov, 'entries': [{'reviewId': 'mc-1', 'governanceConstraintPerformance': 'strong'}]})
        write_json(self.bridge / 'discovery_productivity_report.json', {'provenance': prov, 'entries': [{'reviewId': 'mc-1', 'discoveryProductivity': 0.67}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'value_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'responsibility_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'system_forecast_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--meta-cognition-audit', str(self.bridge / 'meta_cognition_audit.json'),
            '--meta-cognition-recommendations', str(self.bridge / 'meta_cognition_recommendations.json'),
            '--reasoning-efficiency-report', str(self.bridge / 'reasoning_efficiency_report.json'),
            '--pattern-donor-reliability-report', str(self.bridge / 'pattern_donor_reliability_report.json'),
            '--governance-constraint-performance-report', str(self.bridge / 'governance_constraint_performance_report.json'),
            '--discovery-productivity-report', str(self.bridge / 'discovery_productivity_report.json'),
            '--value-dashboard', str(self.registry / 'value_dashboard.json'),
            '--responsibility-dashboard', str(self.registry / 'responsibility_dashboard.json'),
            '--system-forecast-dashboard', str(self.registry / 'system_forecast_dashboard.json'),
            '--out-meta-dashboard', str(self.registry / 'meta_dashboard.json'),
            '--out-reasoning-performance-registry', str(self.registry / 'reasoning_performance_registry.json'),
            '--out-meta-watchlist', str(self.registry / 'meta_watchlist.json'),
            '--out-meta-annotations', str(self.registry / 'meta_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'meta_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'reasoning_performance_registry.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'meta_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['mc-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['mc-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['mc-2'])

    def test_critical_safeguards(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'meta_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noAutonomousSafetyConstraintModification'))
        self.assertTrue(ann.get('humanApprovalRequiredForStructuralChanges'))
        constraints = ann.get('immutableSafetyConstraints', [])
        self.assertIn('evidence maturity gating', constraints)
        self.assertIn('human authority over value judgments', constraints)

    def test_invalid_numeric_values_default_to_zero(self) -> None:
        payload = json.loads((self.bridge / 'reasoning_efficiency_report.json').read_text(encoding='utf-8'))
        payload['entries'][0]['reasoningEfficiency'] = 'not-a-number'
        write_json(self.bridge / 'reasoning_efficiency_report.json', payload)

        d_payload = json.loads((self.bridge / 'discovery_productivity_report.json').read_text(encoding='utf-8'))
        d_payload['entries'][0]['discoveryProductivity'] = True
        write_json(self.bridge / 'discovery_productivity_report.json', d_payload)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'meta_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['reasoningEfficiency'], 0.0)
        self.assertEqual(dashboard['entries'][0]['discoveryProductivity'], 0.0)

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'meta_cognition_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'meta_cognition_audit.json', payload)

        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
