from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_civilizational_delta_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class CivilizationalDeltaOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-be.0', 'producerCommits': ['be123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'civilizational_delta_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'cd-1', 'civilizationalDeltaAuditState': 'verified'}]})
        write_json(self.bridge / 'civilizational_delta_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'cd-1', 'targetPublisherAction': 'docket'},
            {'reviewId': 'cd-2', 'targetPublisherAction': 'watch'},
            {'reviewId': 'cd-3', 'targetPublisherAction': 'suppressed'},
        ]})
        write_json(self.bridge / 'delta_seed_map.json', {'provenance': prov, 'entries': [
            {'reviewId': 'cd-1', 'deltaStatus': 'active', 'deltaSeedClass': 'seeded'},
            {'reviewId': 'cd-2', 'deltaStatus': 'monitor', 'deltaSeedClass': 'candidate'},
        ]})
        write_json(self.bridge / 'paradigm_convergence_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'cd-1', 'convergenceClass': 'convergent', 'riverBraidingDensity': 0.71},
            {'reviewId': 'cd-2', 'convergenceClass': 'branching', 'riverBraidingDensity': 0.32},
        ]})
        write_json(self.bridge / 'epistemic_reorganization_signal.json', {'provenance': prov, 'entries': [
            {'reviewId': 'cd-1', 'reorganizationClass': 'bounded'},
            {'reviewId': 'cd-2', 'reorganizationClass': 'dynamic'},
        ]})
        write_json(self.bridge / 'civilizational_delta_forecast.json', {'provenance': prov, 'entries': [
            {'reviewId': 'cd-1', 'memorySupport': 'supported', 'distributaryPotential': 'high', 'trustSurfaceStability': 'stable', 'pluralityPreservation': 'preserved', 'captureRisk': 'bounded', 'provenanceMarkers': ['prov:ok'], 'canonicalIntegrityMarkers': ['integrity:verified']},
            {'reviewId': 'cd-2', 'memorySupport': 'bounded', 'distributaryPotential': 'medium', 'trustSurfaceStability': 'fragile', 'pluralityPreservation': 'bounded', 'captureRisk': 'high', 'provenanceMarkers': ['prov:gap'], 'canonicalIntegrityMarkers': ['integrity:watch']},
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'knowledge_river_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'discovery_navigation_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'trust_surface_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'value_dashboard.json', {**reg_prov, 'entries': []})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-be-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'no epoch confirmation',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-be.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--civilizational-delta-audit', str(self.bridge / 'civilizational_delta_audit.json'),
            '--civilizational-delta-recommendations', str(self.bridge / 'civilizational_delta_recommendations.json'),
            '--delta-seed-map', str(self.bridge / 'delta_seed_map.json'),
            '--paradigm-convergence-report', str(self.bridge / 'paradigm_convergence_report.json'),
            '--epistemic-reorganization-signal', str(self.bridge / 'epistemic_reorganization_signal.json'),
            '--civilizational-delta-forecast', str(self.bridge / 'civilizational_delta_forecast.json'),
            '--knowledge-river-dashboard', str(self.registry / 'knowledge_river_dashboard.json'),
            '--discovery-navigation-dashboard', str(self.registry / 'discovery_navigation_dashboard.json'),
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--trust-surface-dashboard', str(self.registry / 'trust_surface_dashboard.json'),
            '--value-dashboard', str(self.registry / 'value_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-delta-dashboard', str(self.registry / 'delta_dashboard.json'),
            '--out-paradigm-transition-registry', str(self.registry / 'paradigm_transition_registry.json'),
            '--out-epoch-shift-watchlist', str(self.registry / 'epoch_shift_watchlist.json'),
            '--out-delta-annotations', str(self.registry / 'delta_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'delta_dashboard.json').read_text(encoding='utf-8'))
        transition = json.loads((self.registry / 'paradigm_transition_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'epoch_shift_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['cd-1'])
        self.assertEqual([e['reviewId'] for e in transition['entries']], ['cd-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['cd-2'])

    def test_safeguard_flags_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'delta_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann['noCanonMutation'])
        self.assertTrue(ann['noDeploymentExecution'])
        self.assertTrue(ann['noGovernanceRightMutation'])
        self.assertTrue(ann['noRankingOfPersonsCommunitiesInstitutionsCivilizations'])
        self.assertTrue(ann['deltaMaturityNotTruthAuthority'])
        self.assertTrue(ann['noTheoryCompetitionClosure'])
        self.assertTrue(ann['noEpochConfirmedPresentation'])

    def test_provenance_validation_failure(self) -> None:
        payload = json.loads((self.bridge / 'civilizational_delta_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'civilizational_delta_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_numeric_fallback(self) -> None:
        payload = json.loads((self.bridge / 'paradigm_convergence_report.json').read_text(encoding='utf-8'))
        payload['entries'][0]['riverBraidingDensity'] = 'bad-number'
        write_json(self.bridge / 'paradigm_convergence_report.json', payload)
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'delta_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['riverBraidingDensity'], 0.0)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'delta_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


if __name__ == '__main__':
    unittest.main()
