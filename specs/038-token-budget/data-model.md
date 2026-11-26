# Data model: Cut the token cost of each edit

## Route

One row of the routing table in `SKILL.md`.

- `id`: a short stable name: `short-edit`, `whole-article`, `long-or-multi-round`, `follow-sample`, `voice-profile`, `help`, `review-only`, `typography-only`.
- `files`: the files the row names, resolved relative to the skill folder. `SKILL.md` is always included.
- `bytes`: the sum of the UTF-8 sizes of `files`.

Validation:
- Every file a row names exists.
- A row names no file twice.
- `SKILL.md` is counted once.

## Read budget

One entry per route in `benchmarks/route-budget.json`.

- `route`: the route `id`.
- `max_bytes`: an integer. It is set from the measured candidate value when the candidate is accepted. It starts at the 0.16.2 value.
- `baseline_bytes`: the 0.16.2 value, kept for the report.

Validation:
- Every route in the table has exactly one entry.
- `max_bytes` is at most `baseline_bytes` (FR-003).

## Run record

One logged run of the harness. The format is in [contracts/run-record.md](contracts/run-record.md).

- Identity: `article`, `model`, `version`, `rep`, `label`.
- Cost: `cost_usd`, `cache_write`, `cache_read`, `output`, `seconds`, `turns`.
- Reads: the ordered list of skill loads and files read, with their source path.
- Validity:
  - `valid` is true only when every skill load and read comes from the run's own ZIP install path (research R3).
  - An invalid run is rerun. It is never scored.
