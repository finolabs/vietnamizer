from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "scripts" / "scan-lexicon.py"
LEXICON = ROOT / "references" / "ai-error-lexicon.md"
FIXTURES = ROOT / "tests" / "fixtures" / "lexicon" / "fixtures.json"
CASES = ROOT / "calibration" / "test-cases.md"

sys.path.insert(0, str(ROOT / "scripts"))
import lexicon_check  # noqa: E402

HEADER = (
    "| ID | Dạng | Loại | Pattern | Sửa | Ngữ vực lỗi | Sau không là | "
    "Trước không là | Chữ hoa | Không flag | Ca |"
)


def load_scanner():
    spec = importlib.util.spec_from_file_location("scan_lexicon", SCANNER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixtures() -> list[dict]:
    return json.loads(FIXTURES.read_text(encoding="utf-8"))["fixtures"]


def run_cli(*args: str, data: bytes = b"", script: Path = SCANNER, cwd: Path | None = None):
    return subprocess.run(
        [sys.executable, "-I", str(script), *args],
        input=data,
        capture_output=True,
        cwd=cwd,
        check=False,
        timeout=20,
    )


class LexiconTableTest(unittest.TestCase):
    def errors(self, text: str) -> list[str]:
        return lexicon_check.check_lexicon(
            text,
            lexicon_check.pattern_ids(ROOT),
            lexicon_check.case_index(CASES.read_text(encoding="utf-8")),
        )

    def test_table_file_exists_with_exact_header(self) -> None:
        self.assertTrue(LEXICON.is_file(), "references/ai-error-lexicon.md chưa có")
        lines = LEXICON.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines.count(HEADER), 1)

    def test_table_passes_every_validation_rule(self) -> None:
        self.assertEqual(self.errors(LEXICON.read_text(encoding="utf-8")), [])

    def test_seed_entries_and_values(self) -> None:
        rows = load_scanner().parse_table(LEXICON.read_text(encoding="utf-8"))
        self.assertEqual([row["ID"] for row in rows], [f"L{n:02d}" for n in range(1, 9)])
        self.assertEqual(
            [row["Dạng"] for row in rows],
            ["rườm", "bỡ", "giữ nghĩa", "giữ giọng", "nghĩa và giọng", "gọi tên", "dịch sát", "đội"],
        )
        self.assertEqual(rows[7]["Chữ hoa"], "đầu câu")

    def test_introduction_is_short_and_sections_present(self) -> None:
        text = LEXICON.read_text(encoding="utf-8")
        intro = text.split("\n## Bảng\n")[0].split("\n---\n", 1)[1]
        self.assertLessEqual(len([line for line in intro.splitlines() if line.strip()]), 12)
        self.assertIn("\n## Thêm mục\n", text)
        self.assertIn("Không flag", intro)
        self.assertIn("T1–T6", intro)

    def test_every_entry_has_positive_and_guard_fixture(self) -> None:
        rows = load_scanner().parse_table(LEXICON.read_text(encoding="utf-8"))
        items = fixtures()
        for row in rows:
            hits = [f for f in items if any(c["entry"] == row["ID"] for c in f["expected"])]
            self.assertTrue(any(f["agent"] == "sửa" for f in hits), f"{row['ID']} thiếu fixture lỗi")
            self.assertTrue(any(f["agent"] == "giữ" for f in hits), f"{row['ID']} thiếu fixture giữ")

    def test_fixture_shape(self) -> None:
        items = fixtures()
        self.assertEqual([f["id"] for f in items], [f"LXF{n:02d}" for n in range(1, len(items) + 1)])
        for item in items:
            self.assertIn(item["agent"], {"sửa", "giữ"}, item["id"])
            self.assertEqual("output" in item, item["agent"] == "sửa", item["id"])
            self.assertTrue(item["cases"], item["id"])

    def test_fixture_lx_cases_mirrored_in_calibration(self) -> None:
        cases = lexicon_check.case_index(CASES.read_text(encoding="utf-8"))
        for item in fixtures():
            for case in item["cases"]:
                self.assertIn(case, cases, f"{item['id']}: {case}")
            lx = [case for case in item["cases"] if case.startswith("LX")]
            self.assertEqual(len(lx), 1, item["id"])
            self.assertEqual(cases[lx[0]], item["agent"] == "giữ", item["id"])


