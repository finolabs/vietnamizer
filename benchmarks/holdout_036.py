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
WORD = re.compile(r"\S+")
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


def sentences(paragraph: str) -> list[str]:
    return [s for s in SENTENCE_END.split(paragraph) if s]


def table_rows(text: str, heading: str, width: int) -> list[list[str]]:
    if heading not in text:
        raise ValueError(f"phiếu thiếu mục {heading}")
    block = re.split(r"\n#{1,6} ", text.split(heading, 1)[1], maxsplit=1)[0]
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|") or re.match(r"^\|[\s:|-]+\|$", line):
            continue
        cells = [c.strip() for c in line[1:-1].split("|")]
        if cells[0] == "#":
            continue
        if len(cells) != width:
            raise ValueError(f"dòng phiếu phải có {width} ô: {line[:40]}")
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
        sheets[article] = (sheet, source)
    return data, sheets, found


def source_sentence(source: list[str], row: dict) -> str:
    paragraph = source[row["paragraph"] - 1]
    return next(s for s in sentences(paragraph) if row["span"] in s) if any(
        row["span"] in s for s in sentences(paragraph)) else paragraph


def best_match(source: list[str], output: list[str], row: dict) -> tuple[float, tuple[int, int], str] | None:
    """Câu đầu ra khớp nhất với câu nguồn chứa cụm: trước hết trong đoạn cùng số, chỉ khi đoạn đó
    không có câu nào đạt ngưỡng mới xét hai đoạn kề (bản sửa có thể tách hay gộp đoạn)."""
    target = source_sentence(source, row)
    index = row["paragraph"] - 1

    def best_in(indexes: list[int]) -> tuple[float, tuple[int, int], str] | None:
        best = None
        for p in indexes:
            if not 0 <= p < len(output):
                continue
            for s, sentence in enumerate(sentences(output[p])):
                ratio = difflib.SequenceMatcher(None, target, sentence, autojunk=False).ratio()
                if ratio >= ALIGN_MIN and (best is None or ratio >= best[0]):
                    best = (ratio, (p, s), sentence)
        return best

    return best_in([index]) or best_in([index - 1, index + 1])


def align(source: list[str], output: list[str], row: dict) -> str | None:
    match = best_match(source, output, row)
    return match[2] if match else None


def alignments(source: list[str], output: list[str], rows: list[dict]) -> dict[str, str | None]:
    """Mỗi câu đầu ra chỉ ứng với một câu nguồn. Hai câu nguồn khác nhau cùng khớp một câu đầu ra thì câu
    giống hơn giữ chỗ, câu kia coi như không còn câu khớp (vào danh sách cho Fio, không tính là đã sửa)."""
    matches = {row["id"]: best_match(source, output, row) for row in rows}
    owner: dict[tuple[int, int], tuple[float, str]] = {}
    for row in rows:
        match = matches[row["id"]]
        if match is None:
            continue
        key = (row["paragraph"], source_sentence(source, row))
        held = owner.get(match[1])
        if held is None or match[0] > held[0]:
            owner[match[1]] = (match[0], key)
    result = {}
    for row in rows:
        match = matches[row["id"]]
        key = (row["paragraph"], source_sentence(source, row))
        result[row["id"]] = match[2] if match and owner[match[1]][1] == key else None
    return result


def is_fixed(sentence: str, row: dict) -> bool | None:
    if not row["fixes"]:
        return None
    folded = sentence.casefold()
    present = [fix for fix in row["fixes"] if fix.casefold() in folded]
    if not present:
        return False
    for fix in present:
        folded = folded.replace(fix.casefold(), "\u241f")
    return row["span"].casefold() not in folded


def spans_in_source(source: list[str], rows: list[dict]) -> list[tuple[int, int]]:
    """Vị trí từ (theo WORD) của mọi cụm đã đánh dấu trong bài nối các đoạn bằng khoảng trắng."""
    joined = " ".join(source)
    starts = [m.start() for m in WORD.finditer(joined)]
    offsets, position = [], 0
    for paragraph in source:
        offsets.append(position)
        position += len(paragraph) + 1
    ranges = []
    for row in rows:
        begin = offsets[row["paragraph"] - 1] + source[row["paragraph"] - 1].index(row["span"])
        end = begin + len(row["span"])
        words = [i for i, start in enumerate(starts) if begin <= start < end]
        ranges.append((words[0], words[-1] + 1))
    return ranges


def raw_edits(source: list[str], output: list[str], rows: list[dict]) -> list[dict]:
    """Phần sửa ngoài mọi cụm đã đánh dấu, cùng câu nguồn của các dòng không còn câu đầu ra khớp.
    Khối diff chạm một cụm nhưng còn lan ra ngoài cụm thì cả khối vào danh sách cho Fio xét."""
    aligned_to = alignments(source, output, rows)
    aligned = [row for row in rows if aligned_to[row["id"]] is not None]
    edits = []
    for row in rows:
        if row in aligned:
            continue
        sentence = source_sentence(source, row)
        key = json.dumps(["unaligned", sentence], ensure_ascii=False).encode("utf-8")
        edits.append({"id": hashlib.sha256(key).hexdigest()[:10], "context": "", "source": sentence,
                      "output": "(không còn câu khớp)"})
    missing = [{"paragraph": row["paragraph"], "span": source_sentence(source, row)}
               for row in rows if aligned_to[row["id"]] is None]
    rows = aligned
    source_words = WORD.findall(" ".join(source))
    output_words = WORD.findall(" ".join(output))
    ranges = spans_in_source(source, rows) + spans_in_source(source, missing)
    matcher = difflib.SequenceMatcher(None, source_words, output_words, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        touched = [(start, end) for start, end in ranges
                   if (i1 < end and i2 > start) or (i1 == i2 and start <= i1 <= end)]
        if touched and min(s for s, _ in touched) <= i1 and i2 <= max(e for _, e in touched):
            continue
        before = " ".join(source_words[max(0, i1 - 4):i1])
        old, new = " ".join(source_words[i1:i2]), " ".join(output_words[j1:j2])
        key = json.dumps([before, old, new], ensure_ascii=False).encode("utf-8")
        edits.append({"id": hashlib.sha256(key).hexdigest()[:10], "context": before, "source": old, "output": new})
    return edits


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
        for edit in raw_edits(source, output, sheet["errors"] + sheet["guards"]):
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
        aligned_to = alignments(source, output, sheet["errors"] + sheet["guards"])
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
            sentence = aligned_to[row["id"]]
            fixed = False if sentence is None else is_fixed(sentence, row)
            if fixed is None:
                verdict = row_verdicts.get(row["id"], {}).get(run["label"])
                if verdict is None:
                    bucket["pending"] = bucket.get("pending", 0) + 1
                    continue
                fixed = verdict == "fixed"
            bucket["fixed"] += int(bool(fixed))
        for row in sheet["guards"]:
            group["guards"]["total"] += 1
            sentence = aligned_to[row["id"]]
            group["guards"]["broken"] += int(sentence is None or row["span"] not in sentence)
        for edit in raw_edits(source, output, sheet["errors"] + sheet["guards"]):
            verdict = edit_verdicts.get(edit["id"])
            group["out_of_span"][verdict if verdict in VERDICTS else "pending"] += 1
    results = []
    for group in groups.values():
        group["over_corrections"] = group["out_of_span"]["sai"]
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
