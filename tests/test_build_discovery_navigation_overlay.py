from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_discovery_navigation_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class DiscoveryNavigationOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-ba.0', 'producerCommits': ['ba123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'discovery_navigation_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'dn-1', 'discoveryNavigationAuditState': 'verified'}]})
        write_json(self.bridge / 'discovery_navigation_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'dn-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x'], 'commonsReviewRequirement': 'required'},
            {'reviewId': 'dn-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y'], 'commonsReviewRequirement': 'required'},
            {'reviewId': 'dn-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
        ]})
        write_json(self.bridge / 'discovery_vector_field.json', {'provenance': prov, 'entries': [{'reviewId': 'dn-1', 'discoveryStatus': 'active', 'vectorClass': 'cross-domain'}]})
        write_json(self.bridge / 'cross_domain_bridge_map.json', {'provenance': prov, 'entries': [{'reviewId': 'dn-1', 'bridgeMaturity': 'emergent', 'bridgeConfidence': 0.67}]})
        write_json(self.bridge / 'entropy_reduction_corridor.json', {'provenance': prov, 'entries': [{'reviewId': 'dn-1', 'corridorClass': 'bounded', 'deadZoneAdjacency': 'adjacent', 'corridorScore': 0.58, 'altruisticCorridorScore': 0.64, 'conformityPenalty': 0.22, 'repairCorridorFlag': True, 'riverSeedPotential': 'high', 'riverFormationSignal': 'braiding', 'corridorWeavingScore': 0.61}]})
        write_json(self.bridge / 'discovery_navigation_report.json', {'provenance': prov, 'entries': [{'reviewId': 'dn-1', 'memorySupport': 'supported', 'commonsReviewRequirement': 'required', 'consentFeedbackFriction': 'low', 'multiscaleSupportClass': 'aligned', 'distortionRiskClass': 'bounded'}]})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-ba-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'no autonomous discovery authority',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-ba.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'knowledge_topology_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'operational_maturity_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'value_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--discovery-navigation-audit', str(self.bridge / 'discovery_navigation_audit.json'),
            '--discovery-navigation-recommendations', str(self.bridge / 'discovery_navigation_recommendations.json'),
            '--discovery-vector-field', str(self.bridge / 'discovery_vector_field.json'),
            '--cross-domain-bridge-map', str(self.bridge / 'cross_domain_bridge_map.json'),
            '--entropy-reduction-corridor', str(self.bridge / 'entropy_reduction_corridor.json'),
            '--discovery-navigation-report', str(self.bridge / 'discovery_navigation_report.json'),
            '--knowledge-topology-dashboard', str(self.registry / 'knowledge_topology_dashboard.json'),
            '--operational-maturity-dashboard', str(self.registry / 'operational_maturity_dashboard.json'),
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--value-dashboard', str(self.registry / 'value_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-discovery-navigation-dashboard', str(self.registry / 'discovery_navigation_dashboard.json'),
            '--out-discovery-corridor-registry', str(self.registry / 'discovery_corridor_registry.json'),
            '--out-discovery-risk-watchlist', str(self.registry / 'discovery_risk_watchlist.json'),
            '--out-discovery-annotations', str(self.registry / 'discovery_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'discovery_navigation_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'discovery_corridor_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'discovery_risk_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['dn-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['dn-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['dn-2'])

    def test_guardrails_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'discovery_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noAutonomousResearchExecution'))
        self.assertTrue(ann.get('noDeploymentExecution'))
        self.assertTrue(ann.get('noGovernanceRightsMutation'))
        self.assertTrue(ann.get('noCanonClosure'))
        self.assertTrue(ann.get('corridorPriorityNotTruthAuthority'))

    def test_invalid_numeric_values_default_to_zero(self) -> None:
        payload = json.loads((self.bridge / 'cross_domain_bridge_map.json').read_text(encoding='utf-8'))
        payload['entries'][0]['bridgeConfidence'] = 'bad-number'
        write_json(self.bridge / 'cross_domain_bridge_map.json', payload)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'discovery_navigation_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['bridgeConfidence'], 0.0)

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'discovery_navigation_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'discovery_navigation_audit.json', payload)

        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_canonical_integrity_propagates(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'discovery_navigation_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


    def test_ba1_field_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'discovery_navigation_dashboard.json').read_text(encoding='utf-8'))
        entry = dashboard['entries'][0]
        self.assertEqual(entry['riverSeedPotential'], 'high')
        self.assertEqual(entry['riverFormationSignal'], 'braiding')
        self.assertTrue(entry['repairCorridorFlag'])
        self.assertEqual(entry['distortionRiskClass'], 'bounded')

    def test_repair_corridor_presentation_flag(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        registry = json.loads((self.registry / 'discovery_corridor_registry.json').read_text(encoding='utf-8'))
        self.assertTrue(registry['entries'][0]['repairCorridorFlag'])

    def test_anti_distortion_annotation_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        annotations = json.loads((self.registry / 'discovery_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(annotations['annotations'][0]['antiDistortionSafeguardsRequired'])

    def test_missing_field_backwards_compatibility(self) -> None:
        payload = json.loads((self.bridge / 'entropy_reduction_corridor.json').read_text(encoding='utf-8'))
        for key in ['altruisticCorridorScore', 'conformityPenalty', 'repairCorridorFlag', 'riverSeedPotential', 'riverFormationSignal', 'corridorWeavingScore']:
            payload['entries'][0].pop(key, None)
        write_json(self.bridge / 'entropy_reduction_corridor.json', payload)

        report = json.loads((self.bridge / 'discovery_navigation_report.json').read_text(encoding='utf-8'))
        for key in ['consentFeedbackFriction', 'multiscaleSupportClass', 'distortionRiskClass']:
            report['entries'][0].pop(key, None)
        write_json(self.bridge / 'discovery_navigation_report.json', report)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'discovery_navigation_dashboard.json').read_text(encoding='utf-8'))
        entry = dashboard['entries'][0]
        self.assertEqual(entry['riverSeedPotential'], 'bounded')
        self.assertEqual(entry['riverFormationSignal'], 'emergent')
        self.assertFalse(entry['repairCorridorFlag'])
        self.assertEqual(entry['distortionRiskClass'], 'bounded')

if __name__ == '__main__':
    unittest.main()
