from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_trust_surface_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class TrustSurfaceOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-bd.0', 'producerCommits': ['bd123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'trust_surface_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'ts-1', 'trustSurfaceAuditState': 'verified'}]})
        write_json(self.bridge / 'trust_surface_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'ts-1', 'targetPublisherAction': 'docket'},
            {'reviewId': 'ts-2', 'targetPublisherAction': 'watch'},
            {'reviewId': 'ts-3', 'targetPublisherAction': 'suppressed'},
        ]})
        write_json(self.bridge / 'trust_surface_map.json', {'provenance': prov, 'entries': [
            {'reviewId': 'ts-1', 'trustSurfaceStatus': 'stable', 'persistenceClass': 'persistent'},
            {'reviewId': 'ts-2', 'trustSurfaceStatus': 'monitor', 'persistenceClass': 'volatile'},
        ]})
        write_json(self.bridge / 'delegated_access_registry.json', {'provenance': prov, 'entries': [
            {'reviewId': 'ts-1', 'wrapperLineage': 'open-chain'},
            {'reviewId': 'ts-2', 'wrapperLineage': 'opaque-wrapper'},
        ]})
        write_json(self.bridge / 'revocation_asymmetry_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'ts-1', 'revocationAsymmetryScore': 0.2},
            {'reviewId': 'ts-2', 'revocationAsymmetryScore': 0.8},
        ]})
        write_json(self.bridge / 'interface_legitimacy_risk_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'ts-1', 'interfaceLegitimacyScore': 0.9, 'trustCompressionRisk': 'bounded', 'auditBurdenScore': 0.4},
            {'reviewId': 'ts-2', 'interfaceLegitimacyScore': 0.3, 'trustCompressionRisk': 'high', 'auditBurdenScore': 0.7},
        ]})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-bd-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'no accusations',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-bd.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--trust-surface-audit', str(self.bridge / 'trust_surface_audit.json'),
            '--trust-surface-recommendations', str(self.bridge / 'trust_surface_recommendations.json'),
            '--trust-surface-map', str(self.bridge / 'trust_surface_map.json'),
            '--delegated-access-registry', str(self.bridge / 'delegated_access_registry.json'),
            '--revocation-asymmetry-report', str(self.bridge / 'revocation_asymmetry_report.json'),
            '--interface-legitimacy-risk-report', str(self.bridge / 'interface_legitimacy_risk_report.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-trust-surface-dashboard', str(self.registry / 'trust_surface_dashboard.json'),
            '--out-delegated-access-registry', str(self.registry / 'delegated_access_registry.json'),
            '--out-revocation-watchlist', str(self.registry / 'revocation_watchlist.json'),
            '--out-interface-legitimacy-annotations', str(self.registry / 'interface_legitimacy_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'trust_surface_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'delegated_access_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'revocation_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['ts-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['ts-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['ts-2'])

    def test_ui_signals_and_classes(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        watch = json.loads((self.registry / 'revocation_watchlist.json').read_text(encoding='utf-8'))
        entry = watch['entries'][0]
        self.assertEqual(entry['revocationAsymmetryScore'], 0.8)
        self.assertEqual(entry['interfaceLegitimacyScore'], 0.3)
        self.assertEqual(entry['trustCompressionRisk'], 'high')
        self.assertIn('revocation-asymmetry', entry['atlasClasses'])
        self.assertIn('legitimacy-risk', entry['atlasClasses'])
        self.assertIn('wrapper-provenance-risk', entry['atlasClasses'])
        self.assertIn('trust-compression-warning', entry['atlasClasses'])

    def test_safeguards_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        annotations = json.loads((self.registry / 'interface_legitimacy_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(annotations['noAutomaticAccusation'])
        self.assertTrue(annotations['noEnforcementActions'])
        self.assertTrue(annotations['noIdentityMutation'])
        self.assertTrue(annotations['noGovernanceAuthorityAssignment'])
        self.assertTrue(annotations['informationalSignalsOnly'])

    def test_numeric_fallback(self) -> None:
        payload = json.loads((self.bridge / 'revocation_asymmetry_report.json').read_text(encoding='utf-8'))
        payload['entries'][0]['revocationAsymmetryScore'] = 'bad-number'
        write_json(self.bridge / 'revocation_asymmetry_report.json', payload)
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'trust_surface_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['revocationAsymmetryScore'], 0.0)

    def test_provenance_validation_failure(self) -> None:
        payload = json.loads((self.bridge / 'trust_surface_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'trust_surface_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_canonical_integrity_propagation_and_reset_classes(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'trust_surface_dashboard.json').read_text(encoding='utf-8'))
        annotations = json.loads((self.registry / 'interface_legitimacy_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['trustPresentationDegraded'])
        self.assertIn('trust-surface-stable', annotations['atlasResetRemovesClasses'])
        self.assertIn('revocation-asymmetry', annotations['atlasResetRemovesClasses'])


if __name__ == '__main__':
    unittest.main()
