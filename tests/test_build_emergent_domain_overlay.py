from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_emergent_domain_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class EmergentDomainOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-at.0', 'producerCommits': ['at123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'emergent_domain_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'ed-1', 'emergentDomainAuditState': 'verified'}]})
        write_json(self.bridge / 'emergent_domain_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'ed-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x'], 'commonsLegibilityRequirement': 'required'},
            {'reviewId': 'ed-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y'], 'commonsLegibilityRequirement': 'required'},
            {'reviewId': 'ed-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z'], 'commonsLegibilityRequirement': 'required'},
        ]})
        write_json(self.bridge / 'emergent_domain_map.json', {'provenance': prov, 'entries': [{'reviewId': 'ed-1', 'domainStatus': 'emergent', 'sourceDomains': ['theory', 'value']}]})
        write_json(self.bridge / 'cross_domain_invariant_report.json', {'provenance': prov, 'entries': [{'reviewId': 'ed-1', 'invariantPatternClass': 'convergent'}]})
        write_json(self.bridge / 'field_birth_pressure_report.json', {'provenance': prov, 'entries': [{'reviewId': 'ed-1', 'fieldBirthPressure': 'high', 'fieldBirthPressureScore': 0.81}]})
        write_json(self.bridge / 'domain_boundary_failure_map.json', {'provenance': prov, 'entries': [{'reviewId': 'ed-1', 'domainBoundaryFailure': 'porous'}]})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-at-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'no canon formation',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-at.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'transfer_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'value_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'uncertainty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'social_entropy_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civic_literacy_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--emergent-domain-audit', str(self.bridge / 'emergent_domain_audit.json'),
            '--emergent-domain-recommendations', str(self.bridge / 'emergent_domain_recommendations.json'),
            '--emergent-domain-map', str(self.bridge / 'emergent_domain_map.json'),
            '--cross-domain-invariant-report', str(self.bridge / 'cross_domain_invariant_report.json'),
            '--field-birth-pressure-report', str(self.bridge / 'field_birth_pressure_report.json'),
            '--domain-boundary-failure-map', str(self.bridge / 'domain_boundary_failure_map.json'),
            '--transfer-dashboard', str(self.registry / 'transfer_dashboard.json'),
            '--value-dashboard', str(self.registry / 'value_dashboard.json'),
            '--uncertainty-dashboard', str(self.registry / 'uncertainty_dashboard.json'),
            '--social-entropy-dashboard', str(self.registry / 'social_entropy_dashboard.json'),
            '--civic-literacy-dashboard', str(self.registry / 'civic_literacy_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-emergent-domain-dashboard', str(self.registry / 'emergent_domain_dashboard.json'),
            '--out-domain-birth-registry', str(self.registry / 'domain_birth_registry.json'),
            '--out-domain-boundary-watchlist', str(self.registry / 'domain_boundary_watchlist.json'),
            '--out-emergent-domain-annotations', str(self.registry / 'emergent_domain_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'emergent_domain_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'domain_birth_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'domain_boundary_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['ed-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['ed-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['ed-2'])

    def test_guardrails_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'emergent_domain_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noAutomaticCanonFormation'))
        self.assertTrue(ann.get('noDisciplineRanking'))
        self.assertTrue(ann.get('noFieldSovereigntyClaims'))
        self.assertTrue(ann.get('noScientificCanonMutation'))

    def test_missing_manifest_degrades_trust(self) -> None:
        (self.bridge / 'canonical_integrity_manifest.json').unlink(missing_ok=True)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'emergent_domain_dashboard.json').read_text(encoding='utf-8'))
        self.assertFalse(dashboard['canonicalIntegrityVerified'])
        self.assertTrue(dashboard['modificationDisclosureMissing'])
        self.assertTrue(dashboard['trustPresentationDegraded'])

    def test_invalid_numeric_values_default_to_zero(self) -> None:
        payload = json.loads((self.bridge / 'field_birth_pressure_report.json').read_text(encoding='utf-8'))
        payload['entries'][0]['fieldBirthPressureScore'] = 'bad-number'
        write_json(self.bridge / 'field_birth_pressure_report.json', payload)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'emergent_domain_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['fieldBirthPressureScore'], 0.0)

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'emergent_domain_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'emergent_domain_audit.json', payload)

        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
