"""Kiểm bảng references/ai-error-lexicon.md cho maintainer (không vào gói phát hành).

validate-package.py và tests/test_scan_lexicon.py cùng dùng hàm check_lexicon.
Cấu trúc bảng do parse_table của scripts/scan-lexicon.py kiểm, để hai bên đọc một bảng như nhau.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCANNER = ROOT / "scripts" / "scan-lexicon.py"
LEXICON = "references/ai-error-lexicon.md"
CASES = "calibration/test-cases.md"
PATTERN_HEADING = re.compile(r"^### ([VT]\d+)\.", re.MULTILINE)
BLOCK_HEADING = re.compile(r"^## ([A-Z]{2})(\d{2})–\1(\d{2})\b", re.MULTILINE)
CASE_ID = re.compile(r"^[A-Z]{2}\d{2}$")
FRONT_MATTER = "---\ntype: vietnamizer-ai-error-lexicon\nschema: 1\n---\n"


def load_scanner():
    spec = importlib.util.spec_from_file_location("scan_lexicon", SCANNER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pattern_ids(root: Path = ROOT) -> set[str]:
    ids: set[str] = set()
    for path in sorted((root / "references").glob("*.md")):
        ids.update(PATTERN_HEADING.findall(path.read_text(encoding="utf-8")))
    return ids


def case_index(text: str) -> dict[str, bool]:
    """Ca id → True khi ca là ca chống sửa quá tay (cột Mong đợi bắt đầu bằng "Giữ nguyên")."""
    index: dict[str, bool] = {}
    headings = list(BLOCK_HEADING.finditer(text))
    for number, heading in enumerate(headings):
        prefix, first, last = heading.group(1), int(heading.group(2)), int(heading.group(3))
        end = headings[number + 1].start() if number + 1 < len(headings) else len(text)
        block = text[heading.end():end]
        for line in block.splitlines():
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) >= 3 and cells[0].isdigit() and first <= int(cells[0]) <= last:
                index[f"{prefix}{int(cells[0]):02d}"] = cells[2].startswith("Giữ nguyên")
    return index


def check_lexicon(text: str, patterns: set[str], cases: dict[str, bool] | None) -> list[str]:
    """Trả danh sách lỗi; rỗng khi bảng hợp lệ. cases=None bỏ qua kiểm cột Ca (gói đã stage)."""
    scanner = load_scanner()
    errors: list[str] = []
    if not text.startswith(FRONT_MATTER):
        errors.append("lexicon: thiếu front matter type/schema")
    if text.count("\n## Bảng\n") != 1:
        errors.append("lexicon: phải có đúng một mục ## Bảng")
    try:
        rows = scanner.parse_table(text)
    except scanner.LexiconError as error:
        return errors + [f"lexicon: {error}"]
    for row in rows:
        entry = row["ID"]
        if row["Pattern"] not in patterns:
            errors.append(f"lexicon {entry}: Pattern {row['Pattern']} không có trong catalog")
        fixes = [fix.strip() for fix in row["Sửa"].split(" / ")]
        if any(not fix or fix == row["Dạng"] for fix in fixes):
            errors.append(f"lexicon {entry}: mỗi cách sửa phải khác dạng gốc")
        if cases is None:
            continue
        ids = [item.strip() for item in row["Ca"].split(",")]
        unknown = [item for item in ids if not CASE_ID.match(item) or item not in cases]
        if unknown:
            errors.append(f"lexicon {entry}: Ca không có trong {CASES}: {unknown}")
            continue
        if not any(cases[item] for item in ids):
            errors.append(f"lexicon {entry}: Ca cần ít nhất một ca chống sửa quá tay")
        if all(cases[item] for item in ids):
            errors.append(f"lexicon {entry}: Ca cần ít nhất một ca lỗi")
    return errors
