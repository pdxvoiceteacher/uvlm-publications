from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_symbolic_field_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class SymbolicFieldOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-t.0', 'producerCommits': ['t123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'symbolic_field_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'sf-1', 'symbolicAuditState': 'verified'}]})
        write_json(self.bridge / 'symbolic_field_recommendations.json', {
            'provenance': prov,
            'recommendations': [{'reviewId': 'sf-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']}],
        })
        write_json(self.bridge / 'symbolic_field_state.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'sf-1', 'symbolicFieldStatus': 'strained', 'regimeClass': 'transition-risk', 'lambdaZoneWarningLevel': 'medium'}],
        })
        write_json(self.bridge / 'symbolic_field_summary.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'sf-1', 'architectureHint': 'monitor'}],
        })
        write_json(self.bridge / 'regime_transition_report.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'sf-1', 'regimeWatchStatus': 'none'}],
        })
        write_json(self.bridge / 'early_warning_signal_map.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'sf-1', 'lambdaZoneWarningLevel': 'medium'}],
        })

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'institutional_status.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'queue_health_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'priority_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'closure_registry.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self, extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--symbolic-field-audit', str(self.bridge / 'symbolic_field_audit.json'),
            '--symbolic-field-recommendations', str(self.bridge / 'symbolic_field_recommendations.json'),
            '--symbolic-field-state', str(self.bridge / 'symbolic_field_state.json'),
            '--symbolic-field-summary', str(self.bridge / 'symbolic_field_summary.json'),
            '--regime-transition-report', str(self.bridge / 'regime_transition_report.json'),
            '--early-warning-signal-map', str(self.bridge / 'early_warning_signal_map.json'),
            '--institutional-status', str(self.registry / 'institutional_status.json'),
            '--queue-health-dashboard', str(self.registry / 'queue_health_dashboard.json'),
            '--priority-dashboard', str(self.registry / 'priority_dashboard.json'),
            '--closure-registry', str(self.registry / 'closure_registry.json'),
            '--out-symbolic-field-registry', str(self.registry / 'symbolic_field_registry.json'),
            '--out-early-warning-dashboard', str(self.registry / 'early_warning_dashboard.json'),
            '--out-regime-watchlist', str(self.registry / 'regime_watchlist.json'),
            '--out-symbolic-field-annotations', str(self.registry / 'symbolic_field_annotations.json'),
        ]
        if extra:
            cmd.extend(extra)
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_canonical_artifact_name_usage(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_deprecated_name_rejection(self) -> None:
        result = self.run_builder(['--symbolic-field-snapshot', str(self.bridge / 'symbolic_field_snapshot.json')])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Deprecated artifact alias', result.stdout + result.stderr)

    def test_provenance_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'symbolic_field_registry.json').read_text(encoding='utf-8'))
        self.assertIn('schemaVersions', payload.get('provenance', {}))

    def test_missing_upstream_artifact_failure(self) -> None:
        (self.bridge / 'early_warning_signal_map.json').unlink()
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Missing required canonical artifact', result.stdout + result.stderr)

    def test_non_mutation_guarantee_preserved(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'symbolic_field_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(payload.get('noCanonicalMutation'))
        self.assertTrue(payload.get('noAutomaticIntervention'))
        self.assertTrue(payload.get('noMemoryMutation'))


if __name__ == '__main__':
    unittest.main()
