from __future__ import annotations

import unittest
from pathlib import Path


class TelTerraceOverlayAssetsTests(unittest.TestCase):
    def test_html_has_toggle_and_legend_markers(self) -> None:
        html = Path('atlas/index.html').read_text(encoding='utf-8')
        self.assertIn('show-terrace-readiness', html)
        self.assertIn('show-orthodoxy-risk', html)
        self.assertIn('show-discovery-corridor', html)
        self.assertIn('Approaching Terrace', html)
        self.assertIn('Converged Orthodoxy', html)
        self.assertIn('Orthodoxy Alert (coercive coherence)', html)
        self.assertIn('Discovery Corridor (reopening)', html)

    def test_overlay_module_has_advisory_non_final_language(self) -> None:
        js = Path('atlas/telTerraceOverlay.js').read_text(encoding='utf-8')
        self.assertIn('Bounded guidance', js)
        self.assertIn('no governance claim', js)
        self.assertIn('no closure or finality implied', js)

    def test_atlas_integration_wires_overlay_and_reset(self) -> None:
        js = Path('atlas/atlas.js').read_text(encoding='utf-8')
        self.assertIn('applyTerraceOverlay', js)
        self.assertIn('bindTerraceOverlayToggle', js)
        self.assertIn('terraceResettableClasses', js)
        self.assertIn('terrace-approaching', js)
        self.assertIn('terrace-converged-orthodoxy', js)
        self.assertIn('applyOrthodoxyCorridorOverlay', js)
        self.assertIn('bindOrthodoxyCorridorToggles', js)
        self.assertIn('orthodoxyResettableClasses', js)

    def test_orthodoxy_overlay_module_has_advisory_labels(self) -> None:
        js = Path('atlas/telOrthodoxyOverlay.js').read_text(encoding='utf-8')
        self.assertIn('Orthodoxy Alert', js)
        self.assertIn('Corridor Forming', js)
        self.assertIn('supportive overlay, not a final conclusion', js)



if __name__ == '__main__':
    unittest.main()
