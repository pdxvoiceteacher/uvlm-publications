from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_successor_maturation_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class SuccessorMaturationOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-bi.0', 'producerCommits': ['bi123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'successor_maturation_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'sm-1', 'successorMaturationAuditState': 'verified'}]})
        write_json(self.bridge / 'successor_maturation_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'sm-1', 'targetPublisherAction': 'docket'},
            {'reviewId': 'sm-2', 'targetPublisherAction': 'watch'},
            {'reviewId': 'sm-3', 'targetPublisherAction': 'suppressed'},
        ]})
        write_json(self.bridge / 'successor_maturation_map.json', {'provenance': prov, 'entries': [
            {'reviewId': 'sm-1', 'maturationStatus': 'active', 'maturationClass': 'bounded'},
            {'reviewId': 'sm-2', 'maturationStatus': 'watch', 'maturationClass': 'fragile'},
        ]})
        write_json(self.bridge / 'false_future_risk_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'sm-1', 'falseFutureClass': 'bounded', 'successorCaptureRisk': 'bounded'},
            {'reviewId': 'sm-2', 'falseFutureClass': 'compressed', 'successorCaptureRisk': 'high'},
        ]})
        write_json(self.bridge / 'plurality_retention_scorecard.json', {'provenance': prov, 'entries': [
            {'reviewId': 'sm-1', 'pluralityRetentionClass': 'retained'},
            {'reviewId': 'sm-2', 'pluralityRetentionClass': 'bounded'},
        ]})
        write_json(self.bridge / 'maturation_gate_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'sm-1', 'gateStatus': 'review', 'trustLegibility': 'high', 'memoryContinuity': 'active', 'gateScore': 0.61, 'provenanceMarkers': ['prov:ok'], 'canonicalIntegrityMarkers': ['integrity:verified']},
            {'reviewId': 'sm-2', 'gateStatus': 'pending', 'trustLegibility': 'bounded', 'memoryContinuity': 'fragile', 'gateScore': 0.29, 'provenanceMarkers': ['prov:gap'], 'canonicalIntegrityMarkers': ['integrity:watch']},
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'renewal_braid_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'successor_delta_registry.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'terrace_health_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'epoch_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'delta_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'trust_surface_dashboard.json', {**reg_prov, 'entries': []})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-bi-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'no future secured declaration',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-bi.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--successor-maturation-audit', str(self.bridge / 'successor_maturation_audit.json'),
            '--successor-maturation-recommendations', str(self.bridge / 'successor_maturation_recommendations.json'),
            '--successor-maturation-map', str(self.bridge / 'successor_maturation_map.json'),
            '--false-future-risk-report', str(self.bridge / 'false_future_risk_report.json'),
            '--plurality-retention-scorecard', str(self.bridge / 'plurality_retention_scorecard.json'),
            '--maturation-gate-report', str(self.bridge / 'maturation_gate_report.json'),
            '--renewal-braid-dashboard', str(self.registry / 'renewal_braid_dashboard.json'),
            '--successor-delta-registry', str(self.registry / 'successor_delta_registry.json'),
            '--terrace-health-dashboard', str(self.registry / 'terrace_health_dashboard.json'),
            '--epoch-dashboard', str(self.registry / 'epoch_dashboard.json'),
            '--delta-dashboard', str(self.registry / 'delta_dashboard.json'),
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--trust-surface-dashboard', str(self.registry / 'trust_surface_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-successor-maturation-dashboard', str(self.registry / 'successor_maturation_dashboard.json'),
            '--out-false-future-watchlist', str(self.registry / 'false_future_watchlist.json'),
            '--out-plurality-retention-registry', str(self.registry / 'plurality_retention_registry.json'),
            '--out-future-annotations', str(self.registry / 'future_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'successor_maturation_dashboard.json').read_text(encoding='utf-8'))
        plurality = json.loads((self.registry / 'plurality_retention_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'false_future_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['sm-1'])
        self.assertEqual([e['reviewId'] for e in plurality['entries']], ['sm-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['sm-2'])

    def test_safeguard_flags_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'future_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann['noCanonMutation'])
        self.assertTrue(ann['noDeploymentExecution'])
        self.assertTrue(ann['noGovernanceRightMutation'])
        self.assertTrue(ann['noRankingOfFuturesSuccessorOrdersCivilizationsCommunitiesInstitutions'])
        self.assertTrue(ann['maturationVisibilityNotLegitimateAuthority'])
        self.assertTrue(ann['noTheoryCompetitionClosure'])
        self.assertTrue(ann['noNewAgeConfirmedOrFutureSecuredPresentation'])

    def test_provenance_validation_failure(self) -> None:
        payload = json.loads((self.bridge / 'successor_maturation_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'successor_maturation_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_numeric_fallback(self) -> None:
        payload = json.loads((self.bridge / 'maturation_gate_report.json').read_text(encoding='utf-8'))
        payload['entries'][0]['gateScore'] = 'bad-number'
        write_json(self.bridge / 'maturation_gate_report.json', payload)
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'successor_maturation_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['gateScore'], 0.0)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'successor_maturation_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


if __name__ == '__main__':
    unittest.main()
