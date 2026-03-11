from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_background_coherence_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class BackgroundCoherenceOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-bo.0', 'producerCommits': ['bo123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'background_coherence_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'bo-1', 'backgroundCoherenceAuditState': 'verified'}]})
        write_json(self.bridge / 'background_coherence_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'bo-1', 'targetPublisherAction': 'docket'},
            {'reviewId': 'bo-2', 'targetPublisherAction': 'watch'},
            {'reviewId': 'bo-3', 'targetPublisherAction': 'suppressed'},
        ]})
        write_json(self.bridge / 'background_coherence_map.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bo-1', 'backgroundStatus': 'under_review', 'backgroundClass': 'quiet'},
            {'reviewId': 'bo-2', 'backgroundStatus': 'monitor', 'backgroundClass': 'bounded'},
        ]})
        write_json(self.bridge / 'civilizational_normalization_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bo-1', 'normalizationClass': 'ambient', 'trustOrdinariness': 'high', 'pluralityMetabolization': 'metabolized', 'commonsHabitability': 'habitable', 'provenanceMarkers': ['prov:ok'], 'canonicalIntegrityMarkers': ['integrity:verified']},
            {'reviewId': 'bo-2', 'normalizationClass': 'bounded', 'trustOrdinariness': 'fragile', 'pluralityMetabolization': 'bounded', 'commonsHabitability': 'conditional', 'provenanceMarkers': ['prov:gap'], 'canonicalIntegrityMarkers': ['integrity:watch']},
        ]})
        write_json(self.bridge / 'ambient_memory_registry.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bo-1', 'ambientMemoryClass': 'present', 'pedagogyOrdinariness': 0.67},
            {'reviewId': 'bo-2', 'ambientMemoryClass': 'watch', 'pedagogyOrdinariness': 0.29},
        ]})
        write_json(self.bridge / 'normalization_gate.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bo-1', 'gateStatus': 'review'},
            {'reviewId': 'bo-2', 'gateStatus': 'guarded'},
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'living_terrace_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'plural_habitation_watchlist.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_habitability_registry.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'epochal_surface_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'terrace_seed_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'new_delta_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'epoch_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'delta_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'trust_surface_dashboard.json', {**reg_prov, 'entries': []})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-bo-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'background coherence under review',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-bo.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--background-coherence-audit', str(self.bridge / 'background_coherence_audit.json'),
            '--background-coherence-recommendations', str(self.bridge / 'background_coherence_recommendations.json'),
            '--background-coherence-map', str(self.bridge / 'background_coherence_map.json'),
            '--civilizational-normalization-report', str(self.bridge / 'civilizational_normalization_report.json'),
            '--ambient-memory-registry', str(self.bridge / 'ambient_memory_registry.json'),
            '--normalization-gate', str(self.bridge / 'normalization_gate.json'),
            '--living-terrace-dashboard', str(self.registry / 'living_terrace_dashboard.json'),
            '--plural-habitation-watchlist', str(self.registry / 'plural_habitation_watchlist.json'),
            '--commons-habitability-registry', str(self.registry / 'commons_habitability_registry.json'),
            '--epochal-surface-dashboard', str(self.registry / 'epochal_surface_dashboard.json'),
            '--terrace-seed-dashboard', str(self.registry / 'terrace_seed_dashboard.json'),
            '--new-delta-dashboard', str(self.registry / 'new_delta_dashboard.json'),
            '--epoch-dashboard', str(self.registry / 'epoch_dashboard.json'),
            '--delta-dashboard', str(self.registry / 'delta_dashboard.json'),
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--trust-surface-dashboard', str(self.registry / 'trust_surface_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-background-coherence-dashboard', str(self.registry / 'background_coherence_dashboard.json'),
            '--out-ambient-memory-watchlist', str(self.registry / 'ambient_memory_watchlist.json'),
            '--out-civilizational-normalization-registry', str(self.registry / 'civilizational_normalization_registry.json'),
            '--out-background-coherence-annotations', str(self.registry / 'background_coherence_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'background_coherence_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'civilizational_normalization_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'ambient_memory_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['bo-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['bo-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['bo-2'])

    def test_safeguard_flags_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'background_coherence_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann['noCanonMutation'])
        self.assertTrue(ann['noDeploymentExecution'])
        self.assertTrue(ann['noGovernanceRightMutation'])
        self.assertTrue(ann['noRankingOfFuturesCivilizationsCommunitiesInstitutions'])
        self.assertTrue(ann['backgroundVisibilityNotFinalAuthority'])
        self.assertTrue(ann['noTheoryCompetitionClosure'])
        self.assertTrue(ann['noEpochFinalizedOrFutureSettledPermanentlyPresentation'])

    def test_provenance_validation_failure(self) -> None:
        payload = json.loads((self.bridge / 'background_coherence_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'background_coherence_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_numeric_fallback(self) -> None:
        payload = json.loads((self.bridge / 'ambient_memory_registry.json').read_text(encoding='utf-8'))
        payload['entries'][0]['pedagogyOrdinariness'] = 'bad-number'
        write_json(self.bridge / 'ambient_memory_registry.json', payload)
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'background_coherence_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['pedagogyOrdinariness'], 0.0)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'background_coherence_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


if __name__ == '__main__':
    unittest.main()
