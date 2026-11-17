import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path

from benchmarks import holdout_036 as h
from benchmarks import holdout_marker as m

ARTICLE = (
    "Quy trình còn rườm. Nhân viên mới hay bỡ.\n\n"
    "Bản dịch giữ nghĩa của nguyên tác. Đội đã chốt kế hoạch quý.\n"
)
META = {"genre": "blog cá nhân", "model": "claude / claude-opus-5-5", "date": "17/11/2026", "marker": "Fio"}
ERRORS = [{"paragraph": 1, "span": "còn rườm", "kind": "từ ghép bị cắt", "fixes": "còn rườm rà/ còn rườm rà quá", "note": ""},
          {"paragraph": 2, "span": "Đội đã", "kind": "khác: V12", "fixes": "", "note": "xem lại"}]
GUARDS = [{"paragraph": 2, "span": "giữ nghĩa của nguyên tác", "reason": "đủ ý"}]


class Corpus:
    def __enter__(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        (base / "plan.json").write_text(json.dumps([{"id": "H01", "generator": "claude", "genre": "blog cá nhân"}]),
                                        encoding="utf-8")
        self.root = base / "corpus"
        self.root.mkdir()
        (self.root / "H01.md").write_text(ARTICLE, encoding="utf-8")
        return self.root

    def __exit__(self, *exc):
        self.tmp.cleanup()


class SheetTest(unittest.TestCase):
    def paras(self):
        return h.paragraphs(ARTICLE)

    def test_sheet_round_trips_through_the_scorer(self):
        text = m.build_sheet("H01", "a" * 64, self.paras(), META, ERRORS, GUARDS)
        parsed = h.parse_sheet(text)
        self.assertEqual([r["span"] for r in parsed["errors"]], ["còn rườm", "Đội đã"])
        self.assertEqual(parsed["errors"][0]["fixes"], ["còn rườm rà", "còn rườm rà quá"])
        self.assertEqual(parsed["errors"][1]["kind"], "khác: V12")
        self.assertEqual(parsed["guards"][0]["span"], "giữ nghĩa của nguyên tác")

    def test_read_sheet_restores_rows_and_status(self):
        with Corpus() as root:
            path = root / "H01.sheet.md"
            path.write_text(m.build_sheet("H01", "a" * 64, self.paras(), {**META, "done": True}, ERRORS, GUARDS),
                            encoding="utf-8")
            got = m.read_sheet(path)
        self.assertEqual(got["errors"][1]["note"], "xem lại")
        self.assertEqual(got["guards"][0]["reason"], "đủ ý")
        self.assertTrue(got["meta"]["done"])
        self.assertEqual(got["meta"]["model"], "claude / claude-opus-5-5")

    def test_refuses_rows_the_scorer_would_refuse(self):
        bad = [
            ({"paragraph": 1, "span": "rườm. Nhân", "kind": "dịch sát"}, "vắt qua hai câu"),
            ({"paragraph": 1, "span": "không có", "kind": "dịch sát"}, "không có trong đoạn"),
            ({"paragraph": 3, "span": "Đội", "kind": "dịch sát"}, "không có đoạn"),
            ({"paragraph": 1, "span": "còn", "kind": "lạ"}, "Nhóm không hợp lệ"),
            ({"paragraph": 1, "span": "còn", "kind": "dịch sát", "fixes": "còn"}, "trùng cụm"),
            ({"paragraph": 1, "span": "còn", "kind": "dịch sát", "note": "a|b"}, "dấu |"),
        ]
        for row, message in bad:
            with self.subTest(row=row), self.assertRaisesRegex(ValueError, message):
                m.build_sheet("H01", "a" * 64, self.paras(), META, [row], [])

    def test_refuses_a_span_repeated_in_its_paragraph(self):
        paras = ["Đội làm. Đội nghỉ."]
        with self.assertRaisesRegex(ValueError, "xuất hiện 2 lần"):
            m.build_sheet("H01", "a" * 64, paras, META, [], [{"paragraph": 1, "span": "Đội"}])

    def test_metadata_cannot_hide_rows_or_the_digest(self):
        for key, value in (("genre", "## Bảng lỗi"), ("model", "x SHA-256 bài: " + "b" * 64), ("marker", "Bài: H02")):
            with self.subTest(key=key), self.assertRaises(ValueError):
                m.build_sheet("H01", "a" * 64, self.paras(), {**META, key: value}, ERRORS, GUARDS)

    def test_sentence_offsets_are_utf16_units_like_the_browser(self):
        with Corpus() as root:
            (root / "H01.md").write_text("\U0001F600. Lỗi ở đây.\n", encoding="utf-8")
            data = m.Marker(root).article("H01")
        self.assertEqual(data["sentences"][0], [[0, 3], [4, 14]])

    def test_rejects_ids_outside_the_folder(self):
        with Corpus() as root:
            for article in ("../H01", "H1", "H01/x"):
                with self.subTest(article=article), self.assertRaises(ValueError):
                    m.article_path(root, article, ".md")


class ServerTest(unittest.TestCase):
    def setUp(self):
        self.corpus = Corpus()
        self.root = self.corpus.__enter__()
        handler = m.make_handler(m.Marker(self.root), "tok", b"<html></html>")
        self.server = m.http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.port = self.server.server_address[1]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.corpus.__exit__()

    def call(self, method, path, body=None, host=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port)
        headers = {"Host": host or f"127.0.0.1:{self.port}"}
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        conn.request(method, path, data, headers)
        reply = conn.getresponse()
        return reply.status, reply.read()

    def test_saves_a_sheet_the_scorer_accepts(self):
        status, _ = self.call("POST", "/tok/api/sheet/H01", {"meta": META, "errors": ERRORS, "guards": GUARDS})
        self.assertEqual(status, 200)
        parsed = h.parse_sheet((self.root / "H01.sheet.md").read_text(encoding="utf-8"))
        self.assertEqual(parsed["article_sha256"], h.sha256(self.root / "H01.md"))
        status, body = self.call("GET", "/tok/api/article/H01")
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertEqual(len(data["errors"]), 2)
        self.assertEqual(data["paragraphs"], h.paragraphs(ARTICLE))
        self.assertEqual(data["meta"]["genre"], "blog cá nhân")

    def test_bad_row_is_refused_and_leaves_the_sheet(self):
        self.call("POST", "/tok/api/sheet/H01", {"meta": META, "errors": ERRORS, "guards": []})
        before = (self.root / "H01.sheet.md").read_text(encoding="utf-8")
        status, body = self.call("POST", "/tok/api/sheet/H01",
                                 {"meta": META, "errors": [{"paragraph": 1, "span": "x", "kind": "dịch sát"}], "guards": []})
        self.assertEqual(status, 400)
        self.assertIn("không có trong đoạn", json.loads(body)["error"])
        self.assertEqual((self.root / "H01.sheet.md").read_text(encoding="utf-8"), before)

    def test_needs_token_and_local_host(self):
        self.assertEqual(self.call("GET", "/api/articles")[0], 403)
        self.assertEqual(self.call("GET", "/tok/api/articles", host="evil.example")[0], 403)
        self.assertEqual(self.call("GET", "/tok/api/articles")[0], 200)
        self.assertEqual(self.call("GET", "/tok/api/article/..%2FH01")[0], 400)


if __name__ == "__main__":
    unittest.main()
