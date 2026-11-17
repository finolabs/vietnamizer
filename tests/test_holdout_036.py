import hashlib
import json
import tempfile
import unicodedata
import unittest
from pathlib import Path

from benchmarks import holdout_036 as h

ARTICLE = (
    "Quy trình còn rườm. Nhân viên mới hay bỡ.\n\n"
    "Bản dịch giữ nghĩa của nguyên tác. Đội đã chốt kế hoạch quý.\n"
)
GOOD = (
    "Quy trình còn rườm rà. Nhân viên mới hay bỡ ngỡ.\n\n"
    "Bản dịch giữ nghĩa của nguyên tác. Đội ngũ đã chốt kế hoạch quý.\n"
)
BAD = (
    "Quá trình còn rườm rà. Nhân viên mới hay bỡ.\n\n"
    "Bản dịch giữ nguyên nghĩa của nguyên tác. Đội đã chốt kế hoạch quý này.\n"
)


def sheet(article: str) -> str:
    digest = hashlib.sha256(article.encode("utf-8")).hexdigest()
    return f"""Bài: H01            Thể loại: blog cá nhân        Model sinh bài: claude / claude-sonnet-5-5
Ngày đánh dấu: 18/11/2026   Người đánh dấu: Fio   SHA-256 bài: {digest}

## Bảng lỗi

| # | Đoạn | Cụm như trong bài | Nhóm | Sửa chấp nhận | Ghi chú |
|---|---|---|---|---|---|
| 1 | 1 | còn rườm | từ ghép bị cắt | còn rườm rà | |
| 2 | 1 | hay bỡ | từ ghép bị cắt | hay bỡ ngỡ | |
| 3 | 2 | Đội đã chốt | danh từ tập thể đứng trơ | Đội ngũ đã chốt / Nhóm sản phẩm đã chốt | |
| 4 | 2 | kế hoạch quý | khác: V9 | | |

## Bảng cần giữ

| # | Đoạn | Cụm phải giữ nguyên | Vì sao |
|---|---|---|---|
| 1 | 2 | giữ nghĩa của nguyên tác | câu trang trọng, đã đủ ý |
"""


class HoldoutFixture:
    def __init__(self, root: Path, article: str = ARTICLE) -> None:
        self.root = root
        (root / "H01.md").write_text(article, encoding="utf-8")
        (root / "H01.sheet.md").write_text(sheet(article), encoding="utf-8")
        (root / "good.md").write_text(GOOD, encoding="utf-8")
        (root / "bad.md").write_text(BAD, encoding="utf-8")
        self.manifest = h.manifest(root)

    def runs(self, **override) -> Path:
        data = {
            "schema": 1,
            "corpus_manifest_sha256": self.manifest["manifest_sha256"],
            "lexicon_sha256": "b846635e5b30",
            "runs": [
                {"article": "H01", "model": "claude-sonnet-5-5", "host": "cowork", "version": "0.17.0",
                 "label": "K2", "output": "good.md", "seconds": 30.5, "tokens": 1200},
                {"article": "H01", "model": "claude-sonnet-5-5", "host": "cowork", "version": "0.16.2",
                 "label": "Q9", "output": "bad.md", "seconds": 20.0, "tokens": 900},
            ],
        }
        data.update(override)
        path = self.root / "runs.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return path


