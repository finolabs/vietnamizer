# Tasks: Cut the token cost of each edit

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/](contracts/), [quickstart.md](quickstart.md)

**Tests**: The constitution's release gate 1 requires a red test first for every behavior change. That covers the budget check, the route reads and the moved text. Run at most two test modules per command, and check `uptime` first.

**Isolation**: Edit skill text only from D01–D10 evidence. D11–D34 is the gate, and only counts come back from it (FR-006). Never open `artifacts/holdout-036/`.

## Phase 1: Setup

- [x] T001 Confirm PR 95 is merged, then rebase `spec/038-token-budget` on main. Check that `git diff v0.16.2 HEAD -- SKILL.md references/ profiles/ assets/ agents/` is empty before any text change.
- [x] T002 Build `.finolabs/harness-038/v0162.zip` from tag `v0.16.2` with `scripts/package-plugin.py` in a clean checkout of the tag. Record its SHA-256 in `.finolabs/harness-038/README.md`.

## Phase 2: Foundational (harness and budget check)

- [x] T003 Write `.finolabs/harness-038/run_round.py` from `.finolabs/harness-037/gate/run_round.py`.
  - Run `claude -p` with `--output-format stream-json --verbose`.
  - Parse every `tool_use` into `reads`, and take `cost_usd`, `cache_write`, `cache_read`, `output`, `seconds` and `turns` from the result's `modelUsage`.
  - Set `valid` false when a skill load or read path lies outside the run's own plugin install path ([contracts/run-record.md](contracts/run-record.md)).
  - Rerun invalid runs up to twice. Write only valid runs to the index.
- [x] T004 Probe the harness on D02, one run per model with `v0162.zip`.
  - Confirm `valid` is true and the reads match research R2.
  - Confirm that a run without `--plugin-dir` is marked invalid.
- [x] T005 [P] Write the red tests for the budget check in `tests/test_route_budget.py`:
  - the current tree passes;
  - adding a file to the `whole-article` row fails and names that route (SC-006);
  - a missing file fails;
  - an unmapped row fails;
  - `--write` refuses to set `max_bytes` above `baseline_bytes`.
- [x] T006 Implement `scripts/route_budget.py` per [contracts/route-budget.md](contracts/route-budget.md).
  - Parse the table under `## Chọn đúng tuyến đọc`.
  - Map rows to the route ids `short-edit`, `whole-article`, `long-or-multi-round`, `follow-sample`, `voice-profile`, `help`, `review-only` and `typography-only`.
  - Count `SKILL.md` once per route.
  - Make T005 green.
- [x] T007 Run `python3 scripts/route_budget.py --write` on the 0.16.2 text to create `benchmarks/route-budget.json`, with `baseline_bytes` equal to `max_bytes` for every route. Commit it with T005 and T006.

**Checkpoint**: the harness logs clean runs, and the 0.16.2 bytes per route are recorded.

## Phase 3: User Story 1 - whole-article edits cost less (P1) 🎯 MVP

**Goal**: The always-loaded text is at most 10 KB, the whole-article route reads less, and quality holds.

**Independent test**: Run D01–D10 with both versions, then the gate on D11–D34 (quickstart steps 3 and 5).

- [ ] T008 [US1] Make the contract tests check the new text before the move, in `tests/test_skill_contract.py`. They must fail on the current text.
  - `SKILL.md` is at most 10,240 bytes.
  - The five gates, the data boundary, the frozen zones and every route row stay in `SKILL.md`.
  - The card table and the whole-article read list live in `references/writing-workflow.md`.
- [ ] T009 [US1] Rewrite `SKILL.md` to at most 10 KB, and make T008 green. Keep it to the scope, the data boundary and frozen zones, the five gates, and a routing table whose rows name files only. Move these out:
  - the card table and the whole-article read details, to `references/writing-workflow.md`;
  - the return-format details of rare routes, to the file each route reads.
- [ ] T010 [US1] Shorten the whole-article route in `references/writing-workflow.md`.
  - One step lists every file to read before writing.
  - The agent reads them together, then writes the article once.
  - No narration between tool calls.
  - Keep every rule, with one owner per rule.
- [ ] T011 [US1] Run the existing contract, package security, distribution and consistency tests, two modules per command. Follow moved text in the tests without dropping a rule (FR-008). Run `python3 scripts/validate-package.py`.
- [ ] T012 [US1] Lower `max_bytes` to the candidate's measured bytes with `python3 scripts/route_budget.py --write`. Confirm that `whole-article` is below `baseline_bytes` in `benchmarks/route-budget.json`.
- [ ] T013 [US1] Early check (plan P4).
  - Run D01–D10 with `v0162.zip` and the candidate ZIP, two runs per model per article, through `.finolabs/harness-038/run_round.py`.
  - Report mean cost, writes, output, time and turns per model and version, plus fixes and guard breaks as counts.
  - When the saving is under 5% for a model, stop and report to Fio before T014.
- [ ] T014 [US1] Gate (plan P6).
  - Run D11–D34 with both versions in one batch, two runs per model per article, all runs valid.
  - Score with `python3 benchmarks/holdout_036.py score`.
  - Pass when every condition below holds per model:
    - mean cost is at least 10% lower than 0.16.2;
    - mean time is lower;
    - lexicon-kind fixes, other fixes and guard breaks are no worse than 0.16.2 by more than 2 each.
  - A fail allows one retry, after a change made from D01–D10 only.

