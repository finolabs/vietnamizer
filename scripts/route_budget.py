#!/usr/bin/env python3
"""Kiểm số byte mỗi tuyến đọc của skill (spec 038). Công cụ của maintainer, không vào gói.

Đọc bảng dưới `## Chọn đúng tuyến đọc` trong SKILL.md, lấy các đường dẫn đặt trong backtick ở cột
"Đọc thêm trước khi làm", cộng byte của chúng với SKILL.md và so với benchmarks/route-budget.json.
Mã thoát: 0 khi mọi tuyến trong ngân sách, 1 khi có tuyến vượt, thiếu file hoặc dòng chưa có tuyến.
`--write` ghi số đo hiện tại làm max_bytes (lần đầu ghi cả baseline_bytes), không cho vượt baseline.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
BUDGET = ROOT / "benchmarks" / "route-budget.json"
HEADING = "## Chọn đúng tuyến đọc"
ROUTES = (
    ("Sửa một cụm", "short-edit"),
    ("Biên tập toàn bài", "whole-article"),
    ("Bài dài", "long-or-multi-round"),
    ("Theo mẫu", "follow-sample"),
    ("Học, lưu", "voice-profile"),
    ("Hỏi Vietnamizer", "help"),
    ("Chỉ review", "review-only"),
    ("Chỉ typography", "typography-only"),
)
PATH = re.compile(r"`((?:references|profiles)/[^`\s]+\.md)`")


def table_rows(skill: str) -> list[list[str]]:
    start = skill.index(HEADING)
    rows, seen_table = [], False
    for line in skill[start:].splitlines()[1:]:
        if line.startswith("## "):
            break
        if line.startswith("|"):
            seen_table = True
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if cells and not set(cells[0]) <= set("-: ") and cells[0] != "Việc được giao":
                rows.append(cells)
        elif seen_table:
            break
    return rows


def measure() -> tuple[dict[str, int], list[str]]:
    skill_path = ROOT / "SKILL.md"
    skill = skill_path.read_text(encoding="utf-8")
    base = skill_path.stat().st_size
    totals, problems = {}, []
    for cells in table_rows(skill):
        route = next((rid for prefix, rid in ROUTES if cells[0].startswith(prefix)), None)
        if route is None:
            problems.append(f"dòng chưa có tuyến: {cells[0][:60]}")
            continue
        files = list(dict.fromkeys(PATH.findall(cells[1] if len(cells) > 1 else "")))
        size = base
        for relative in files:
            path = ROOT / relative
            if not path.is_file():
                problems.append(f"{route}: thiếu file {relative}")
                continue
            size += path.stat().st_size
        totals[route] = size
    for _, rid in ROUTES:
        if rid not in totals and not any(p.startswith(f"{rid}:") for p in problems):
            problems.append(f"{rid}: không tìm thấy dòng trong bảng tuyến")
    return totals, problems


def main(argv: list[str]) -> int:
    totals, problems = measure()
    budget = json.loads(BUDGET.read_text(encoding="utf-8")) if BUDGET.exists() else {"schema": 1, "routes": {}}
    routes = budget.setdefault("routes", {})
    if "--write" in argv:
        if problems:
            print("\n".join(problems), file=sys.stderr)
            return 1
        refused = []
        for route, size in totals.items():
            entry = routes.setdefault(route, {"baseline_bytes": size, "max_bytes": size})
            if size > entry["baseline_bytes"]:
                refused.append(f"{route}: {size} > baseline {entry['baseline_bytes']}")
                continue
            entry["max_bytes"] = size
        if refused:
            print("\n".join(refused), file=sys.stderr)
            return 1
        BUDGET.parent.mkdir(parents=True, exist_ok=True)
        BUDGET.write_text(json.dumps(budget, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    failed = list(problems)
    for route, size in totals.items():
        limit = routes.get(route, {}).get("max_bytes")
        print(f"{route} {size} / {limit}")
        if limit is None:
            failed.append(f"{route}: chưa có ngân sách")
        elif size > limit:
            failed.append(f"{route}: {size} byte, vượt ngân sách {limit}")
    if failed:
        print("\n".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
