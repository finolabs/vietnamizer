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
        self.assertEqual(bad["over_corrections"], 2)  # một sửa ngoài cụm "sai" và một cụm cần giữ bị phá

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
        row = {"id": "H01#1", "paragraph": 1, "span": "còn rườm", "fixes": ["còn rườm rà"]}
        self.assertEqual(h.alignments(source, output, [row])["H01#1"], "Quy trình còn rườm rà.")

    def test_neighbour_used_when_paragraph_moved(self) -> None:
        source = ["Mở bài ngắn.", "Quy trình còn rườm."]
        output = ["Quy trình còn rườm rà."]
        row = {"id": "H01#1", "paragraph": 2, "span": "còn rườm", "fixes": ["còn rườm rà"]}
        self.assertEqual(h.alignments(source, output, [row])["H01#1"], "Quy trình còn rườm rà.")

    def test_spans_keep_extra_whitespace(self) -> None:
        source = h.paragraphs("Quy  trình\tcòn   rườm.\n\nĐội đã  chốt.")
        rows = [{"id": "H01#1", "paragraph": 1, "span": "còn   rườm", "fixes": ["còn rườm rà"]},
                {"id": "H01#2", "paragraph": 2, "span": "đã  chốt", "fixes": ["đã chốt"]}]
        result = h.compare("H01", source, h.paragraphs("Quy  trình\tcòn rườm rà.\n\nĐội đã chốt."), rows)
        self.assertEqual([result["rows"][r]["fixed"] for r in ("H01#1", "H01#2")], [True, True])
        self.assertEqual(result["edits"], [])

    def test_rows_after_a_later_heading_are_not_read(self) -> None:
        text = sheet(ARTICLE).replace("## Bảng cần giữ", "### Ghi chú\n\n| 9 | 1 | x | khác | | |\n\n## Bảng cần giữ")
        self.assertEqual(len(h.parse_sheet(text)["errors"]), 4)


class ReviewRegressionTest(unittest.TestCase):
    def test_one_output_sentence_cannot_serve_two_source_sentences(self) -> None:
        source = ["Quy trình A còn rườm. Quy trình B còn rườm."]
        output = ["Quy trình B còn rườm rà."]
        rows = [{"id": "H01#1", "paragraph": 1, "span": "A còn rườm", "fixes": ["còn rườm rà"]},
                {"id": "H01#2", "paragraph": 1, "span": "B còn rườm", "fixes": ["còn rườm rà"]}]
        aligned = h.alignments(source, output, rows)
        self.assertIsNone(aligned["H01#1"])
        self.assertEqual(aligned["H01#2"], "Quy trình B còn rườm rà.")

    def test_edit_spilling_outside_a_span_is_listed(self) -> None:
        source = ["Quy trình còn rườm."]
        output = ["Quy trình vẫn rườm rà."]
        rows = [{"id": "H01#1", "paragraph": 1, "span": "rườm", "fixes": ["rườm rà"]}]
        edits = h.compare("H01", source, output, rows)["edits"]
        self.assertEqual([(e["source"], e["output"]) for e in edits], [("còn", "vẫn")])

    def test_whitespace_change_breaks_a_guard(self) -> None:
        source = ["Bản dịch giữ nghĩa của nguyên tác."]
        output = ["Bản dịch giữ  nghĩa của nguyên tác."]
        rows = [{"id": "H01#g1", "paragraph": 1, "span": "giữ nghĩa của nguyên tác"}]
        self.assertNotIn("giữ nghĩa của nguyên tác", h.alignments(source, output, rows)["H01#g1"])

    def test_duplicate_row_numbers_are_refused(self) -> None:
        text = sheet(ARTICLE).replace("| 2 | 1 | hay bỡ |", "| 1 | 1 | hay bỡ |")
        with self.assertRaises(ValueError):
            h.parse_sheet(text)

    def test_article_id_outside_pattern_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = HoldoutFixture(Path(temp))
            runs = fixture.runs()
            data = json.loads(runs.read_text(encoding="utf-8"))
            data["runs"][0]["article"] = "../outside/H01"
            runs.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                h.score(runs)

    def test_article_symlink_outside_folder_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            corpus = Path(temp) / "corpus"
            corpus.mkdir()
            fixture = HoldoutFixture(corpus)
            outside = Path(temp) / "H02.md"
            outside.write_text(ARTICLE, encoding="utf-8")
            (corpus / "H02.md").symlink_to(outside)
            with self.assertRaises(ValueError):
                h.manifest(corpus)
            self.assertTrue(fixture.manifest["manifest_sha256"])


