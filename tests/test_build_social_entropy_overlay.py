from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_social_entropy_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class SocialEntropyOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-aq.0', 'producerCommits': ['aq123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'social_entropy_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'se-1', 'socialEntropyAuditState': 'verified'}]})
        write_json(self.bridge / 'social_entropy_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'se-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x'], 'repairPriority': 'high'},
            {'reviewId': 'se-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y'], 'repairPriority': 'monitor'},
            {'reviewId': 'se-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z'], 'repairPriority': 'low'},
        ]})
        write_json(self.bridge / 'social_entropy_map.json', {'provenance': prov, 'entries': [{'reviewId': 'se-1', 'socialStatus': 'fraying', 'socialEntropy': 0.71}]})
        write_json(self.bridge / 'civic_cohesion_report.json', {'provenance': prov, 'entries': [{'reviewId': 'se-1', 'cohesionClass': 'fragile'}]})
        write_json(self.bridge / 'legitimacy_drift_report.json', {'provenance': prov, 'entries': [{'reviewId': 'se-1', 'legitimacyDrift': 'elevated'}]})
        write_json(self.bridge / 'review_participation_risk_map.json', {'provenance': prov, 'entries': [{'reviewId': 'se-1', 'reviewerConcentration': 0.67, 'reviewerFatigue': 'high'}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'collaborative_review_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'theory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'value_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'architecture_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--social-entropy-audit', str(self.bridge / 'social_entropy_audit.json'),
            '--social-entropy-recommendations', str(self.bridge / 'social_entropy_recommendations.json'),
            '--social-entropy-map', str(self.bridge / 'social_entropy_map.json'),
            '--civic-cohesion-report', str(self.bridge / 'civic_cohesion_report.json'),
            '--legitimacy-drift-report', str(self.bridge / 'legitimacy_drift_report.json'),
            '--review-participation-risk-map', str(self.bridge / 'review_participation_risk_map.json'),
            '--collaborative-review-dashboard', str(self.registry / 'collaborative_review_dashboard.json'),
            '--theory-dashboard', str(self.registry / 'theory_dashboard.json'),
            '--value-dashboard', str(self.registry / 'value_dashboard.json'),
            '--architecture-dashboard', str(self.registry / 'architecture_dashboard.json'),
            '--out-social-entropy-dashboard', str(self.registry / 'social_entropy_dashboard.json'),
            '--out-civic-cohesion-registry', str(self.registry / 'civic_cohesion_registry.json'),
            '--out-legitimacy-watchlist', str(self.registry / 'legitimacy_watchlist.json'),
            '--out-social-repair-annotations', str(self.registry / 'social_repair_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'social_entropy_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'civic_cohesion_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'legitimacy_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['se-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['se-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['se-2'])

    def test_guardrails_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'social_repair_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noAutomaticSuppression'))
        self.assertTrue(ann.get('noRankingOfPersons'))
        self.assertTrue(ann.get('noCoerciveNormalization'))
        self.assertTrue(ann.get('noGovernanceRightsMutation'))

    def test_invalid_numeric_values_default_to_zero(self) -> None:
        payload = json.loads((self.bridge / 'social_entropy_map.json').read_text(encoding='utf-8'))
        payload['entries'][0]['socialEntropy'] = 'bad-value'
        write_json(self.bridge / 'social_entropy_map.json', payload)
        risk_payload = json.loads((self.bridge / 'review_participation_risk_map.json').read_text(encoding='utf-8'))
        risk_payload['entries'][0]['reviewerConcentration'] = True
        write_json(self.bridge / 'review_participation_risk_map.json', risk_payload)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'social_entropy_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['socialEntropy'], 0.0)
        self.assertEqual(dashboard['entries'][0]['reviewerConcentration'], 0.0)

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'social_entropy_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'social_entropy_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
