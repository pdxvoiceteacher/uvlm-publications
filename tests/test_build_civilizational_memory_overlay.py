from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.canonical_integrity_manifest import compute_constraint_signature_sha256

SCRIPT = Path('scripts/build_civilizational_memory_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class CivilizationalMemoryOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-av.0', 'producerCommits': ['av123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'civilizational_memory_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'cm-1', 'civilizationalMemoryAuditState': 'verified'}]})
        write_json(self.bridge / 'civilizational_memory_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'cm-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x'], 'preservationCriticality': 'high'},
            {'reviewId': 'cm-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y'], 'preservationCriticality': 'monitor'},
            {'reviewId': 'cm-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z'], 'preservationCriticality': 'hold'},
        ]})
        write_json(self.bridge / 'civilizational_memory_map.json', {'provenance': prov, 'entries': [{'reviewId': 'cm-1', 'memoryStatus': 'active', 'preservationCriticality': 'high'}]})
        write_json(self.bridge / 'intergenerational_legibility_report.json', {'provenance': prov, 'entries': [{'reviewId': 'cm-1', 'legibilityPersistence': 'durable'}]})
        write_json(self.bridge / 'epistemic_resilience_scorecard.json', {'provenance': prov, 'entries': [{'reviewId': 'cm-1', 'recoverability': 'strong', 'custodyDiversity': 'high', 'epistemicResilienceScore': 0.82}]})
        write_json(self.bridge / 'memory_fragility_report.json', {'provenance': prov, 'entries': [{'reviewId': 'cm-1', 'vocabularyDriftRisk': 'watch', 'notationFragility': 'bounded'}]})

        manifest = {
            'originProject': 'uvlm-publications',
            'canonicalPhaselock': 'phase-av-lock',
            'modificationDisclosureRequired': True,
            'ethicalBoundaryNotice': 'no canon mutation',
            'commonsIntegrityNotice': 'provenance required',
            'constraintSignatureVersion': 'phase-av.integrity.v1',
        }
        manifest['constraintSignatureSha256'] = compute_constraint_signature_sha256(manifest)
        write_json(self.bridge / 'canonical_integrity_manifest.json', manifest)
        write_json(self.registry / 'canonical_integrity_manifest.json', manifest)

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'theory_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'commons_sovereignty_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'civic_literacy_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'knowledge_priority_registry.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--civilizational-memory-audit', str(self.bridge / 'civilizational_memory_audit.json'),
            '--civilizational-memory-recommendations', str(self.bridge / 'civilizational_memory_recommendations.json'),
            '--civilizational-memory-map', str(self.bridge / 'civilizational_memory_map.json'),
            '--intergenerational-legibility-report', str(self.bridge / 'intergenerational_legibility_report.json'),
            '--epistemic-resilience-scorecard', str(self.bridge / 'epistemic_resilience_scorecard.json'),
            '--memory-fragility-report', str(self.bridge / 'memory_fragility_report.json'),
            '--theory-dashboard', str(self.registry / 'theory_dashboard.json'),
            '--commons-sovereignty-dashboard', str(self.registry / 'commons_sovereignty_dashboard.json'),
            '--civic-literacy-dashboard', str(self.registry / 'civic_literacy_dashboard.json'),
            '--knowledge-priority-registry', str(self.registry / 'knowledge_priority_registry.json'),
            '--bridge-canonical-integrity-manifest', str(self.bridge / 'canonical_integrity_manifest.json'),
            '--registry-canonical-integrity-manifest', str(self.registry / 'canonical_integrity_manifest.json'),
            '--out-civilizational-memory-dashboard', str(self.registry / 'civilizational_memory_dashboard.json'),
            '--out-epistemic-resilience-registry', str(self.registry / 'epistemic_resilience_registry.json'),
            '--out-memory-fragility-watchlist', str(self.registry / 'memory_fragility_watchlist.json'),
            '--out-civilizational-memory-annotations', str(self.registry / 'civilizational_memory_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'civilizational_memory_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'epistemic_resilience_registry.json').read_text(encoding='utf-8'))
        watch = json.loads((self.registry / 'memory_fragility_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['cm-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['cm-1'])
        self.assertEqual([e['reviewId'] for e in watch['entries']], ['cm-2'])

    def test_guardrails_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'civilizational_memory_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noCanonMutation'))
        self.assertTrue(ann.get('noCommunityOrTraditionRanking'))
        self.assertTrue(ann.get('noNegativeResultSuppression'))
        self.assertTrue(ann.get('noAutomaticTheoryCompetitionClosure'))
        self.assertTrue(ann.get('noGovernanceRightsMutation'))

    def test_invalid_numeric_values_default_to_zero(self) -> None:
        payload = json.loads((self.bridge / 'epistemic_resilience_scorecard.json').read_text(encoding='utf-8'))
        payload['entries'][0]['epistemicResilienceScore'] = 'bad-number'
        write_json(self.bridge / 'epistemic_resilience_scorecard.json', payload)

        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'civilizational_memory_dashboard.json').read_text(encoding='utf-8'))
        self.assertEqual(dashboard['entries'][0]['epistemicResilienceScore'], 0.0)

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'civilizational_memory_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'civilizational_memory_audit.json', payload)

        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_canonical_integrity_propagates(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'civilizational_memory_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(dashboard['canonicalIntegrityVerified'])
        self.assertFalse(dashboard['modificationDisclosureMissing'])
        self.assertFalse(dashboard['trustPresentationDegraded'])


if __name__ == '__main__':
    unittest.main()
