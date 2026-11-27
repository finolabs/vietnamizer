# Implementation Plan: Style cards for common Vietnamese writer types

**Branch**: `spec/040-writer-styles` | **Date**: 2026-11-27 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/040-writer-styles/spec.md`

## Summary

The package gains four style cards, all following the existing eight-field contract and each at most 1,500 bytes:
- `customer-reply` under `personal-blog`;
- `internal-announcement`, `product-requirements` and `news-report` under `enterprise-technical`.

To keep `SKILL.md` within its route budget, the seven-row card table becomes a two-item list. One lead line gives the path pattern, and each family item carries purpose → `card` pairs. Research R1 measured the list at 749 bytes, against 764 for the old table; an id-only table would be 897. The validator gets one source for card families and parses the list. Each card gets one positive and two leak routing cases (WS01–WS12). Before any docs work, an early paid model run compares the candidate with v0.16.3 on D11–D34, MS01–MS14 and WS01–WS12. A cheap probe goes first, because many 038 runs read no card at all (R4).

## Technical Context

**Language/Version**: Markdown skill text; Python 3 standard library for the validator, the tests and the maintainer runner.

**Primary Dependencies**: none new.

**Storage**: files in the package; run outputs stay in `artifacts/dev-037/articles/` and `.finolabs/harness-040/`, both outside Git.

**Testing**:
- `unittest`: `tests.test_skill_contract`, `tests.test_package_security`, `tests.test_route_budget`;
- `scripts/validate-package.py`;
- `scripts/route_budget.py`;
- the model run through the 038 runner and `benchmarks/holdout_036.py score`.

**Target Platform**: every host Vietnamizer ships to: Claude Code, Codex, Antigravity, claude.ai and Cowork.

**Project Type**: a Markdown skill package.

**Performance Goals**:
- `SKILL.md` stays at or under 14,428 bytes;
- no route's `max_bytes` is raised;
- mean cost per run rises by at most 5% per model.

**Constraints**:
- each card is at most 1,500 bytes;
- the resolver grows by at most 600 bytes;
- `SKILL.md` stays at or under its 550-line limit;
- no new V, T, B or K pattern;
- no edit to `references/voice-profile*.md`;
- the T1–T6-only gate is unchanged.

**Scale/Scope**:
- 4 new cards;
- 12 new calibration cases;
- about 560 paid runs, estimated at $98 (R6).

## Constitution Check

| Principle or gate | How the plan meets it | Status |
|---|---|---|
| I. Vietnamese evidence before convention | Convention claims cite `docs/sources.md` or carry a *suy luận* label (R5, FR-008) | Pass, with sources checked during implementation |
| II. Meaning and voice before polish | Each card's "Không tự thêm" names the meaning-changing additions for its function (FR-006); the five chốt are untouched | Pass |
| III. Shared rules apart from genre profiles | Cards own no pattern; the V/T/B/K inventory and `docs/patterns.md` are unchanged | Pass |
| IV. Labelled evidence | WS cases are labelled maintainer-built development cases, never holdout; `artifacts/holdout-036/` stays closed | Pass |
| V. Self-standing Markdown skill | No new script in the package; the runner stays in `.finolabs/` | Pass |
| Package constraints | `SKILL.md` line and byte limits are kept; the version is not bumped in this spec, and release work is separate | Pass |
| Gate 1: a red test first | Contract tests are written to fail on main first (contracts/card-list.md "Tests") | Planned |
| Gate 3: behavioral eval reports | `docs/benchmarks.md` records fixes, guard breaks, cost, seconds and card picks per model and arm | Planned |
| Gate 5: pre-release list | Out of scope; it runs at release | n/a |

The check holds again after the Phase 1 design. One change follows from research: the card list is a list, not a table (R1). FR-003's requirements are met in substance, but its wording says "table", so the spec text is updated in the same change.

## Project Structure

### Documentation (this feature)

```text
specs/040-writer-styles/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/card-list.md
└── tasks.md            # next: speckit-tasks
```

### Source code (repository root)

```text
SKILL.md                                    # card table → card list block
references/style-resolution.md             # registry +4 rows, ≤1 line per card
profiles/personal-blog/styles/customer-reply.md
profiles/enterprise-technical/styles/internal-announcement.md
profiles/enterprise-technical/styles/product-requirements.md
profiles/enterprise-technical/styles/news-report.md
scripts/validate-package.py                 # STYLE_FAMILIES, list parse
tests/test_skill_contract.py                # red tests for list and cards
tests/test_package_security.py              # inventory +4 paths
calibration/test-cases.md                   # WS01–WS12
docs/sources.md                             # sources for convention claims
docs/style-and-voice.md, README.md, docs/architecture.md   # after the model run
docs/benchmarks.md                          # run record
```

**Structure decision**: the existing package layout, with no new folder in the package.

## Order and the depth gate

Work happens in this order:

1. Red tests.
2. Validator and card list.
3. Four cards and the resolver rows.
4. WS cases.
5. Sources.
6. Probe.
7. Model run.
8. Docs.
9. Review gate.

The work spans several files with a paid run in the middle, so it needs ordering. Per the Spec Kit depth gate, `speckit-tasks` runs next.

## Open decisions

| Decision | Owner | Blocks |
|---|---|---|
| FR-003 says "table" and the plan ships a list (R1) | Settled 27/11/2026: the list ("Duyệt, làm tiếp") | — |
| How a run that reads no card counts (R4) | Settled 27/11/2026: SC-004 counts only runs that read a card ("Đếm card đúng khi đọc") | — |

## Complexity Tracking

No constitution violation; nothing to justify.
