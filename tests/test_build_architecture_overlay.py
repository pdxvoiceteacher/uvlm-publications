from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_architecture_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class ArchitectureOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-ap.0', 'producerCommits': ['ap123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'architecture_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'ar-1', 'architectureAuditState': 'verified'}]})
        write_json(self.bridge / 'architecture_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'ar-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
            {'reviewId': 'ar-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
            {'reviewId': 'ar-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
        ]})
        write_json(self.bridge / 'module_performance_report.json', {'provenance': prov, 'entries': [{'reviewId': 'ar-1', 'modulePerformance': 'strong', 'modulePerformanceScore': 0.82}]})
        write_json(self.bridge / 'discovery_productivity_report.json', {'provenance': prov, 'entries': [{'reviewId': 'ar-1', 'discoveryProductivity': 0.69}]})
        write_json(self.bridge / 'safeguard_performance_report.json', {'provenance': prov, 'entries': [{'reviewId': 'ar-1', 'safeguardPerformance': 'strong'}]})
        write_json(self.bridge / 'architecture_proposal_report.json', {'provenance': prov, 'entries': [{'reviewId': 'ar-1', 'architectureImprovementProposal': 'proposal-queued'}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'meta_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'value_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'responsibility_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--architecture-audit', str(self.bridge / 'architecture_audit.json'),
            '--architecture-recommendations', str(self.bridge / 'architecture_recommendations.json'),
            '--module-performance-report', str(self.bridge / 'module_performance_report.json'),
            '--discovery-productivity-report', str(self.bridge / 'discovery_productivity_report.json'),
            '--safeguard-performance-report', str(self.bridge / 'safeguard_performance_report.json'),
            '--architecture-proposal-report', str(self.bridge / 'architecture_proposal_report.json'),
            '--meta-dashboard', str(self.registry / 'meta_dashboard.json'),
            '--value-dashboard', str(self.registry / 'value_dashboard.json'),
            '--responsibility-dashboard', str(self.registry / 'responsibility_dashboard.json'),
            '--out-architecture-dashboard', str(self.registry / 'architecture_dashboard.json'),
            '--out-module-performance-registry', str(self.registry / 'module_performance_registry.json'),
            '--out-architecture-watchlist', str(self.registry / 'architecture_watchlist.json'),
            '--out-architecture-annotations', str(self.registry / 'architecture_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'architecture_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'module_performance_registry.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'architecture_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['ar-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['ar-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['ar-2'])

    def test_safeguard_flags(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'architecture_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noAutonomousCoreSafetyMutation'))
        self.assertTrue(ann.get('humanApprovalRequiredForArchitectureChanges'))
        self.assertTrue(ann.get('noCanonicalMutation'))

    def test_invalid_numeric_values_default_to_zero(self) -> None:
        payload = json.loads((self.bridge / 'module_performance_report.json').read_text(encoding='utf-8'))
        payload['entries'][0]['modulePerformanceScore'] = 'bad-number'
        write_json(self.bridge / 'module_performance_report.json', payload)

        d_payload = json.loads((self.bridge / 'discovery_productivity_report.json').read_text(encoding='utf-8'))
        d_payload['entries'][0]['discoveryProductivity'] = True
        write_json(self.bridge / 'discovery_productivity_report.json', d_payload)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'architecture_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['modulePerformanceScore'], 0.0)
        self.assertEqual(dashboard['entries'][0]['discoveryProductivity'], 0.0)

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'architecture_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'architecture_audit.json', payload)

        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
