#!/usr/bin/env python3
"""Trang chấm phiếu holdout của spec 036 (contracts/holdout-marking-sheet.md), chạy trên máy người chấm.

  python3 benchmarks/holdout_marker.py <thư-mục-bài>

Script mở một máy chủ chỉ nghe ở 127.0.0.1, mở trình duyệt vào trang chấm và ghi phiếu Hnn.sheet.md cạnh
từng bài Hnn.md (hoặc Dnn của bộ phát triển spec 037) mỗi khi người chấm thêm, sửa hoặc xoá một dòng. Thể loại và model sinh bài lấy từ
plan.json ở thư mục cha nếu có. Chỉ dùng thư viện chuẩn, không gọi mạng ra ngoài, không đọc file nào ngoài
thư mục bài và plan.json. Agent chỉ viết và kiểm script này bằng bài giả; bài thật chỉ người chấm đọc.
"""

from __future__ import annotations

import datetime
import http.server
import json
import re
import secrets
import sys
import threading
import webbrowser
from pathlib import Path

try:
    from benchmarks import holdout_036 as h
except ImportError:  # chạy trực tiếp bằng python3 benchmarks/holdout_marker.py
    import holdout_036 as h

ARTICLE_ID = re.compile(h.ARTICLE_ID)
MAX_BODY = 1_000_000


def article_path(root: Path, article: str, suffix: str) -> Path:
    if not ARTICLE_ID.fullmatch(article):
        raise ValueError("mã bài phải có dạng Hnn hoặc Dnn")
    return h.inside(root, root / f"{article}{suffix}")


def plan_entries(root: Path) -> dict:
    plan = root.parent / "plan.json"
    if not plan.is_file():
        return {}
    try:
        return {e["id"]: e for e in json.loads(plan.read_text(encoding="utf-8")) if isinstance(e, dict) and "id" in e}
    except (ValueError, TypeError, KeyError):
        return {}


def clean(value: object, field: str, limit: int = 300) -> str:
    text = h.nfc(str(value or "")).strip()
    if "|" in text or "\n" in text or len(text) > limit:
        raise ValueError(f"{field}: không được chứa dấu | hay xuống dòng, tối đa {limit} ký tự")
    return text


META_FORBIDDEN = re.compile(r"#|SHA-256|Bài:|Trạng thái:|Thể loại:|Model sinh bài:|Ngày đánh dấu:|Người đánh dấu:")


def clean_meta(meta: dict, key: str, field: str) -> str:
    value = clean(meta.get(key), field)
    if META_FORBIDDEN.search(value):
        raise ValueError(f"{field}: không được chứa #, SHA-256 hay nhãn của đầu phiếu")
    return value


def utf16(text: str, offset: int) -> int:
    """Vị trí theo đơn vị UTF-16 như chuỗi trong trình duyệt."""
    return len(text[:offset].encode("utf-16-le")) // 2


def check_span(paragraphs: list[str], number: int, span: str, label: str) -> None:
    if not span:
        raise ValueError(f"{label}: cụm trống")
    if not 1 <= number <= len(paragraphs):
        raise ValueError(f"{label}: không có đoạn {number}")
    text = paragraphs[number - 1]
    count = text.count(span)
    if count == 0:
        raise ValueError(f"{label}: cụm không có trong đoạn {number}")
    if count > 1:
        raise ValueError(f"{label}: cụm xuất hiện {count} lần trong đoạn; bôi dài hơn cho duy nhất")
    if not any(span in sentence for _, sentence in h.split_sentences(text)):
        raise ValueError(f"{label}: cụm vắt qua hai câu; chỉ bôi trong một câu")


