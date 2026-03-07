from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_verification_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class VerificationOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-u.0', 'producerCommits': ['u123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'verification_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'vf-1', 'verificationAuditState': 'verified'}]})
        write_json(self.bridge / 'verification_recommendations.json', {
            'provenance': prov,
            'recommendations': [{'reviewId': 'vf-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']}],
        })
        write_json(self.bridge / 'claim_type_map.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'vf-1', 'claimType': 'factual-claim'}],
        })
        write_json(self.bridge / 'entity_resolution_map.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'vf-1', 'entityResolutionStatus': 'partially-resolved'}],
        })
        write_json(self.bridge / 'entity_resolution_summary.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'vf-1', 'ambiguityLevel': 'medium'}],
        })
        write_json(self.bridge / 'verification_task_map.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'vf-1', 'verificationUrgency': 'high', 'verificationTaskSummary': 'cross-source-check'}],
        })

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'symbolic_field_registry.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'closure_registry.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'priority_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self, extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--verification-audit', str(self.bridge / 'verification_audit.json'),
            '--verification-recommendations', str(self.bridge / 'verification_recommendations.json'),
            '--claim-type-map', str(self.bridge / 'claim_type_map.json'),
            '--entity-resolution-map', str(self.bridge / 'entity_resolution_map.json'),
            '--entity-resolution-summary', str(self.bridge / 'entity_resolution_summary.json'),
            '--verification-task-map', str(self.bridge / 'verification_task_map.json'),
            '--symbolic-field-registry', str(self.registry / 'symbolic_field_registry.json'),
            '--closure-registry', str(self.registry / 'closure_registry.json'),
            '--priority-dashboard', str(self.registry / 'priority_dashboard.json'),
            '--out-verification-dashboard', str(self.registry / 'verification_dashboard.json'),
            '--out-entity-watchlist', str(self.registry / 'entity_watchlist.json'),
            '--out-claim-type-registry', str(self.registry / 'claim_type_registry.json'),
            '--out-verification-annotations', str(self.registry / 'verification_annotations.json'),
        ]
        if extra:
            cmd.extend(extra)
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_canonical_artifact_name_usage(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_deprecated_name_rejection(self) -> None:
        result = self.run_builder(['--verification-snapshot', str(self.bridge / 'verification_snapshot.json')])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Deprecated artifact alias', result.stdout + result.stderr)

    def test_provenance_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'verification_dashboard.json').read_text(encoding='utf-8'))
        self.assertIn('schemaVersions', payload.get('provenance', {}))

    def test_missing_upstream_artifact_failure(self) -> None:
        (self.bridge / 'verification_task_map.json').unlink()
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Missing required canonical artifact', result.stdout + result.stderr)

    def test_non_mutation_guarantee_preserved(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'verification_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(payload.get('noCanonicalMutation'))
        self.assertTrue(payload.get('noAutomaticAccusation'))
        self.assertTrue(payload.get('noAutomaticIdentityResolution'))


if __name__ == '__main__':
    unittest.main()
