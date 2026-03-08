from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_collaborative_review_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class CollaborativeReviewOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-ac.0', 'producerCommits': ['ac123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'collaborative_review_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'cr-1', 'collaborativeAuditState': 'verified'}]})
        write_json(self.bridge / 'collaborative_review_recommendations.json', {
            'provenance': prov,
            'recommendations': [
                {'reviewId': 'cr-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x']},
                {'reviewId': 'cr-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
                {'reviewId': 'cr-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
            ],
        })
        write_json(self.bridge / 'reviewer_deliberation_map.json', {'provenance': prov, 'entries': [{'reviewId': 'cr-1', 'collaborativeStatus': 'active-deliberation'}]})
        write_json(self.bridge / 'reviewer_position_map.json', {'provenance': prov, 'entries': [{'reviewId': 'cr-1', 'maturityConstraints': ['bounded-claiming'], 'reviewerPositions': ['support', 'qualified-support']}]})
        write_json(self.bridge / 'consensus_state_report.json', {'provenance': prov, 'entries': [{'reviewId': 'cr-1', 'consensusClass': 'provisional-consensus'}]})
        write_json(self.bridge / 'dissent_trace_report.json', {'provenance': prov, 'entries': [{'reviewId': 'cr-2', 'dissentPresent': True, 'dissentTraceCount': 2}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'review_packet_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'causal_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'authority_gate_dashboard.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--collaborative-review-audit', str(self.bridge / 'collaborative_review_audit.json'),
            '--collaborative-review-recommendations', str(self.bridge / 'collaborative_review_recommendations.json'),
            '--reviewer-deliberation-map', str(self.bridge / 'reviewer_deliberation_map.json'),
            '--reviewer-position-map', str(self.bridge / 'reviewer_position_map.json'),
            '--consensus-state-report', str(self.bridge / 'consensus_state_report.json'),
            '--dissent-trace-report', str(self.bridge / 'dissent_trace_report.json'),
            '--review-packet-dashboard', str(self.registry / 'review_packet_dashboard.json'),
            '--causal-dashboard', str(self.registry / 'causal_dashboard.json'),
            '--authority-gate-dashboard', str(self.registry / 'authority_gate_dashboard.json'),
            '--out-collaborative-review-dashboard', str(self.registry / 'collaborative_review_dashboard.json'),
            '--out-consensus-registry', str(self.registry / 'consensus_registry.json'),
            '--out-dissent-watchlist', str(self.registry / 'dissent_watchlist.json'),
            '--out-deliberation-annotations', str(self.registry / 'deliberation_annotations.json'),
        ]
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'collaborative_review_dashboard.json').read_text(encoding='utf-8'))
        registry = json.loads((self.registry / 'consensus_registry.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'dissent_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['cr-1'])
        self.assertEqual([e['reviewId'] for e in registry['entries']], ['cr-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['cr-2'])

    def test_non_mutation_guarantees(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        payload = json.loads((self.registry / 'deliberation_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(payload.get('noAutomaticConsensusRatification'))
        self.assertTrue(payload.get('noAutomaticDissentSuppression'))
        self.assertTrue(payload.get('noCanonicalMutation'))

    def test_required_artifact_validation(self) -> None:
        (self.bridge / 'dissent_trace_report.json').unlink()
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Missing required canonical artifact', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
