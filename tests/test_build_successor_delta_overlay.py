from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_successor_delta_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class SuccessorDeltaOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-bh.0', 'producerCommits': ['bh123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'successor_delta_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'sd-1', 'successorDeltaAuditState': 'verified'}]})
        write_json(self.bridge / 'successor_delta_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'sd-1', 'targetPublisherAction': 'docket'},
            {'reviewId': 'sd-2', 'targetPublisherAction': 'watch'},
            {'reviewId': 'sd-3', 'targetPublisherAction': 'suppressed'},
        ]})
        write_json(self.bridge / 'renewal_braid_map.json', {'provenance': prov, 'entries': [
            {'reviewId': 'sd-1', 'successorStatus': 'active', 'braidClass': 'braided'},
            {'reviewId': 'sd-2', 'successorStatus': 'watch', 'braidClass': 'emergent'},
        ]})
        write_json(self.bridge / 'successor_delta_seed_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'sd-1', 'successorSeedClass': 'seeded'},
            {'reviewId': 'sd-2', 'successorSeedClass': 'candidate'},
        ]})
        write_json(self.bridge / 'plurality_recovery_registry.json', {'provenance': prov, 'entries': [
            {'reviewId': 'sd-1', 'pluralityClass': 'recovery'},
            {'reviewId': 'sd-2', 'pluralityClass': 'bounded'},
        ]})
        write_json(self.bridge / 'transition_coupling_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'sd-1', 'transitionCouplingClass': 'coupled', 'trustRepair': 'active', 'memoryReactivation': 'active', 'successorCaptureRisk': 'bounded', 'couplingScore': 0.66, 'provenanceMarkers': ['prov:ok'], 'canonicalIntegrityMarkers': ['integrity:verified']},
            {'reviewId': 'sd-2', 'transitionCouplingClass': 'aligned', 'trustRepair': 'bounded', 'memoryReactivation': 'fragile', 'successorCaptureRisk': 'high', 'couplingScore': 0.31, 'provenanceMarkers': ['prov:gap'], 'canonicalIntegrityMarkers': ['integrity:watch']},
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'terrace_health_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'epoch_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'delta_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'knowledge_river_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'trust_surface_dashboard.json', {**reg_prov, 'entries': []})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-bh-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'no successor coronation',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-bh.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--successor-delta-audit', str(self.bridge / 'successor_delta_audit.json'),
            '--successor-delta-recommendations', str(self.bridge / 'successor_delta_recommendations.json'),
            '--renewal-braid-map', str(self.bridge / 'renewal_braid_map.json'),
            '--successor-delta-seed-report', str(self.bridge / 'successor_delta_seed_report.json'),
            '--plurality-recovery-registry', str(self.bridge / 'plurality_recovery_registry.json'),
            '--transition-coupling-report', str(self.bridge / 'transition_coupling_report.json'),
            '--terrace-health-dashboard', str(self.registry / 'terrace_health_dashboard.json'),
            '--epoch-dashboard', str(self.registry / 'epoch_dashboard.json'),
            '--delta-dashboard', str(self.registry / 'delta_dashboard.json'),
            '--knowledge-river-dashboard', str(self.registry / 'knowledge_river_dashboard.json'),
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--trust-surface-dashboard', str(self.registry / 'trust_surface_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-renewal-braid-dashboard', str(self.registry / 'renewal_braid_dashboard.json'),
            '--out-successor-delta-registry', str(self.registry / 'successor_delta_registry.json'),
            '--out-plurality-recovery-watchlist', str(self.registry / 'plurality_recovery_watchlist.json'),
            '--out-transition-annotations', str(self.registry / 'transition_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'renewal_braid_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'successor_delta_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'plurality_recovery_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['sd-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['sd-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['sd-2'])

    def test_safeguard_flags_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'transition_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann['noCanonMutation'])
        self.assertTrue(ann['noDeploymentExecution'])
        self.assertTrue(ann['noGovernanceRightMutation'])
        self.assertTrue(ann['noRankingOfSuccessorOrdersCivilizationsInstitutionsCommunities'])
        self.assertTrue(ann['successorVisibilityNotEpochAuthority'])
        self.assertTrue(ann['noTheoryCompetitionClosure'])
        self.assertTrue(ann['noNewAgeConfirmedPresentation'])

    def test_provenance_validation_failure(self) -> None:
        payload = json.loads((self.bridge / 'successor_delta_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'successor_delta_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_numeric_fallback(self) -> None:
        payload = json.loads((self.bridge / 'transition_coupling_report.json').read_text(encoding='utf-8'))
        payload['entries'][0]['couplingScore'] = 'bad-number'
        write_json(self.bridge / 'transition_coupling_report.json', payload)
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'renewal_braid_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['couplingScore'], 0.0)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'renewal_braid_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


if __name__ == '__main__':
    unittest.main()
