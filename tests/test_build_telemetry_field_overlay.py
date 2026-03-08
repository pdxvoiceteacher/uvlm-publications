from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_telemetry_field_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class TelemetryFieldOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-ad.0', 'producerCommits': ['ad123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'telemetry_field_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'tf-1', 'telemetryAuditState': 'verified'}]})
        write_json(self.bridge / 'telemetry_field_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'tf-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
            {'reviewId': 'tf-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
            {'reviewId': 'tf-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
        ]})
        write_json(self.bridge / 'telemetry_field_map.json', {'provenance': prov, 'entries': [{'reviewId': 'tf-1', 'telemetryFieldStatus': 'coherent'}]})
        write_json(self.bridge / 'lattice_projection_map.json', {'provenance': prov, 'entries': [{'reviewId': 'tf-1', 'latticeCoordinates': '0,0,1', 'latticeRegime': 'bounded-order'}]})
        write_json(self.bridge / 'pattern_donation_registry.json', {'provenance': prov, 'entries': [{'reviewId': 'tf-2', 'donorPatternPedigree': ['p1'], 'donationWatchStatus': 'watch'}]})
        write_json(self.bridge / 'action_functional_scorecard.json', {'provenance': prov, 'entries': [{'reviewId': 'tf-1', 'tafScoreSummary': 'bounded-positive', 'tafScore': 0.8}]})
        write_json(self.bridge / 'branch_emergence_report.json', {'provenance': prov, 'entries': [{'reviewId': 'tf-1', 'branchNovelty': 'moderate', 'maturityCeiling': 'bounded-review'}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'symbolic_field_registry.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'investigation_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'authority_gate_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--telemetry-field-audit', str(self.bridge / 'telemetry_field_audit.json'),
            '--telemetry-field-recommendations', str(self.bridge / 'telemetry_field_recommendations.json'),
            '--telemetry-field-map', str(self.bridge / 'telemetry_field_map.json'),
            '--lattice-projection-map', str(self.bridge / 'lattice_projection_map.json'),
            '--pattern-donation-registry', str(self.bridge / 'pattern_donation_registry.json'),
            '--action-functional-scorecard', str(self.bridge / 'action_functional_scorecard.json'),
            '--branch-emergence-report', str(self.bridge / 'branch_emergence_report.json'),
            '--symbolic-field-registry', str(self.registry / 'symbolic_field_registry.json'),
            '--investigation-dashboard', str(self.registry / 'investigation_dashboard.json'),
            '--authority-gate-dashboard', str(self.registry / 'authority_gate_dashboard.json'),
            '--out-telemetry-dashboard', str(self.registry / 'telemetry_dashboard.json'),
            '--out-lattice-projection-registry', str(self.registry / 'lattice_projection_registry.json'),
            '--out-pattern-donation-watchlist', str(self.registry / 'pattern_donation_watchlist.json'),
            '--out-action-functional-annotations', str(self.registry / 'action_functional_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'telemetry_dashboard.json').read_text(encoding='utf-8'))
        lattice = json.loads((self.registry / 'lattice_projection_registry.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'pattern_donation_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['tf-1'])
        self.assertEqual([e['reviewId'] for e in lattice['entries']], ['tf-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['tf-2'])

    def test_non_mutation_guarantee(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'action_functional_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noAutomaticBranchActivation'))
        self.assertTrue(ann.get('noCanonicalMutation'))

    def test_missing_required_input_fails(self) -> None:
        (self.bridge / 'branch_emergence_report.json').unlink()
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Missing required canonical artifact', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
