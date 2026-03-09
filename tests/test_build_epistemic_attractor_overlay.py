from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_epistemic_attractor_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class EpistemicAttractorOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-aw.0', 'producerCommits': ['aw123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'epistemic_attractor_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'ea-1', 'epistemicAttractorAuditState': 'verified'}]})
        write_json(self.bridge / 'epistemic_attractor_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'ea-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x'], 'memoryRetentionStrength': 'strong'},
            {'reviewId': 'ea-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y'], 'memoryRetentionStrength': 'bounded'},
            {'reviewId': 'ea-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z'], 'memoryRetentionStrength': 'hold'},
        ]})
        write_json(self.bridge / 'epistemic_attractor_map.json', {'provenance': prov, 'entries': [{'reviewId': 'ea-1', 'epistemicStatus': 'stable', 'attractorClass': 'convergent'}]})
        write_json(self.bridge / 'knowledge_basin_registry.json', {'provenance': prov, 'entries': [{'reviewId': 'ea-1', 'basinClass': 'deep'}]})
        write_json(self.bridge / 'dead_zone_report.json', {'provenance': prov, 'entries': [{'reviewId': 'ea-1', 'deadZoneRecurrence': 'watch'}]})
        write_json(self.bridge / 'paradigm_shift_forecast.json', {'provenance': prov, 'entries': [{'reviewId': 'ea-1', 'paradigmShiftForecast': 'rising', 'shiftProbability': 0.73}]})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-aw-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'no final truth claims',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-aw.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'emergent_domain_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civilizational_memory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'value_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--epistemic-attractor-audit', str(self.bridge / 'epistemic_attractor_audit.json'),
            '--epistemic-attractor-recommendations', str(self.bridge / 'epistemic_attractor_recommendations.json'),
            '--epistemic-attractor-map', str(self.bridge / 'epistemic_attractor_map.json'),
            '--knowledge-basin-registry', str(self.bridge / 'knowledge_basin_registry.json'),
            '--dead-zone-report', str(self.bridge / 'dead_zone_report.json'),
            '--paradigm-shift-forecast', str(self.bridge / 'paradigm_shift_forecast.json'),
            '--emergent-domain-dashboard', str(self.registry / 'emergent_domain_dashboard.json'),
            '--civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--value-dashboard', str(self.registry / 'value_dashboard.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-knowledge-topology-dashboard', str(self.registry / 'knowledge_topology_dashboard.json'),
            '--out-attractor-registry', str(self.registry / 'attractor_registry.json'),
            '--out-dead-zone-watchlist', str(self.registry / 'dead_zone_watchlist.json'),
            '--out-paradigm-shift-annotations', str(self.registry / 'paradigm_shift_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'knowledge_topology_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'attractor_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'dead_zone_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['ea-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['ea-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['ea-2'])

    def test_guardrails_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'paradigm_shift_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noCanonMutation'))
        self.assertTrue(ann.get('noRankingOfPersonsCommunitiesTraditions'))
        self.assertTrue(ann.get('noTheoryCompetitionClosure'))
        self.assertTrue(ann.get('noGovernanceRightsMutation'))
        self.assertTrue(ann.get('noFinalTruthClaims'))

    def test_invalid_numeric_values_default_to_zero(self) -> None:
        payload = json.loads((self.bridge / 'paradigm_shift_forecast.json').read_text(encoding='utf-8'))
        payload['entries'][0]['shiftProbability'] = 'bad-number'
        write_json(self.bridge / 'paradigm_shift_forecast.json', payload)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'knowledge_topology_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['shiftProbability'], 0.0)

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'epistemic_attractor_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'epistemic_attractor_audit.json', payload)

        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_canonical_integrity_propagates(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'knowledge_topology_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


if __name__ == '__main__':
    unittest.main()
