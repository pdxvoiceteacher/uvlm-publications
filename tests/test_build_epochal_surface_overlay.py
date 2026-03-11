from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_epochal_surface_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class EpochalSurfaceOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-bm.0', 'producerCommits': ['bm123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'epochal_surface_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'bm-1', 'epochalSurfaceAuditState': 'verified'}]})
        write_json(self.bridge / 'epochal_surface_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'bm-1', 'targetPublisherAction': 'docket'},
            {'reviewId': 'bm-2', 'targetPublisherAction': 'watch'},
            {'reviewId': 'bm-3', 'targetPublisherAction': 'suppressed'},
        ]})
        write_json(self.bridge / 'epochal_surface_map.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bm-1', 'surfaceStatus': 'under_review', 'surfaceClass': 'emergent'},
            {'reviewId': 'bm-2', 'surfaceStatus': 'monitor', 'surfaceClass': 'bounded'},
        ]})
        write_json(self.bridge / 'habitable_plateau_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bm-1', 'plateauClass': 'habitable', 'trustStability': 'high', 'memoryTeachability': 'strong', 'pluralityDurability': 'durable', 'provenanceMarkers': ['prov:ok'], 'canonicalIntegrityMarkers': ['integrity:verified']},
            {'reviewId': 'bm-2', 'plateauClass': 'conditional', 'trustStability': 'fragile', 'memoryTeachability': 'thin', 'pluralityDurability': 'bounded', 'provenanceMarkers': ['prov:gap'], 'canonicalIntegrityMarkers': ['integrity:watch']},
        ]})
        write_json(self.bridge / 'reopened_experiment_registry.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bm-1', 'experimentClass': 'reopened', 'experimentationRecovery': 0.64},
            {'reviewId': 'bm-2', 'experimentClass': 'experimental', 'experimentationRecovery': 0.23},
        ]})
        write_json(self.bridge / 'surface_emergence_gate.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bm-1', 'gateStatus': 'review'},
            {'reviewId': 'bm-2', 'gateStatus': 'guarded'},
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'terrace_seed_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'repluralization_watchlist.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'sedimentation_readiness_registry.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'new_delta_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'successor_crossing_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'successor_maturation_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'renewal_braid_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'terrace_health_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'epoch_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'delta_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'trust_surface_dashboard.json', {**reg_prov, 'entries': []})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-bm-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'epochal surface under review',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-bm.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--epochal-surface-audit', str(self.bridge / 'epochal_surface_audit.json'),
            '--epochal-surface-recommendations', str(self.bridge / 'epochal_surface_recommendations.json'),
            '--epochal-surface-map', str(self.bridge / 'epochal_surface_map.json'),
            '--habitable-plateau-report', str(self.bridge / 'habitable_plateau_report.json'),
            '--reopened-experiment-registry', str(self.bridge / 'reopened_experiment_registry.json'),
            '--surface-emergence-gate', str(self.bridge / 'surface_emergence_gate.json'),
            '--terrace-seed-dashboard', str(self.registry / 'terrace_seed_dashboard.json'),
            '--repluralization-watchlist', str(self.registry / 'repluralization_watchlist.json'),
            '--sedimentation-readiness-registry', str(self.registry / 'sedimentation_readiness_registry.json'),
            '--new-delta-dashboard', str(self.registry / 'new_delta_dashboard.json'),
            '--successor-crossing-dashboard', str(self.registry / 'successor_crossing_dashboard.json'),
            '--successor-maturation-dashboard', str(self.registry / 'successor_maturation_dashboard.json'),
            '--renewal-braid-dashboard', str(self.registry / 'renewal_braid_dashboard.json'),
            '--terrace-health-dashboard', str(self.registry / 'terrace_health_dashboard.json'),
            '--epoch-dashboard', str(self.registry / 'epoch_dashboard.json'),
            '--delta-dashboard', str(self.registry / 'delta_dashboard.json'),
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--trust-surface-dashboard', str(self.registry / 'trust_surface_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-epochal-surface-dashboard', str(self.registry / 'epochal_surface_dashboard.json'),
            '--out-reopened-experiment-watchlist', str(self.registry / 'reopened_experiment_watchlist.json'),
            '--out-habitable-plateau-registry', str(self.registry / 'habitable_plateau_registry.json'),
            '--out-epochal-surface-annotations', str(self.registry / 'epochal_surface_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'epochal_surface_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'habitable_plateau_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'reopened_experiment_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['bm-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['bm-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['bm-2'])

    def test_safeguard_flags_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'epochal_surface_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann['noCanonMutation'])
        self.assertTrue(ann['noDeploymentExecution'])
        self.assertTrue(ann['noGovernanceRightMutation'])
        self.assertTrue(ann['noRankingOfFuturesSuccessorOrdersCivilizationsCommunitiesInstitutions'])
        self.assertTrue(ann['surfaceVisibilityNotSettledAuthority'])
        self.assertTrue(ann['noTheoryCompetitionClosure'])
        self.assertTrue(ann['noNewAgeFormedOrFutureSecuredPermanentlyPresentation'])

    def test_provenance_validation_failure(self) -> None:
        payload = json.loads((self.bridge / 'epochal_surface_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'epochal_surface_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_numeric_fallback(self) -> None:
        payload = json.loads((self.bridge / 'reopened_experiment_registry.json').read_text(encoding='utf-8'))
        payload['entries'][0]['experimentationRecovery'] = 'bad-number'
        write_json(self.bridge / 'reopened_experiment_registry.json', payload)
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'epochal_surface_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['experimentationRecovery'], 0.0)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'epochal_surface_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


if __name__ == '__main__':
    unittest.main()
