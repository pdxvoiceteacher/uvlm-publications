from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_new_delta_stabilization_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class NewDeltaStabilizationOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-bk.0', 'producerCommits': ['bk123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'new_delta_stabilization_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'bk-1', 'stabilizationAuditState': 'verified'}]})
        write_json(self.bridge / 'new_delta_stabilization_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'bk-1', 'targetPublisherAction': 'docket'},
            {'reviewId': 'bk-2', 'targetPublisherAction': 'watch'},
            {'reviewId': 'bk-3', 'targetPublisherAction': 'suppressed'},
        ]})
        write_json(self.bridge / 'new_delta_stabilization_map.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bk-1', 'stabilizationStatus': 'under_review', 'stabilizationClass': 'durable'},
            {'reviewId': 'bk-2', 'stabilizationStatus': 'monitor', 'stabilizationClass': 'bounded'},
        ]})
        write_json(self.bridge / 'fragmented_renewal_reversion_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bk-1', 'reversionClass': 'fragmented', 'renewalScatter': 0.18},
            {'reviewId': 'bk-2', 'reversionClass': 'scatter', 'renewalScatter': 0.73},
        ]})
        write_json(self.bridge / 'crossing_resilience_scorecard.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bk-1', 'resilienceClass': 'guarded', 'trustLegibility': 'high', 'memoryContinuity': 'strong', 'pluralityRetention': 'retained', 'provenanceMarkers': ['prov:ok'], 'canonicalIntegrityMarkers': ['integrity:verified']},
            {'reviewId': 'bk-2', 'resilienceClass': 'stressed', 'trustLegibility': 'fragile', 'memoryContinuity': 'thin', 'pluralityRetention': 'bounded', 'provenanceMarkers': ['prov:gap'], 'canonicalIntegrityMarkers': ['integrity:watch']},
        ]})
        write_json(self.bridge / 'post_crossing_governance_gate.json', {'provenance': prov, 'entries': [
            {'reviewId': 'bk-1', 'gateStatus': 'review'},
            {'reviewId': 'bk-2', 'gateStatus': 'guarded'},
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'successor_crossing_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'false_future_decay_watchlist.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'delta_gate_registry.json', {**reg_prov, 'entries': []})
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
            'canonicalPhaselock': 'phase-bk-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'stabilization under review',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-bk.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--new-delta-stabilization-audit', str(self.bridge / 'new_delta_stabilization_audit.json'),
            '--new-delta-stabilization-recommendations', str(self.bridge / 'new_delta_stabilization_recommendations.json'),
            '--new-delta-stabilization-map', str(self.bridge / 'new_delta_stabilization_map.json'),
            '--fragmented-renewal-reversion-report', str(self.bridge / 'fragmented_renewal_reversion_report.json'),
            '--crossing-resilience-scorecard', str(self.bridge / 'crossing_resilience_scorecard.json'),
            '--post-crossing-governance-gate', str(self.bridge / 'post_crossing_governance_gate.json'),
            '--successor-crossing-dashboard', str(self.registry / 'successor_crossing_dashboard.json'),
            '--false-future-decay-watchlist', str(self.registry / 'false_future_decay_watchlist.json'),
            '--delta-gate-registry', str(self.registry / 'delta_gate_registry.json'),
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
            '--out-new-delta-dashboard', str(self.registry / 'new_delta_dashboard.json'),
            '--out-reversion-watchlist', str(self.registry / 'reversion_watchlist.json'),
            '--out-crossing-resilience-registry', str(self.registry / 'crossing_resilience_registry.json'),
            '--out-post-crossing-annotations', str(self.registry / 'post_crossing_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'new_delta_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'crossing_resilience_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'reversion_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['bk-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['bk-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['bk-2'])

    def test_safeguard_flags_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'post_crossing_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann['noCanonMutation'])
        self.assertTrue(ann['noDeploymentExecution'])
        self.assertTrue(ann['noGovernanceRightMutation'])
        self.assertTrue(ann['noRankingOfFuturesSuccessorOrdersCivilizationsCommunitiesInstitutions'])
        self.assertTrue(ann['stabilizationVisibilityNotLegitimateAuthority'])
        self.assertTrue(ann['noTheoryCompetitionClosure'])
        self.assertTrue(ann['noNewAgeConfirmedOrFutureSecuredPermanentlyPresentation'])

    def test_provenance_validation_failure(self) -> None:
        payload = json.loads((self.bridge / 'new_delta_stabilization_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'new_delta_stabilization_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_numeric_fallback(self) -> None:
        payload = json.loads((self.bridge / 'fragmented_renewal_reversion_report.json').read_text(encoding='utf-8'))
        payload['entries'][0]['renewalScatter'] = 'bad-number'
        write_json(self.bridge / 'fragmented_renewal_reversion_report.json', payload)
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'new_delta_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['renewalScatter'], 0.0)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'new_delta_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


if __name__ == '__main__':
    unittest.main()
