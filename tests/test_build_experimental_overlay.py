from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_experimental_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class ExperimentalOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-ag.0', 'producerCommits': ['ag123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'experimental_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'ex-1', 'experimentalAuditState': 'verified'}]})
        write_json(self.bridge / 'experimental_recommendations.json', {'provenance': prov, 'recommendations': [
            {'reviewId': 'ex-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
            {'reviewId': 'ex-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
            {'reviewId': 'ex-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
        ]})
        write_json(self.bridge / 'experimental_hypothesis_map.json', {'provenance': prov, 'entries': [{'reviewId': 'ex-1', 'experimentalStatus': 'active-design', 'hypothesisClass': 'mechanistic'}]})
        write_json(self.bridge / 'falsification_design_report.json', {'provenance': prov, 'entries': [{'reviewId': 'ex-1', 'falsificationReadiness': 'ready', 'falsificationPlan': ['probe']}]})
        write_json(self.bridge / 'replication_pathway_map.json', {'provenance': prov, 'entries': [{'reviewId': 'ex-1', 'replicationPathwayStatus': 'defined', 'replicationPathways': ['path-1']}]})
        write_json(self.bridge / 'theory_promotion_gate.json', {'provenance': prov, 'entries': [{'reviewId': 'ex-1', 'theoryGateClass': 'hold', 'theoryGateReason': 'human-ratification-required'}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'prediction_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'branch_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'authority_gate_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--experimental-audit', str(self.bridge / 'experimental_audit.json'),
            '--experimental-recommendations', str(self.bridge / 'experimental_recommendations.json'),
            '--experimental-hypothesis-map', str(self.bridge / 'experimental_hypothesis_map.json'),
            '--falsification-design-report', str(self.bridge / 'falsification_design_report.json'),
            '--replication-pathway-map', str(self.bridge / 'replication_pathway_map.json'),
            '--theory-promotion-gate', str(self.bridge / 'theory_promotion_gate.json'),
            '--prediction-dashboard', str(self.registry / 'prediction_dashboard.json'),
            '--branch-dashboard', str(self.registry / 'branch_dashboard.json'),
            '--authority-gate-dashboard', str(self.registry / 'authority_gate_dashboard.json'),
            '--out-experiment-dashboard', str(self.registry / 'experiment_dashboard.json'),
            '--out-hypothesis-registry', str(self.registry / 'hypothesis_registry.json'),
            '--out-falsification-watchlist', str(self.registry / 'falsification_watchlist.json'),
            '--out-theory-gate-annotations', str(self.registry / 'theory_gate_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'experiment_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'hypothesis_registry.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'falsification_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['ex-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['ex-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['ex-2'])

    def test_non_mutation_guarantee(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        ann = json.loads((self.registry / 'theory_gate_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(ann.get('noAutomaticTheoryPromotion'))
        self.assertTrue(ann.get('noCanonicalMutation'))


    def test_empty_provenance_commit_list_fails(self) -> None:
        payload = json.loads((self.bridge / 'experimental_audit.json').read_text(encoding='utf-8'))
        payload['provenance']['producerCommits'] = []
        write_json(self.bridge / 'experimental_audit.json', payload)
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be a non-empty list of non-empty strings', result.stdout + result.stderr)

    def test_missing_required_input_fails(self) -> None:
        (self.bridge / 'theory_promotion_gate.json').unlink()
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Missing required canonical artifact', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
