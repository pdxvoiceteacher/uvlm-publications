from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_value_alignment_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class ValueAlignmentOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-an.0', 'producerCommits': ['an123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'value_alignment_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'va-1', 'valueAlignmentAuditState': 'verified'}]})
        write_json(self.bridge / 'value_alignment_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'va-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
            {'reviewId': 'va-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
            {'reviewId': 'va-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
        ]})
        write_json(self.bridge / 'knowledge_priority_map.json', {'provenance': prov, 'entries': [{'reviewId': 'va-1', 'knowledgePriorityRank': 1}]})
        write_json(self.bridge / 'welfare_impact_report.json', {'provenance': prov, 'entries': [{'reviewId': 'va-1', 'welfareImpactScore': 0.8, 'welfareImpactIndicator': 'positive'}]})
        write_json(self.bridge / 'fairness_impact_report.json', {'provenance': prov, 'entries': [{'reviewId': 'va-1', 'fairnessImpactMarker': 'equity-watch'}]})
        write_json(self.bridge / 'value_risk_report.json', {'provenance': prov, 'entries': [{'reviewId': 'va-1', 'valueRiskFlag': 'elevated', 'valueRiskScore': 0.6}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'uncertainty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'responsibility_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'system_forecast_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--value-alignment-audit', str(self.bridge / 'value_alignment_audit.json'),
            '--value-alignment-recommendations', str(self.bridge / 'value_alignment_recommendations.json'),
            '--knowledge-priority-map', str(self.bridge / 'knowledge_priority_map.json'),
            '--welfare-impact-report', str(self.bridge / 'welfare_impact_report.json'),
            '--fairness-impact-report', str(self.bridge / 'fairness_impact_report.json'),
            '--value-risk-report', str(self.bridge / 'value_risk_report.json'),
            '--uncertainty-dashboard', str(self.registry / 'uncertainty_dashboard.json'),
            '--responsibility-dashboard', str(self.registry / 'responsibility_dashboard.json'),
            '--system-forecast-dashboard', str(self.registry / 'system_forecast_dashboard.json'),
            '--out-value-dashboard', str(self.registry / 'value_dashboard.json'),
            '--out-knowledge-priority-registry', str(self.registry / 'knowledge_priority_registry.json'),
            '--out-value-risk-watchlist', str(self.registry / 'value_risk_watchlist.json'),
            '--out-value-annotations', str(self.registry / 'value_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'value_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'knowledge_priority_registry.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'value_risk_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['va-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['va-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['va-2'])

    def test_final_safeguards(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'value_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('humanCommunitiesRetainFinalValueAuthority'))
        self.assertTrue(ann.get('triadIlluminatesMoralConsequencesNotEthicsReplacement'))
        self.assertTrue(ann.get('noAutomaticValueJudgmentExecution'))

    def test_invalid_numeric_values_default_to_zero(self) -> None:
        payload = json.loads((self.bridge / 'welfare_impact_report.json').read_text(encoding='utf-8'))
        payload['entries'][0]['welfareImpactScore'] = 'nan-value'
        write_json(self.bridge / 'welfare_impact_report.json', payload)

        risk_payload = json.loads((self.bridge / 'value_risk_report.json').read_text(encoding='utf-8'))
        risk_payload['entries'][0]['valueRiskScore'] = True
        write_json(self.bridge / 'value_risk_report.json', risk_payload)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)

        dashboard = json.loads((self.registry / 'value_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['welfareImpactScore'], 0.0)
        self.assertEqual(dashboard['entries'][0]['valueRiskScore'], 0.0)

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'value_alignment_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'value_alignment_audit.json', payload)

        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
