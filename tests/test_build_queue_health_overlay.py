from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_queue_health_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class QueueHealthOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {
            'schemaVersion': 'phase-q.0',
            'producerCommits': ['qqq123'],
            'sourceMode': 'fixture',
        }

        write_json(self.bridge / 'load_shedding_audit.json', {
            'provenance': prov,
            'audits': [{'reviewId': 'qh-1', 'watchState': 'none'}],
        })
        write_json(self.bridge / 'load_shedding_recommendations.json', {
            'provenance': prov,
            'recommendations': [{
                'reviewId': 'qh-1',
                'queueId': 'q1',
                'targetPublisherAction': 'docket',
                'linkedTargetIds': ['concept:x'],
            }],
        })
        write_json(self.bridge / 'queue_pressure_map.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'qh-1', 'queueStatus': 'high-pressure', 'backlogPressure': 'high'}],
        })
        write_json(self.bridge / 'queue_pressure_summary.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'qh-1', 'loadSheddingRecommendationSummary': 'rebalance'}],
        })
        write_json(self.bridge / 'review_load_distribution.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'qh-1', 'fatigueLoadClass': 'elevated'}],
        })
        write_json(self.bridge / 'goodhart_risk_report.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'qh-1', 'metricGamingWatchStatus': 'none'}],
        })

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'institutional_status.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'system_health_dashboard.json', {**reg_prov, 'entries': []})

        for name in [
            'review_docket.json',
            'governance_review_docket.json',
            'deliberation_docket.json',
            'recovery_docket.json',
            'witness_docket.json',
            'case_docket.json',
            'stress_test_docket.json',
        ]:
            write_json(self.registry / name, {'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self, extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--load-shedding-audit', str(self.bridge / 'load_shedding_audit.json'),
            '--load-shedding-recommendations', str(self.bridge / 'load_shedding_recommendations.json'),
            '--queue-pressure-map', str(self.bridge / 'queue_pressure_map.json'),
            '--queue-pressure-summary', str(self.bridge / 'queue_pressure_summary.json'),
            '--review-load-distribution', str(self.bridge / 'review_load_distribution.json'),
            '--goodhart-risk-report', str(self.bridge / 'goodhart_risk_report.json'),
            '--institutional-status', str(self.registry / 'institutional_status.json'),
            '--system-health-dashboard', str(self.registry / 'system_health_dashboard.json'),
            '--review-docket', str(self.registry / 'review_docket.json'),
            '--governance-review-docket', str(self.registry / 'governance_review_docket.json'),
            '--deliberation-docket', str(self.registry / 'deliberation_docket.json'),
            '--recovery-docket', str(self.registry / 'recovery_docket.json'),
            '--witness-docket', str(self.registry / 'witness_docket.json'),
            '--case-docket', str(self.registry / 'case_docket.json'),
            '--stress-test-docket', str(self.registry / 'stress_test_docket.json'),
            '--out-queue-health-dashboard', str(self.registry / 'queue_health_dashboard.json'),
            '--out-review-backlog-watchlist', str(self.registry / 'review_backlog_watchlist.json'),
            '--out-metric-gaming-watchlist', str(self.registry / 'metric_gaming_watchlist.json'),
            '--out-load-shedding-annotations', str(self.registry / 'load_shedding_annotations.json'),
        ]
        if extra:
            cmd.extend(extra)
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_canonical_artifact_name_usage(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_deprecated_name_rejection(self) -> None:
        result = self.run_builder(['--queue-health-snapshot', str(self.bridge / 'queue_snapshot.json')])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Deprecated artifact alias', result.stdout + result.stderr)

    def test_provenance_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'queue_health_dashboard.json').read_text(encoding='utf-8'))
        prov = payload.get('provenance', {})
        self.assertIn('schemaVersions', prov)
        self.assertIn('producerCommits', prov)
        self.assertIn('derivedFromFixtures', prov)

    def test_missing_upstream_artifact_failure(self) -> None:
        (self.bridge / 'goodhart_risk_report.json').unlink()
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Missing required canonical artifact', result.stdout + result.stderr)

    def test_non_mutation_guarantee_preserved(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'load_shedding_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(payload.get('noAutomaticQueueMutation'))
        self.assertTrue(payload.get('noCanonicalMutation'))
        self.assertTrue(all(a.get('noCanonicalMutation') for a in payload.get('annotations', [])))


if __name__ == '__main__':
    unittest.main()
