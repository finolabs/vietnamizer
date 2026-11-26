# Implementation Plan: Cut the token cost of each edit

**Branch**: `spec/038-token-budget` | **Date**: 2026-11-26 | **Spec**: [spec.md](spec.md)

**Input**: `specs/038-token-budget/spec.md` (Fio, 26/11/2026: "Token trước"; FR-004 tolerance "Lệch tối đa 2"). Router depth NORMAL, trigger `consumers`: the change moves text between files that every route and the contract tests read.

## Summary

The aim is to make each run load less new text while keeping every 0.16.2 behavior. Most of the cost is new context (64–66%) and output (about 30%), not the number of turns (research R1).

- **P1:** `SKILL.md` shrinks to at most 10 KB. It keeps the scope, the data boundary, the five gates and a pointer-only routing table.
- **P2:** route-only text moves to the files those routes already read.
- **P3:** `voice-profile.md` splits by task behind an index.
- **P4:** a maintainer check pins the bytes each route reads.

Quality is measured on D01–D10 while tuning, then gated once on D11–D34. The gate runs 0.16.2 again in the same batch, with logged reads, because the T035 runs cannot be shown free of the user-installed plugin (R3).

## Technical Context

**Language/Version**: Markdown skill text (Vietnamese). Python 3 standard library for maintainer checks only.

**Primary Dependencies**: none in the package. The runs need the Claude Code CLI (`claude -p`) and `benchmarks/holdout_036.py`.

**Storage**:
- Run outputs go under `artifacts/` (ignored).
- Budgets go in `benchmarks/route-budget.json` (tracked).

**Testing**:
- `tests/test_skill_contract.py`, `tests/test_package_security.py`, `tests/test_distribution.py` and `tests/test_check_consistency.py`.
- A new `tests/test_route_budget.py`.
- Manual route cases in `calibration/test-cases.md`.

**Target Platform**: Claude Cowork, claude.ai and cloud hosts, plus Claude Code, Codex and Antigravity. Claude Code `-p` is the measuring host.

**Project Type**: Agent skill package (Markdown).

**Performance Goals**:
- Whole-article cost per run at least 25% lower than 0.16.2 per model (SC-001).
- Time per run lower (SC-002).
- Always-loaded text at most 10 KB (SC-005).

**Constraints**:
- Every 0.16.2 behavior is kept (FR-001).
- Quality within 2 per count (FR-004).
- D11–D34 runs as the gate at most twice (FR-006).
- The package stays Markdown only (FR-010).
- One owner per rule.

**Scale/Scope**:
- 1 core file and 1 routing table with 8 rows.
- 1 reference split (`voice-profile.md`).
- 10 development and 24 gate articles.
- 8 manual route cases.

## Constitution Check

| Principle | How this plan meets it | Status |
|---|---|---|
| I. Vietnamese evidence first | No rule or example changes. Text only moves, and wording changes only where a pointer replaces a list. | Pass |
| II. Meaning and voice | The five gates stay in the always-loaded text. FR-004 bounds any drop in fixes or rise in guard breaks. | Pass |
| III. General rules vs profiles | Cards and profiles keep their content. The card table moves to the route that picks a card. | Pass |
| IV. Labelled evidence | Tuning uses D01–D10. D11–D34 is the gate, run at most twice. No threshold is tuned on the gate. | Pass |
| V. Self-contained Markdown | The package stays Markdown only. `route_budget.py` lives in the repository, outside the package. | Pass |
| Release gate 3 (eval reports latency and cost) | Every run reports cost, tokens, output, time and turns. | Pass |

Re-check after design: Pass. The design adds no runtime dependency, network call or script to the package.

## Project Structure

### Documentation (this feature)

```text
specs/038-token-budget/
├── spec.md
├── plan.md              # this file
├── research.md          # R1–R6
├── data-model.md        # route, read budget, run record
├── quickstart.md        # how to measure and gate
├── contracts/
│   ├── route-budget.md  # check interface and budget file
│   └── run-record.md    # what each logged run must hold
└── checklists/requirements.md
```

### Source Code (repository root)

```text
SKILL.md                         # at most 10 KB: scope, boundary, gates, pointer routing table
references/writing-workflow.md   # gains the card table and the whole-article read list
references/voice-profile.md      # becomes a short index
references/voice-profile-*.md    # learn, apply, update, registry parts
benchmarks/route-budget.json     # budget per route
scripts/route_budget.py          # maintainer check (not packaged)
tests/test_route_budget.py
tests/test_skill_contract.py     # follows moved text; drops no rule
calibration/test-cases.md        # 8 manual route cases (RB01–RB08)
.finolabs/harness-038/           # runner with stream-json read logging (ignored)
```

**Structure Decision**: This is a single package. Text moves between existing files. Only `voice-profile.md` splits into new files, and the validator's reference list gains those files.

## Delivery order

- **P1. Harness.**
  - A runner like `run_round.py` that logs `stream-json`.
  - It rejects a run whose skill loads or reads come from outside its own ZIP (R3).
  - It records cost, writes, reads, output, time, turns and the files read.
- **P2. Budget check.**
  - `route_budget.py` and its test.
  - Measure the 0.16.2 bytes per route and record them as the starting budget. The candidate's budget is then lowered to its measured value.
- **P3. Text changes, in order:**
  1. Shrink `SKILL.md`, moving route-only text to the files those routes already read.
  2. Split `voice-profile.md`.
  3. Change the contract tests only where text moved.
  4. Write the manual cases RB01–RB08.
- **P4. Early check on D01–D10.**
  - Run 0.16.2 and the candidate, two runs per model per article, about 80 runs.
  - When the saving is under 15% for a model, stop and report to Fio before any gate run.
  - Quality on D01–D10 is reported but not used as the bar.
- **P5. Manual route cases.** RB01–RB08, once per model, on 0.16.2 and the candidate. Pass when the expected outcome holds and the bytes read are not higher.
- **P6. Gate on D11–D34.**
  - 0.16.2 and the candidate in one batch, two runs per model per article, 192 valid runs.
  - Score them and check SC-001 to SC-003. A retry is allowed once, only after a change made on D01–D10.
- **P7. Report, reviews, release.**
  - Counts go to `docs/benchmarks.md`.
  - Changelog and version: 0.17.0, if the gate passes.
  - Drift review, then code and security reviews.
  - Merge, tag and release only on Fio's go.

## Complexity Tracking

| Item | Why needed | Simpler option rejected because |
|---|---|---|
| Re-running 0.16.2 in the gate batch, 96 extra runs | The T035 baseline cannot be shown clean of the user-installed plugin (R3) | Reusing T035 would compare against a baseline of unknown provenance |
| A new maintainer check | Keeps the saving after this spec (User Story 3) | A one-off measurement would not stop the next spec from adding reads, as spec 037 did |