**Checkpoint**: SC-001, SC-002, SC-003 and SC-005 are met, or the result goes to Fio.

## Phase 4: User Story 2 - other routes keep working (P2)

**Goal**: Each route the pool does not measure behaves as 0.16.2 and reads no more.

**Independent test**: Run RB01–RB08 once per model per version, with reads logged.

- [ ] T015 [P] [US2] Write the manual cases RB01–RB08 in `calibration/test-cases.md`, one per route:
  - writing from a brief;
  - following a sample;
  - learning a voice profile;
  - applying a saved profile;
  - brand voice;
  - help;
  - review only;
  - typography only.

  Each case states its input, the expected outcome, and the files 0.16.2 reads for it.
- [ ] T016 [US2] Write red tests in `tests/test_skill_contract.py` for the voice-profile split, before the split:
  - `references/voice-profile.md` is an index under 4 KB that names the parts;
  - applying a saved profile points only to the apply part;
  - every rule of the old file appears in exactly one part.
- [ ] T017 [US2] Split `references/voice-profile.md` into the index and the parts `references/voice-profile-learn.md`, `references/voice-profile-apply.md`, `references/voice-profile-update.md` and `references/voice-profile-registry.md`.
  - Update the pointers in `SKILL.md`, `references/voice-sources.md`, `references/brand-voice.md` and `references/help.md`.
  - Make T016 green.
- [ ] T018 [US2] Add the new parts to `REFERENCE_FILES` in `scripts/validate-package.py`, and to any reference list in `tests/test_distribution.py`. Run the validator and both test modules. Then run `python3 scripts/route_budget.py --write` again.
- [ ] T019 [US2] Run RB01–RB08 through the harness, once per model per version. Record pass or fail and the bytes read per case in `docs/benchmarks.md`. A case that fails, or reads more than on 0.16.2, blocks the release (SC-004).

## Phase 5: User Story 3 - maintainers see the cost (P3)

**Goal**: The budget check runs with the tests and is documented.

- [ ] T020 [P] [US3] Document `scripts/route_budget.py` and `benchmarks/route-budget.json` in `AGENTS.md` (repository files table and release checks) and `docs/architecture.md`. Say that it runs outside the package.
- [ ] T021 [US3] Add `python3 scripts/route_budget.py` to the release checks list in `AGENTS.md`. Confirm that `tests/test_route_budget.py` runs it.

## Phase 6: Polish and release

- [ ] T022 Write the results to `docs/benchmarks.md` as counts: per model and version the cost, writes, output, time, turns, fixes and guard breaks; the model ids, host and date; the manifest hash `1f388f615f4c`; and both package commits.
- [ ] T023 Drift review of every product description against what ships: README (version, packaging, the release summary), `docs/usage.md`, `docs/architecture.md`, `docs/installation.md`, `references/help.md`, `AGENTS.md` and the manifests.
- [ ] T024 Changelog and version per `versioning`: 0.17.0 in `docs/changelog.md`, `SKILL.md` metadata, the three manifests and README, with the measured saving. Do this only if T014 and T019 pass.
- [ ] T025 Open the pull request with the router marker `<!-- fnl-router depth=NORMAL trigger=consumers -->`, and get the posted code and security reviews.
- [ ] T026 Merge, tag `v0.17.0`, release, and move the catalog pin in `finolabs/plugins`, each only on Fio's explicit go.

## Dependencies

- T001 → T002 → T003 → T004.
- T005 → T006 → T007.
- T007 → T008 → T009 → T010 → T011 → T012 → T013 → T014.
- T015 can start after T007. T016 → T017 → T018 → T019 come after T011.
- T020 and T021 come after T007.
- T022 to T026 come after T014 and T019.
- US2 runs beside US1 only after T011, because both touch `SKILL.md` pointers.

## Parallel opportunities

- T005 (tests) and T003 (harness) touch different files.
- T015 (manual cases) and T020 (docs) can run while T009 and T010 are in progress.
- T019's runs and T014's gate are both heavy jobs. Run them one at a time, never together.

## Implementation strategy

The MVP is US1 through T014. It alone proves the saving on the measured route. US2 must pass before any release, because the split can break unmeasured routes. US3 is small and lands with US1. The early check, T013, is the stop point: if the saving is not there, Fio decides before 192 gate runs are spent.

## Requirements coverage

| Requirement | Tasks |
|---|---|
| FR-001 behaviors kept | T008, T011, T016, T019 |
| FR-002 smaller always-loaded text | T008, T009 |
| FR-003 no route reads more | T006, T007, T012, T018, T019 |
| FR-004 quality tolerance | T014 |
| FR-005 setup and fresh baseline | T002, T003, T004, T014 |
| FR-006 D01–D10 tuning, gate at most twice | T013, T014 |
| FR-007 manual route cases | T015, T019 |
| FR-008 contract tests | T008, T011, T016 |
| FR-009 budget check | T005, T006, T021 |
| FR-010 Markdown-only package | T011, T018 |
| FR-011 report | T022 |
