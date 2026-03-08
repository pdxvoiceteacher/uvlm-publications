from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_information_value_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class InformationValueOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-am.0', 'producerCommits': ['am123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'information_value_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'iv-1', 'informationValueAuditState': 'verified'}]})
        write_json(self.bridge / 'information_value_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'iv-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
            {'reviewId': 'iv-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
            {'reviewId': 'iv-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
        ]})
        write_json(self.bridge / 'uncertainty_map.json', {'provenance': prov, 'entries': [{'reviewId': 'iv-1', 'uncertaintyGradient': 'high'}]})
        write_json(self.bridge / 'information_gain_report.json', {'provenance': prov, 'entries': [{'reviewId': 'iv-1', 'informationGain': 0.7}]})
        write_json(self.bridge / 'experiment_priority_map.json', {'provenance': prov, 'entries': [{'reviewId': 'iv-1', 'experimentPriority': 'high'}]})
        write_json(self.bridge / 'entropy_reduction_forecast.json', {'provenance': prov, 'entries': [{'reviewId': 'iv-1', 'entropyReductionForecast': 0.4}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'system_forecast_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'experiment_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'theory_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--information-value-audit', str(self.bridge / 'information_value_audit.json'),
            '--information-value-recommendations', str(self.bridge / 'information_value_recommendations.json'),
            '--uncertainty-map', str(self.bridge / 'uncertainty_map.json'),
            '--information-gain-report', str(self.bridge / 'information_gain_report.json'),
            '--experiment-priority-map', str(self.bridge / 'experiment_priority_map.json'),
            '--entropy-reduction-forecast', str(self.bridge / 'entropy_reduction_forecast.json'),
            '--system-forecast-dashboard', str(self.registry / 'system_forecast_dashboard.json'),
            '--experiment-dashboard', str(self.registry / 'experiment_dashboard.json'),
            '--theory-dashboard', str(self.registry / 'theory_dashboard.json'),
            '--out-uncertainty-dashboard', str(self.registry / 'uncertainty_dashboard.json'),
            '--out-observation-priority-registry', str(self.registry / 'observation_priority_registry.json'),
            '--out-curiosity-watchlist', str(self.registry / 'curiosity_watchlist.json'),
            '--out-curiosity-annotations', str(self.registry / 'curiosity_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'uncertainty_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'observation_priority_registry.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'curiosity_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['iv-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['iv-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['iv-2'])

    def test_surveillance_guardrails(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'curiosity_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noSurveillanceExpansionWithoutHumanAuthorization'))
        self.assertTrue(ann.get('curiosityGuidesInvestigationNotIntrusion'))
        self.assertTrue(ann.get('noCanonicalMutation'))


    def test_invalid_numeric_values_default_to_zero(self) -> None:
        gain_payload = json.loads((self.bridge / 'information_gain_report.json').read_text(encoding='utf-8'))
        gain_payload['entries'][0]['informationGain'] = 'not-a-number'
        write_json(self.bridge / 'information_gain_report.json', gain_payload)

        entropy_payload = json.loads((self.bridge / 'entropy_reduction_forecast.json').read_text(encoding='utf-8'))
        entropy_payload['entries'][0]['entropyReductionForecast'] = True
        write_json(self.bridge / 'entropy_reduction_forecast.json', entropy_payload)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)

        dashboard = json.loads((self.registry / 'uncertainty_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['informationGain'], 0.0)
        self.assertEqual(dashboard['entries'][0]['entropyReductionForecast'], 0.0)

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'information_value_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'information_value_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
