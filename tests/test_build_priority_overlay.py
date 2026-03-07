from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_priority_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class PriorityOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-r.0', 'producerCommits': ['r123'], 'sourceMode': 'fixture'}

        write_json(self.bridge / 'triage_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'pr-1', 'watchState': 'none'}]})
        write_json(self.bridge / 'triage_recommendations.json', {
            'provenance': prov,
            'recommendations': [{'reviewId': 'pr-1', 'candidateId': 'c1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']}],
        })
        write_json(self.bridge / 'priority_state_map.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'pr-1', 'triageStatus': 'ready', 'urgencyLevel': 'high', 'priorityClass': 'critical-integrity'}],
        })
        write_json(self.bridge / 'priority_state_summary.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'pr-1', 'recommendationSummary': 'review-now'}],
        })
        write_json(self.bridge / 'triage_candidate_map.json', {
            'provenance': prov,
            'candidates': [{'candidateId': 'c1', 'linkedTargetIds': ['concept:x']}],
        })
        write_json(self.bridge / 'triage_conflict_report.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'pr-1', 'triageConflictStatus': 'none'}],
        })

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'queue_health_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'system_health_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'review_backlog_watchlist.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'metric_gaming_watchlist.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self, extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--triage-audit', str(self.bridge / 'triage_audit.json'),
            '--triage-recommendations', str(self.bridge / 'triage_recommendations.json'),
            '--priority-state-map', str(self.bridge / 'priority_state_map.json'),
            '--priority-state-summary', str(self.bridge / 'priority_state_summary.json'),
            '--triage-candidate-map', str(self.bridge / 'triage_candidate_map.json'),
            '--triage-conflict-report', str(self.bridge / 'triage_conflict_report.json'),
            '--queue-health-dashboard', str(self.registry / 'queue_health_dashboard.json'),
            '--system-health-dashboard', str(self.registry / 'system_health_dashboard.json'),
            '--review-backlog-watchlist', str(self.registry / 'review_backlog_watchlist.json'),
            '--metric-gaming-watchlist', str(self.registry / 'metric_gaming_watchlist.json'),
            '--out-priority-dashboard', str(self.registry / 'priority_dashboard.json'),
            '--out-triage-docket', str(self.registry / 'triage_docket.json'),
            '--out-triage-watchlist', str(self.registry / 'triage_watchlist.json'),
            '--out-priority-annotations', str(self.registry / 'priority_annotations.json'),
        ]
        if extra:
            cmd.extend(extra)
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_canonical_artifact_name_usage(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_deprecated_name_rejection(self) -> None:
        result = self.run_builder(['--priority-snapshot', str(self.bridge / 'priority_snapshot.json')])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Deprecated artifact alias', result.stdout + result.stderr)

    def test_provenance_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'priority_dashboard.json').read_text(encoding='utf-8'))
        self.assertIn('schemaVersions', payload.get('provenance', {}))

    def test_missing_upstream_artifact_failure(self) -> None:
        (self.bridge / 'triage_conflict_report.json').unlink()
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Missing required canonical artifact', result.stdout + result.stderr)

    def test_non_mutation_guarantee_preserved(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'priority_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(payload.get('noCanonicalMutation'))
        self.assertTrue(payload.get('noAutomaticQueueReordering'))


if __name__ == '__main__':
    unittest.main()
