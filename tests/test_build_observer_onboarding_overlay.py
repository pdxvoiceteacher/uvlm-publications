from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_observer_onboarding_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class ObserverOnboardingOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-bc.0', 'producerCommits': ['bc123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'observer_onboarding_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'ob-1', 'observerOnboardingAuditState': 'verified'}]})
        write_json(self.bridge / 'observer_onboarding_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'ob-1', 'targetPublisherAction': 'docket', 'observerClass': 'guided'},
            {'reviewId': 'ob-2', 'targetPublisherAction': 'watch', 'observerClass': 'public'},
            {'reviewId': 'ob-3', 'targetPublisherAction': 'suppress', 'observerClass': 'witness'},
        ]})
        write_json(self.bridge / 'observer_class_map.json', {'provenance': prov, 'entries': [{'reviewId': 'ob-1', 'observerClass': 'guided'}]})
        write_json(self.bridge / 'visualization_readiness_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'ob-1', 'viewLegibility': 'high', 'guidedInterfaceRequired': True, 'translationSupportRequired': False, 'visualizationReadiness': 0.7, 'panelEligibility': ['summary', 'steward'], 'detailLevel': 'high', 'renderMode': 'provenance-rich', 'cognitiveLoadClass': 'medium', 'translationSupportRequirements': ['none']},
            {'reviewId': 'ob-2', 'viewLegibility': 'low', 'guidedInterfaceRequired': True, 'translationSupportRequired': True, 'visualizationReadiness': 0.2, 'panelEligibility': ['summary'], 'detailLevel': 'bounded', 'renderMode': 'public-summary', 'cognitiveLoadClass': 'low', 'translationSupportRequirements': ['translation']},
        ]})
        write_json(self.bridge / 'participatory_standing_registry.json', {'provenance': prov, 'entries': [
            {'reviewId': 'ob-1', 'participatoryStanding': 'bounded', 'suffrageReviewFlag': False, 'voteEligibilityBasis': 'bounded-review', 'revocationConditions': ['capture-risk-elevation']},
            {'reviewId': 'ob-2', 'participatoryStanding': 'review', 'suffrageReviewFlag': True},
            {'reviewId': 'ob-3', 'participatoryStanding': 'review', 'suffrageReviewFlag': True, 'witnessOnly': True},
        ]})
        write_json(self.bridge / 'onboarding_capture_risk_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'ob-1', 'captureRisk': 'bounded', 'provenanceMarkers': ['chain:ok'], 'canonicalIntegrityMarkers': ['integrity:verified']},
            {'reviewId': 'ob-2', 'captureRisk': 'high', 'provenanceMarkers': ['chain:gap'], 'canonicalIntegrityMarkers': ['integrity:watch']},
            {'reviewId': 'ob-3', 'captureRisk': 'elevated', 'provenanceMarkers': ['chain:watch'], 'canonicalIntegrityMarkers': ['integrity:watch']},
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'knowledge_river_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'river_capture_watchlist.json', {**reg_prov, 'entries': []})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-bc-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'no observer governance transfer',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-bc.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--observer-onboarding-audit', str(self.bridge / 'observer_onboarding_audit.json'),
            '--observer-onboarding-recommendations', str(self.bridge / 'observer_onboarding_recommendations.json'),
            '--observer-class-map', str(self.bridge / 'observer_class_map.json'),
            '--visualization-readiness-report', str(self.bridge / 'visualization_readiness_report.json'),
            '--participatory-standing-registry', str(self.bridge / 'participatory_standing_registry.json'),
            '--onboarding-capture-risk-report', str(self.bridge / 'onboarding_capture_risk_report.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--knowledge-river-dashboard', str(self.registry / 'knowledge_river_dashboard.json'),
            '--river-capture-watchlist', str(self.registry / 'river_capture_watchlist.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-observer-dashboard', str(self.registry / 'observer_dashboard.json'),
            '--out-visualization-registry', str(self.registry / 'visualization_registry.json'),
            '--out-onboarding-watchlist', str(self.registry / 'onboarding_watchlist.json'),
            '--out-participation-annotations', str(self.registry / 'participation_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_routing_behavior(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'observer_dashboard.json').read_text(encoding='utf-8'))
        visual = json.loads((self.registry / 'visualization_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'onboarding_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['ob-1'])
        self.assertEqual([e['reviewId'] for e in visual['entries']], ['ob-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['ob-2'])

    def test_safeguard_fields_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        annotations = json.loads((self.registry / 'participation_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(annotations.get('noGovernanceRightMutation'))
        self.assertTrue(annotations.get('noSovereignAuthorityAssignment'))
        self.assertTrue(annotations.get('noAutomaticWorthRanking'))
        self.assertTrue(annotations.get('noCoerciveNormalization'))
        self.assertTrue(annotations.get('noCanonClosure'))
        self.assertTrue(annotations.get('noHiddenMutationControls'))

    def test_numeric_and_string_fallback(self) -> None:
        payload = json.loads((self.bridge / 'visualization_readiness_report.json').read_text(encoding='utf-8'))
        payload['entries'][0]['visualizationReadiness'] = 'bad'
        payload['entries'][0]['viewLegibility'] = ''
        write_json(self.bridge / 'visualization_readiness_report.json', payload)
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'observer_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['visualizationReadiness'], 0.0)

    def test_provenance_validation_failure(self) -> None:
        payload = json.loads((self.bridge / 'observer_onboarding_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'observer_onboarding_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_canonical_integrity_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'observer_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])

    def test_visualization_mode_generation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        visual = json.loads((self.registry / 'visualization_registry.json').read_text(encoding='utf-8'))
        modes = [m['mode'] for m in visual['entries'][0]['visualizationModes']]
        self.assertIn('Sophia Internal', modes)
        self.assertIn('Human Steward', modes)
        self.assertIn('Human Public / Commons', modes)
        self.assertIn('Recognized/Guided Other-Intelligence View', modes)

    def test_annotation_presence_and_reset_safe_classes(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'participation_annotations.json').read_text(encoding='utf-8'))
        suppress_ann = next(e for e in ann['annotations'] if e['reviewId'] == 'ob-3')
        self.assertTrue(suppress_ann['witnessOnly'])
        self.assertIn('standing-review', suppress_ann['atlasClasses'])
        self.assertIn('capture-risk', suppress_ann['atlasClasses'])
        self.assertIn('observer-guided', ann['atlasResetRemovesClasses'])
        self.assertIn('trust-presentation-degraded', ann['atlasResetRemovesClasses'])


if __name__ == '__main__':
    unittest.main()