def build_sheet(article: str, digest: str, paragraphs: list[str], meta: dict, errors: list, guards: list) -> str:
    """Phiếu đúng mẫu contract; từ chối dòng mà holdout_036.py sẽ từ chối."""
    lines = [
        f"Bài: {article}            Thể loại: {clean_meta(meta, 'genre', 'Thể loại')}        "
        f"Model sinh bài: {clean_meta(meta, 'model', 'Model sinh bài')}",
        f"Ngày đánh dấu: {clean_meta(meta, 'date', 'Ngày')}   Người đánh dấu: {clean_meta(meta, 'marker', 'Người đánh dấu')}"
        f"   SHA-256 bài: {digest}",
        f"Trạng thái: {'xong' if meta.get('done') else 'đang chấm'}",
        "",
        "## Bảng lỗi",
        "",
        "| # | Đoạn | Cụm như trong bài | Nhóm | Sửa chấp nhận | Ghi chú |",
        "|---|---|---|---|---|---|",
    ]
    for n, row in enumerate(errors, 1):
        label = f"lỗi {n}"
        span, kind = clean(row.get("span"), label), clean(row.get("kind"), label)
        number = int(row.get("paragraph", 0))
        check_span(paragraphs, number, span, label)
        if kind not in h.LEXICON_KINDS and not h.OTHER_KIND.match(kind):
            raise ValueError(f"{label}: Nhóm không hợp lệ: {kind}")
        fixes = [f.strip() for f in clean(row.get("fixes"), label).split("/") if f.strip()]
        if span in fixes:
            raise ValueError(f"{label}: cách sửa trùng cụm lỗi")
        lines.append(f"| {n} | {number} | {span} | {kind} | {' / '.join(fixes)} | {clean(row.get('note'), label)} |")
    lines += ["", "## Bảng cần giữ", "", "| # | Đoạn | Cụm phải giữ nguyên | Vì sao |", "|---|---|---|---|"]
    for n, row in enumerate(guards, 1):
        label = f"cụm giữ {n}"
        span, number = clean(row.get("span"), label), int(row.get("paragraph", 0))
        check_span(paragraphs, number, span, label)
        lines.append(f"| {n} | {number} | {span} | {clean(row.get('reason'), label)} |")
    text = "\n".join(lines) + "\n"
    parsed = h.parse_sheet(text)  # cùng bộ đọc với bộ chấm; phải đọc lại đúng những gì vừa ghi
    if (parsed["article"], parsed["article_sha256"]) != (article, digest) or \
            [r["span"] for r in parsed["errors"]] != [r.get("span") and h.nfc(r["span"]).strip() for r in errors] or \
            [r["span"] for r in parsed["guards"]] != [r.get("span") and h.nfc(r["span"]).strip() for r in guards]:
        raise ValueError("phiếu ghi ra không đọc lại đúng; kiểm tra các ô đầu phiếu")
    return text


def read_sheet(path: Path) -> dict:
    if not path.is_file():
        return {"errors": [], "guards": [], "meta": {}}
    text = h.nfc(path.read_text(encoding="utf-8"))
    meta = {}
    for key, pattern in (("genre", r"Thể loại:\s*(.*?)\s{2,}"), ("model", r"Model sinh bài:\s*(.*)"),
                         ("date", r"Ngày đánh dấu:\s*(\S+)"), ("marker", r"Người đánh dấu:\s*(.*?)\s{2,}")):
        found = re.search(pattern, text)
        if found:
            meta[key] = found[1].strip()
    meta["done"] = bool(re.search(r"^Trạng thái:\s*xong\s*$", text, re.M))
    errors = [{"paragraph": int(c[1]), "span": c[2], "kind": c[3], "fixes": c[4], "note": c[5]}
              for c in h.table_rows(text, "## Bảng lỗi", 6)]
    guards = [{"paragraph": int(c[1]), "span": c[2], "reason": c[3]} for c in h.table_rows(text, "## Bảng cần giữ", 4)]
    return {"errors": errors, "guards": guards, "meta": meta}


def default_meta(entry: dict) -> dict:
    model = " / ".join(x for x in (entry.get("generator"), entry.get("model")) if x)
    return {"genre": entry.get("genre", ""), "model": model, "marker": "Fio",
            "date": datetime.date.today().strftime("%d/%m/%Y")}