class LexiconGrowthTest(unittest.TestCase):
    """Một dòng thiếu bằng chứng không được qua kiểm."""

    def mutate(self, column: str, value: str) -> list[str]:
        text = LEXICON.read_text(encoding="utf-8")
        scanner = load_scanner()
        columns = list(scanner.COLUMNS)
        lines = text.splitlines()
        index = next(i for i, line in enumerate(lines) if line.startswith("| L01 |"))
        cells = scanner.split_row(lines[index])
        cells[columns.index(column)] = value
        lines[index] = "| " + " | ".join(cells) + " |"
        return LexiconTableTest.errors(self, "\n".join(lines) + "\n")

    def test_missing_pattern_fails(self) -> None:
        self.assertTrue(self.mutate("Pattern", ""))

    def test_unknown_pattern_fails(self) -> None:
        self.assertTrue(self.mutate("Pattern", "V99"))

    def test_missing_case_fails(self) -> None:
        self.assertTrue(self.mutate("Ca", ""))

    def test_case_without_guard_fails(self) -> None:
        self.assertTrue(self.mutate("Ca", "HF02, HF10"))

    def test_case_without_error_fails(self) -> None:
        self.assertTrue(self.mutate("Ca", "HF09"))

    def test_missing_fix_fails(self) -> None:
        self.assertTrue(self.mutate("Sửa", ""))

    def test_fix_equal_to_form_fails(self) -> None:
        self.assertTrue(self.mutate("Sửa", "rườm"))

    def test_missing_khong_flag_fails(self) -> None:
        self.assertTrue(self.mutate("Không flag", ""))

    def test_dash_outside_neighbour_columns_fails(self) -> None:
        self.assertTrue(self.mutate("Không flag", "—"))

    def test_bad_kind_and_case_mode_fail(self) -> None:
        self.assertTrue(self.mutate("Loại", "lỗi khác"))
        self.assertTrue(self.mutate("Chữ hoa", "hoa"))

    def test_bad_form_fails(self) -> None:
        self.assertTrue(self.mutate("Dạng", "Rườm"))
        self.assertTrue(self.mutate("Dạng", "một hai ba bốn năm"))

    def test_second_table_fails(self) -> None:
        text = LEXICON.read_text(encoding="utf-8") + "\n| a | b |\n|---|---|\n| 1 | 2 |\n"
        self.assertTrue(LexiconTableTest.errors(self, text))

    errors = LexiconTableTest.errors


class ScannerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scanner = load_scanner()
        cls.entries = cls.scanner.load_entries(LEXICON.read_text(encoding="utf-8"))

    def test_every_fixture_returns_exact_candidates(self) -> None:
        for item in fixtures():
            with self.subTest(item["id"]):
                got = [
                    {key: c[key] for key in ("entry", "text", "line", "column", "zone")}
                    for c in self.scanner.scan(item["text"], self.entries)
                ]
                self.assertEqual(got, item["expected"])

    def test_paragraph_numbers(self) -> None:
        got = self.scanner.scan("Mở bài.\n\n\nĐội đã xong.\nDòng hai rườm.\n\nCuối rườm.", self.entries)
        self.assertEqual([c["paragraph"] for c in got], [2, 2, 3])

    def test_overlap_reports_both_entries_in_order(self) -> None:
        got = self.scanner.scan("Giữ nghĩa và giọng.", self.entries)
        self.assertEqual([c["entry"] for c in got], ["L03", "L05"])

    def test_inner_lowercase_doi_and_verb_are_not_candidates(self) -> None:
        self.assertEqual(self.scanner.scan("Anh ấy đội mũ. Đội mũ vào.", self.entries), [])

    def test_blank_line_breaks_a_multi_syllable_form(self) -> None:
        self.assertEqual(self.scanner.scan("Cần giữ\n\nnghĩa.", self.entries), [])


