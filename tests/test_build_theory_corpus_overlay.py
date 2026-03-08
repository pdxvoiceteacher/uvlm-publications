from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_theory_corpus_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class TheoryCorpusOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-ah.0', 'producerCommits': ['ah123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'theory_corpus_audit.json', {'provenance': prov, 'audits': [
            {'reviewId': 'th-1', 'theoryAuditState': 'verified'}
        ]})
        write_json(self.bridge / 'theory_corpus_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'th-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
            {'reviewId': 'th-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
            {'reviewId': 'th-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
        ]})
        write_json(self.bridge / 'theory_corpus_map.json', {'provenance': prov, 'entries': [
            {'reviewId': 'th-1', 'theoryStatus': 'provisional', 'falsificationStatus': 'tested', 'replicationStatus': 'replicated', 'competitionState': 'contested-leading'}
        ]})
        write_json(self.bridge / 'theory_revision_lineage.json', {'provenance': prov, 'entries': [
            {'reviewId': 'th-1', 'revisionLineage': ['v1', 'v2']}
        ]})
        write_json(self.bridge / 'negative_result_registry.json', {'provenance': prov, 'entries': [
            {'reviewId': 'th-1', 'negativeResultIndicators': ['failed-a']},
            {'reviewId': 'th-2', 'negativeResultIndicators': ['failed-b']}
        ]})
        write_json(self.bridge / 'theory_competition_report.json', {'provenance': prov, 'entries': [
            {'reviewId': 'th-1', 'competitionState': 'contested-leading', 'competitionPeers': ['theory:q']}
        ]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'experiment_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'prediction_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'branch_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--theory-corpus-audit', str(self.bridge / 'theory_corpus_audit.json'),
            '--theory-corpus-recommendations', str(self.bridge / 'theory_corpus_recommendations.json'),
            '--theory-corpus-map', str(self.bridge / 'theory_corpus_map.json'),
            '--theory-revision-lineage', str(self.bridge / 'theory_revision_lineage.json'),
            '--negative-result-registry', str(self.bridge / 'negative_result_registry.json'),
            '--theory-competition-report', str(self.bridge / 'theory_competition_report.json'),
            '--experiment-dashboard', str(self.registry / 'experiment_dashboard.json'),
            '--prediction-dashboard', str(self.registry / 'prediction_dashboard.json'),
            '--branch-dashboard', str(self.registry / 'branch_dashboard.json'),
            '--out-theory-dashboard', str(self.registry / 'theory_dashboard.json'),
            '--out-theory-registry', str(self.registry / 'theory_registry.json'),
            '--out-negative-result-watchlist', str(self.registry / 'negative_result_watchlist.json'),
            '--out-theory-annotations', str(self.registry / 'theory_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'theory_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'theory_registry.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'negative_result_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['th-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['th-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['th-2'])

    def test_non_mutation_guarantee(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'theory_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noAutomaticTheoryCertification'))
        self.assertTrue(ann.get('noCanonicalMutation'))

    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'theory_corpus_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'theory_corpus_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