def custom_sheet(article_id: str, article: str, errors: list[tuple], guards: list[tuple]) -> str:
    digest = hashlib.sha256(article.encode("utf-8")).hexdigest()
    error_lines = "\n".join(f"| {n} | {p} | {span} | {kind} | {fixes} | |"
                            for n, (p, span, kind, fixes) in enumerate(errors, 1))
    guard_lines = "\n".join(f"| {n} | {p} | {span} | lý do |" for n, (p, span) in enumerate(guards, 1))
    return f"""Bài: {article_id}   SHA-256 bài: {digest}

## Bảng lỗi

| # | Đoạn | Cụm như trong bài | Nhóm | Sửa chấp nhận | Ghi chú |
|---|---|---|---|---|---|
{error_lines}

## Bảng cần giữ

| # | Đoạn | Cụm phải giữ nguyên | Vì sao |
|---|---|---|---|
{guard_lines}
"""


def corpus(root: Path, articles: dict[str, tuple[str, list, list]], runs: list[tuple[str, str, str]]) -> Path:
    """articles: id -> (bài, dòng lỗi, dòng cần giữ); runs: (mã bài, version, văn bản đầu ra)."""
    for article_id, (text, errors, guards) in articles.items():
        (root / f"{article_id}.md").write_text(text, encoding="utf-8")
        (root / f"{article_id}.sheet.md").write_text(custom_sheet(article_id, text, errors, guards), encoding="utf-8")
    entries = []
    for n, (article_id, version, text) in enumerate(runs):
        (root / f"out{n}.md").write_text(text, encoding="utf-8")
        entries.append({"article": article_id, "model": "m", "host": "h", "version": version,
                        "label": f"L{n}", "output": f"out{n}.md"})
    path = root / "runs.json"
    path.write_text(json.dumps({"schema": 1, "corpus_manifest_sha256": h.manifest(root)["manifest_sha256"],
                                "runs": entries}, ensure_ascii=False), encoding="utf-8")
    return path


class Round4RegressionTest(unittest.TestCase):
    def by_version(self, report: dict) -> dict:
        return {r["version"]: r for r in report["results"]}

    def test_deleted_marked_sentence_is_not_aligned_to_an_unmarked_neighbour(self) -> None:
        article = "Quy trình A còn rườm. Quy trình B còn rườm rà.\n"
        with tempfile.TemporaryDirectory() as temp:
            runs = corpus(Path(temp), {"H01": (article, [(1, "A còn rườm", "từ ghép bị cắt", "còn rườm rà")], [])},
                          [("H01", "v1", "Quy trình B còn rườm rà.\n")])
            report, edits = h.score(runs), h.blind_edits(runs)
        self.assertEqual(self.by_version(report)["v1"]["lexicon_kind"], {"fixed": 0, "total": 1})
        self.assertEqual([e["source"] for e in edits["edits"]], ["Quy trình A còn rườm."])

    def test_unchanged_span_containing_its_fix_is_not_fixed(self) -> None:
        article = "Nhóm tiến hành thực hiện kế hoạch.\n"
        with tempfile.TemporaryDirectory() as temp:
            runs = corpus(Path(temp), {"H01": (article, [(1, "tiến hành thực hiện", "dịch sát", "thực hiện")], [])},
                          [("H01", "same", article), ("H01", "fixed", "Nhóm thực hiện kế hoạch.\n"),
                           ("H01", "suffix", "Nhóm tiến hành thực hiện ngay kế hoạch.\n")])
            results = self.by_version(h.score(runs))
        self.assertEqual(results["same"]["lexicon_kind"]["fixed"], 0)
        self.assertEqual(results["fixed"]["lexicon_kind"]["fixed"], 1)
        self.assertEqual(results["suffix"]["lexicon_kind"]["fixed"], 0)

    def test_deletion_just_before_an_unchanged_span_is_not_a_fix(self) -> None:
        source = ["Nhóm rất,tiến hành thực hiện kế hoạch."]
        output = ["Nhóm tiến hành thực hiện kế hoạch."]
        rows = [{"id": "H01#1", "paragraph": 1, "span": "tiến hành thực hiện", "fixes": ["thực hiện"]}]
        result = h.compare("H01", source, output, rows)
        self.assertFalse(result["rows"]["H01#1"]["fixed"])
        self.assertEqual([(e["source"], e["output"]) for e in result["edits"]], [("rất,", "")])

    def test_punctuation_and_whitespace_edits_next_to_a_span_are_listed(self) -> None:
        article = "Quy trình còn rườm.\n"
        with tempfile.TemporaryDirectory() as temp:
            runs = corpus(Path(temp), {"H01": (article, [(1, "rườm", "từ ghép bị cắt", "rườm rà")], [])},
                          [("H01", "bang", "Quy trình còn rườm rà!\n"), ("H01", "space", "Quy trình  còn rườm rà.\n")])
            edits = h.blind_edits(runs)
            results = self.by_version(h.score(runs))
        self.assertEqual(sorted((e["source"], e["output"]) for e in edits["edits"]), [(" ", "  "), (".", "!")])
        self.assertEqual(results["bang"]["lexicon_kind"]["fixed"], 1)

    def test_table_line_without_outer_pipes_is_refused(self) -> None:
        text = sheet(ARTICLE).replace("| 2 | 1 | hay bỡ | từ ghép bị cắt | hay bỡ ngỡ | |",
                                      "2 | 1 | hay bỡ | từ ghép bị cắt | hay bỡ ngỡ |")
        with self.assertRaises(ValueError):
            h.parse_sheet(text)

    def test_edit_ids_keep_articles_apart_and_dedupe_versions(self) -> None:
        article = "Quy trình còn rườm. Kết thúc.\n"
        output = "Quá trình còn rườm rà. Kết thúc.\n"
        row = ([(1, "còn rườm", "từ ghép bị cắt", "còn rườm rà")], [])
        with tempfile.TemporaryDirectory() as temp:
            runs = corpus(Path(temp), {"H01": (article, *row), "H02": (article, *row)},
                          [("H01", "v1", output), ("H01", "v2", output), ("H02", "v1", output)])
            edits = h.blind_edits(runs)["edits"]
        self.assertEqual([e["article"] for e in edits], ["H01", "H02"])
        self.assertNotEqual(edits[0]["id"], edits[1]["id"])


