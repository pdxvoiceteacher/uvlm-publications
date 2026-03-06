from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

VALID_FIXTURE = Path("tests/fixtures/atlas_timeline.valid.json")
INVALID_FIXTURES = sorted(Path("tests/fixtures").glob("atlas_timeline.invalid.*.json"))


class ValidateAtlasTimelineCLITests(unittest.TestCase):
    def run_validator(self, fixture: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", "scripts/validate_atlas_timeline.py", str(fixture)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_valid_fixture(self) -> None:
        result = self.run_validator(VALID_FIXTURE)
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_invalid_fixtures(self) -> None:
        self.assertGreater(len(INVALID_FIXTURES), 0)
        for fixture in INVALID_FIXTURES:
            with self.subTest(fixture=fixture.name):
                result = self.run_validator(fixture)
                self.assertNotEqual(result.returncode, 0, msg=f"{fixture} unexpectedly passed\n{result.stdout}{result.stderr}")


if __name__ == "__main__":
    unittest.main()