class Marker:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.plan = plan_entries(self.root)
        self.lock = threading.Lock()

    def articles(self) -> list:
        found = []
        for path in sorted(p for p in self.root.glob("*.md") if ARTICLE_ID.fullmatch(p.stem)):
            try:
                sheet_path = h.inside(self.root, path.with_name(f"{path.stem}.sheet.md"))
                h.inside(self.root, path)
            except ValueError:
                continue
            sheet = read_sheet(sheet_path)
            entry = self.plan.get(path.stem, {})
            found.append({"id": path.stem, "genre": entry.get("genre", ""), "errors": len(sheet["errors"]),
                          "guards": len(sheet["guards"]), "done": bool(sheet["meta"].get("done"))})
        return found

    def article(self, article: str) -> dict:
        path = article_path(self.root, article, ".md")
        sheet = read_sheet(article_path(self.root, article, ".sheet.md"))
        meta = {**default_meta(self.plan.get(article, {})), **sheet["meta"]}
        paras = h.paragraphs(path.read_text(encoding="utf-8"))
        sentences = [[[utf16(p, o), utf16(p, o + len(s))] for o, s in h.split_sentences(p)] for p in paras]
        return {"id": article, "paragraphs": paras, "sentences": sentences, "meta": meta,
                "errors": sheet["errors"], "guards": sheet["guards"]}

    def save(self, article: str, body: dict) -> dict:
        path = article_path(self.root, article, ".md")
        paras = h.paragraphs(path.read_text(encoding="utf-8"))
        text = build_sheet(article, h.sha256(path), paras, body.get("meta", {}),
                           body.get("errors", []), body.get("guards", []))
        with self.lock:
            target = article_path(self.root, article, ".sheet.md")
            tmp = target.with_name(f".{target.name}.tmp")
            tmp.write_text(text, encoding="utf-8")
            tmp.replace(target)
        return {"saved": target.name}


def make_handler(marker: Marker, token: str, page: bytes):
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args):  # không in nội dung bài ra terminal
            pass

        def reply(self, status: int, body: bytes, kind: str = "application/json; charset=utf-8"):
            self.send_response(status)
            self.send_header("Content-Type", kind)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'")
            self.end_headers()
            self.wfile.write(body)

        def json(self, status: int, data: object):
            self.reply(status, json.dumps(data, ensure_ascii=False).encode("utf-8"))

        def allowed(self) -> list | None:
            host = self.headers.get("Host", "")
            parts = self.path.split("?")[0].strip("/").split("/")
            if host.split(":")[0] not in ("127.0.0.1", "localhost") or not parts or parts[0] != token:
                self.json(403, {"error": "sai địa chỉ"})
                return None
            return parts[1:]

        def do_GET(self):
            parts = self.allowed()
            if parts is None:
                return
            try:
                if not parts or parts == [""]:
                    self.reply(200, page, "text/html; charset=utf-8")
                elif parts == ["api", "articles"]:
                    self.json(200, marker.articles())
                elif len(parts) == 3 and parts[:2] == ["api", "article"]:
                    self.json(200, marker.article(parts[2]))
                else:
                    self.json(404, {"error": "không có"})
            except (ValueError, OSError) as exc:
                self.json(400, {"error": str(exc)})

        def do_POST(self):
            parts = self.allowed()
            if parts is None:
                return
            if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                self.json(415, {"error": "cần JSON"})
                return
            length = int(self.headers.get("Content-Length") or 0)
            if not 0 < length <= MAX_BODY or len(parts) != 3 or parts[:2] != ["api", "sheet"]:
                self.json(400, {"error": "yêu cầu không hợp lệ"})
                return
            try:
                self.json(200, marker.save(parts[2], json.loads(self.rfile.read(length))))
            except (ValueError, TypeError, AttributeError, OSError) as exc:
                self.json(400, {"error": str(exc)})

    return Handler


def main(argv: list[str]) -> int:
    if len(argv) != 2 or not Path(argv[1]).is_dir():
        print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
        return 2
    marker = Marker(Path(argv[1]))
    token = secrets.token_urlsafe(16)
    page = (Path(__file__).with_name("holdout_marker.html")).read_bytes()
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), make_handler(marker, token, page))
    url = f"http://127.0.0.1:{server.server_address[1]}/{token}/"
    print(f"Trang chấm: {url}\nBấm Ctrl+C để dừng. Phiếu được ghi cạnh bài sau mỗi thay đổi.")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
