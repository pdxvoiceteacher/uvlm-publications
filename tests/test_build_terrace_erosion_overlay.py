from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_terrace_erosion_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class TerraceErosionOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-bg.0', 'producerCommits': ['bg123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'terrace_erosion_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'te-1', 'terraceErosionAuditState': 'verified'}]})
        write_json(self.bridge / 'terrace_erosion_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'te-1', 'targetPublisherAction': 'docket'},
            {'reviewId': 'te-2', 'targetPublisherAction': 'watch'},
            {'reviewId': 'te-3', 'targetPublisherAction': 'suppressed'},
        ]})
        write_json(self.bridge / 'terrace_erosion_map.json', {'provenance': prov, 'entries': [
            {'reviewId': 'te-1', 'erosionStatus': 'monitor', 'erosionClass': 'bounded'},
            {'reviewId': 'te-2', 'erosionStatus': 'watch', 'erosionClass': 'high'},
        ]})
        write_json(self.bridge / 'orthodoxy_pressure_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'te-1', 'orthodoxyClass': 'bounded'},
            {'reviewId': 'te-2', 'orthodoxyClass': 'rigid'},
        ]})
        write_json(self.bridge / 'renewal_corridor_registry.json', {'provenance': prov, 'entries': [
            {'reviewId': 'te-1', 'renewalClass': 'active'},
            {'reviewId': 'te-2', 'renewalClass': 'emergent'},
        ]})
        write_json(self.bridge / 'epochal_transition_forecast.json', {'provenance': prov, 'entries': [
            {'reviewId': 'te-1', 'pluralityCollapseRecovery': 'recovery', 'trustErosion': 'bounded', 'memoryReactivation': 'active', 'phaseTransitionLikelihood': 0.33, 'provenanceMarkers': ['prov:ok'], 'canonicalIntegrityMarkers': ['integrity:verified']},
            {'reviewId': 'te-2', 'pluralityCollapseRecovery': 'bounded', 'trustErosion': 'high', 'memoryReactivation': 'fragile', 'phaseTransitionLikelihood': 0.77, 'provenanceMarkers': ['prov:gap'], 'canonicalIntegrityMarkers': ['integrity:watch']},
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'epoch_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'delta_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'knowledge_river_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'trust_surface_dashboard.json', {**reg_prov, 'entries': []})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-bg-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'no collapse certainty',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-bg.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--terrace-erosion-audit', str(self.bridge / 'terrace_erosion_audit.json'),
            '--terrace-erosion-recommendations', str(self.bridge / 'terrace_erosion_recommendations.json'),
            '--terrace-erosion-map', str(self.bridge / 'terrace_erosion_map.json'),
            '--orthodoxy-pressure-report', str(self.bridge / 'orthodoxy_pressure_report.json'),
            '--renewal-corridor-registry', str(self.bridge / 'renewal_corridor_registry.json'),
            '--epochal-transition-forecast', str(self.bridge / 'epochal_transition_forecast.json'),
            '--epoch-dashboard', str(self.registry / 'epoch_dashboard.json'),
            '--delta-dashboard', str(self.registry / 'delta_dashboard.json'),
            '--knowledge-river-dashboard', str(self.registry / 'knowledge_river_dashboard.json'),
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--trust-surface-dashboard', str(self.registry / 'trust_surface_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-terrace-health-dashboard', str(self.registry / 'terrace_health_dashboard.json'),
            '--out-orthodoxy-watchlist', str(self.registry / 'orthodoxy_watchlist.json'),
            '--out-renewal-corridor-registry', str(self.registry / 'renewal_corridor_registry.json'),
            '--out-epoch-transition-annotations', str(self.registry / 'epoch_transition_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'terrace_health_dashboard.json').read_text(encoding='utf-8'))
        renewal = json.loads((self.registry / 'renewal_corridor_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'orthodoxy_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['te-1'])
        self.assertEqual([e['reviewId'] for e in renewal['entries']], ['te-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['te-2'])

    def test_safeguard_flags_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'epoch_transition_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann['noCanonMutation'])
        self.assertTrue(ann['noDeploymentExecution'])
        self.assertTrue(ann['noGovernanceRightMutation'])
        self.assertTrue(ann['noRankingOfCivilizationsInstitutionsSuccessorOrders'])
        self.assertTrue(ann['erosionNotCollapseCertainty'])
        self.assertTrue(ann['noNewAgeConfirmedPresentation'])
        self.assertTrue(ann['noTheoryCompetitionClosure'])

    def test_provenance_validation_failure(self) -> None:
        payload = json.loads((self.bridge / 'terrace_erosion_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'terrace_erosion_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_numeric_fallback(self) -> None:
        payload = json.loads((self.bridge / 'epochal_transition_forecast.json').read_text(encoding='utf-8'))
        payload['entries'][0]['phaseTransitionLikelihood'] = 'bad-number'
        write_json(self.bridge / 'epochal_transition_forecast.json', payload)
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'terrace_health_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['phaseTransitionLikelihood'], 0.0)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'terrace_health_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


if __name__ == '__main__':
    unittest.main()
