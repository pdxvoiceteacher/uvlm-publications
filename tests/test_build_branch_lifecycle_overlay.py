from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_branch_lifecycle_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class BranchLifecycleOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-ae.0', 'producerCommits': ['ae123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'branch_lifecycle_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'bl-1', 'branchAuditState': 'verified'}]})
        write_json(self.bridge / 'branch_lifecycle_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'bl-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
            {'reviewId': 'bl-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
            {'reviewId': 'bl-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
        ]})
        write_json(self.bridge / 'branch_state_map.json', {'provenance': prov, 'entries': [{'reviewId': 'bl-1', 'branchLifecycleStatus': 'active-lifecycle', 'branchStage': 'stabilizing'}]})
        write_json(self.bridge / 'branch_conflict_graph.json', {'provenance': prov, 'entries': [{'reviewId': 'bl-1', 'conflictNodes': ['n1'], 'conflictEdges': ['e1']}]})
        write_json(self.bridge / 'branch_decay_report.json', {'provenance': prov, 'entries': [{'reviewId': 'bl-2', 'decayRisk': 'high', 'decaySignals': ['sig']}]})
        write_json(self.bridge / 'branch_reinforcement_trend.json', {'provenance': prov, 'entries': [{'reviewId': 'bl-1', 'reinforcementTrend': 'up', 'contradictionTrend': 'low'}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'telemetry_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'causal_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'collaborative_review_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--branch-lifecycle-audit', str(self.bridge / 'branch_lifecycle_audit.json'),
            '--branch-lifecycle-recommendations', str(self.bridge / 'branch_lifecycle_recommendations.json'),
            '--branch-state-map', str(self.bridge / 'branch_state_map.json'),
            '--branch-conflict-graph', str(self.bridge / 'branch_conflict_graph.json'),
            '--branch-decay-report', str(self.bridge / 'branch_decay_report.json'),
            '--branch-reinforcement-trend', str(self.bridge / 'branch_reinforcement_trend.json'),
            '--telemetry-dashboard', str(self.registry / 'telemetry_dashboard.json'),
            '--causal-dashboard', str(self.registry / 'causal_dashboard.json'),
            '--collaborative-review-dashboard', str(self.registry / 'collaborative_review_dashboard.json'),
            '--out-branch-dashboard', str(self.registry / 'branch_dashboard.json'),
            '--out-branch-registry', str(self.registry / 'branch_registry.json'),
            '--out-branch-watchlist', str(self.registry / 'branch_watchlist.json'),
            '--out-branch-annotations', str(self.registry / 'branch_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'branch_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'branch_registry.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'branch_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['bl-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['bl-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['bl-2'])

    def test_non_mutation_guarantees(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'branch_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noAutomaticBranchActivation'))
        self.assertTrue(ann.get('noCanonicalMutation'))

    def test_missing_required_input_fails(self) -> None:
        (self.bridge / 'branch_decay_report.json').unlink()
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Missing required canonical artifact', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
