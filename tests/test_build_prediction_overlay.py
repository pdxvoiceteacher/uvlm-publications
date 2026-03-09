from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_prediction_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class PredictionOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-af.0', 'producerCommits': ['af123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'prediction_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'pr-1', 'predictionAuditState': 'verified'}]})
        write_json(self.bridge / 'prediction_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'pr-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
            {'reviewId': 'pr-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
            {'reviewId': 'pr-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
        ]})
        write_json(self.bridge / 'forecast_map.json', {'provenance': prov, 'entries': [{'reviewId': 'pr-1', 'forecastAccuracy': 'high', 'forecastConfidence': 'bounded-high'}]})
        write_json(self.bridge / 'calibration_report.json', {'provenance': prov, 'entries': [{'reviewId': 'pr-1', 'calibrationTrend': 'improving', 'calibrationError': 0.1}]})
        write_json(self.bridge / 'branch_reliability_report.json', {'provenance': prov, 'entries': [{'reviewId': 'pr-1', 'branchReliability': 'stable', 'reliabilityScore': 0.8}]})
        write_json(self.bridge / 'prediction_outcome_timeline.json', {'provenance': prov, 'entries': [{'reviewId': 'pr-1', 'outcomeTimeline': [{'date': '2026-02-01', 'outcome': 'hit'}]}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'branch_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'telemetry_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'collaborative_review_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--prediction-audit', str(self.bridge / 'prediction_audit.json'),
            '--prediction-recommendations', str(self.bridge / 'prediction_recommendations.json'),
            '--forecast-map', str(self.bridge / 'forecast_map.json'),
            '--calibration-report', str(self.bridge / 'calibration_report.json'),
            '--branch-reliability-report', str(self.bridge / 'branch_reliability_report.json'),
            '--prediction-outcome-timeline', str(self.bridge / 'prediction_outcome_timeline.json'),
            '--branch-dashboard', str(self.registry / 'branch_dashboard.json'),
            '--telemetry-dashboard', str(self.registry / 'telemetry_dashboard.json'),
            '--collaborative-review-dashboard', str(self.registry / 'collaborative_review_dashboard.json'),
            '--out-prediction-dashboard', str(self.registry / 'prediction_dashboard.json'),
            '--out-forecast-registry', str(self.registry / 'forecast_registry.json'),
            '--out-prediction-watchlist', str(self.registry / 'prediction_watchlist.json'),
            '--out-calibration-annotations', str(self.registry / 'calibration_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'prediction_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'forecast_registry.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'prediction_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['pr-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['pr-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['pr-2'])

    def test_non_mutation_guarantee(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'calibration_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noAutomaticPredictionPromotion'))
        self.assertTrue(ann.get('noCanonicalMutation'))

    def test_missing_required_input_fails(self) -> None:
        (self.bridge / 'calibration_report.json').unlink()
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Missing required canonical artifact', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
