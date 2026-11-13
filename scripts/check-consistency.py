#!/usr/bin/env python3
"""Đếm các biến thể không nhất quán trong một văn bản tiếng Việt (công cụ tùy chọn, ngoài gói).

Chỉ đếm bằng quy tắc cố định, không gọi mạng hay model và không sửa file. Kết quả là ứng viên để
người đọc xem ngữ cảnh, không phải lỗi: một biến thể dùng nhất quán là lựa chọn hợp lệ.
Dùng: check-consistency.py [--json] FILE [FILE...]   (FILE là "-" để đọc stdin)
Thoát 0 kể cả khi có ứng viên; 2 khi đầu vào không hợp lệ.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

MAX_BYTES = 2_000_000
TONES = {"̀", "́", "̉", "̃", "̣"}
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)
IY_PAIRS = [("lí", "lý"), ("kí", "ký"), ("kĩ", "kỹ"), ("mĩ", "mỹ"), ("quí", "quý"), ("sĩ", "sỹ")]
FIRST_PERSON = ["tôi", "mình", "chúng tôi", "chúng ta", "chúng mình", "em", "ta"]
SECOND_PERSON = ["bạn", "anh", "chị", "em"]


def clusters(word: str) -> list[tuple[str, set[str]]]:
    """Tách từ thành cụm (chữ gốc, dấu thanh) sau khi phân rã NFD."""
    result: list[list] = []
    for ch in unicodedata.normalize("NFD", word.lower()):
        if unicodedata.combining(ch) and result:
            if ch in TONES:
                result[-1][1].add(ch)
            else:
                result[-1][2].append(ch)
        else:
            result.append([ch, set(), []])
    return [(c[0], c[1]) for c in result]


def tone_style(word: str) -> str | None:
    """'dau-dau' khi dấu thanh ở nguyên âm đầu của oa/oe/uy (hoà, thuỷ), 'dau-cuoi' khi ở
    nguyên âm cuối (hòa, thủy), None nếu từ không thuộc nhóm này."""
    cl = clusters(word)
    if len(cl) < 2:
        return None
    ending = cl[-2][0] + cl[-1][0]
    if ending not in {"oa", "oe", "uy"}:
        return None
    if ending == "uy" and len(cl) >= 3 and cl[-3][0] == "q":
        return None
    first, last = bool(cl[-2][1]), bool(cl[-1][1])
    if first and not last:
        return "dau-dau"
    if last and not first:
        return "dau-cuoi"
    return None


def analyze(text: str) -> dict:
    text = unicodedata.normalize("NFC", text)
    words = [w.lower() for w in WORD.findall(text)]
    counts = Counter(words)
    findings: list[dict] = []

    tone: dict[str, list[str]] = {"dau-dau": [], "dau-cuoi": []}
    for w in sorted(set(words)):
        style = tone_style(w)
        if style:
            tone[style].extend([w] * counts[w])
    if tone["dau-dau"] and tone["dau-cuoi"]:
        findings.append({
            "axis": "vi-tri-dau-thanh",
            "note": "Cùng văn bản có dấu thanh đặt ở nguyên âm đầu (hoà, thuỷ) và ở nguyên âm cuối (hòa, thủy).",
            "counts": {k: len(v) for k, v in tone.items()},
            "examples": {k: sorted(set(v))[:6] for k, v in tone.items()},
        })

    for a, b in IY_PAIRS:
        if counts[a] and counts[b]:
            findings.append({
                "axis": "i-y", "note": f"Cả '{a}' và '{b}' cùng xuất hiện.",
                "counts": {a: counts[a], b: counts[b]},
            })

    dot_thousand = len(re.findall(r"(?<![\d.,])\d{1,3}(?:\.\d{3})+(?![\d.,])", text))
    comma_thousand = len(re.findall(r"(?<![\d.,])\d{1,3}(?:,\d{3})+(?![\d.,])", text))
    comma_decimal = len(re.findall(r"(?<![\d.,])\d+,\d{1,2}(?![\d.,])", text))
    dot_decimal = len(re.findall(r"(?<![\d.,])\d+\.\d{1,2}(?![\d.,])", text))
    if (dot_thousand and comma_thousand) or (comma_decimal and dot_decimal):
        findings.append({
            "axis": "so",
            "note": "Dấu phân cách số không thống nhất; ngữ cảnh quyết định (số tiền, mã, phiên bản có thể hợp lệ).",
            "counts": {"nghin-cham": dot_thousand, "nghin-phay": comma_thousand,
                       "thap-phan-phay": comma_decimal, "thap-phan-cham": dot_decimal},
        })

    lowered = text.lower()

    def count_phrase(phrase: str) -> int:
        return len(re.findall(rf"(?<!\w){re.escape(phrase)}(?!\w)", lowered))

    first = {p: count_phrase(p) for p in FIRST_PERSON}
    second = {p: count_phrase(p) for p in SECOND_PERSON}
    used_first = [p for p, n in first.items() if n]
    if len(used_first) >= 2:
        findings.append({
            "axis": "xung-ho", "note": "Nhiều cách tự xưng cùng xuất hiện; có thể do nhiều người nói hoặc trích dẫn.",
            "counts": {p: first[p] for p in used_first},
        })
    return {
        "words": len(words),
        "findings": findings,
        "xung_ho": {"ngoi-thu-nhat": {p: n for p, n in first.items() if n},
                    "ngoi-thu-hai": {p: n for p, n in second.items() if n}},
    }


def read_input(name: str) -> str:
    if name == "-":
        data = sys.stdin.buffer.read(MAX_BYTES + 1)
    else:
        path = Path(name)
        if not path.is_file():
            raise ValueError(f"không phải file thường: {name}")
        with path.open("rb") as handle:
            data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError(f"quá {MAX_BYTES} byte: {name}")
    return data.decode("utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = {}
    try:
        for name in args.files:
            report[name] = analyze(read_input(name))
    except (ValueError, UnicodeDecodeError) as error:
        print(f"LỖI: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    for name, result in report.items():
        print(f"{name}: {result['words']} từ, {len(result['findings'])} ứng viên")
        for finding in result["findings"]:
            print(f"  [{finding['axis']}] {finding['note']} {json.dumps(finding['counts'], ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
