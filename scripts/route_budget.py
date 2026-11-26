#!/usr/bin/env python3
"""Kiểm số byte mỗi tuyến đọc của skill (spec 038). Công cụ của maintainer, không vào gói.

Đọc bảng dưới `## Chọn đúng tuyến đọc` trong SKILL.md, lấy các đường dẫn đặt trong backtick ở cột
"Đọc thêm trước khi làm", cộng byte của chúng với SKILL.md và so với benchmarks/route-budget.json.
Mã thoát: 0 khi mọi tuyến trong ngân sách, 1 khi có tuyến vượt, thiếu file hoặc dòng chưa có tuyến.
`--write` ghi số đo hiện tại làm max_bytes (lần đầu ghi cả baseline_bytes), không cho vượt baseline.
Spec 039: tuyến hồ sơ giọng còn đo từng việc (TASKS), bằng file của tuyến cộng phần việc ấy đọc thêm.
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
# (việc, tuyến gốc hoặc None nếu chỉ SKILL.md, các file việc ấy đọc thêm)
TASKS = (
    ("voice-profile-learn", "voice-profile", ("references/voice-profile-learn.md", "references/voice-analysis.md")),
    ("voice-profile-save", "voice-profile", ("references/voice-profile-save.md", "references/voice-profile-apply.md")),
    ("voice-profile-apply", "voice-profile", ("references/voice-profile-apply.md", "references/voice-from-samples.md")),
    ("voice-profile-update", "voice-profile", ("references/voice-profile-update.md", "references/voice-profile-save.md")),
    ("voice-profile-reminder", None, ("references/voice-profile-reminder.md",)),
)
PATH = re.compile(r"`((?:references|profiles)/[^`\s]+\.md)`")


def inside(relative: str) -> Path | None:
    """Trả đường dẫn trong repo, hoặc None khi có `..`, symlink hay trỏ ra ngoài repo."""
    if ".." in Path(relative).parts:
        return None
    path, root = ROOT / relative, ROOT.resolve()
    current = ROOT
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink():
            return None
    try:
        path.resolve().relative_to(root)
    except ValueError:
        return None
    return path


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


def measure() -> tuple[dict[str, int], dict[str, list[str]], list[str]]:
    skill_path = inside("SKILL.md")
    if skill_path is None or not skill_path.is_file():
        return {}, {}, ["SKILL.md: thiếu, là symlink hoặc ra ngoài repo"]
    skill = skill_path.read_text(encoding="utf-8")
    base = skill_path.stat().st_size
    totals, listed, problems = {}, {}, []
    for cells in table_rows(skill):
        route = next((rid for prefix, rid in ROUTES if cells[0].startswith(prefix)), None)
        if route is None:
            problems.append(f"dòng chưa có tuyến: {cells[0][:60]}")
            continue
        files = list(dict.fromkeys(PATH.findall(cells[1] if len(cells) > 1 else "")))
        size = base
        for relative in files:
            path = inside(relative)
            if path is None:
                problems.append(f"{route}: đường dẫn ra ngoài repo hoặc qua symlink: {relative}")
                continue
            if not path.is_file():
                problems.append(f"{route}: thiếu file {relative}")
                continue
            size += path.stat().st_size
        totals[route] = size
        listed[route] = files
    for task, route, extra in TASKS:
        if route is not None and route not in totals:
            continue
        files = (listed[route] if route else []) + [f for f in extra if route is None or f not in listed[route]]
        size = base
        for relative in files:
            path = inside(relative)
            if path is None or not path.is_file():
                problems.append(f"{task}: thiếu file, symlink hoặc ra ngoài repo: {relative}")
                continue
            size += path.stat().st_size
        totals[task] = size
        listed[task] = files
    for _, rid in ROUTES:
        if rid not in totals and not any(p.startswith(f"{rid}:") for p in problems):
            problems.append(f"{rid}: không tìm thấy dòng trong bảng tuyến")
    return totals, listed, problems


def main(argv: list[str]) -> int:
    totals, listed, problems = measure()
    if inside("benchmarks/route-budget.json") is None:
        print("benchmarks/route-budget.json hoặc thư mục của nó là symlink hoặc ra ngoài repo; không đọc", file=sys.stderr)
        return 1
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
        if BUDGET.is_symlink() or BUDGET.parent.is_symlink():
            print("benchmarks/route-budget.json hoặc thư mục của nó là symlink; không ghi", file=sys.stderr)
            return 1
        BUDGET.parent.mkdir(parents=True, exist_ok=True)
        BUDGET.write_text(json.dumps(budget, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    failed = list(problems)
    for route, size in totals.items():
        limit = routes.get(route, {}).get("max_bytes")
        print(f"{route} {size} / {limit}: " + ", ".join(["SKILL.md", *listed.get(route, [])]))
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
