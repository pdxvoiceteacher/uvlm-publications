from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_operationalization_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class OperationalizationOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-ax.0', 'producerCommits': ['ax123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'operationalization_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'op-1', 'operationalizationAuditState': 'verified'}]})
        write_json(self.bridge / 'operationalization_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'op-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x'], 'requiredSafeguards': ['human-review'], 'commonsReviewRequirement': 'required'},
            {'reviewId': 'op-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y'], 'requiredSafeguards': ['pause-gate'], 'commonsReviewRequirement': 'required'},
            {'reviewId': 'op-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
        ]})
        write_json(self.bridge / 'operational_maturity_map.json', {'provenance': prov, 'entries': [{'reviewId': 'op-1', 'operationalStatus': 'bounded-ready', 'maturityClass': 'field-tested', 'readinessScore': 0.71}]})
        write_json(self.bridge / 'deployment_boundary_report.json', {'provenance': prov, 'entries': [{'reviewId': 'op-1', 'deploymentReadiness': 'bounded', 'deadZoneAdjacency': 'adjacent'}]})
        write_json(self.bridge / 'translation_risk_register.json', {'provenance': prov, 'entries': [{'reviewId': 'op-1', 'translationRisk': 'medium', 'translationRiskScore': 0.44}]})
        write_json(self.bridge / 'operationalization_gate.json', {'provenance': prov, 'entries': [{'reviewId': 'op-1', 'requiredSafeguards': ['commons-review', 'human-oversight'], 'commonsReviewRequirement': 'required'}]})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-ax-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'no deployment authority',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-ax.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'knowledge_topology_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'emergent_domain_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'value_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--operationalization-audit', str(self.bridge / 'operationalization_audit.json'),
            '--operationalization-recommendations', str(self.bridge / 'operationalization_recommendations.json'),
            '--operational-maturity-map', str(self.bridge / 'operational_maturity_map.json'),
            '--deployment-boundary-report', str(self.bridge / 'deployment_boundary_report.json'),
            '--translation-risk-register', str(self.bridge / 'translation_risk_register.json'),
            '--operationalization-gate', str(self.bridge / 'operationalization_gate.json'),
            '--knowledge-topology-dashboard', str(self.registry / 'knowledge_topology_dashboard.json'),
            '--emergent-domain-dashboard', str(self.registry / 'emergent_domain_dashboard.json'),
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--value-dashboard', str(self.registry / 'value_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-operational-maturity-dashboard', str(self.registry / 'operational_maturity_dashboard.json'),
            '--out-deployment-boundary-registry', str(self.registry / 'deployment_boundary_registry.json'),
            '--out-translation-risk-watchlist', str(self.registry / 'translation_risk_watchlist.json'),
            '--out-operationalization-annotations', str(self.registry / 'operationalization_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'operational_maturity_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'deployment_boundary_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'translation_risk_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['op-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['op-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['op-2'])

    def test_guardrails_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'operationalization_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noDeploymentExecution'))
        self.assertTrue(ann.get('noPolicyEnactment'))
        self.assertTrue(ann.get('noGovernanceRightsMutation'))
        self.assertTrue(ann.get('noCanonClosure'))
        self.assertTrue(ann.get('scientificMaturityNotOperationalControlLicense'))

    def test_invalid_numeric_values_default_to_zero(self) -> None:
        payload = json.loads((self.bridge / 'operational_maturity_map.json').read_text(encoding='utf-8'))
        payload['entries'][0]['readinessScore'] = 'bad-number'
        write_json(self.bridge / 'operational_maturity_map.json', payload)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'operational_maturity_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['readinessScore'], 0.0)

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'operationalization_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'operationalization_audit.json', payload)

        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_canonical_integrity_propagates(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'operational_maturity_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


if __name__ == '__main__':
    unittest.main()
