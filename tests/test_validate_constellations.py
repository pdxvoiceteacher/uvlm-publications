from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

GRAPH = Path("registry/knowledge_graph.json")
VALID = Path("tests/fixtures/constellations.valid.json")
INVALIDS = sorted(Path("tests/fixtures").glob("constellations.invalid.*.json"))


class ValidateConstellationsCLITests(unittest.TestCase):
    def run_validator(self, fixture: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "python3",
                "scripts/validate_constellations.py",
                str(fixture),
                str(GRAPH),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_valid_constellation_fixture(self) -> None:
        result = self.run_validator(VALID)
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_invalid_constellation_fixtures(self) -> None:
        self.assertGreater(len(INVALIDS), 0)
        for fixture in INVALIDS:
            with self.subTest(fixture=fixture.name):
                result = self.run_validator(fixture)
                self.assertNotEqual(
                    result.returncode,
                    0,
                    msg=f"{fixture} unexpectedly passed\n{result.stdout}{result.stderr}",
                )


if __name__ == "__main__":
    unittest.main()
