from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_evidence_authority_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class EvidenceAuthorityOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-x1.0', 'producerCommits': ['x123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'evidence_authority_audit.json', {
            'provenance': prov,
            'audits': [{'reviewId': 'ea-1', 'authorityAuditState': 'verified'}],
        })
        write_json(self.bridge / 'evidence_authority_recommendations.json', {
            'provenance': prov,
            'recommendations': [
                {'reviewId': 'ea-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x'], 'evidenceMaturity': 'corroborated'},
                {'reviewId': 'ea-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y'], 'evidenceMaturity': 'weak'},
                {'reviewId': 'ea-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z'], 'evidenceMaturity': 'weak'},
            ],
        })
        write_json(self.bridge / 'evidence_authority_map.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'ea-1', 'claimType': 'integrity-risk', 'allowedAuthorityClass': 'review-only'}],
        })
        write_json(self.bridge / 'evidence_authority_summary.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'ea-1', 'authorityMismatchFlag': False}],
        })
        write_json(self.bridge / 'propagation_rights_map.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'ea-1', 'propagationRestrictions': ['no-public-forwarding'], 'allowedPropagationRights': ['internal-review']}],
        })
        write_json(self.bridge / 'maturity_gate_report.json', {
            'provenance': prov,
            'entries': [{'reviewId': 'ea-1', 'maturityGateStatus': 'gated', 'maturityGateReason': 'requires-independent-corroboration'}],
        })

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'verification_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'public_record_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'symbolic_field_registry.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'investigation_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self, extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--evidence-authority-audit', str(self.bridge / 'evidence_authority_audit.json'),
            '--evidence-authority-recommendations', str(self.bridge / 'evidence_authority_recommendations.json'),
            '--evidence-authority-map', str(self.bridge / 'evidence_authority_map.json'),
            '--evidence-authority-summary', str(self.bridge / 'evidence_authority_summary.json'),
            '--propagation-rights-map', str(self.bridge / 'propagation_rights_map.json'),
            '--maturity-gate-report', str(self.bridge / 'maturity_gate_report.json'),
            '--verification-dashboard', str(self.registry / 'verification_dashboard.json'),
            '--public-record-dashboard', str(self.registry / 'public_record_dashboard.json'),
            '--symbolic-field-registry', str(self.registry / 'symbolic_field_registry.json'),
            '--investigation-dashboard', str(self.registry / 'investigation_dashboard.json'),
            '--out-authority-gate-dashboard', str(self.registry / 'authority_gate_dashboard.json'),
            '--out-weak-evidence-watchlist', str(self.registry / 'weak_evidence_watchlist.json'),
            '--out-propagation-annotations', str(self.registry / 'propagation_annotations.json'),
            '--out-maturity-restriction-registry', str(self.registry / 'maturity_restriction_registry.json'),
        ]
        if extra:
            cmd.extend(extra)
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_canonical_artifact_name_usage(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_deprecated_name_rejection(self) -> None:
        result = self.run_builder(['--evidence-authority-snapshot', str(self.bridge / 'old.json')])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Deprecated artifact alias', result.stdout + result.stderr)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        dashboard = json.loads((self.registry / 'authority_gate_dashboard.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'weak_evidence_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['ea-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['ea-2'])

    def test_output_contract_validation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        for name in [
            'authority_gate_dashboard.json',
            'weak_evidence_watchlist.json',
            'propagation_annotations.json',
            'maturity_restriction_registry.json',
        ]:
            payload = json.loads((self.registry / name).read_text(encoding='utf-8'))
            self.assertIsInstance(payload, dict)
            self.assertIn('provenance', payload)

    def test_non_mutation_guarantee_preserved(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'propagation_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(payload.get('noCanonicalMutation'))
        self.assertTrue(payload.get('noAutomaticRestrictionLifting'))
        self.assertTrue(payload.get('noAutomaticGraphHardening'))


if __name__ == '__main__':
    unittest.main()
