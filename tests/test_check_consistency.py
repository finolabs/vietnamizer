from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check-consistency.py"
spec = importlib.util.spec_from_file_location("check_consistency", SCRIPT)
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)


def axes(text: str) -> set[str]:
    return {f["axis"] for f in cc.analyze(text)["findings"]}


class CheckConsistencyTest(unittest.TestCase):
    def test_tone_placement_mixed_is_flagged(self) -> None:
        self.assertIn("vi-tri-dau-thanh", axes("Hòa bình và thuỷ điện, hoà giải."))

    def test_tone_placement_consistent_is_not_flagged(self) -> None:
        self.assertNotIn("vi-tri-dau-thanh", axes("Hòa bình, thủy điện, khỏe mạnh, quý khách."))
        self.assertNotIn("vi-tri-dau-thanh", axes("Hoà bình, thuỷ điện, khoẻ mạnh."))

    def test_iy_pair(self) -> None:
        self.assertIn("i-y", axes("Kỹ thuật và kĩ năng."))
        self.assertNotIn("i-y", axes("Kỹ thuật và kỹ năng."))

    def test_number_separators(self) -> None:
        self.assertIn("so", axes("Giá 1.000 đồng, tổng 2,500 sản phẩm."))
        self.assertIn("so", axes("Tăng 1,5 lần, đạt 2.5 điểm."))
        self.assertNotIn("so", axes("Giá 1.000 đồng và 2.500 sản phẩm, tăng 1,5 lần."))

    def test_first_person_variants(self) -> None:
        self.assertIn("xung-ho", axes("Tôi nghĩ vậy. Chúng ta cần làm."))
        self.assertNotIn("xung-ho", axes("Tôi nghĩ vậy. Tôi sẽ làm."))

    def test_cli_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "a.md"
            good.write_text("Hòa bình và thuỷ điện.", encoding="utf-8")
            ok = subprocess.run([sys.executable, "-I", str(SCRIPT), str(good)],
                                capture_output=True, text=True, check=False)
            self.assertEqual(ok.returncode, 0)
            self.assertIn("vi-tri-dau-thanh", ok.stdout)
            bad = subprocess.run([sys.executable, "-I", str(SCRIPT), str(Path(tmp) / "none.md")],
                                 capture_output=True, text=True, check=False)
            self.assertEqual(bad.returncode, 2)

    def test_script_has_no_network_or_write_calls(self) -> None:
        source = SCRIPT.read_text(encoding="utf-8")
        for token in ("socket", "urllib", "requests", "subprocess", "write_text", "open(\"w"):
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