class ScannerCliTest(unittest.TestCase):
    def test_json_output_schema(self) -> None:
        result = run_cli(data="Quy trình còn rườm.".encode("utf-8"))
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout.decode("utf-8"))
        self.assertEqual(set(payload), {"schema", "lexicon_sha256", "candidates"})
        self.assertEqual(payload["schema"], 1)
        self.assertEqual(payload["lexicon_sha256"], hashlib.sha256(LEXICON.read_bytes()).hexdigest()[:12])
        self.assertEqual(
            payload["candidates"],
            [{"entry": "L01", "text": "rườm", "line": 1, "column": 15, "paragraph": 1, "zone": None}],
        )
        self.assertIn("rườm".encode("utf-8"), result.stdout)

    def test_no_candidates_still_exit_zero(self) -> None:
        result = run_cli(data="Thủ tục rườm rà.".encode("utf-8"))
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["candidates"], [])

    def test_bom_is_stripped(self) -> None:
        result = run_cli(data=b"\xef\xbb\xbf" + "Đội đã xong.".encode("utf-8"))
        self.assertEqual(json.loads(result.stdout)["candidates"][0]["column"], 1)

    def test_help(self) -> None:
        result = run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("stdin", result.stdout.decode("utf-8"))

    def assert_refused(self, result, code: int) -> None:
        self.assertEqual(result.returncode, code)
        self.assertEqual(result.stdout, b"")
        self.assertEqual(len(result.stderr.decode("utf-8").strip().splitlines()), 1)

    def test_bad_input_exits_two(self) -> None:
        self.assert_refused(run_cli("bai.md", data=b"x"), 2)
        self.assert_refused(run_cli("--lexicon", "x", data=b"x"), 2)
        self.assert_refused(run_cli(data=b""), 2)
        self.assert_refused(run_cli(data=b"\xff\xfe"), 2)
        self.assert_refused(run_cli(data=b"a" * 1_000_001), 2)

    def test_exactly_the_byte_cap_is_accepted(self) -> None:
        self.assertEqual(run_cli(data=b"a" * 1_000_000).returncode, 0)

    def copy_tree(self, directory: Path) -> Path:
        (directory / "scripts").mkdir()
        (directory / "references").mkdir()
        script = directory / "scripts" / "scan-lexicon.py"
        shutil.copy(SCANNER, script)
        return script

    def test_missing_or_malformed_lexicon_exits_three(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            script = self.copy_tree(Path(temp))
            self.assert_refused(run_cli(data=b"x", script=script), 3)
            (Path(temp) / "references" / "ai-error-lexicon.md").write_text("# rỗng\n", encoding="utf-8")
            self.assert_refused(run_cli(data=b"x", script=script), 3)

    def test_quickstart_commands(self) -> None:
        result = run_cli(data="Quy trình còn rườm và dễ làm nhân viên mới bỡ.".encode("utf-8"))
        self.assertEqual([c["entry"] for c in json.loads(result.stdout)["candidates"]], ["L01", "L02"])
        self.assertEqual(run_cli("--help").returncode, 0)

    def test_runs_in_read_only_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            script = self.copy_tree(Path(temp))
            shutil.copy(LEXICON, Path(temp) / "references" / "ai-error-lexicon.md")
            for path in [Path(temp) / "scripts", Path(temp) / "references", Path(temp)]:
                os.chmod(path, stat.S_IRUSR | stat.S_IXUSR)
            try:
                result = run_cli(data="Đội đã xong.".encode("utf-8"), script=script, cwd=Path(temp))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(sorted(p.name for p in (Path(temp) / "scripts").iterdir()), ["scan-lexicon.py"])
            finally:
                for path in [Path(temp), Path(temp) / "scripts", Path(temp) / "references"]:
                    os.chmod(path, stat.S_IRWXU)


class ScannerPrincipleVTest(unittest.TestCase):
    ALLOWED = {"__future__", "argparse", "hashlib", "json", "pathlib", "re", "sys", "unicodedata"}
    FORBIDDEN_ATTRIBUTES = {
        "environ", "getenv", "write_text", "write_bytes", "unlink", "rename", "mkdir",
        "touch", "rmdir", "symlink_to", "chmod", "system", "popen",
    }

    @classmethod
    def setUpClass(cls) -> None:
        cls.tree = ast.parse(SCANNER.read_text(encoding="utf-8"))

    def test_imports_are_in_the_closed_set(self) -> None:
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertIn(alias.name.split(".")[0], self.ALLOWED, alias.name)
            elif isinstance(node, ast.ImportFrom):
                self.assertIn((node.module or "").split(".")[0], self.ALLOWED, node.module)

    def test_no_dynamic_import_exec_or_eval(self) -> None:
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Name):
                self.assertNotIn(node.id, {"__import__", "exec", "eval", "compile", "globals"}, node.id)

    def test_no_environment_or_write_attribute(self) -> None:
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Attribute):
                self.assertNotIn(node.attr, self.FORBIDDEN_ATTRIBUTES, node.attr)

    def test_open_only_for_reading(self) -> None:
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                name = node.func.id if isinstance(node.func, ast.Name) else getattr(node.func, "attr", "")
                if name == "open":
                    modes = [a.value for a in node.args[1:2] if isinstance(a, ast.Constant)]
                    modes += [k.value.value for k in node.keywords if k.arg == "mode" and isinstance(k.value, ast.Constant)]
                    self.assertTrue(modes and modes[0] in {"r", "rb"}, ast.dump(node))

    def test_lexicon_path_is_fixed(self) -> None:
        scanner = load_scanner()
        self.assertEqual(scanner.LEXICON, SCANNER.resolve().parent.parent / "references" / "ai-error-lexicon.md")
        self.assertNotIn("argv[1]", SCANNER.read_text(encoding="utf-8"))

    def test_output_has_no_edited_text_field(self) -> None:
        result = run_cli(data="Quy trình còn rườm.".encode("utf-8"))
        payload = json.loads(result.stdout)
        for candidate in payload["candidates"]:
            self.assertEqual(set(candidate), {"entry", "text", "line", "column", "paragraph", "zone"})


if __name__ == "__main__":
    unittest.main()
