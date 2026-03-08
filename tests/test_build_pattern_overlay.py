from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_pattern_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class PatternOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-z.0', 'producerCommits': ['z123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'pattern_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'pat-1', 'patternAuditState': 'verified'}]})
        write_json(self.bridge / 'pattern_recommendations.json', {
            'provenance': prov,
            'recommendations': [
                {'reviewId': 'pat-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
                {'reviewId': 'pat-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
                {'reviewId': 'pat-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
            ],
        })
        write_json(self.bridge / 'pattern_cluster_map.json', {'provenance': prov, 'entries': [{'reviewId': 'pat-1', 'patternCluster': 'cluster-a'}]})
        write_json(self.bridge / 'pattern_maturity_map.json', {'provenance': prov, 'entries': [{'reviewId': 'pat-1', 'patternMaturity': 'emergent-stable'}]})
        write_json(self.bridge / 'cross_case_relationship_map.json', {'provenance': prov, 'entries': [{'reviewId': 'pat-1', 'crossCaseRelationshipHints': ['case-1~case-2']}]})
        write_json(self.bridge / 'pattern_conflict_report.json', {'provenance': prov, 'entries': [{'reviewId': 'pat-1', 'conflictMarkers': ['timing-drift']}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'investigation_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'authority_gate_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'review_packet_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self, extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--pattern-audit', str(self.bridge / 'pattern_audit.json'),
            '--pattern-recommendations', str(self.bridge / 'pattern_recommendations.json'),
            '--pattern-cluster-map', str(self.bridge / 'pattern_cluster_map.json'),
            '--pattern-maturity-map', str(self.bridge / 'pattern_maturity_map.json'),
            '--cross-case-relationship-map', str(self.bridge / 'cross_case_relationship_map.json'),
            '--pattern-conflict-report', str(self.bridge / 'pattern_conflict_report.json'),
            '--investigation-dashboard', str(self.registry / 'investigation_dashboard.json'),
            '--authority-gate-dashboard', str(self.registry / 'authority_gate_dashboard.json'),
            '--review-packet-dashboard', str(self.registry / 'review_packet_dashboard.json'),
            '--out-pattern-dashboard', str(self.registry / 'pattern_dashboard.json'),
            '--out-pattern-registry', str(self.registry / 'pattern_registry.json'),
            '--out-pattern-watchlist', str(self.registry / 'pattern_watchlist.json'),
            '--out-pattern-annotations', str(self.registry / 'pattern_annotations.json'),
        ]
        if extra:
            cmd.extend(extra)
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_canonical_artifact_name_usage(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_deprecated_name_rejection(self) -> None:
        result = self.run_builder(['--pattern-snapshot', str(self.bridge / 'old.json')])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Deprecated artifact alias', result.stdout + result.stderr)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        dashboard = json.loads((self.registry / 'pattern_dashboard.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'pattern_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['pat-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['pat-2'])

    def test_output_contract_validation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        for name in ['pattern_dashboard.json', 'pattern_registry.json', 'pattern_watchlist.json', 'pattern_annotations.json']:
            payload = json.loads((self.registry / name).read_text(encoding='utf-8'))
            self.assertIsInstance(payload, dict)
            self.assertIn('provenance', payload)

    def test_non_mutation_guarantee_preserved(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'pattern_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(payload.get('noCanonicalMutation'))
        self.assertTrue(payload.get('noAutomaticAccusation'))
        self.assertTrue(payload.get('noAutomaticGraphMutation'))


if __name__ == '__main__':
    unittest.main()
