from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path('scripts/build_pattern_temporal_overlay.py')


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


class PatternTemporalOverlayBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bridge = self.root / 'bridge'
        self.registry = self.root / 'registry'

        prov = {'schemaVersion': 'phase-z1.0', 'producerCommits': ['z1'], 'sourceMode': 'fixture'}
        write_json(self.bridge / 'pattern_temporal_audit.json', {'provenance': prov, 'audits': [{'reviewId': 'pt-1', 'patternTemporalAuditState': 'verified'}]})
        write_json(self.bridge / 'pattern_temporal_recommendations.json', {
            'provenance': prov,
            'recommendations': [
                {'reviewId': 'pt-1', 'targetPublisherAction': 'docket', 'linkedTargetIds': ['concept:x'], 'timelineEvents': [{'date': '2026-01-01', 'event': 'a'}]},
                {'reviewId': 'pt-2', 'targetPublisherAction': 'watch', 'linkedTargetIds': ['concept:y']},
                {'reviewId': 'pt-3', 'targetPublisherAction': 'suppressed', 'linkedTargetIds': ['concept:z']},
            ],
        })
        write_json(self.bridge / 'pattern_timeline_map.json', {'provenance': prov, 'entries': [{'reviewId': 'pt-1', 'patternTimelineStatus': 'tracked', 'timelineEvents': [{'date': '2026-01-01', 'event': 'a'}]}]})
        write_json(self.bridge / 'pattern_persistence_map.json', {'provenance': prov, 'entries': [{'reviewId': 'pt-1', 'patternPersistence': 'stable'}]})
        write_json(self.bridge / 'pattern_temporal_conflict_report.json', {'provenance': prov, 'entries': [{'reviewId': 'pt-1', 'temporalConflictMarkers': ['window-shift']}]})

        reg_prov = {'provenance': {'schemaVersions': {'x': '1'}, 'producerCommits': ['abc'], 'derivedFromFixtures': True}}
        write_json(self.registry / 'pattern_dashboard.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'pattern_registry.json', {**reg_prov, 'entries': []})
        write_json(self.registry / 'pattern_watchlist.json', {**reg_prov, 'entries': []})

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_builder(self, extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        cmd = [
            'python3', str(SCRIPT),
            '--pattern-temporal-audit', str(self.bridge / 'pattern_temporal_audit.json'),
            '--pattern-temporal-recommendations', str(self.bridge / 'pattern_temporal_recommendations.json'),
            '--pattern-timeline-map', str(self.bridge / 'pattern_timeline_map.json'),
            '--pattern-persistence-map', str(self.bridge / 'pattern_persistence_map.json'),
            '--pattern-temporal-conflict-report', str(self.bridge / 'pattern_temporal_conflict_report.json'),
            '--pattern-dashboard', str(self.registry / 'pattern_dashboard.json'),
            '--pattern-registry', str(self.registry / 'pattern_registry.json'),
            '--pattern-watchlist', str(self.registry / 'pattern_watchlist.json'),
            '--out-pattern-timeline-dashboard', str(self.registry / 'pattern_timeline_dashboard.json'),
            '--out-pattern-persistence-registry', str(self.registry / 'pattern_persistence_registry.json'),
            '--out-pattern-temporal-watchlist', str(self.registry / 'pattern_temporal_watchlist.json'),
            '--out-pattern-temporal-annotations', str(self.registry / 'pattern_temporal_annotations.json'),
        ]
        if extra:
            cmd.extend(extra)
        return subprocess.run(cmd, text=True, capture_output=True)

    def test_canonical_artifact_name_usage(self) -> None:
        self.assertEqual(self.run_builder().returncode, 0)

    def test_deprecated_name_rejection(self) -> None:
        result = self.run_builder(['--pattern-temporal-snapshot', str(self.bridge / 'old.json')])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Deprecated artifact alias', result.stdout + result.stderr)

    def test_action_filters(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        dashboard = json.loads((self.registry / 'pattern_timeline_dashboard.json').read_text(encoding='utf-8'))
        watchlist = json.loads((self.registry / 'pattern_temporal_watchlist.json').read_text(encoding='utf-8'))
        self.assertEqual([e['reviewId'] for e in dashboard['entries']], ['pt-1'])
        self.assertEqual([e['reviewId'] for e in watchlist['entries']], ['pt-2'])

    def test_non_mutation_guarantee_preserved(self) -> None:
        result = self.run_builder()
        self.assertEqual(result.returncode, 0)
        payload = json.loads((self.registry / 'pattern_temporal_annotations.json').read_text(encoding='utf-8'))
        self.assertTrue(payload.get('noCanonicalMutation'))
        self.assertTrue(payload.get('noAutomaticAccusation'))


if __name__ == '__main__':
    unittest.main()