class SheetTest(unittest.TestCase):
    def test_parses_header_errors_and_guards(self) -> None:
        parsed = h.parse_sheet(sheet(ARTICLE))
        self.assertEqual(parsed["article"], "H01")
        self.assertEqual(len(parsed["errors"]), 4)
        self.assertEqual(parsed["errors"][2]["fixes"], ["Đội ngũ đã chốt", "Nhóm sản phẩm đã chốt"])
        self.assertEqual(parsed["errors"][3]["fixes"], [])
        self.assertTrue(parsed["errors"][0]["lexicon_kind"])
        self.assertFalse(parsed["errors"][3]["lexicon_kind"])
        self.assertEqual(parsed["guards"][0]["span"], "giữ nghĩa của nguyên tác")

    def test_rejects_unknown_kind(self) -> None:
        bad = sheet(ARTICLE).replace("| từ ghép bị cắt | còn rườm rà |", "| lỗi lạ | còn rườm rà |")
        with self.assertRaises(ValueError):
            h.parse_sheet(bad)

    def test_rejects_span_missing_from_paragraph(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = HoldoutFixture(Path(temp))
            text = sheet(ARTICLE).replace("| 2 | 1 | hay bỡ |", "| 2 | 2 | hay bỡ |")
            (Path(temp) / "H01.sheet.md").write_text(text, encoding="utf-8")
            with self.assertRaises(ValueError):
                h.score(fixture.runs(corpus_manifest_sha256=h.manifest(Path(temp))["manifest_sha256"]))

    def test_rejects_fix_equal_to_span(self) -> None:
        with self.assertRaises(ValueError):
            h.parse_sheet(sheet(ARTICLE).replace("| còn rườm | từ ghép bị cắt | còn rườm rà |", "| còn rườm | từ ghép bị cắt | còn rườm |"))

    def test_rejects_span_repeated_in_paragraph(self) -> None:
        article = ARTICLE.replace("Nhân viên mới hay bỡ.", "Nhân viên mới hay bỡ. Khách cũng hay bỡ.")
        with tempfile.TemporaryDirectory() as temp:
            fixture = HoldoutFixture(Path(temp), article)
            with self.assertRaises(ValueError):
                h.score(fixture.runs())

    def test_rejects_output_outside_runs_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            corpus = Path(temp) / "corpus"
            corpus.mkdir()
            fixture = HoldoutFixture(corpus)
            (Path(temp) / "outside.md").write_text(GOOD, encoding="utf-8")
            runs = fixture.runs()
            data = json.loads(runs.read_text(encoding="utf-8"))
            data["runs"][0]["output"] = "../outside.md"
            runs.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                h.score(runs)

    def test_rejects_sheet_hash_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = HoldoutFixture(Path(temp))
            (Path(temp) / "H01.md").write_text(ARTICLE + "Thêm.\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                h.score(fixture.runs(corpus_manifest_sha256=h.manifest(Path(temp))["manifest_sha256"]))


class ScoreTest(unittest.TestCase):
    def report(self, judgments: dict | None = None) -> dict:
        with tempfile.TemporaryDirectory() as temp:
            fixture = HoldoutFixture(Path(temp))
            runs = fixture.runs()
            judgment_path = None
            if judgments is not None:
                judgment_path = Path(temp) / "judgments.json"
                judgment_path.write_text(json.dumps(judgments, ensure_ascii=False), encoding="utf-8")
            return h.score(runs, judgment_path)

    def row(self, report: dict, version: str) -> dict:
        return next(r for r in report["results"] if r["version"] == version)

    def test_good_output_fixes_lexicon_errors_and_keeps_guard(self) -> None:
        good = self.row(self.report(), "0.17.0")
        self.assertEqual(good["lexicon_kind"], {"fixed": 3, "total": 3})
        self.assertEqual(good["other"], {"fixed": 0, "total": 1, "pending": 1})
        self.assertEqual(good["guards"], {"broken": 0, "total": 1})
        self.assertEqual(good["out_of_span"], {"đúng": 0, "không cần": 0, "sai": 0, "pending": 0})
        self.assertEqual((good["seconds"], good["tokens"]), (30.5, 1200))

    def test_bad_output_counts_misses_breaks_and_out_of_span(self) -> None:
        bad = self.row(self.report(), "0.16.2")
        self.assertEqual(bad["lexicon_kind"], {"fixed": 1, "total": 3})
        self.assertEqual(bad["guards"], {"broken": 1, "total": 1})
        self.assertEqual(bad["out_of_span"]["pending"], 1)

    def test_judgments_resolve_pending_rows_and_edits(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = HoldoutFixture(Path(temp))
            edits = h.blind_edits(fixture.runs())
        self.assertEqual(len(edits["edits"]), 1)
        edit = edits["edits"][0]
        self.assertEqual((edit["source"], edit["output"]), ("Quy", "Quá"))
        self.assertNotIn("version", json.dumps(edits))
        self.assertNotIn("model", json.dumps(edits))
        report = self.report({"edits": {edit["id"]: "sai"}, "rows": {"H01#4": {"K2": "fixed", "Q9": "not"}}})
        good, bad = self.row(report, "0.17.0"), self.row(report, "0.16.2")
        self.assertEqual(good["other"], {"fixed": 1, "total": 1, "pending": 0})
        self.assertEqual(bad["other"], {"fixed": 0, "total": 1, "pending": 0})
        self.assertEqual(bad["out_of_span"]["sai"], 1)
        self.assertEqual(bad["over_corrections"], 1)

    def test_report_records_versions_and_hashes(self) -> None:
        report = self.report()
        self.assertEqual(report["lexicon_sha256"], "b846635e5b30")
        self.assertEqual(len(report["corpus_manifest_sha256"]), 64)
        self.assertEqual({(r["model"], r["host"], r["version"]) for r in report["results"]},
                         {("claude-sonnet-5-5", "cowork", "0.17.0"), ("claude-sonnet-5-5", "cowork", "0.16.2")})

    def test_nfd_output_is_not_a_change(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = HoldoutFixture(Path(temp))
            (Path(temp) / "good.md").write_text(unicodedata.normalize("NFD", GOOD), encoding="utf-8")
            report = h.score(fixture.runs())
        good = self.row(report, "0.17.0")
        self.assertEqual(good["lexicon_kind"]["fixed"], 3)
        self.assertEqual(good["guards"]["broken"], 0)
        self.assertEqual(good["out_of_span"]["pending"], 0)

    def test_deleted_sentence_is_not_fixed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = HoldoutFixture(Path(temp))
            (Path(temp) / "good.md").write_text(
                "Quy trình còn rườm rà.\n\nBản dịch giữ nghĩa của nguyên tác. Đội ngũ đã chốt kế hoạch quý.\n",
                encoding="utf-8",
            )
            report = h.score(fixture.runs())
        good = self.row(report, "0.17.0")
        self.assertEqual(good["lexicon_kind"], {"fixed": 2, "total": 3})
        self.assertEqual(good["out_of_span"]["pending"], 1)

    def test_manifest_hash_mismatch_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = HoldoutFixture(Path(temp))
            with self.assertRaises(ValueError):
                h.score(fixture.runs(corpus_manifest_sha256="0" * 64))


class AlignmentTest(unittest.TestCase):
    def test_same_paragraph_wins_over_a_closer_neighbour(self) -> None:
        source = ["Quy trình còn rườm.", "Quy trình còn rườm lắm."]
        output = ["Quy trình còn rườm rà.", "Quy trình còn rườm lắm."]
        row = {"paragraph": 1, "span": "còn rườm", "fixes": ["còn rườm rà"]}
        self.assertEqual(h.align(source, output, row), "Quy trình còn rườm rà.")

    def test_neighbour_used_when_paragraph_moved(self) -> None:
        source = ["Mở bài ngắn.", "Quy trình còn rườm."]
        output = ["Quy trình còn rườm rà."]
        row = {"paragraph": 2, "span": "còn rườm", "fixes": ["còn rườm rà"]}
        self.assertEqual(h.align(source, output, row), "Quy trình còn rườm rà.")

    def test_word_offsets_survive_extra_whitespace(self) -> None:
        source = h.paragraphs("Quy  trình\tcòn   rườm.\n\nĐội đã  chốt.")
        ranges = h.spans_in_source(source, [{"paragraph": 1, "span": "còn rườm"}, {"paragraph": 2, "span": "đã chốt"}])
        self.assertEqual(ranges, [(2, 4), (5, 7)])

    def test_rows_after_a_later_heading_are_not_read(self) -> None:
        text = sheet(ARTICLE).replace("## Bảng cần giữ", "### Ghi chú\n\n| 9 | 1 | x | khác | | |\n\n## Bảng cần giữ")
        self.assertEqual(len(h.parse_sheet(text)["errors"]), 4)


class ManifestTest(unittest.TestCase):
    def test_manifest_lists_hashes_not_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = HoldoutFixture(Path(temp))
            manifest = fixture.manifest
        self.assertEqual([a["id"] for a in manifest["articles"]], ["H01"])
        self.assertEqual(manifest["articles"][0]["article_sha256"], hashlib.sha256(ARTICLE.encode()).hexdigest())
        self.assertNotIn("rườm", json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    unittest.main()
