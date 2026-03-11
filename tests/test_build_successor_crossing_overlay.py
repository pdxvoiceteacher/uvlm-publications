from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_successor_crossing_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class SuccessorCrossingOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-bj.0', 'producerCommits': ['bj123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'successor_crossing_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'sc-1', 'crossingAuditState': 'verified'}]})
        write_json(self.bridge / 'successor_crossing_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'sc-1', 'targetPublisherAction': 'docket'},
            {'reviewId': 'sc-2', 'targetPublisherAction': 'watch'},
            {'reviewId': 'sc-3', 'targetPublisherAction': 'suppressed'},
        ]})
        write_json(self.bridge / 'successor_crossing_map.json', {'provenance': prov, 'entries': [
            {'reviewId': 'sc-1', 'crossingStatus': 'under_review', 'crossingClass': 'threshold'},
            {'reviewId': 'sc-2', 'crossingStatus': 'monitor', 'crossingClass': 'bounded'},
        ]})
        write_json(self.bridge / 'false_future_decay_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'sc-1', 'decayClass': 'drift', 'captureExposure': 'low'},
            {'reviewId': 'sc-2', 'decayClass': 'coherence-loss', 'captureExposure': 'elevated'},
        ]})
        write_json(self.bridge / 'delta_crossing_gate.json', {'provenance': prov, 'entries': [
            {'reviewId': 'sc-1', 'gateStatus': 'review'},
            {'reviewId': 'sc-2', 'gateStatus': 'guarded'},
        ]})
        write_json(self.bridge / 'future_viability_forecast.json', {'provenance': prov, 'entries': [
            {'reviewId': 'sc-1', 'viabilityScore': 0.74, 'trustLegibility': 'high', 'memoryContinuity': 'strong', 'pluralityRetention': 'retained', 'provenanceMarkers': ['prov:ok'], 'canonicalIntegrityMarkers': ['integrity:verified']},
            {'reviewId': 'sc-2', 'viabilityScore': 0.22, 'trustLegibility': 'fragile', 'memoryContinuity': 'thin', 'pluralityRetention': 'bounded', 'provenanceMarkers': ['prov:gap'], 'canonicalIntegrityMarkers': ['integrity:watch']},
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'successor_maturation_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'false_future_watchlist.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'plurality_retention_registry.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'renewal_braid_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'terrace_health_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'epoch_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'delta_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'trust_surface_dashboard.json', {**reg_prov, 'entries': []})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-bj-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'crossing under review',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-bj.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--successor-crossing-audit', str(self.bridge / 'successor_crossing_audit.json'),
            '--successor-crossing-recommendations', str(self.bridge / 'successor_crossing_recommendations.json'),
            '--successor-crossing-map', str(self.bridge / 'successor_crossing_map.json'),
            '--false-future-decay-report', str(self.bridge / 'false_future_decay_report.json'),
            '--delta-crossing-gate', str(self.bridge / 'delta_crossing_gate.json'),
            '--future-viability-forecast', str(self.bridge / 'future_viability_forecast.json'),
            '--successor-maturation-dashboard', str(self.registry / 'successor_maturation_dashboard.json'),
            '--false-future-watchlist', str(self.registry / 'false_future_watchlist.json'),
            '--plurality-retention-registry', str(self.registry / 'plurality_retention_registry.json'),
            '--renewal-braid-dashboard', str(self.registry / 'renewal_braid_dashboard.json'),
            '--terrace-health-dashboard', str(self.registry / 'terrace_health_dashboard.json'),
            '--epoch-dashboard', str(self.registry / 'epoch_dashboard.json'),
            '--delta-dashboard', str(self.registry / 'delta_dashboard.json'),
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--trust-surface-dashboard', str(self.registry / 'trust_surface_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-successor-crossing-dashboard', str(self.registry / 'successor_crossing_dashboard.json'),
            '--out-false-future-decay-watchlist', str(self.registry / 'false_future_decay_watchlist.json'),
            '--out-delta-gate-registry', str(self.registry / 'delta_gate_registry.json'),
            '--out-future-crossing-annotations', str(self.registry / 'future_crossing_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'successor_crossing_dashboard.json').read_text(encoding='utf-8'))
        gates = json.loads((self.registry / 'delta_gate_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'false_future_decay_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['sc-1'])
        self.assertEqual([e['reviewId'] for e in gates['entries']], ['sc-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['sc-2'])

    def test_safeguard_flags_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'future_crossing_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann['noCanonMutation'])
        self.assertTrue(ann['noDeploymentExecution'])
        self.assertTrue(ann['noGovernanceRightMutation'])
        self.assertTrue(ann['noRankingOfFuturesSuccessorOrdersCivilizationsCommunitiesInstitutions'])
        self.assertTrue(ann['crossingVisibilityNotLegitimateAuthority'])
        self.assertTrue(ann['noTheoryCompetitionClosure'])
        self.assertTrue(ann['noNewAgeConfirmedOrFutureSecuredPresentation'])

    def test_provenance_validation_failure(self) -> None:
        payload = json.loads((self.bridge / 'successor_crossing_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'successor_crossing_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_numeric_fallback(self) -> None:
        payload = json.loads((self.bridge / 'future_viability_forecast.json').read_text(encoding='utf-8'))
        payload['entries'][0]['viabilityScore'] = 'bad-number'
        write_json(self.bridge / 'future_viability_forecast.json', payload)
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'successor_crossing_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['viabilityScore'], 0.0)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'successor_crossing_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


if __name__ == '__main__':
    unittest.main()
