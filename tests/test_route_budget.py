"""Tests for scripts/route_budget.py (spec 038, contracts/route-budget.md)."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "route_budget.py"


class RouteBudgetTest(unittest.TestCase):
    def copy_repo(self, temp: Path) -> Path:
        repo = temp / "repo"
        for relative in ("SKILL.md", "references", "profiles", "benchmarks/route-budget.json", "scripts/route_budget.py"):
            source, target = ROOT / relative, repo / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, target)
            else:
                shutil.copy2(source, target)
        return repo

    def run_check(self, repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, "-I", str(repo / "scripts" / "route_budget.py"), *args],
                              cwd=repo, capture_output=True, text=True, check=False)

    def test_current_tree_is_within_budget(self) -> None:
        result = subprocess.run([sys.executable, "-I", str(SCRIPT)], cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for route in ("short-edit", "whole-article", "long-or-multi-round", "follow-sample", "voice-profile",
                      "help", "review-only", "typography-only"):
            self.assertIn(route, result.stdout)

    def test_adding_a_file_to_the_whole_article_route_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = self.copy_repo(Path(temporary))
            skill = repo / "SKILL.md"
            text = skill.read_text(encoding="utf-8")
            lines = text.splitlines(keepends=True)
            for index, line in enumerate(lines):
                if line.startswith("| Biên tập toàn bài"):
                    cells = line.split(" | ")
                    cells[1] = cells[1] + " và `references/sino-vietnamese.md`"
                    lines[index] = " | ".join(cells)
                    break
            else:
                self.fail("whole-article row not found")
            skill.write_text("".join(lines), encoding="utf-8")
            result = self.run_check(repo)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("whole-article", result.stdout + result.stderr)

    def test_missing_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = self.copy_repo(Path(temporary))
            (repo / "references" / "typography.md").unlink()
            result = self.run_check(repo)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("references/typography.md", result.stdout + result.stderr)

    def test_unmapped_row_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = self.copy_repo(Path(temporary))
            skill = repo / "SKILL.md"
            text = skill.read_text(encoding="utf-8")
            marker = "| Chỉ typography"
            self.assertIn(marker, text)
            text = text.replace(marker, "| Việc lạ chưa có tuyến | `references/typography.md` | - |\n" + marker, 1)
            skill.write_text(text, encoding="utf-8")
            result = self.run_check(repo)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("Việc lạ", result.stdout + result.stderr)

    def test_write_refuses_to_raise_above_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = self.copy_repo(Path(temporary))
            budget_path = repo / "benchmarks" / "route-budget.json"
            budget = json.loads(budget_path.read_text(encoding="utf-8"))
            budget["routes"]["help"]["baseline_bytes"] = 10
            budget_path.write_text(json.dumps(budget), encoding="utf-8")
            result = self.run_check(repo, "--write")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("help", result.stdout + result.stderr)
            self.assertEqual(json.loads(budget_path.read_text(encoding="utf-8"))["routes"]["help"]["baseline_bytes"], 10)


if __name__ == "__main__":
    unittest.main()
