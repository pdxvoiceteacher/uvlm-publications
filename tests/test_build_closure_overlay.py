from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_closure_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class ClosureOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-s.0', 'producerCommits': ['s123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'closure_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'cl-1', 'closureAuditState': 'verified'}]})
        write_json(self.bridge / 'closure_recommendations.json', {
            'provenance': prov,
            'recommendations': [{'reviewId': 'cl-1', 'candidateId': 'rc1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']}],
        })
        write_json(self.bridge / 'closure_state_map.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'cl-1', 'closureStatus': 'provisional-closed', 'closureConfidence': 'medium', 'repairUrgency': 'high'}],
        })
        write_json(self.bridge / 'closure_state_summary.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'cl-1', 'outcomeDurability': 'bounded-stable'}],
        })
        write_json(self.bridge / 'repair_candidate_map.json', {
            'provenance': prov,
            'candidates': [{'candidateId': 'rc1', 'linkedTargetIds': ['concept:x']}],
        })
        write_json(self.bridge / 'reopen_signal_report.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'cl-1', 'reopenedCaseWatchStatus': 'none'}],
        })

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'priority_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'triage_docket.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'triage_watchlist.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self, extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--closure-audit', str(self.bridge / 'closure_audit.json'),
            '--closure-recommendations', str(self.bridge / 'closure_recommendations.json'),
            '--closure-state-map', str(self.bridge / 'closure_state_map.json'),
            '--closure-state-summary', str(self.bridge / 'closure_state_summary.json'),
            '--repair-candidate-map', str(self.bridge / 'repair_candidate_map.json'),
            '--reopen-signal-report', str(self.bridge / 'reopen_signal_report.json'),
            '--priority-dashboard', str(self.registry / 'priority_dashboard.json'),
            '--triage-docket', str(self.registry / 'triage_docket.json'),
            '--triage-watchlist', str(self.registry / 'triage_watchlist.json'),
            '--out-closure-registry', str(self.registry / 'closure_registry.json'),
            '--out-repair-docket', str(self.registry / 'repair_docket.json'),
            '--out-reopened-case-watchlist', str(self.registry / 'reopened_case_watchlist.json'),
            '--out-closure-annotations', str(self.registry / 'closure_annotations.json'),
        ]
        if extra:
            cmd.extend(extra)
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_canonical_artifact_name_usage(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_deprecated_name_rejection(self) -> None:
        result = self.run_builder(['--closure-snapshot', str(self.bridge / 'closure_snapshot.json')])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Deprecated artifact alias', result.stdout + result.stderr)

    def test_provenance_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'closure_registry.json').read_text(encoding='utf-8'))
        self.assertIn('schemaVersions', payload.get('provenance', {}))

    def test_missing_upstream_artifact_failure(self) -> None:
        (self.bridge / 'reopen_signal_report.json').unlink()
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Missing required canonical artifact', result.stdout + result.stderr)

    def test_non_mutation_guarantee_preserved(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'closure_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(payload.get('noCanonicalMutation'))
        self.assertTrue(payload.get('noAutomaticClosure'))
        self.assertTrue(payload.get('noAutomaticReopen'))
        self.assertTrue(payload.get('noAutomaticRepair'))


if __name__ == '__main__':
    unittest.main()
