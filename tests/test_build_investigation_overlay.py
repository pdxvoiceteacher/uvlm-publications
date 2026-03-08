from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_investigation_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class InvestigationOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-v.0', 'producerCommits': ['v123'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'triage_recommendations.json', {
            'provenance': prov,
            'recommendations': [
                {'reviewId': 'iv-001', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x'], 'investigationStage': 'intake'}
            ],
        })
        write_json(self.bridge / 'verification_recommendations.json', {
            'provenance': prov,
            'recommendations': [
                {'reviewId': 'iv-002', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:x'], 'investigationStage': 'verification'}
            ],
        })
        write_json(self.bridge / 'public_record_recommendations.json', {
            'provenance': prov,
            'recommendations': [
                {'reviewId': 'iv-003', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:y'], 'investigationStage': 'dependency-mapping'}
            ],
        })
        write_json(self.bridge / 'artifact_escrow_plan.json', {
            'entries': [
                {'artifactId': 'registry/knowledge_graph.json', 'escrowStatus': 'ready-for-review', 'dependencyPaths': ['registry/catalog.json']},
                {'artifactId': 'registry/atlas_timeline.json', 'escrowStatus': 'pending', 'dependencyPaths': ['registry/knowledge_graph.json']},
            ]
        })

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self, extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--triage-recommendations', str(self.bridge / 'triage_recommendations.json'),
            '--verification-recommendations', str(self.bridge / 'verification_recommendations.json'),
            '--public-record-recommendations', str(self.bridge / 'public_record_recommendations.json'),
            '--artifact-escrow-plan', str(self.bridge / 'artifact_escrow_plan.json'),
            '--out-investigation-dashboard', str(self.registry / 'investigation_dashboard.json'),
            '--out-investigation-plan-registry', str(self.registry / 'investigation_plan_registry.json'),
            '--out-investigation-watchlist', str(self.registry / 'investigation_watchlist.json'),
            '--out-investigation-annotations', str(self.registry / 'investigation_annotations.json'),
        ]
        if extra:
            cmd.extend(extra)
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_canonical_artifact_name_usage(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_deprecated_name_rejection(self) -> None:
        result = self.run_builder(['--investigation-snapshot', str(self.bridge / 'investigation_snapshot.json')])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Deprecated artifact alias', result.stdout + result.stderr)

    def test_dependency_graph_present(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'investigation_dashboard.json').read_text(encoding='utf-8'))
        self.assertTrue(payload['entries'])
        self.assertIn('dependencyGraph', payload['entries'][0])
        self.assertGreaterEqual(len(payload['entries'][0]['dependencyGraph']['edges']), 1)

    def test_missing_upstream_artifact_failure(self) -> None:
        (self.bridge / 'triage_recommendations.json').unlink()
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Missing required canonical artifact', result.stdout + result.stderr)

    def test_non_mutation_guarantee_preserved(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'investigation_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(payload.get('noCanonicalMutation'))
        self.assertTrue(payload.get('noAutomaticAccusation'))
        self.assertTrue(payload.get('noAutomaticPlanMutation'))


if __name__ == '__main__':
    unittest.main()
