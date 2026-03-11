from __future__ import annotations

import json
import unittest
from pathlib import Path


class LegibilityDashboardRouteFixturesTests(unittest.TestCase):
    def test_lineage_fixture_keys_present(self) -> None:
        payload = json.loads(Path('tests/fixtures/legibility_routes/lineage_route_sample.json').read_text(encoding='utf-8'))
        self.assertIsInstance(payload.get('entries'), list)
        self.assertGreater(len(payload['entries']), 0)
        row = payload['entries'][0]
        for key in ('phaseId', 'phaseLineageVisibility', 'glossaryAvailability', 'canonicalBoundaryNote', 'upstreamArtifacts', 'downstreamArtifacts'):
            self.assertIn(key, row)

    def test_memory_fixture_keys_present(self) -> None:
        payload = json.loads(Path('tests/fixtures/legibility_routes/memory_route_sample.json').read_text(encoding='utf-8'))
        self.assertIsInstance(payload.get('entries'), list)
        self.assertGreater(len(payload['entries']), 0)
        for row in payload['entries']:
            for key in ('memoryId', 'memoryTier', 'preservationCriticality', 'invariantHash'):
                self.assertIn(key, row)
            self.assertIn(row['memoryTier'], {'hot', 'warm', 'cold'})

    def test_trace_fixture_keys_present(self) -> None:
        payload = json.loads(Path('tests/fixtures/legibility_routes/coherence_memory_trace_sample.json').read_text(encoding='utf-8'))
        self.assertIsInstance(payload.get('entries'), list)
        self.assertGreater(len(payload['entries']), 0)
        row = payload['entries'][0]
        self.assertIn('phaseId', row)
        self.assertIn('donorPatternsApplied', row)
        self.assertIn('unresolvedTensions', row)

    def test_route_pages_contain_boundary_label(self) -> None:
        lineage_html = Path('lineage/index.html').read_text(encoding='utf-8')
        memory_html = Path('memory/index.html').read_text(encoding='utf-8')
        self.assertIn('Canonical legibility aid only', lineage_html)
        self.assertIn('Canonical legibility aid only', memory_html)
        lineage_js = Path('lineage/lineage.js').read_text(encoding='utf-8')
        memory_js = Path('memory/memory.js').read_text(encoding='utf-8')
        self.assertIn('fetchJsonWithFallback', lineage_js)
        self.assertIn('fetchJsonWithFallback', memory_js)


if __name__ == '__main__':
    unittest.main()
