# Contract: route budget check

`python3 scripts/route_budget.py [--write]`, run from the repository root. Maintainer only; not in the package.

**Default (check mode):**
- Parses the routing table under `## Chọn đúng tuyến đọc` in `SKILL.md`.
- Maps each row to a route id by a fixed table in the script.
- Resolves every backticked path that the row's read column names.
- Prints one line per route: `<route> <bytes> / <max_bytes>`.
- Exits 0 when every route is within budget.
- Exits 1 and names each route over budget, each missing file and each unmapped row.

**`--write`:** records the current byte totals as `max_bytes`. When `benchmarks/route-budget.json` is first created, it also records `baseline_bytes`. It refuses to raise `max_bytes` above `baseline_bytes`.

**Budget file:** `benchmarks/route-budget.json`, holding `{"schema": 1, "routes": {"<route>": {"baseline_bytes": int, "max_bytes": int}}}`.

**Tests (`tests/test_route_budget.py`):**
- The current tree passes.
- Adding a file to the whole-article row fails it (SC-006).
- A missing file fails.
- An unmapped row fails.
- `--write` refuses to go above the baseline.
