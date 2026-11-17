#!/usr/bin/env python3
"""Chấm tất định bộ holdout của spec 036 (research.md R6, contracts/holdout-marking-sheet.md).

Chỉ nằm trong repo, không vào gói. Bài, phiếu đánh dấu và đầu ra nằm ngoài Git; repo chỉ giữ manifest
SHA-256. Script không gọi model, không gọi mạng; chỉ đọc file người chạy chỉ định.

  python3 benchmarks/holdout_036.py manifest <thư-mục-bài>
  python3 benchmarks/holdout_036.py edits <runs.json>
  python3 benchmarks/holdout_036.py score <runs.json> [<judgments.json>]

Thư mục bài chứa H01.md và H01.sheet.md, H02.md và H02.sheet.md, ... runs.json ghi từng đầu ra:
{"schema": 1, "corpus_manifest_sha256": "...", "lexicon_sha256": "...", "runs": [{"article": "H01",
"model": "...", "host": "...", "version": "0.17.0", "label": "K2", "output": "out/K2.md",
"seconds": 30.5, "tokens": 1200}]}. Đường dẫn tính từ thư mục của runs.json; bài và phiếu nằm cùng
thư mục đó. judgments.json do Fio ghi: {"edits": {"<id>": "đúng|không cần|sai"},
"rows": {"H01#4": {"K2": "fixed|not"}}}; nhãn đầu ra là nhãn ngẫu nhiên, không lộ version.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

LEXICON_KINDS = {"từ ghép bị cắt", "dịch sát", "từ nghề hiểu sai", "danh từ tập thể đứng trơ"}
OTHER_KIND = re.compile(r"^khác(?:: [VT]\d+)?$")
SENTENCE_END = re.compile(r"(?<=[.!?…])\s+")
TOKEN = re.compile(r"\w+|\s+|[^\w\s]")
VERDICTS = ("đúng", "không cần", "sai")
ALIGN_MIN = 0.5


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def paragraphs(text: str) -> list[str]:
    """Đoạn sau NFC; chỉ chỗ xuống dòng trong đoạn thành một dấu cách, mọi khoảng trắng khác giữ nguyên."""
    return [re.sub(r"[ \t]*\n[ \t]*", " ", p.strip()) for p in re.split(r"\n[ \t]*\n", nfc(text)) if p.strip()]


def inside(root: Path, path: Path) -> Path:
    resolved = path.resolve()
    if root.resolve() not in resolved.parents:
        raise ValueError(f"{path.name} phải nằm trong thư mục của bộ bài")
    return resolved


def split_sentences(paragraph: str) -> list[tuple[int, str]]:
    """Câu của một đoạn kèm vị trí ký tự đầu câu; khoảng trắng giữa hai câu không thuộc câu nào."""
    found, start = [], 0
    for gap in SENTENCE_END.finditer(paragraph):
        found.append((start, paragraph[start:gap.start()]))
        start = gap.end()
    found.append((start, paragraph[start:]))
    return [(offset, text) for offset, text in found if text]


def article_sentences(source: list[str]) -> list[tuple[int, str, str]]:
    """Mọi câu của bài theo thứ tự: số thứ tự đoạn (từ 0), câu, và khoảng ngăn với câu sau (khoảng trắng
    trong đoạn, hai dấu xuống dòng khi câu sau sang đoạn mới, rỗng ở câu cuối)."""
    found = []
    for p, paragraph in enumerate(source):
        parts = split_sentences(paragraph)
        for n, (offset, text) in enumerate(parts):
            gap = paragraph[offset + len(text):parts[n + 1][0]] if n + 1 < len(parts) else "\n\n"
            found.append((p, text, gap))
    if found:
        found[-1] = (found[-1][0], found[-1][1], "")
    return found


def table_rows(text: str, heading: str, width: int) -> list[list[str]]:
    """Dòng dữ liệu của một bảng. Trong mục của bảng, dòng nào có dấu | phải là dòng bảng đủ hai dấu |
    ngoài cùng và đủ số ô; dòng không có | là ghi chú và được bỏ qua."""
    if heading not in text:
        raise ValueError(f"phiếu thiếu mục {heading}")
    block = re.split(r"\n#{1,6} ", text.split(heading, 1)[1], maxsplit=1)[0]
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if "|" not in line:
            continue
        if not (line.startswith("|") and line.endswith("|") and len(line) > 1):
            raise ValueError(f"dòng bảng phải mở và đóng bằng |: {line[:40]}")
        cells = [c.strip() for c in line[1:-1].split("|")]
        if len(cells) != width:
            raise ValueError(f"dòng phiếu phải có {width} ô: {line[:40]}")
        if cells[0] == "#" or re.match(r"^\|[\s:|-]+\|$", line):
            continue
        rows.append(cells)
    return rows


def parse_sheet(text: str) -> dict:
    text = nfc(text)
    article = re.search(r"Bài:\s*(H\d{2})\b", text)
    digest = re.search(r"SHA-256 bài:\s*([0-9a-f]{64})", text)
    if not article or not digest:
        raise ValueError("phiếu thiếu mã bài hoặc SHA-256 bài")
    errors = []
    seen_numbers: set[str] = set()
    for cells in table_rows(text, "## Bảng lỗi", 6):
        if not cells[0].isdigit() or cells[0] in seen_numbers:
            raise ValueError(f"số dòng lỗi phải là số và không trùng: {cells[0]}")
        seen_numbers.add(cells[0])
        number, paragraph, span, kind, fixes = cells[:5]
        if kind not in LEXICON_KINDS and not OTHER_KIND.match(kind):
            raise ValueError(f"Nhóm không hợp lệ ở dòng lỗi {number}: {kind}")
        fix_list = [f.strip() for f in fixes.split(" / ") if f.strip()]
        if span in fix_list:
            raise ValueError(f"dòng lỗi {number}: cách sửa trùng cụm lỗi")
        errors.append({
            "id": f"{article[1]}#{number}", "paragraph": int(paragraph), "span": span, "kind": kind,
            "lexicon_kind": kind in LEXICON_KINDS,
            "fixes": fix_list,
        })
    guard_rows = table_rows(text, "## Bảng cần giữ", 4)
    numbers = [cells[0] for cells in guard_rows]
    if not all(n.isdigit() for n in numbers) or len(set(numbers)) != len(numbers):
        raise ValueError("số dòng cần giữ phải là số và không trùng")
    guards = [
        {"id": f"{article[1]}#g{cells[0]}", "paragraph": int(cells[1]), "span": cells[2]}
        for cells in guard_rows
    ]
    return {"article": article[1], "article_sha256": digest[1], "errors": errors, "guards": guards}


def manifest(directory: Path) -> dict:
    articles = []
    for path in sorted(directory.glob("H[0-9][0-9].md")):
        inside(directory, path)
        sheet = path.with_name(f"{path.stem}.sheet.md")
        if sheet.exists():
            inside(directory, sheet)
        articles.append({
            "id": path.stem,
            "article_sha256": sha256(path),
            "sheet_sha256": sha256(sheet) if sheet.is_file() else None,
        })
    body = json.dumps(articles, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return {"schema": 1, "articles": articles, "manifest_sha256": hashlib.sha256(body).hexdigest()}


def load_corpus(runs_path: Path) -> tuple[dict, dict, dict]:
    data = json.loads(runs_path.read_text(encoding="utf-8"))
    if data.get("schema") != 1:
        raise ValueError("runs.json phải có schema 1")
    root = runs_path.parent
    found = manifest(root)
    if found["manifest_sha256"] != data.get("corpus_manifest_sha256"):
        raise ValueError("manifest của bộ bài khác giá trị ghi trong runs.json")
    sheets = {}
    for article in {run["article"] for run in data["runs"]}:
        if not isinstance(article, str) or not re.fullmatch(r"H[0-9]{2}", article):
            raise ValueError("mã bài trong runs.json phải có dạng Hnn")
        path = inside(root, root / f"{article}.md")
        sheet = parse_sheet(inside(root, root / f"{article}.sheet.md").read_text(encoding="utf-8"))
        if sheet["article"] != article or sheet["article_sha256"] != sha256(path):
            raise ValueError(f"phiếu {article} không khớp SHA-256 của bài")
        source = paragraphs(path.read_text(encoding="utf-8"))
        for row in sheet["errors"] + sheet["guards"]:
            if not 1 <= row["paragraph"] <= len(source) or row["span"] not in source[row["paragraph"] - 1]:
                raise ValueError(f"{row['id']}: cụm không có trong đoạn {row['paragraph']}")
            if source[row["paragraph"] - 1].count(row["span"]) > 1:
                raise ValueError(f"{row['id']}: cụm xuất hiện nhiều lần trong đoạn; chép dài hơn cho duy nhất")
            if not any(row["span"] in text for _, text in split_sentences(source[row["paragraph"] - 1])):
                raise ValueError(f"{row['id']}: cụm vắt qua hai câu; chỉ đánh dấu trong một câu")
        sheets[article] = (sheet, source)
    return data, sheets, found


def ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def align_sentences(src: list[str], out: list[str]) -> list[int | None]:
    """Căn một-một, giữ thứ tự, mọi câu nguồn với câu đầu ra. Câu giống hệt làm mốc (difflib trên danh sách
    câu); trong mỗi khoảng giữa hai mốc, quy hoạch động chọn các cặp giữ thứ tự có tổng ratio lớn nhất,
    chỉ nhận cặp có ratio >= ALIGN_MIN. Câu nguồn không có cặp nhận None."""
    pairs: list[int | None] = [None] * len(src)
    matcher = difflib.SequenceMatcher(None, src, out, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                pairs[i1 + k] = j1 + k
            continue
        n, m = i2 - i1, j2 - j1
        if not n or not m:
            continue
        score = [[ratio(src[i1 + a], out[j1 + b]) for b in range(m)] for a in range(n)]
        best = [[0.0] * (m + 1) for _ in range(n + 1)]
        for a in range(1, n + 1):
            for b in range(1, m + 1):
                take = best[a - 1][b - 1] + score[a - 1][b - 1] if score[a - 1][b - 1] >= ALIGN_MIN else -1.0
                best[a][b] = max(best[a - 1][b], best[a][b - 1], take)
        a, b = n, m
        while a and b:
            r = score[a - 1][b - 1]
            if r >= ALIGN_MIN and best[a][b] == best[a - 1][b - 1] + r:
                pairs[i1 + a - 1] = j1 + b - 1
                a, b = a - 1, b - 1
            elif best[a][b] == best[a - 1][b]:
                a -= 1
            else:
                b -= 1
    return pairs


def char_opcodes(a: str, b: str) -> list[tuple[str, int, int, int, int]]:
    """Diff một cặp câu theo token (cụm chữ, một dãy khoảng trắng, từng dấu câu), trả vị trí ký tự.
    Khoảng trắng và dấu câu là token riêng nên mọi thay đổi của chúng đều hiện ra."""
    spans_a = [m.span() for m in TOKEN.finditer(a)]
    spans_b = [m.span() for m in TOKEN.finditer(b)]
    starts_a = [s for s, _ in spans_a] + [len(a)]
    starts_b = [s for s, _ in spans_b] + [len(b)]
    matcher = difflib.SequenceMatcher(None, [a[s:e] for s, e in spans_a], [b[s:e] for s, e in spans_b],
                                      autojunk=False)
    return [(tag, starts_a[i1], starts_a[i2], starts_b[j1], starts_b[j2])
            for tag, i1, i2, j1, j2 in matcher.get_opcodes()]


def touches(op: tuple, start: int, end: int) -> bool:
    """Khối diff chạm cụm [start, end): đè lên cụm hoặc sát mép cụm (cách sửa có thể nối dài cụm)."""
    _, i1, i2, _, _ = op
    return i1 <= end and i2 >= start


def fix_found(output: str, ops: list[tuple], start: int, end: int, fixes: list[str]) -> tuple[int, int] | None:
    """Vị trí trong đầu ra của cách sửa chấp nhận làm dòng lỗi thành đã sửa, hoặc None.

    Phải có khối diff chạm cụm, và cách sửa phải nằm trong vùng đầu ra của cụm đồng thời gồm phần đầu ra
    vừa đổi (khi cụm bị xoá bớt chữ, chỉ cần nằm trong vùng). Cách sửa có sẵn trong cụm mà cụm không đổi,
    hay chỉ có chữ chèn thêm cạnh nó, không tính là đã sửa."""
    changed = [op for op in ops if op[0] != "equal" and touches(op, start, end)]
    if not changed:
        return None
    low = min([j1 + start - i1 for tag, i1, i2, j1, _ in ops if tag == "equal" and i1 <= start < i2]
              + [op[3] for op in changed])
    high = max([j1 + end - i1 for tag, i1, i2, j1, _ in ops if tag == "equal" and i1 < end <= i2]
               + [op[4] for op in changed])
    deleted = any(j1 == j2 and i1 < end and i2 > start for _, i1, i2, j1, j2 in changed)
    for fix in fixes:
        # Cách sửa phải khớp trọn từ: "thực hiện" không khớp phần đầu của "thực hiệnx".
        pattern = (r"(?<!\w)" if re.match(r"\w", fix) else "") + re.escape(fix)
        pattern += r"(?!\w)" if re.search(r"\w$", fix) else ""
        for found in re.finditer(pattern, output, re.IGNORECASE):
            o1, o2 = found.span()
            if not (o1 < high and o2 > low):
                continue
            if deleted or any(j1 < j2 and o1 < j2 and o2 > j1 for _, _, _, j1, j2 in changed):
                return o1, o2
    return None


def trim(begin: int, finish: int, covered: list[tuple[int, int]]) -> tuple[int, int]:
    """Bỏ phần đầu và phần cuối của [begin, finish) đã thuộc một khoảng trong covered."""
    moved = True
    while moved and begin < finish:
        moved = False
        for s, e in covered:
            if s <= begin < e:
                begin, moved = min(e, finish), True
            if s < finish <= e:
                finish, moved = max(s, begin), True
    return begin, finish


def is_broken(ops: list[tuple], start: int, end: int) -> bool:
    """Cụm cần giữ hỏng khi bất kỳ ký tự nào trong cụm đổi, hoặc có chữ chèn vào giữa cụm."""
    return any(tag != "equal" and ((i1 < end and i2 > start) or (i1 == i2 and start < i1 < end))
               for tag, i1, i2, _, _ in ops)


def inside_spans(op: tuple, judged: list[tuple[int, int]], others: list[tuple[int, int]]) -> bool:
    """Khối diff nằm trọn trong hợp các cụm của câu. Chỗ chèn nằm trong cụm thuộc cụm. Chỗ chèn sát mép chỉ
    thuộc cụm lỗi bỏ trống cách sửa (Fio tự xét cả câu); với cụm lỗi có cách sửa, phần do cách sửa giải
    thích được cắt ở bước sau, còn cụm cần giữ không nhận chữ chèn nào."""
    _, i1, i2, _, _ = op
    if i1 == i2:
        return any(s <= i1 <= e for s, e in judged) or any(s < i1 < e for s, e in others)
    merged: list[list[int]] = []
    for s, e in sorted(judged + others):
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return any(s <= i1 and i2 <= e for s, e in merged)


def edit_id(*key: object) -> str:
    return hashlib.sha256(json.dumps(key, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]


def compare(article: str, source: list[str], output: list[str], rows: list[dict]) -> dict:
    """So một đầu ra với bài nguồn. Trả kết quả từng dòng phiếu (câu đầu ra đã căn, fixed, broken) và
    danh sách sửa ngoài cụm cho Fio: khối diff không nằm trọn trong cụm, câu nguồn không còn câu đầu ra
    tương ứng, câu đầu ra mới. ID sửa = mã bài + số câu nguồn + vị trí ký tự + cũ/mới, nên cùng một sửa
    ở nhiều version/model gộp làm một, còn hai bài khác nhau không bao giờ chung ID."""
    src, out = article_sentences(source), article_sentences(output)
    pairs = align_sentences([t for _, t, _ in src], [t for _, t, _ in out])
    marked: dict[int, list[tuple[dict, int, int]]] = {}
    for row in rows:
        p = row["paragraph"] - 1
        k, text = next((k, t) for k, (q, t, _) in enumerate(src) if q == p and row["span"] in t)
        start = text.index(row["span"])
        marked.setdefault(k, []).append((row, start, start + len(row["span"])))
    results: dict[str, dict] = {}
    edits: list[dict] = []
    for k, (_, text, gap) in enumerate(src):
        j = pairs[k]
        if j is None:
            for row, _, _ in marked.get(k, []):
                results[row["id"]] = {"sentence": None, "fixed": False, "broken": True}
            edits.append({"id": edit_id(article, k, "deleted", text), "sentence": text, "offset": 0,
                          "source": text, "output": "",
                          "guarded": any("fixes" not in row for row, _, _ in marked.get(k, []))})
            continue
        if k + 1 < len(src) and pairs[k + 1] == j + 1 and out[j][2] != gap:
            edits.append({"id": edit_id(article, k, "gap", gap, out[j][2]), "sentence": text,
                          "offset": len(text), "source": gap, "output": out[j][2]})
        ops = char_opcodes(text, out[j][1])
        error_spans = [(s, e) for row, s, e in marked.get(k, []) if "fixes" in row]
        judged_spans = [(s, e) for row, s, e in marked.get(k, []) if "fixes" in row and not row["fixes"]]
        other_spans = [(s, e) for row, s, e in marked.get(k, []) if row.get("fixes") or "fixes" not in row]
        fixes_at: list[tuple[int, int]] = []
        for row, s, e in marked.get(k, []):
            found = fix_found(out[j][1], ops, s, e, row["fixes"]) if row.get("fixes") else None
            if found:
                fixes_at.append(found)
            results[row["id"]] = {
                "sentence": out[j][1],
                "fixed": (found is not None) if row.get("fixes") else None,
                "broken": is_broken(ops, s, e),
            }
        for op in ops:
            if op[0] == "equal" or inside_spans(op, judged_spans, other_spans):
                continue
            # Đầu/cuối khối thuộc cụm lỗi (phía nguồn) hay thuộc cách sửa đã nhận (phía đầu ra) là phần
            # của dòng lỗi; phần còn lại là sửa ngoài cụm, vd. "rườm." -> "rườm rà!" chỉ còn "." -> "!".
            i1, i2 = trim(op[1], op[2], error_spans)
            j1, j2 = trim(op[3], op[4], fixes_at)
            if i1 == i2 and j1 == j2:
                continue
            old, new = text[i1:i2], out[j][1][j1:j2]
            edits.append({"id": edit_id(article, k, i1, old, new), "sentence": text, "offset": i1,
                          "source": old, "output": new})
    owner = {j: k for k, j in enumerate(pairs) if j is not None}
    previous = -1
    for j, (_, text, _) in enumerate(out):
        if j in owner:
            previous = owner[j]
            continue
        context = src[previous][1] if previous >= 0 else ""
        edits.append({"id": edit_id(article, previous, "inserted", text), "sentence": context, "offset": 0,
                      "source": "", "output": text})
    return {"rows": results, "edits": edits}


def alignments(source: list[str], output: list[str], rows: list[dict]) -> dict[str, str | None]:
    """Câu đầu ra đã căn cho từng dòng phiếu; None khi câu nguồn của dòng không còn câu tương ứng."""
    return {key: value["sentence"] for key, value in compare("", source, output, rows)["rows"].items()}


def output_text(runs_path: Path, run: dict) -> list[str]:
    root = runs_path.parent.resolve()
    path = (root / run["output"]).resolve()
    if root not in path.parents:
        raise ValueError(f"đầu ra {run['label']} phải nằm trong thư mục của runs.json")
    return paragraphs(path.read_text(encoding="utf-8"))


def blind_edits(runs_path: Path) -> dict:
    data, sheets, _ = load_corpus(runs_path)
    seen: dict[str, dict] = {}
    for run in data["runs"]:
        sheet, source = sheets[run["article"]]
        output = output_text(runs_path, run)
        for edit in compare(run["article"], source, output, sheet["errors"] + sheet["guards"])["edits"]:
            edit.pop("guarded", None)
            seen.setdefault(edit["id"], {"article": run["article"], **edit})
    return {"schema": 1, "edits": sorted(seen.values(), key=lambda e: (e["article"], e["id"]))}


def score(runs_path: Path, judgments_path: Path | None = None) -> dict:
    data, sheets, found = load_corpus(runs_path)
    judgments = json.loads(judgments_path.read_text(encoding="utf-8")) if judgments_path else {}
    edit_verdicts = judgments.get("edits", {})
    row_verdicts = judgments.get("rows", {})
    groups: dict[tuple[str, str, str], dict] = {}
    for run in data["runs"]:
        sheet, source = sheets[run["article"]]
        output = output_text(runs_path, run)
        compared = compare(run["article"], source, output, sheet["errors"] + sheet["guards"])
        key = (run["model"], run["host"], run["version"])
        group = groups.setdefault(key, {
            "model": run["model"], "host": run["host"], "version": run["version"],
            "lexicon_kind": {"fixed": 0, "total": 0}, "other": {"fixed": 0, "total": 0, "pending": 0},
            "guards": {"broken": 0, "total": 0},
            "out_of_span": {"đúng": 0, "không cần": 0, "sai": 0, "pending": 0},
            "over_corrections": 0, "seconds": 0.0, "tokens": 0, "outputs": 0,
        })
        group["outputs"] += 1
        group["seconds"] += float(run.get("seconds", 0))
        group["tokens"] += int(run.get("tokens", 0))
        for row in sheet["errors"]:
            bucket = group["lexicon_kind"] if row["lexicon_kind"] else group["other"]
            bucket["total"] += 1
            fixed = compared["rows"][row["id"]]["fixed"]
            if fixed is None:
                verdict = row_verdicts.get(row["id"], {}).get(run["label"])
                if verdict is None:
                    bucket["pending"] = bucket.get("pending", 0) + 1
                    continue
                fixed = verdict == "fixed"
            bucket["fixed"] += int(bool(fixed))
        for row in sheet["guards"]:
            group["guards"]["total"] += 1
            broken = int(compared["rows"][row["id"]]["broken"])
            group["guards"]["broken"] += broken
            group["over_corrections"] += broken
        for edit in compared["edits"]:
            verdict = edit_verdicts.get(edit["id"])
            group["out_of_span"][verdict if verdict in VERDICTS else "pending"] += 1
            # Câu bị xoá có cụm cần giữ đã được tính một lần ở guards; không đếm lại khi Fio chấm "sai".
            group["over_corrections"] += int(verdict == "sai" and not edit.get("guarded"))
    results = []
    for group in groups.values():
        group["seconds"] = round(group["seconds"], 3)
        results.append(group)
    results.sort(key=lambda g: (g["model"], g["host"], g["version"]))
    return {
        "schema": 1,
        "corpus_manifest_sha256": found["manifest_sha256"],
        "lexicon_sha256": data.get("lexicon_sha256"),
        "articles": len(sheets),
        "results": results,
    }


def main(argv: list[str]) -> int:
    try:
        if len(argv) == 2 and argv[0] == "manifest":
            result = manifest(Path(argv[1]))
        elif len(argv) == 2 and argv[0] == "edits":
            result = blind_edits(Path(argv[1]))
        elif len(argv) in (2, 3) and argv[0] == "score":
            result = score(Path(argv[1]), Path(argv[2]) if len(argv) == 3 else None)
        else:
            print("Dùng: holdout_036.py manifest <thư-mục> | edits <runs.json> | score <runs.json> [<judgments.json>]",
                  file=sys.stderr)
            return 2
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"holdout_036: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
