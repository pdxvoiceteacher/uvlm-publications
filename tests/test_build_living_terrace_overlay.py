from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_living_terrace_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class LivingTerraceOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-bn.0', 'producerCommits': ['bn123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'living_terrace_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'bn-1', 'livingTerraceAuditState': 'verified'}]})
        write_json(self.bridge / 'living_terrace_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'bn-1', 'targetPublisherAction': 'docket'},
            {'reviewId': 'bn-2', 'targetPublisherAction': 'watch'},
            {'reviewId': 'bn-3', 'targetPublisherAction': 'suppressed'},
        ]})
        write_json(self.bridge / 'living_terrace_map.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bn-1', 'terraceStatus': 'under_review', 'livingTerraceClass': 'emergent'},
            {'reviewId': 'bn-2', 'terraceStatus': 'monitor', 'livingTerraceClass': 'bounded'},
        ]})
        write_json(self.bridge / 'commons_habitability_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bn-1', 'habitabilityClass': 'habitable', 'trustOrdinariness': 'high', 'memoryTeachability': 'strong', 'pluralityMetabolization': 'metabolized', 'provenanceMarkers': ['prov:ok'], 'canonicalIntegrityMarkers': ['integrity:verified']},
            {'reviewId': 'bn-2', 'habitabilityClass': 'conditional', 'trustOrdinariness': 'fragile', 'memoryTeachability': 'thin', 'pluralityMetabolization': 'bounded', 'provenanceMarkers': ['prov:gap'], 'canonicalIntegrityMarkers': ['integrity:watch']},
        ]})
        write_json(self.bridge / 'plural_habitation_registry.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bn-1', 'habitationClass': 'open', 'ordinaryStewardUsability': 0.71},
            {'reviewId': 'bn-2', 'habitationClass': 'plural', 'ordinaryStewardUsability': 0.28},
        ]})
        write_json(self.bridge / 'terrace_consolidation_gate.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bn-1', 'gateStatus': 'review'},
            {'reviewId': 'bn-2', 'gateStatus': 'guarded'},
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'epochal_surface_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'reopened_experiment_watchlist.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'habitable_plateau_registry.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'terrace_seed_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'new_delta_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'successor_crossing_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'terrace_health_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'epoch_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'delta_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'trust_surface_dashboard.json', {**reg_prov, 'entries': []})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-bn-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'living terrace under review',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-bn.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--living-terrace-audit', str(self.bridge / 'living_terrace_audit.json'),
            '--living-terrace-recommendations', str(self.bridge / 'living_terrace_recommendations.json'),
            '--living-terrace-map', str(self.bridge / 'living_terrace_map.json'),
            '--commons-habitability-report', str(self.bridge / 'commons_habitability_report.json'),
            '--plural-habitation-registry', str(self.bridge / 'plural_habitation_registry.json'),
            '--terrace-consolidation-gate', str(self.bridge / 'terrace_consolidation_gate.json'),
            '--epochal-surface-dashboard', str(self.registry / 'epochal_surface_dashboard.json'),
            '--reopened-experiment-watchlist', str(self.registry / 'reopened_experiment_watchlist.json'),
            '--habitable-plateau-registry', str(self.registry / 'habitable_plateau_registry.json'),
            '--terrace-seed-dashboard', str(self.registry / 'terrace_seed_dashboard.json'),
            '--new-delta-dashboard', str(self.registry / 'new_delta_dashboard.json'),
            '--successor-crossing-dashboard', str(self.registry / 'successor_crossing_dashboard.json'),
            '--terrace-health-dashboard', str(self.registry / 'terrace_health_dashboard.json'),
            '--epoch-dashboard', str(self.registry / 'epoch_dashboard.json'),
            '--delta-dashboard', str(self.registry / 'delta_dashboard.json'),
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--trust-surface-dashboard', str(self.registry / 'trust_surface_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-living-terrace-dashboard', str(self.registry / 'living_terrace_dashboard.json'),
            '--out-plural-habitation-watchlist', str(self.registry / 'plural_habitation_watchlist.json'),
            '--out-commons-habitability-registry', str(self.registry / 'commons_habitability_registry.json'),
            '--out-living-terrace-annotations', str(self.registry / 'living_terrace_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'living_terrace_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'commons_habitability_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'plural_habitation_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['bn-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['bn-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['bn-2'])

    def test_safeguard_flags_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'living_terrace_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann['noCanonMutation'])
        self.assertTrue(ann['noDeploymentExecution'])
        self.assertTrue(ann['noGovernanceRightMutation'])
        self.assertTrue(ann['noRankingOfFuturesSuccessorOrdersCivilizationsCommunitiesInstitutions'])
        self.assertTrue(ann['terraceVisibilityNotSettledAuthority'])
        self.assertTrue(ann['noTheoryCompetitionClosure'])
        self.assertTrue(ann['noNewAgeSettledOrFutureSecuredPermanentlyPresentation'])

    def test_provenance_validation_failure(self) -> None:
        payload = json.loads((self.bridge / 'living_terrace_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'living_terrace_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_numeric_fallback(self) -> None:
        payload = json.loads((self.bridge / 'plural_habitation_registry.json').read_text(encoding='utf-8'))
        payload['entries'][0]['ordinaryStewardUsability'] = 'bad-number'
        write_json(self.bridge / 'plural_habitation_registry.json', payload)
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'living_terrace_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['ordinaryStewardUsability'], 0.0)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'living_terrace_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


if __name__ == '__main__':
    unittest.main()
