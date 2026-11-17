#!/usr/bin/env python3
"""Tìm ứng viên lỗi AI theo bảng references/ai-error-lexicon.md.

Công cụ của maintainer trong repo nguồn, không vào gói phát hành (spec 037).

Đọc văn bản từ stdin, in một đối tượng JSON gồm các ứng viên. Chỗ khớp nằm trong front
matter, code, địa chỉ link, ngoặc kép hay blockquote bị bỏ qua. Script không sửa
văn bản, không ghi file, không gọi mạng và không đọc biến môi trường; sửa hay giữ
là việc của agent theo pattern và cột Không flag.

Cách gọi: python3 -I scripts/scan-lexicon.py < bai.md
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

SCHEMA = 1
MAX_BYTES = 1_000_000
LEXICON = Path(__file__).resolve().parent.parent / "references" / "ai-error-lexicon.md"
HEADER = (
    "| ID | Dạng | Loại | Pattern | Sửa | Ngữ vực lỗi | Sau không là | "
    "Trước không là | Chữ hoa | Không flag | Ca |"
)
COLUMNS = (
    "ID", "Dạng", "Loại", "Pattern", "Sửa", "Ngữ vực lỗi", "Sau không là",
    "Trước không là", "Chữ hoa", "Không flag", "Ca",
)
KINDS = {"từ ghép bị cắt", "dịch sát", "từ nghề hiểu sai", "danh từ tập thể đứng trơ"}
CASE_MODES = {"mọi", "đầu câu"}
NEIGHBOUR_COLUMNS = {"Sau không là", "Trước không là"}
EMPTY = "—"
SYLLABLE = re.compile(r"[^\W\d_]+")
DROPPED = {"­", "​", "‌", "‍", "⁠", "﻿"}
SEPARATOR_ROW = re.compile(r"^\|(?:\s*:?-+:?\s*\|)+$")
LINE_START = re.compile(r"\s*(?:(?:[-*+>]|\d+[.)]|#{1,6})\s*)?")
CLAUSE_END = re.compile(r"[.!?…:;—][\"'”’»)\]]*\s*$")
HELP = (
    "Cách dùng: python3 -I scan-lexicon.py < văn-bản\n"
    "Đọc văn bản UTF-8 từ stdin, in JSON các ứng viên theo references/ai-error-lexicon.md.\n"
    "Mã thoát: 0 đã quét, 2 đầu vào sai, 3 bảng thiếu hoặc hỏng.\n"
)


class LexiconError(ValueError):
    """Bảng thiếu hoặc sai cấu trúc."""


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip()[1:-1].split("|")]


def parse_table(text: str) -> list[dict[str, str]]:
    """Trả các dòng của bảng duy nhất, mỗi dòng là dict theo COLUMNS."""
    lines = text.splitlines()
    if [line.strip() for line in lines].count(HEADER) != 1:
        raise LexiconError("bảng phải có đúng một dòng tiêu đề chuẩn")
    if sum(1 for line in lines if SEPARATOR_ROW.match(line.strip())) != 1:
        raise LexiconError("file chỉ được có một bảng")
    start = [line.strip() for line in lines].index(HEADER)
    if start + 1 >= len(lines) or not SEPARATOR_ROW.match(lines[start + 1].strip()):
        raise LexiconError("thiếu dòng phân cách sau tiêu đề")
    rows = []
    for line in lines[start + 2:]:
        if not line.strip().startswith("|"):
            break
        cells = split_row(line)
        if len(cells) != len(COLUMNS):
            raise LexiconError(f"dòng phải có {len(COLUMNS)} ô: {line.strip()[:40]}")
        rows.append(dict(zip(COLUMNS, cells)))
    if not rows:
        raise LexiconError("bảng không có dòng nào")
    for number, row in enumerate(rows, start=1):
        if row["ID"] != f"L{number:02d}":
            raise LexiconError(f"ID phải liên tục từ L01: {row['ID']}")
        for column, value in row.items():
            if not value:
                raise LexiconError(f"{row['ID']}: ô {column} trống")
            if value == EMPTY and column not in NEIGHBOUR_COLUMNS:
                raise LexiconError(f"{row['ID']}: chỉ cột láng giềng được để —")
        if row["Loại"] not in KINDS:
            raise LexiconError(f"{row['ID']}: Loại không hợp lệ")
        if row["Chữ hoa"] not in CASE_MODES:
            raise LexiconError(f"{row['ID']}: Chữ hoa không hợp lệ")
        form = row["Dạng"]
        syllables = SYLLABLE.findall(form)
        if (
            form != unicodedata.normalize("NFC", form)
            or form != form.lower()
            or " ".join(syllables) != form
            or not 1 <= len(syllables) <= 4
        ):
            raise LexiconError(f"{row['ID']}: Dạng phải là 1–4 tiếng NFC, chữ thường")
    return rows


def neighbour_set(value: str) -> set[str]:
    if value == EMPTY:
        return set()
    return {unicodedata.normalize("NFC", item.strip()).casefold() for item in value.split(",")}


def load_entries(text: str) -> list[dict]:
    return [
        {
            "id": row["ID"],
            "syllables": tuple(s.casefold() for s in SYLLABLE.findall(row["Dạng"])),
            "after": neighbour_set(row["Sau không là"]),
            "before": neighbour_set(row["Trước không là"]),
            "sentence_start": row["Chữ hoa"] == "đầu câu",
        }
        for row in parse_table(text)
    ]


def normalise(text: str) -> tuple[str, list[int], list[int]]:
    """NFC theo từng cụm ký tự gốc; trả chuỗi chuẩn và vị trí đầu, cuối trong bản gốc."""
    chars: list[str] = []
    starts: list[int] = []
    ends: list[int] = []
    index = 0
    while index < len(text):
        end = index + 1
        while end < len(text) and unicodedata.combining(text[end]):
            end += 1
        for char in unicodedata.normalize("NFC", text[index:end]):
            if char in DROPPED:
                continue
            chars.append(char)
            starts.append(index)
            ends.append(end)
        index = end
    return "".join(chars), starts, ends


def line_starts(text: str) -> list[int]:
    starts = [0]
    for index, char in enumerate(text):
        if char == "\n":
            starts.append(index + 1)
    return starts


def locate(starts: list[int], offset: int) -> int:
    low, high = 0, len(starts) - 1
    while low < high:
        middle = (low + high + 1) // 2
        if starts[middle] <= offset:
            low = middle
        else:
            high = middle - 1
    return low


def paragraph_numbers(lines: list[str]) -> list[int]:
    numbers = []
    current = 0
    blank_before = True
    for line in lines:
        if line.strip():
            if blank_before:
                current += 1
            blank_before = False
        else:
            blank_before = True
        numbers.append(max(current, 1))
    return numbers


def zone_spans(text: str, lines: list[str], starts: list[int]) -> list[tuple[int, int, str]]:
    spans: list[tuple[int, int, str]] = []
    if lines and lines[0].strip() == "---":
        for number in range(1, len(lines)):
            if lines[number].strip() == "---":
                spans.append((0, starts[number] + len(lines[number]), "frontmatter"))
                break
    fence = None
    for number, line in enumerate(lines):
        stripped = line.strip()
        if fence is None and (stripped.startswith("```") or stripped.startswith("~~~")):
            fence = (stripped[:3], starts[number])
        elif fence is not None and stripped.startswith(fence[0]):
            spans.append((fence[1], starts[number] + len(line), "code"))
            fence = None
    if fence is not None:
        spans.append((fence[1], len(text), "code"))
    # Code span vắt được qua một lần xuống dòng trong cùng đoạn, không qua dòng trống (CommonMark).
    for match in re.finditer(r"(`+)((?:(?!\n[ \t]*\n)[\s\S])+?)\1", text):
        spans.append((match.start(), match.end(), "code"))
    for match in re.finditer(r"\]\(([^)\n]*)\)", text):
        spans.append((match.start(1), match.end(1), "link-url"))
    for match in re.finditer(r"<[A-Za-z][A-Za-z0-9+.-]*:[^>\s]*>", text):
        spans.append((match.start(), match.end(), "link-url"))
    for match in re.finditer(r"“[^”]*?”|\"[^\"]*?\"", text):
        if not re.search(r"\n[ \t]*\n", match.group(0)):
            spans.append((match.start(), match.end(), "quote"))
    for number, line in enumerate(lines):
        if line.lstrip().startswith(">"):
            spans.append((starts[number], starts[number] + len(line), "blockquote"))
    return spans


ZONE_ORDER = ("frontmatter", "code", "link-url", "quote", "blockquote")


def zone_at(spans: list[tuple[int, int, str]], offset: int) -> str | None:
    found = {zone for start, end, zone in spans if start <= offset < end}
    for zone in ZONE_ORDER:
        if zone in found:
            return zone
    return None


def joined(gap: str) -> bool:
    """Hai tiếng liền nhau khi giữa chúng chỉ có khoảng trắng và không có dòng trống."""
    return bool(gap) and gap.isspace() and not re.search(r"\n[ \t]*\n", gap)


def at_sentence_start(text: str, line_start: int, offset: int) -> bool:
    prefix = text[line_start:offset]
    return bool(LINE_START.fullmatch(prefix) or CLAUSE_END.search(prefix))


def scan(text: str, entries: list[dict]) -> list[dict]:
    normal, starts_of, ends_of = normalise(text)
    tokens = [(m.start(), m.end(), m.group(0)) for m in SYLLABLE.finditer(normal)]
    folded = [unicodedata.normalize("NFC", token[2].casefold()) for token in tokens]
    lines = text.split("\n")
    starts = line_starts(text)
    paragraphs = paragraph_numbers(lines)
    spans = zone_spans(text, lines, starts)
    candidates: list[dict] = []
    offsets: list[int] = []
    for index in range(len(tokens)):
        for entry in entries:
            size = len(entry["syllables"])
            last = index + size - 1
            if last >= len(tokens) or tuple(folded[index:last + 1]) != entry["syllables"]:
                continue
            if any(
                not joined(normal[tokens[i][1]:tokens[i + 1][0]]) for i in range(index, last)
            ):
                continue
            if last + 1 < len(tokens) and folded[last + 1] in entry["after"] and joined(
                normal[tokens[last][1]:tokens[last + 1][0]]
            ):
                continue
            if index > 0 and folded[index - 1] in entry["before"] and joined(
                normal[tokens[index - 1][1]:tokens[index][0]]
            ):
                continue
            begin = starts_of[tokens[index][0]]
            finish = ends_of[tokens[last][1] - 1]
            if zone_at(spans, begin) is not None:
                continue
            line = locate(starts, begin)
            if entry["sentence_start"] and not (
                tokens[index][2][0].isupper() and at_sentence_start(text, starts[line], begin)
            ):
                continue
            candidates.append(
                {
                    "entry": entry["id"],
                    "text": text[begin:finish],
                    "line": line + 1,
                    "column": begin - starts[line] + 1,
                    "paragraph": paragraphs[line],
                }
            )
            offsets.append(begin)
    order = sorted(range(len(candidates)), key=lambda i: (offsets[i], candidates[i]["entry"]))
    return [candidates[i] for i in order]


def refuse(code: int, message: str) -> int:
    sys.stderr.write(message + "\n")
    return code


def main(argv: list[str]) -> int:
    if argv == ["--help"]:
        sys.stdout.write(HELP)
        return 0
    if argv:
        return refuse(2, "scan-lexicon: chỉ nhận --help; văn bản đưa qua stdin")
    data = sys.stdin.buffer.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        return refuse(2, "scan-lexicon: văn bản quá 1.000.000 byte")
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    if not data:
        return refuse(2, "scan-lexicon: không có văn bản trên stdin")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return refuse(2, "scan-lexicon: văn bản không phải UTF-8 hợp lệ")
    try:
        raw = LEXICON.read_bytes()
        entries = load_entries(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, LexiconError) as error:
        return refuse(3, f"scan-lexicon: không đọc được bảng lexicon ({type(error).__name__})")
    result = {
        "schema": SCHEMA,
        "lexicon_sha256": hashlib.sha256(raw).hexdigest()[:12],
        "candidates": scan(text, entries),
    }
    sys.stdout.buffer.write((json.dumps(result, ensure_ascii=False) + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
