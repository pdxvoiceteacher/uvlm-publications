from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_institutional_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class InstitutionalOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        provenance = {
            'schemaVersion': 'phase-p.1',
            'producerCommits': ['abc1234'],
            'sourceMode': 'fixture',
        }

        write_json(self.bridge / 'institutional_audit.json', {
            'provenance': provenance,
            'audits': [{'reviewId': 'inst-001', 'watchState': 'none'}],
        })
        write_json(self.bridge / 'institutional_recommendations.json', {
            'provenance': provenance,
            'recommendations': [{
                'reviewId': 'inst-001',
                'institutionId': 'institution-001',
                'targetPublisherAction': 'docket',
                'linkedTargetIds': ['concept:x'],
            }],
        })
        write_json(self.bridge / 'institutional_state_map.json', {
            'provenance': provenance,
            'entries': [{'reviewId': 'inst-001', 'institutionalStatus': 'stable', 'chamberConflictLevel': 'low'}],
        })
        write_json(self.bridge / 'institutional_state_summary.json', {
            'provenance': provenance,
            'entries': [{'reviewId': 'inst-001', 'systemHealthScore': 0.9, 'systemHealthOverview': 'stable'}],
        })
        write_json(self.bridge / 'institutional_conflict_report.json', {
            'provenance': provenance,
            'entries': [{'reviewId': 'inst-001', 'chamberConflictLevel': 'low'}],
        })
        write_json(self.bridge / 'institutional_health_projection.json', {
            'provenance': provenance,
            'entries': [{'reviewId': 'inst-001', 'systemHealthScore': 0.9, 'systemHealthOverview': 'stable'}],
        })

        for name in [
            'governance_review_docket.json',
            'quorum_resilience_watchlist.json',
            'integrity_testimony_watchlist.json',
            'divergence_watchlist.json',
        ]:
            write_json(self.registry / name, {'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self, extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--institutional-audit', str(self.bridge / 'institutional_audit.json'),
            '--institutional-recommendations', str(self.bridge / 'institutional_recommendations.json'),
            '--institutional-state-map', str(self.bridge / 'institutional_state_map.json'),
            '--institutional-state-summary', str(self.bridge / 'institutional_state_summary.json'),
            '--institutional-conflict-report', str(self.bridge / 'institutional_conflict_report.json'),
            '--institutional-health-projection', str(self.bridge / 'institutional_health_projection.json'),
            '--governance-review-docket', str(self.registry / 'governance_review_docket.json'),
            '--quorum-resilience-watchlist', str(self.registry / 'quorum_resilience_watchlist.json'),
            '--integrity-testimony-watchlist', str(self.registry / 'integrity_testimony_watchlist.json'),
            '--divergence-watchlist', str(self.registry / 'divergence_watchlist.json'),
            '--out-institutional-status', str(self.registry / 'institutional_status.json'),
            '--out-system-health-dashboard', str(self.registry / 'system_health_dashboard.json'),
            '--out-institutional-conflict-watchlist', str(self.registry / 'institutional_conflict_watchlist.json'),
            '--out-institutional-annotations', str(self.registry / 'institutional_annotations.json'),
        ]
        if extra:
            cmd.extend(extra)
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_canonical_artifact_name_usage(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_deprecated_name_rejection(self) -> None:
        result = self.run_builder(['--institutional-synthesis', str(self.bridge / 'institutional_synthesis.json')])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Deprecated artifact alias', result.stdout + result.stderr)

    def test_provenance_propagation(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'institutional_status.json').read_text(encoding='utf-8'))
        prov = payload.get('provenance', {})
        self.assertIn('schemaVersions', prov)
        self.assertIn('producerCommits', prov)
        self.assertIn('derivedFromFixtures', prov)

    def test_missing_upstream_artifact_failure(self) -> None:
        (self.bridge / 'institutional_conflict_report.json').unlink()
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Missing required canonical artifact', result.stdout + result.stderr)

    def test_non_mutation_guarantee_preserved(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads((self.registry / 'institutional_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(payload.get('noCanonicalMutation'))
        self.assertTrue(all(a.get('noCanonicalMutation') for a in payload.get('annotations', [])))


if __name__ == '__main__':
    unittest.main()
