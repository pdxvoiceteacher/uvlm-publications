from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_responsibility_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class ResponsibilityOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-aj.0', 'producerCommits': ['aj123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'responsibility_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'rs-1', 'responsibilityAuditState': 'verified'}]})
        write_json(self.bridge / 'responsibility_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'rs-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
            {'reviewId': 'rs-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
            {'reviewId': 'rs-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
        ]})
        write_json(self.bridge / 'responsibility_mode_map.json', {'provenance': prov, 'entries': [{'reviewId': 'rs-1', 'responsibilityStatus': 'support-accountable'}]})
        write_json(self.bridge / 'support_pathway_map.json', {'provenance': prov, 'entries': [{'reviewId': 'rs-1', 'supportPathway': 'assistive-guarded'}]})
        write_json(self.bridge / 'intervention_boundary_report.json', {'provenance': prov, 'entries': [{'reviewId': 'rs-1', 'consentRequirement': 'required', 'coercionCeiling': 'strict', 'interventionBoundaryState': 'bounded'}]})
        write_json(self.bridge / 'sanction_suppression_gate.json', {'provenance': prov, 'entries': [{'reviewId': 'rs-1', 'sanctionSuppressionState': 'enabled'}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'agency_mode_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'theory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'experiment_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--responsibility-audit', str(self.bridge / 'responsibility_audit.json'),
            '--responsibility-recommendations', str(self.bridge / 'responsibility_recommendations.json'),
            '--responsibility-mode-map', str(self.bridge / 'responsibility_mode_map.json'),
            '--support-pathway-map', str(self.bridge / 'support_pathway_map.json'),
            '--intervention-boundary-report', str(self.bridge / 'intervention_boundary_report.json'),
            '--sanction-suppression-gate', str(self.bridge / 'sanction_suppression_gate.json'),
            '--agency-mode-dashboard', str(self.registry / 'agency_mode_dashboard.json'),
            '--theory-dashboard', str(self.registry / 'theory_dashboard.json'),
            '--experiment-dashboard', str(self.registry / 'experiment_dashboard.json'),
            '--out-responsibility-dashboard', str(self.registry / 'responsibility_dashboard.json'),
            '--out-support-registry', str(self.registry / 'support_registry.json'),
            '--out-intervention-watchlist', str(self.registry / 'intervention_watchlist.json'),
            '--out-responsibility-annotations', str(self.registry / 'responsibility_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'responsibility_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'support_registry.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'intervention_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['rs-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['rs-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['rs-2'])

    def test_non_mutation_guarantee(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'responsibility_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noAutomaticSanctioning'))
        self.assertTrue(ann.get('noCanonicalMutation'))

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'responsibility_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'responsibility_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
