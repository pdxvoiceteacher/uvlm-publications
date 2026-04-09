import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path("scripts/build_phaselock_provenance_overlay.py")


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


class TestPhaselockProvenanceOverlay(unittest.TestCase):
    def test_builds_dashboard_and_warns_when_attention_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bridge = root / "bridge"
            registry = root / "registry"

            write_json(bridge / "coherence_drift_map.json", {
                "nodes": [{"node_id": "n1", "drift_score": 0.42}]
            })
            write_json(bridge / "triadic_run_manifest.json", {
                "run_hash": "run-abc-123"
            })
            write_json(bridge / "grounding_policy.json", {
                "source_first_clarification_suppressed": True
            })
            write_json(bridge / "source_evidence_packet.json", {
                "audited": True,
                "by_node": {
                    "n1": {
                        "grounded": True,
                        "citation_count": 2,
                        "bundle_count": 1,
                        "audited": True,
                    }
                }
            })
            # no attention_updates.json on purpose

            out = registry / "phaselock_provenance_dashboard.json"

            subprocess.run(
                [
                    "python",
                    str(SCRIPT),
                    "--coherence-drift-map", str(bridge / "coherence_drift_map.json"),
                    "--triadic-run-manifest", str(bridge / "triadic_run_manifest.json"),
                    "--grounding-policy", str(bridge / "grounding_policy.json"),
                    "--source-evidence-packet", str(bridge / "source_evidence_packet.json"),
                    "--attention-updates", str(bridge / "attention_updates.json"),
                    "--out-dashboard", str(out),
                ],
                check=True,
            )

            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema"], "atlas.phaselock.provenance.v1")
            self.assertIn("attention_updates_missing_bounded_warning", payload["warnings"])
            self.assertEqual(payload["nodes"]["n1"]["canonical_run_hash"], "run-abc-123")
            self.assertTrue(payload["nodes"]["n1"]["grounded"])
            self.assertEqual(payload["nodes"]["n1"]["citation_count"], 2)
            self.assertEqual(payload["nodes"]["n1"]["bundle_count"], 1)
            self.assertTrue(payload["nodes"]["n1"]["source_first_clarification_suppressed"])


if __name__ == "__main__":
    unittest.main()
