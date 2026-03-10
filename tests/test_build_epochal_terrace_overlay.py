from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_epochal_terrace_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class EpochalTerraceOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-bf.0', 'producerCommits': ['bf123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'epochal_terrace_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'et-1', 'epochalTerraceAuditState': 'verified'}]})
        write_json(self.bridge / 'epochal_terrace_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'et-1', 'targetPublisherAction': 'docket'},
            {'reviewId': 'et-2', 'targetPublisherAction': 'watch'},
            {'reviewId': 'et-3', 'targetPublisherAction': 'suppressed'},
        ]})
        write_json(self.bridge / 'epochal_terrace_map.json', {'provenance': prov, 'entries': [
            {'reviewId': 'et-1', 'terraceStatus': 'stable', 'terraceClass': 'living'},
            {'reviewId': 'et-2', 'terraceStatus': 'watch', 'terraceClass': 'transitional'},
        ]})
        write_json(self.bridge / 'stability_plateau_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'et-1', 'plateauClass': 'bounded', 'pluralityRetention': 'preserved', 'trustSurfaceStability': 'stable'},
            {'reviewId': 'et-2', 'plateauClass': 'fragile', 'pluralityRetention': 'bounded', 'trustSurfaceStability': 'volatile'},
        ]})
        write_json(self.bridge / 'institutional_sedimentation_registry.json', {'provenance': prov, 'entries': [
            {'reviewId': 'et-1', 'sedimentClass': 'layered', 'institutionalEmbedment': 0.65},
            {'reviewId': 'et-2', 'sedimentClass': 'contested', 'institutionalEmbedment': 0.42},
        ]})
        write_json(self.bridge / 'terrace_erosion_risk_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'et-1', 'erosionRisk': 'bounded', 'provenanceMarkers': ['prov:ok'], 'canonicalIntegrityMarkers': ['integrity:verified']},
            {'reviewId': 'et-2', 'erosionRisk': 'high', 'provenanceMarkers': ['prov:gap'], 'canonicalIntegrityMarkers': ['integrity:watch']},
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'delta_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'knowledge_river_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'trust_surface_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'value_dashboard.json', {**reg_prov, 'entries': []})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-bf-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'no epoch forever confirmation',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-bf.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--epochal-terrace-audit', str(self.bridge / 'epochal_terrace_audit.json'),
            '--epochal-terrace-recommendations', str(self.bridge / 'epochal_terrace_recommendations.json'),
            '--epochal-terrace-map', str(self.bridge / 'epochal_terrace_map.json'),
            '--stability-plateau-report', str(self.bridge / 'stability_plateau_report.json'),
            '--institutional-sedimentation-registry', str(self.bridge / 'institutional_sedimentation_registry.json'),
            '--terrace-erosion-risk-report', str(self.bridge / 'terrace_erosion_risk_report.json'),
            '--delta-dashboard', str(self.registry / 'delta_dashboard.json'),
            '--knowledge-river-dashboard', str(self.registry / 'knowledge_river_dashboard.json'),
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--trust-surface-dashboard', str(self.registry / 'trust_surface_dashboard.json'),
            '--value-dashboard', str(self.registry / 'value_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-epoch-dashboard', str(self.registry / 'epoch_dashboard.json'),
            '--out-plateau-registry', str(self.registry / 'plateau_registry.json'),
            '--out-terrace-watchlist', str(self.registry / 'terrace_watchlist.json'),
            '--out-epoch-annotations', str(self.registry / 'epoch_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'epoch_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'plateau_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'terrace_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['et-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['et-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['et-2'])

    def test_safeguard_flags_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        annotations = json.loads((self.registry / 'epoch_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(annotations['noCanonMutation'])
        self.assertTrue(annotations['noDeploymentExecution'])
        self.assertTrue(annotations['noGovernanceRightMutation'])
        self.assertTrue(annotations['noRankingOfCivilizationsCommunitiesInstitutionsTraditions'])
        self.assertTrue(annotations['terraceStabilityNotTruthAuthority'])
        self.assertTrue(annotations['noTheoryCompetitionClosure'])
        self.assertTrue(annotations['noEpochConfirmedForeverPresentation'])

    def test_provenance_validation_failure(self) -> None:
        payload = json.loads((self.bridge / 'epochal_terrace_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'epochal_terrace_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_numeric_fallback(self) -> None:
        payload = json.loads((self.bridge / 'institutional_sedimentation_registry.json').read_text(encoding='utf-8'))
        payload['entries'][0]['institutionalEmbedment'] = 'bad-number'
        write_json(self.bridge / 'institutional_sedimentation_registry.json', payload)
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'epoch_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['institutionalEmbedment'], 0.0)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'epoch_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


if __name__ == '__main__':
    unittest.main()
