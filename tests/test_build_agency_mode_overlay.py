from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_agency_mode_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class AgencyModeOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-ai.0', 'producerCommits': ['ai123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'agency_mode_audit.json', {'provenance': prov, 'audits': [
            {'reviewId': 'ag-1', 'agencyAuditState': 'verified'}
        ]})
        write_json(self.bridge / 'agency_mode_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'ag-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
            {'reviewId': 'ag-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
            {'reviewId': 'ag-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
        ]})
        write_json(self.bridge / 'agency_mode_hypothesis_map.json', {'provenance': prov, 'entries': [
            {'reviewId': 'ag-1', 'agencyStatus': 'comparative-provisional'}
        ]})
        write_json(self.bridge / 'agency_fit_comparison_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'ag-1', 'deterministicFit': 0.6, 'volitionalFit': 0.5, 'provisionalVHat': 0.55}
        ]})
        write_json(self.bridge / 'tel_branch_signature_map.json', {'provenance': prov, 'entries': [
            {'reviewId': 'ag-1', 'telBranchSignature': 'tel:bounded'}
        ]})
        write_json(self.bridge / 'agency_governance_mode_gate.json', {'provenance': prov, 'entries': [
            {'reviewId': 'ag-1', 'governanceModeClass': 'bounded-consensual', 'consentSignal': 'required', 'blameSuppressionSignal': 'enabled'}
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'theory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'prediction_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'experiment_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--agency-mode-audit', str(self.bridge / 'agency_mode_audit.json'),
            '--agency-mode-recommendations', str(self.bridge / 'agency_mode_recommendations.json'),
            '--agency-mode-hypothesis-map', str(self.bridge / 'agency_mode_hypothesis_map.json'),
            '--agency-fit-comparison-report', str(self.bridge / 'agency_fit_comparison_report.json'),
            '--tel-branch-signature-map', str(self.bridge / 'tel_branch_signature_map.json'),
            '--agency-governance-mode-gate', str(self.bridge / 'agency_governance_mode_gate.json'),
            '--theory-dashboard', str(self.registry / 'theory_dashboard.json'),
            '--prediction-dashboard', str(self.registry / 'prediction_dashboard.json'),
            '--experiment-dashboard', str(self.registry / 'experiment_dashboard.json'),
            '--out-agency-mode-dashboard', str(self.registry / 'agency_mode_dashboard.json'),
            '--out-agency-fit-registry', str(self.registry / 'agency_fit_registry.json'),
            '--out-agency-disagreement-watchlist', str(self.registry / 'agency_disagreement_watchlist.json'),
            '--out-agency-governance-annotations', str(self.registry / 'agency_governance_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'agency_mode_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'agency_fit_registry.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'agency_disagreement_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['ag-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['ag-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['ag-2'])

    def test_non_mutation_guarantee(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'agency_governance_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noAutomaticMetaphysicalClassification'))
        self.assertTrue(ann.get('noCanonicalMutation'))

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'agency_mode_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'agency_mode_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
