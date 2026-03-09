from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_authorship_integrity_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class AuthorshipIntegrityOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-bc.1', 'producerCommits': ['bc100'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'authorship_integrity_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'ai-1', 'authorshipIntegrityAuditState': 'verified'}]})
        write_json(self.bridge / 'authorship_integrity_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'ai-1', 'targetPublisherAction': 'docket'},
            {'reviewId': 'ai-2', 'targetPublisherAction': 'watch'},
            {'reviewId': 'ai-3', 'targetPublisherAction': 'suppressed'},
        ]})
        write_json(self.bridge / 'canonical_authorship_manifest.json', {
            'provenance': prov,
            'originProject': 'Ultra Verba Lux Mentis / Triadic Commons Architecture',
            'canonicalAuthors': ['Thomas Prislac', 'Envoy Echo'],
            'canonicalAttributionNotice': 'This architecture includes foundational code and governance design authored by Thomas Prislac and Envoy Echo within the Ultra Verba Lux Mentis / triadic commons lineage. Derivatives must preserve provenance, disclose modifications, and may not claim canonical equivalence when safety or governance boundaries have changed.',
            'derivativeDisclosureRequired': True,
        })
        write_json(self.bridge / 'derivative_disclosure_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'ai-1', 'derivativeDisclosed': True, 'disclosureCompleteness': 'complete', 'retainedAttributionMarkers': ['author-tag'], 'safetyBoundaryChangeDeclarations': ['none'], 'signatureMetadata': {'type': 'release-signature'}},
            {'reviewId': 'ai-2', 'derivativeDisclosed': False, 'disclosureCompleteness': 'missing'},
        ]})
        write_json(self.bridge / 'misattribution_risk_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'ai-1', 'trustDegraded': False, 'attributionDivergenceDetected': False, 'divergenceFlags': [], 'divergenceReasons': []},
            {'reviewId': 'ai-2', 'trustDegraded': True, 'attributionDivergenceDetected': True, 'missingAttribution': True, 'provenanceBreakage': True, 'undeclaredSafetyBoundaryChanges': True, 'falseCanonicalEquivalenceClaims': True, 'captureRiskLinkedToMisrepresentation': 0.75, 'divergenceFlags': ['missing-attribution'], 'divergenceReasons': ['provenance gap']},
            {'reviewId': 'ai-3', 'trustDegraded': True, 'attributionDivergenceDetected': True, 'provenanceBreakage': True},
        ]})
        write_json(self.bridge / 'authorship_integrity_summary.json', {'provenance': prov, 'entries': [
            {'reviewId': 'ai-1', 'authorshipVerified': True, 'sourceRepos': ['repo:a'], 'sourceManifestHashPresent': True, 'constraintSignaturePresent': True, 'releaseSignaturePresent': True, 'constraintSignature': 'sig-1', 'releaseSignature': 'rel-1'},
            {'reviewId': 'ai-2', 'authorshipVerified': False, 'sourceRepos': ['repo:b'], 'sourceManifestHashPresent': False, 'constraintSignaturePresent': False, 'releaseSignaturePresent': False},
            {'reviewId': 'ai-3', 'authorshipVerified': False, 'sourceRepos': ['repo:c']},
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'observer_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'knowledge_river_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-bc1-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'no sabotage enforcement',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-bc1.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--authorship-integrity-audit', str(self.bridge / 'authorship_integrity_audit.json'),
            '--authorship-integrity-recommendations', str(self.bridge / 'authorship_integrity_recommendations.json'),
            '--canonical-authorship-manifest', str(self.bridge / 'canonical_authorship_manifest.json'),
            '--derivative-disclosure-report', str(self.bridge / 'derivative_disclosure_report.json'),
            '--misattribution-risk-report', str(self.bridge / 'misattribution_risk_report.json'),
            '--authorship-integrity-summary', str(self.bridge / 'authorship_integrity_summary.json'),
            '--observer-dashboard', str(self.registry / 'observer_dashboard.json'),
            '--knowledge-river-dashboard', str(self.registry / 'knowledge_river_dashboard.json'),
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-authorship-integrity-dashboard', str(self.registry / 'authorship_integrity_dashboard.json'),
            '--out-derivative-registry', str(self.registry / 'derivative_registry.json'),
            '--out-misattribution-watchlist', str(self.registry / 'misattribution_watchlist.json'),
            '--out-authorship-annotations', str(self.registry / 'authorship_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'authorship_integrity_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'derivative_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'misattribution_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['ai-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['ai-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['ai-2'])

    def test_safeguards_and_no_retaliation_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'authorship_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann['noHiddenSabotage'])
        self.assertTrue(ann['noCovertPunishment'])
        self.assertTrue(ann['noDeletionOrDisablingLogic'])
        self.assertTrue(ann['noAutoBlockingDerivativesSolelyForBeingDerivatives'])
        self.assertTrue(ann['annotations'][0]['noRetaliation'])
        self.assertTrue(ann['annotations'][0]['noSabotage'])

    def test_provenance_validation_failure(self) -> None:
        payload = json.loads((self.bridge / 'authorship_integrity_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'authorship_integrity_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'authorship_integrity_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])

    def test_derivative_disclosure_handling(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        registry = json.loads((self.registry / 'derivative_registry.json').read_text(encoding='utf-8'))
        entry = registry['entries'][0]
        self.assertTrue(entry['derivativeDisclosed'])
        self.assertEqual(entry['disclosureCompleteness'], 'complete')
        self.assertEqual(entry['retainedAttributionMarkers'], ['author-tag'])

    def test_trust_degradation_signaling(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        watch = json.loads((self.registry / 'misattribution_watchlist.json').read_text(encoding='utf-8'))
        entry = watch['entries'][0]
        self.assertTrue(entry['trustDegraded'])
        self.assertTrue(entry['attributionDivergenceDetected'])
        self.assertTrue(entry['falseCanonicalEquivalenceClaims'])

    def test_reset_safe_atlas_classes(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'authorship_annotations.json').read_text(encoding='utf-8'))
        self.assertIn('authorship-verified', ann['atlasResetRemovesClasses'])
        self.assertIn('derivative-disclosed', ann['atlasResetRemovesClasses'])
        self.assertIn('trust-degraded', ann['atlasResetRemovesClasses'])
        suppressed = next(e for e in ann['annotations'] if e['reviewId'] == 'ai-3')
        self.assertEqual(suppressed['targetPublisherAction'], 'suppress')


if __name__ == '__main__':
    unittest.main()
