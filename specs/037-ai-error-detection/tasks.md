# Tasks: Detect AI errors in fresh Vietnamese text

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [contracts/](contracts/), [quickstart.md](quickstart.md)
**Tests**: red first for every behaviour change (phrase guards, payload rule, scorer ids). One test module per command, `uptime` first.

**Isolation rule for every task below** (spec FR-011): whoever edits skill text, rules, the lexicon, calibration or tests never opens `artifacts/holdout-036/`, the H15–H20 files or their sheets, and uses no example from them. Only the runner (T024–T027) touches the holdout, and it edits none of those files.

## Phase 1: Setup

- [x] T001 Record the baseline: `python3 scripts/validate-package.py`, then `python3 -m unittest tests.test_skill_contract`, then `python3 -m unittest tests.test_package_security` (separate commands) on the branch base; note counts in the PR

## Phase 2: Scanner out of the package (US5, FR-008; one pull request)

- [x] T002 [US5] Red: in `tests/test_package_security.py`, turn `test_payload_scripts_hold_only_the_scanner`, `test_validator_rejects_extra_payload_script`, `test_validator_rejects_whole_scripts_folder_copy` and `test_source_checkout_requires_the_scanner` into tests that a staged payload or archive with any entry under `scripts/` (the scanner included) is rejected, while the source checkout still requires `scripts/scan-lexicon.py` (the validator's `check_lexicon` imports its table parser through `scripts/lexicon_check.py`; keep `test_source_checkout_requires_the_scanner`); run that module and see it fail
- [x] T003 [US5] `scripts/validate-package.py`: drop `scripts` from `PACKAGE_PAYLOAD`, `EXACT_DIRECTORY_FILES` and `PACKAGE_COPY_SOURCES` and the file-level copy rule; add an explicit staged-payload prohibition for `scripts/` beside the `SOURCE_ONLY_DIRECTORIES` check (`validate_payload_tree` only visits configured roots, so dropping the root alone accepts an extra `scripts/helper.py`); keep the source checkout's requirement of `scripts/scan-lexicon.py` for `check_lexicon`; `scripts/package-skill.sh`: stop staging `scripts/`; T002 green
- [x] T004 [US5] Red then green in `tests/test_skill_contract.py`: `SKILL.md` and `references/writing-workflow.md` name no `scripts/scan-lexicon.py` and no shell command for detection (contracts/skill-text.md); remove the scanner sentence from `SKILL.md` and the "Tìm ứng viên bằng script" section from `references/writing-workflow.md`; update the guards that checked them (`test_lexicon_reading_path_in_skill_routing`, `test_scanner_invocation_rules`, `test_skill_text_works_without_scanner`); in `.plugin-skills/vietnamizer/SKILL.md` stop resolving a packaged `scripts/` path and update its guard in `test_lexicon_in_validator_inventory`
- [x] T005 [P] [US5] `references/ai-error-lexicon.md` intro and `scripts/lexicon_check.py` docstring: rows are known examples, an article with no hit is not clean, the scanner is a maintainer tool outside the package; public Vietnamese text through Vietnamizer
- [x] T006 [P] [US5] Consumer documents: `AGENTS.md` (file table, "Không có evaluator ngoài"), `README.md`, `docs/architecture.md`, `docs/usage.md`, `docs/plugin-distribution.md`, `PRIVACY.md`, `SECURITY.md`: the package is Markdown only, the scanner is a source-only maintainer tool; public Vietnamese text through Vietnamizer in Fio's voice
- [x] T007 [US5] `docs/changelog.md` 0.17.0 entry (still unreleased): no scanner in the package; build both archives with `scripts/package-skill.sh` and `python3 scripts/package-plugin.py`, check neither holds a script (SC-006); run `python3 scripts/validate-package.py`, `tests.test_package_security`, `tests.test_skill_contract`, `tests.test_scan_lexicon`, `tests.test_distribution` (one per command)
- [ ] T008 [US5] Pull request for Phase 2 with `review-gate` code and security reviews posted; merge only on Fio's go

## Phase 3: Development pool (FR-009, FR-010)

- [x] T009 Red then green: `benchmarks/holdout_036.py` and `benchmarks/holdout_marker.py` accept article ids `D` + two digits beside `H` + two digits (plan); tests in `tests/test_holdout_036.py` and `tests/test_holdout_marker.py`
- [x] T010 A fresh agent that edits no skill file generates D01–D10 per research.md R5 into `artifacts/dev-037/articles/` and pre-marks each sheet ("AI đề xuất"); prompts recorded beside the files
- [x] T011 Fio or a marker Fio names reviews D01–D10 sheets, in `benchmarks/holdout_marker.py` or on the shared marking page, and sets each to `xong` with the marker's name (decision 5); export shared sheets through `holdout_marker.build_sheet`; record O2 disagreements
- [x] T012 Commit `benchmarks/dev-037-manifest.json` (`holdout_036.py manifest artifacts/dev-037/articles`) and a `calibration/LOG.md` row for the T044 finding and the pool

## Phase 4: Recognition tests and detection pass (US1, US2, US3; one pull request)

Writers read D01–D03 and D06–D08 only (plan P2).

- [x] T013 [US1] Red: guards in `tests/test_skill_contract.py` for the V9 calque test (contracts/skill-text.md rows 1 and 4)
- [x] T014 [US1] Write **Phép thử nhận diện** for V9 in `references/sentence-structure.md` (research.md R2), with at least three examples from the tuning articles or HF/LX, and its **Không flag**; T013 green
- [x] T015 [P] [US2] Red: guards for the V20 clipped-compound and bare-collective tests
- [x] T016 [US2] Write both tests in V20 of `references/missing-words.md`, examples from development sources only; T015 green
- [x] T017 [US1] Red then green: `SKILL.md` long-form routing row names `references/missing-words.md` and `references/sentence-structure.md`; the small-edit row does not
- [x] T018 [US1] Red then green: the detection pass at the head of "Kê cụm khi biên tập toàn bài" in `references/writing-workflow.md` (contracts/skill-text.md row 6); check `SKILL.md` stays ≤ 550 lines and the pattern count stays 55 with `python3 scripts/validate-package.py`
- [x] T019 [P] [US3] `calibration/test-cases.md` block DT: positive and guard cases for each test from the tuning articles; agent runs of DT, HF01–HF18 and LX01–LX29 recorded as a development result (DT block written; agent runs of DT, HF01–HF17 and LX01–LX29 on candidate 1c3e9b7 recorded 21/11/2026 in `docs/benchmarks.md` "Spec 037"; HF18 not run, it needs a saved brand profile)
- [x] T020 [US1] Development iteration (plan P8): run Opus 5.5 and Sonnet 5.5 on Claude Code over the tuning articles, score with `holdout_036.py`, adjust the tests from those articles only; stop when the tuning articles clear the P3 ratios
- [ ] T021 Pull request for Phase 4 with `review-gate` reviews posted; Vietnamese text through Vietnamizer's own review; merge only on Fio's go

## Phase 5: Gate and freeze (FR-012)

- [ ] T022 Gate run on Cowork (plan P3): 0.16.2 and the candidate on D04–D05 and D09–D10, Opus 5.5 and Sonnet 5.5; record counts in the PR or `docs/benchmarks.md` development section. Fail: back to T020 (the gate articles then become tuning articles and the next gate needs new development articles). **Run 21/11/2026 on Claude Code `-p`** (Fio: no Cowork): candidate 1c3e9b7 Opus 1/4, Sonnet 0/4 lexicon-kind, guards 1/12 and 0/12 (0.16.2: 0/4, 0/4, guards 1/12 each); **failed**, counts in `docs/benchmarks.md` "Spec 037"
- [ ] T023 Freeze: record the candidate commit; build the test skill from it

## Phase 6: Holdout batch (runner only; FR-013–FR-017)

- [ ] T024 Runner generates H15–H20 with Gemini per spec 036 research.md R6 after the freeze, stores them outside Git, commits their manifest; Fio marks them
- [ ] T025 Runner enables `vietnamizer-0162-test` and a new test skill for the candidate on Fio's Cowork account, runs H01–H14 and H15–H20 with both versions on Opus 5.5 and Sonnet 5.5 (other models when quota allows) with the T044 prompt, random labels, records file reads and whether a detection pass shows (FR-017); disables both test skills after
- [ ] T026 Runner scores with `holdout_036.py score`, gets Fio's blind judgments via `holdout_036.py edits`, and returns contracts/holdout-report.md
- [ ] T027 Write the report to `docs/benchmarks.md` as counts only (FR-016), with the verdict against FR-014; a second holdout run is allowed once, only after a development-only change (FR-012)

## Phase 7: Release (FR-018, O1)

- [ ] T028 Review every product description against what ships (diagrams, README, docs, in-product help); fix drift or say why not
- [ ] T029 Release pull request (0.17.0 changelog, version files per `versioning`); merge, tag, release and catalog pin only on Fio's explicit go

## Requirements coverage

| Requirement | Tasks |
|---|---|
| FR-001–FR-004 tests under V9/V20 | T013–T016, T019 |
| FR-005–FR-007 detection pass | T017, T018 |
| FR-008 lexicon kept, scanner out | T002–T007 |
| FR-009–FR-010 development pool | T009–T012 |
| FR-011 isolation | all; T024–T027 by the runner |
| FR-012 gate, freeze, two runs | T022, T023, T027 |
| FR-013–FR-017 measurement | T024–T027 |
| FR-018 release | T029 |
| SC-001–SC-005 | T026, T027 |
| SC-006 | T007 |
| SC-007 | T019, T026 |

## Dependencies

- Phase 2 is independent of Phases 3–4 except `tests/test_skill_contract.py` and `references/writing-workflow.md` (Phase 4 starts after Phase 2 merges).
- T009 before T010–T012; T011 before T014, T016, T019.
- Phase 5 after Phase 4 merges; Phase 6 after T023; Phase 7 after T027 and Fio's go.
- Parallel: T005 ∥ T006; T015 ∥ T014 (different files).
