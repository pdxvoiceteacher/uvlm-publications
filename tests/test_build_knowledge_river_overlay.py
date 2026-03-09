from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_knowledge_river_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class KnowledgeRiverOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-bb.0', 'producerCommits': ['bb123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'knowledge_river_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'kr-1', 'knowledgeRiverAuditState': 'verified'}]})
        write_json(self.bridge / 'knowledge_river_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'kr-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:a']},
            {'reviewId': 'kr-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:b']},
            {'reviewId': 'kr-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:c']},
        ]})
        write_json(self.bridge / 'knowledge_river_map.json', {'provenance': prov, 'entries': [{'reviewId': 'kr-1', 'riverStatus': 'active', 'riverClass': 'braided'}]})
        write_json(self.bridge / 'corridor_braiding_report.json', {'provenance': prov, 'entries': [{'reviewId': 'kr-1', 'corridorWeavingScore': 0.74, 'braidStability': 'stable', 'multiscaleValidation': 'aligned', 'altruisticWeighting': 0.68}]})
        write_json(self.bridge / 'tributary_support_registry.json', {'provenance': prov, 'entries': [{'reviewId': 'kr-1', 'tributaryClass': 'supportive', 'memorySupport': 'strong'}]})
        write_json(self.bridge / 'river_capture_risk_report.json', {'provenance': prov, 'entries': [{'reviewId': 'kr-1', 'riverCaptureRisk': 'bounded', 'provenanceMarkers': ['chain:ok'], 'canonicalIntegrityMarkers': ['integrity:verified']}]})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-bb-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'no ranked prestige routing',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-bb.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'discovery_navigation_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'knowledge_topology_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'value_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--knowledge-river-audit', str(self.bridge / 'knowledge_river_audit.json'),
            '--knowledge-river-recommendations', str(self.bridge / 'knowledge_river_recommendations.json'),
            '--knowledge-river-map', str(self.bridge / 'knowledge_river_map.json'),
            '--corridor-braiding-report', str(self.bridge / 'corridor_braiding_report.json'),
            '--tributary-support-registry', str(self.bridge / 'tributary_support_registry.json'),
            '--river-capture-risk-report', str(self.bridge / 'river_capture_risk_report.json'),
            '--discovery-navigation-dashboard', str(self.registry / 'discovery_navigation_dashboard.json'),
            '--knowledge-topology-dashboard', str(self.registry / 'knowledge_topology_dashboard.json'),
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--value-dashboard', str(self.registry / 'value_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-knowledge-river-dashboard', str(self.registry / 'knowledge_river_dashboard.json'),
            '--out-river-registry', str(self.registry / 'river_registry.json'),
            '--out-river-capture-watchlist', str(self.registry / 'river_capture_watchlist.json'),
            '--out-river-annotations', str(self.registry / 'river_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_rules(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'knowledge_river_dashboard.json').read_text(encoding='utf-8'))
        river_registry = json.loads((self.registry / 'river_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'river_capture_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['kr-1'])
        self.assertEqual([e['reviewId'] for e in river_registry['entries']], ['kr-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['kr-2'])

    def test_safeguard_flags_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        annotations = json.loads((self.registry / 'river_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(annotations.get('noCanonMutation'))
        self.assertTrue(annotations.get('noDeploymentExecution'))
        self.assertTrue(annotations.get('noGovernanceRightsMutation'))
        self.assertTrue(annotations.get('noRankingOfPersonsCommunitiesInstitutionsTraditions'))
        self.assertTrue(annotations.get('riverMaturityNotTruthAuthority'))
        self.assertTrue(annotations.get('noTheoryCompetitionClosure'))

    def test_provenance_failure(self) -> None:
        payload = json.loads((self.bridge / 'knowledge_river_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'knowledge_river_audit.json', payload)

        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_numeric_fallback(self) -> None:
        payload = json.loads((self.bridge / 'corridor_braiding_report.json').read_text(encoding='utf-8'))
        payload['entries'][0]['corridorWeavingScore'] = 'bad-number'
        write_json(self.bridge / 'corridor_braiding_report.json', payload)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'knowledge_river_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['corridorWeavingScore'], 0.0)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'knowledge_river_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


if __name__ == '__main__':
    unittest.main()
