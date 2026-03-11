from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_terrace_seed_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class TerraceSeedOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-bl.0', 'producerCommits': ['bl123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'terrace_seed_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'bl-1', 'terraceSeedAuditState': 'verified'}]})
        write_json(self.bridge / 'terrace_seed_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'bl-1', 'targetPublisherAction': 'docket'},
            {'reviewId': 'bl-2', 'targetPublisherAction': 'watch'},
            {'reviewId': 'bl-3', 'targetPublisherAction': 'suppressed'},
        ]})
        write_json(self.bridge / 'terrace_seed_map.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bl-1', 'seedStatus': 'under_review', 'terraceSeedClass': 'early'},
            {'reviewId': 'bl-2', 'seedStatus': 'monitor', 'terraceSeedClass': 'bounded'},
        ]})
        write_json(self.bridge / 'experimental_repluralization_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bl-1', 'repluralizationClass': 'reopened', 'experimentationRecovery': 0.61},
            {'reviewId': 'bl-2', 'repluralizationClass': 'experimental', 'experimentationRecovery': 0.27},
        ]})
        write_json(self.bridge / 'sedimentation_readiness_scorecard.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bl-1', 'readinessClass': 'guarded', 'trustStability': 'high', 'memoryTeachability': 'strong', 'pluralityDurability': 'durable', 'provenanceMarkers': ['prov:ok'], 'canonicalIntegrityMarkers': ['integrity:verified']},
            {'reviewId': 'bl-2', 'readinessClass': 'conditional', 'trustStability': 'fragile', 'memoryTeachability': 'thin', 'pluralityDurability': 'bounded', 'provenanceMarkers': ['prov:gap'], 'canonicalIntegrityMarkers': ['integrity:watch']},
        ]})
        write_json(self.bridge / 'terrace_seed_gate.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bl-1', 'gateStatus': 'review'},
            {'reviewId': 'bl-2', 'gateStatus': 'guarded'},
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'new_delta_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'reversion_watchlist.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'crossing_resilience_registry.json', {**reg_prov, 'entries': []})
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
            'canonicalPhaselock': 'phase-bl-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'terrace seed under review',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-bl.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--terrace-seed-audit', str(self.bridge / 'terrace_seed_audit.json'),
            '--terrace-seed-recommendations', str(self.bridge / 'terrace_seed_recommendations.json'),
            '--terrace-seed-map', str(self.bridge / 'terrace_seed_map.json'),
            '--experimental-repluralization-report', str(self.bridge / 'experimental_repluralization_report.json'),
            '--sedimentation-readiness-scorecard', str(self.bridge / 'sedimentation_readiness_scorecard.json'),
            '--terrace-seed-gate', str(self.bridge / 'terrace_seed_gate.json'),
            '--new-delta-dashboard', str(self.registry / 'new_delta_dashboard.json'),
            '--reversion-watchlist', str(self.registry / 'reversion_watchlist.json'),
            '--crossing-resilience-registry', str(self.registry / 'crossing_resilience_registry.json'),
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
            '--out-terrace-seed-dashboard', str(self.registry / 'terrace_seed_dashboard.json'),
            '--out-repluralization-watchlist', str(self.registry / 'repluralization_watchlist.json'),
            '--out-sedimentation-readiness-registry', str(self.registry / 'sedimentation_readiness_registry.json'),
            '--out-terrace-seed-annotations', str(self.registry / 'terrace_seed_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'terrace_seed_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'sedimentation_readiness_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'repluralization_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['bl-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['bl-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['bl-2'])

    def test_safeguard_flags_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'terrace_seed_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann['noCanonMutation'])
        self.assertTrue(ann['noDeploymentExecution'])
        self.assertTrue(ann['noGovernanceRightMutation'])
        self.assertTrue(ann['noRankingOfFuturesSuccessorOrdersCivilizationsCommunitiesInstitutions'])
        self.assertTrue(ann['seedVisibilityNotSettledAuthority'])
        self.assertTrue(ann['noTheoryCompetitionClosure'])
        self.assertTrue(ann['noNewAgeFormedOrFutureSecuredPermanentlyPresentation'])

    def test_provenance_validation_failure(self) -> None:
        payload = json.loads((self.bridge / 'terrace_seed_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'terrace_seed_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_numeric_fallback(self) -> None:
        payload = json.loads((self.bridge / 'experimental_repluralization_report.json').read_text(encoding='utf-8'))
        payload['entries'][0]['experimentationRecovery'] = 'bad-number'
        write_json(self.bridge / 'experimental_repluralization_report.json', payload)
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'terrace_seed_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['experimentationRecovery'], 0.0)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'terrace_seed_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


if __name__ == '__main__':
    unittest.main()
