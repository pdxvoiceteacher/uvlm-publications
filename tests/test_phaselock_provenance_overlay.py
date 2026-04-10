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
    def test_builds_contract_and_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            coh_bridge = root / "CoherenceLattice" / "bridge"
            sophia_bridge = root / "Sophia" / "bridge"
            out = root / "registry" / "phaselock_provenance_dashboard.json"

            write_json(coh_bridge / "triadic_run_manifest.json", {
                "normalized_sha256s": [
                    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                ]
            })
            write_json(coh_bridge / "grounding_policy.json", {
                "source_context_mode": "bundle_compact",
                "clarification_state": "source_resolved",
            })
            write_json(coh_bridge / "source_evidence_packet.json", {
                "by_node": {
                    "n1": {
                        "grounded": True,
                        "citation_count": 3,
                        "sha256": "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                    },
                    "n2": {
                        "grounded": False,
                        "citation_count": 2,
                    },
                }
            })
            write_json(sophia_bridge / "attention_updates.json", {"legacy_alias_projection": True})

            cmd = [
                "python",
                str(SCRIPT),
                "--triadic-run-manifest", str(coh_bridge / "triadic_run_manifest.json"),
                "--grounding-policy", str(coh_bridge / "grounding_policy.json"),
                "--source-evidence-packet", str(coh_bridge / "source_evidence_packet.json"),
                "--attention-updates", str(sophia_bridge / "attention_updates.json"),
                "--out-dashboard", str(out),
            ]
            subprocess.run(cmd, check=True)
            first = out.read_text(encoding="utf-8")
            subprocess.run(cmd, check=True)
            second = out.read_text(encoding="utf-8")

            self.assertEqual(first, second)
            payload = json.loads(first)
            self.assertEqual(
                payload,
                {
                    "grounded": True,
                    "grounding_count": 1,
                    "normalized_sha256s": [
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                    ],
                    "citation_count": 5,
                    "citation_ready": True,
                    "source_context_mode": "bundle_compact",
                    "clarification_state": "source_resolved",
                    "legacy_alias_projection": True,
                },
            )

    def test_missing_attention_file_still_emits_dashboard(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            coh_bridge = root / "CoherenceLattice" / "bridge"
            out = root / "registry" / "phaselock_provenance_dashboard.json"

            write_json(coh_bridge / "triadic_run_manifest.json", {})
            write_json(coh_bridge / "grounding_policy.json", {})
            write_json(coh_bridge / "source_evidence_packet.json", {})

            subprocess.run(
                [
                    "python",
                    str(SCRIPT),
                    "--triadic-run-manifest", str(coh_bridge / "triadic_run_manifest.json"),
                    "--grounding-policy", str(coh_bridge / "grounding_policy.json"),
                    "--source-evidence-packet", str(coh_bridge / "source_evidence_packet.json"),
                    "--attention-updates", str(root / "Sophia" / "bridge" / "attention_updates.json"),
                    "--out-dashboard", str(out),
                ],
                check=True,
            )

            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertFalse(payload["grounded"])
            self.assertEqual(payload["grounding_count"], 0)
            self.assertEqual(payload["citation_count"], 0)
            self.assertFalse(payload["citation_ready"])
            self.assertEqual(payload["source_context_mode"], "bundle_compact")
            self.assertEqual(payload["clarification_state"], "source_resolved")
            self.assertTrue(payload["legacy_alias_projection"])


if __name__ == "__main__":
    unittest.main()
