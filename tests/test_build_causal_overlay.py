from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_causal_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class CausalOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-ab.0', 'producerCommits': ['ab123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'causal_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'ca-1', 'causalAuditState': 'verified'}]})
        write_json(self.bridge / 'causal_recommendations.json', {
            'provenance': prov,
            'recommendations': [
                {'reviewId': 'ca-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
                {'reviewId': 'ca-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
                {'reviewId': 'ca-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
            ],
        })
        write_json(self.bridge / 'causal_bundle_map.json', {'provenance': prov, 'entries': [{'reviewId': 'ca-1', 'causalBundleType': 'bundle-a'}]})
        write_json(self.bridge / 'mechanism_candidate_map.json', {'provenance': prov, 'entries': [{'reviewId': 'ca-1', 'mechanismCandidates': ['m1']}]})
        write_json(self.bridge / 'mechanism_separation_report.json', {'provenance': prov, 'entries': [{'reviewId': 'ca-1', 'explanatoryGap': 'moderate', 'prohibitedConclusions': ['pc1']}]})
        write_json(self.bridge / 'causal_conflict_report.json', {'provenance': prov, 'entries': [{'reviewId': 'ca-1', 'causalConflictState': 'bounded-disagreement'}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'pattern_timeline_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'environment_integrity_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'authority_gate_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self, extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--causal-audit', str(self.bridge / 'causal_audit.json'),
            '--causal-recommendations', str(self.bridge / 'causal_recommendations.json'),
            '--causal-bundle-map', str(self.bridge / 'causal_bundle_map.json'),
            '--mechanism-candidate-map', str(self.bridge / 'mechanism_candidate_map.json'),
            '--mechanism-separation-report', str(self.bridge / 'mechanism_separation_report.json'),
            '--causal-conflict-report', str(self.bridge / 'causal_conflict_report.json'),
            '--pattern-timeline-dashboard', str(self.registry / 'pattern_timeline_dashboard.json'),
            '--environment-integrity-dashboard', str(self.registry / 'environment_integrity_dashboard.json'),
            '--authority-gate-dashboard', str(self.registry / 'authority_gate_dashboard.json'),
            '--out-causal-dashboard', str(self.registry / 'causal_dashboard.json'),
            '--out-mechanism-registry', str(self.registry / 'mechanism_registry.json'),
            '--out-causal-watchlist', str(self.registry / 'causal_watchlist.json'),
            '--out-causal-annotations', str(self.registry / 'causal_annotations.json'),
        ]
        if extra:
            cmd.extend(extra)
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_canonical_artifact_name_usage(self) -> None:
        self.assertEqual(self.run_builder().returncode, 0)

    def test_deprecated_name_rejection(self) -> None:
        result = self.run_builder(['--causal-snapshot', str(self.bridge / 'old.json')])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Deprecated artifact alias', result.stdout + result.stderr)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'causal_dashboard.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'causal_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['ca-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['ca-2'])

    def test_non_mutation_guarantee_preserved(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        payload = json.loads((self.registry / 'causal_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(payload.get('noCanonicalMutation'))
        self.assertTrue(payload.get('noAutomaticAccusation'))
        self.assertTrue(payload.get('noAutomaticAttribution'))


if __name__ == '__main__':
    unittest.main()