class Round5RegressionTest(unittest.TestCase):
    def one(self, source: str, output: str, span: str, fixes: list[str] | None) -> dict:
        row = {"id": "H01#1", "paragraph": 1, "span": span}
        if fixes is not None:
            row["fixes"] = fixes
        result = h.compare("H01", [source], [output], [row])
        return {"row": result["rows"]["H01#1"], "edits": [(e["source"], e["output"]) for e in result["edits"]]}

    def test_fix_must_match_whole_words(self) -> None:
        result = self.one("Nhóm tiến hành thực hiện kế hoạch.", "Nhóm tiến hành thực hiệnx kế hoạch.",
                          "tiến hành thực hiện", ["thực hiện"])
        self.assertFalse(result["row"]["fixed"])

    def test_extra_text_inserted_at_a_span_edge_is_listed(self) -> None:
        result = self.one("Quy trình còn rườm.", "Quy trình còn rườm rà vô lý.", "rườm", ["rườm rà"])
        self.assertTrue(result["row"]["fixed"])
        self.assertEqual(result["edits"], [("", " vô lý")])

    def test_whitespace_between_sentences_is_listed(self) -> None:
        result = h.compare("H01", ["Quy trình tốt. Kết thúc."], ["Quy trình tốt.  Kết thúc."], [])
        self.assertEqual([(e["source"], e["output"]) for e in result["edits"]], [(" ", "  ")])

    def test_broken_guard_counts_as_an_over_correction(self) -> None:
        article = "Bản dịch giữ nghĩa của nguyên tác.\n"
        with tempfile.TemporaryDirectory() as temp:
            runs = corpus(Path(temp), {"H01": (article, [], [(1, "giữ nghĩa")])},
                          [("H01", "v1", "Bản dịch giữ nguyên nghĩa của nguyên tác.\n")])
            result = h.score(runs)["results"][0]
        self.assertEqual(result["guards"]["broken"], 1)
        self.assertEqual(result["over_corrections"], 1)

    def test_header_and_separator_need_the_table_width(self) -> None:
        for bad in ("| # | sai |", "|---|"):
            text = sheet(ARTICLE).replace("| # | Đoạn | Cụm như trong bài | Nhóm | Sửa chấp nhận | Ghi chú |"
                                          if bad.startswith("| #") else "|---|---|---|---|---|---|", bad, 1)
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                h.parse_sheet(text)


class Round6RegressionTest(unittest.TestCase):
    def pieces(self, source: list[str], output: list[str]) -> list[tuple[str, str]]:
        return sorted((e["source"], e["output"]) for e in h.compare("H01", source, output, [])["edits"])

    def test_gap_before_an_inserted_sentence_is_compared(self) -> None:
        self.assertEqual(self.pieces(["Câu một. Câu hai."], ["Câu một.  Câu mới. Câu hai."]),
                         [("", "  "), ("", "Câu mới.")])

    def test_clean_insertion_lists_only_the_sentence(self) -> None:
        self.assertEqual(self.pieces(["Câu một. Câu hai."], ["Câu một. Câu mới. Câu hai."]), [("", "Câu mới.")])

    def test_deleted_sentence_takes_its_gap_with_it(self) -> None:
        self.assertEqual(self.pieces(["Câu một. Câu xoá.", "Câu hai."], ["Câu một.", "Câu hai."]), [("Câu xoá.", "")])

    def test_replaced_gap_around_a_deleted_sentence_is_listed(self) -> None:
        self.assertEqual(self.pieces(["Câu một. Câu xoá. Câu hai."], ["Câu một.\tCâu hai."]),
                         [(" ", "\t"), ("Câu xoá.", "")])


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
