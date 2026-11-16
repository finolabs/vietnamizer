# Tasks: AI-error lexicon, phrase inventory and optional scanner

**Input**: Design documents from `specs/036-ai-error-lexicon/` (spec.md, plan.md, research.md, data-model.md, contracts/, quickstart.md)
**Prerequisites**: plan.md (merged in PR 65), constitution 2.8.0 on main, Fio's decisions P1–P8 and O6 (16/11/2026)

**Tests**: requested. The plan's delivery order is red first (a failing test before each file it checks), and FR-005, FR-017, FR-019 and FR-021 each name a test. Run `uptime` first and one test module per command (owner rule).

**Organization**: by user story from spec.md. US1 and US2 are P1, US3 and US4 are P2, US5 is P3. Phase 2 holds what every story needs: the constitution amendment and the lexicon table.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel (different files, no dependency on an unfinished task)
- **[Story]**: US1–US5 from spec.md

## Path conventions

Agent skill package at the repository root: `SKILL.md`, `references/`, `scripts/`, `tests/`, `calibration/`, `docs/`. Payload is built by `scripts/package-skill.sh` and checked by `scripts/validate-package.py`.

---

## Phase 1: Setup

**Purpose**: a branch and a clean baseline before any change.

- [ ] T001 Create branch `feat/036-ai-error-lexicon` from main in its own worktree under `.claude/worktrees/036-impl`, and record the baseline: `python3 scripts/validate-package.py` (expect v0.16.2, 55 patterns), then `python3 -m unittest tests.test_package_security`, then `python3 -m unittest tests.test_skill_contract`, one per command, in the PR notes
- [ ] T002 Read the current Principle V paragraph in `.specify/memory/constitution.md` and confirm the replaced span runs from "`SKILL.md` và các profile MUST dùng được" to "MUST NOT phụ thuộc một repo local khác." exactly as spec.md "Constitution amendment" says; stop and report if it differs

---

## Phase 2: Foundational (blocks every story)

**Purpose**: the amendment that permits the scanner, and the single lexicon table both paths read.

**⚠️ CRITICAL**: no package change before T003 is committed (plan Constitution Check V).

- [ ] T003 Apply the constitution amendment as its own commit in `.specify/memory/constitution.md`: replace the Principle V span with the two paragraphs of spec.md "Constitution amendment" verbatim, keep the Jev/TypeSafe sentence unchanged, set the version line to 2.9.0 with Last Amended set to the date this commit lands, and add a Sync Impact Report entry "2.8.0 -> 2.9.0 (MINOR: Principle V allows optional offline scripts in the package; no obligation removed)" with owner approval "Fio, 15/11/2026, 'Bản mày sửa' (spec 036 decision 6)"
- [ ] T004 Write the red table-structure test in `tests/test_scan_lexicon.py` (class `LexiconTableTest`) that fails while `references/ai-error-lexicon.md` is absent. It checks every rule of contracts/lexicon-table.md "Validation": header row byte-identical to `| ID | Dạng | Loại | Pattern | Sửa | Ngữ vực lỗi | Sau không là | Trước không là | Chữ hoa | Không flag | Ca |`; 11 non-empty cells per row with `—` only in `Sau không là` and `Trước không là`; IDs "Unique, continuous from `L01` in table order"; `Loại` in {`từ ghép bị cắt`, `dịch sát`, `từ nghề hiểu sai`, `danh từ tập thể đứng trơ`}; `Chữ hoa` in {`mọi`, `đầu câu`}; `Pattern` exists in the V/T catalogs; `Dạng` "1–4 syllables, written in NFC, lower case. One form per row"; every fix in `Sửa` (split on ` / `) differs from the form; every `Ca` id exists in `calibration/test-cases.md`; exactly one table in the file
- [ ] T005 Create `references/ai-error-lexicon.md` per contracts/lexicon-table.md "Layout": front matter `type: vietnamizer-ai-error-lexicon`, `schema: 1`; a Vietnamese introduction of at most 12 lines (a hit is a candidate, never an edit by itself; the row's and the owning pattern's **Không flag** both apply; the table runs only on prose outside the T1–T6-only genres; how to read the neighbour columns); `## Bảng` with entries L01–L08 from data-model.md "Seed entries", final Vietnamese wording written here; `## Thêm mục` restating FR-004 in one paragraph. Edit the Vietnamese with Vietnamizer's own review (AGENTS.md "Khi sửa nội dung"). T004 turns green
- [ ] T006 Create `tests/fixtures/lexicon/fixtures.json` with fixtures `LXF01`… holding `id` (`LXF` + two digits), `text`, `expected` (list of `entry`, `text`, `line`, `column`, `zone`; empty for a lexical guard), `agent` (`sửa` with expected output, or `giữ`) and `cases`. Cover data-model.md "Fixture": one positive and one guard per entry (FR-017); lexical guards *rườm rà*, *bỡ ngỡ*, *Đội ngũ*, *giữ nghĩa vụ*, *dịch sát nghĩa*; register guards HF08, HF12, HF13, HF15, HF16, HF17; NFD input, a soft hyphen inside *rườm­rà*, a line break between *giữ* and *nghĩa*, sentence-initial *Đội* in a paragraph, after `- `, `1. `, `> ` and `: `, inner *đội*, the L03/L05 overlap of HF11, and one match in each zone `frontmatter`, `code`, `link-url`, `quote`, `blockquote`
- [ ] T007 Extend `LexiconTableTest` in `tests/test_scan_lexicon.py` to fail when an entry lacks a positive or a guard fixture in `tests/fixtures/lexicon/fixtures.json`; run `python3 -m unittest tests.test_scan_lexicon` green

**Checkpoint**: constitution 2.9.0 committed; the table and fixtures exist and pass their structure test.

---

## Phase 3: User Story 1 - Known AI errors are caught in a long article on any host (P1) 🎯 MVP

**Goal**: the reading path. On the whole-article and writing routes the agent reads the lexicon and checks each hit against **Không flag**, with no script.

**Independent test**: edit the HF fixture articles with the scanner absent; the fixed spans equal the expected set (spec US1).

### Tests for User Story 1

- [ ] T008 [US1] Add red guards to `tests/test_skill_contract.py` per contracts/skill-text.md: the `SKILL.md` routing row "Biên tập toàn bài hoặc viết từ brief/outline" names `references/ai-error-lexicon.md` and the small-edit row does not; one sentence under the routing table says the script may run where code runs, the table is read otherwise, and no edit waits on the script; no sentence asks the user to enable or install anything; V20 in `references/missing-words.md`, V9 in `references/sentence-structure.md` and V19 in `references/terms-and-lead-ins.md` each have one line under **Dấu hiệu** naming their lexicon ids; pattern count stays 55

### Implementation for User Story 1

- [ ] T009 [US1] Add `references/ai-error-lexicon.md` to the long-form routing row of `SKILL.md` and add the one optional-scanner sentence under the routing table; keep `SKILL.md` ≤ 550 lines and the small-edit path's "luôn rà soát V20" line unchanged (plan P4)
- [ ] T010 [P] [US1] Add one line under **Dấu hiệu** of V20 in `references/missing-words.md` naming L01–L05 and L08; pattern body otherwise unchanged
- [ ] T011 [P] [US1] Add one line under **Dấu hiệu** of V9 in `references/sentence-structure.md` naming L06; pattern body otherwise unchanged
- [ ] T012 [P] [US1] Add one line under **Dấu hiệu** of V19 in `references/terms-and-lead-ins.md` naming L07; pattern body otherwise unchanged
- [ ] T013 [US1] Add `references/ai-error-lexicon.md` to `REFERENCE_FILES` in `scripts/validate-package.py` and run the table checks of T004 there too (header, cells, ids, kinds, patterns, forms, fixes); `Ca` ids are checked only in a source checkout because the payload has no `calibration/`
- [ ] T014 [US1] Write the inline-context rule in `references/ai-error-lexicon.md` load note or `SKILL.md` routing text: when the skill is given inline and the file is absent, say once that the lexicon is not available, keep the catalog checks and never invent rows (contracts/lexicon-table.md "Load route"); run `python3 -m unittest tests.test_skill_contract` green

**Checkpoint**: the reading path works on any host; the scanner does not exist yet.

---

## Phase 4: User Story 2 - Every paragraph of a long edit is examined (P1)

**Goal**: the internal phrase inventory on the long-form route.

**Independent test**: on a fixture article, ask to see the inventory; every paragraph appears, every lexicon hit is a row, every output edit traces to a kept row (spec US2).

### Tests for User Story 2

- [ ] T015 [US2] Add red guards to `tests/test_skill_contract.py` for the inventory section in `references/writing-workflow.md` per contracts/skill-text.md: the section exists before "Rà câu, đoạn và toàn bài"; it says every paragraph is visited and small edits build none (FR-006); it names phrase, paragraph, suspect pattern or entry, evidence, fix and **Không flag** result (FR-007); it says every candidate is a row and catalog suspects are rows too (FR-008); it says edit in place with no reassembly in edit mode, while writing from a brief keeps the workflow's assembly (FR-009); it says the inventory is not returned and is shown only on explicit request within the 5-line limit of "Trả kết quả" or to ask one point (FR-010)

### Implementation for User Story 2

- [ ] T016 [US2] Write the inventory section in `references/writing-workflow.md` before "Rà câu, đoạn và toàn bài", with the row fields and rules of data-model.md "Inventory row": overlapping candidates share one row with the union of their spans and one fix; `giữ` leaves the phrase byte-identical (SC-006); zone semantics of data-model.md "Zone semantics for the agent" (`frontmatter`, `code`, `link-url` frozen; `quote` frozen when verbatim; `blockquote` judged like prose unless it is a quotation). Pure Markdown, no file or tool beyond reading (FR-011). Vietnamese through Vietnamizer's own review; run `python3 -m unittest tests.test_skill_contract` green

**Checkpoint**: US1 + US2 give the MVP: every long-form edit walks every paragraph and every known form, on every host.

---

## Phase 5: User Story 3 - Claude Code and sandbox hosts use the scanner, with the same result (P2)

**Goal**: `scripts/scan-lexicon.py` in the package, optional, returning the same candidates as the reading path.

**Independent test**: the scanner returns exactly the expected candidates on `tests/fixtures/lexicon/fixtures.json` (SC-001), and the reading path flags the same set (spec US3).

### Tests for User Story 3

- [ ] T017 [US3] Add red scanner tests to `tests/test_scan_lexicon.py` (class `ScannerTest`), importing the module and calling `scan(text, entries)` directly (research R4): every fixture returns exactly its `expected` candidates, ordered by position then entry id, with `line`, `column` (1-based, Unicode code points of the original input) and `paragraph` (1-based, separated by blank lines); overlapping entries are all reported
- [ ] T018 [US3] Add red CLI tests to `tests/test_scan_lexicon.py` (class `ScannerCliTest`) running `python3 -I scripts/scan-lexicon.py` as a subprocess per contracts/scanner-cli.md: stdout one JSON object `{"schema": 1, "lexicon_sha256": <first 12 hex>, "candidates": [...]}` with `ensure_ascii=False`; exit 0 with or without candidates; exit 2 with one stderr line and empty stdout on any argument other than `--help`, empty input, invalid UTF-8, or more than 1,000,000 bytes; exit 3 on a missing or malformed lexicon (use a copy of the script in a temp tree); a UTF-8 BOM is stripped; the two quickstart.md §1 commands give the stated results
- [ ] T019 [US3] Add the red AST allow-list test to `tests/test_scan_lexicon.py` (class `ScannerPrincipleVTest`) per contracts/scanner-cli.md "Principle V mapping": imports limited to `__future__`, `argparse`, `hashlib`, `json`, `pathlib`, `re`, `sys`, `unicodedata`; reject `os`, `io`, `importlib`, `builtins`, `socket`, `urllib`, `http`, `ssl`, `subprocess`, `tempfile`, `shutil` and dynamic `__import__`; reject attribute access to `environ`, `getenv`; reject any `open` other than the lexicon read in mode `"r"` or `"rb"` and any `pathlib` write, `unlink`, `rename`, `mkdir` or `touch`; the output schema has no field holding edited text; run the CLI once inside a read-only temp directory

### Implementation for User Story 3

- [ ] T020 [US3] Implement `scripts/scan-lexicon.py` (Python 3.9+, standard library only): read `sys.stdin.buffer.read(1_000_001)`, strip BOM, refuse per R4; read the lexicon only from `../references/ai-error-lexicon.md` relative to the script file and parse the table by its exact header row; normalise to NFC, drop U+00AD and zero-width characters, fold whitespace runs inside a paragraph to one space with an offset map back to the original (R2); tokenise syllables with `[^\W\d_]+`; match 1–4 syllable forms with `casefold()` equality unless `Chữ hoa` is `đầu câu` (data-model "Sentence start": line start after one Markdown marker `-`, `*`, `+`, `1.`/`1)`, `>`, `#`–`######`, or after `.`, `!`, `?`, `…`, `:`, `;`, `—` with optional closing quotes); apply `Sau không là` and `Trước không là`; set `zone` per R5 and drop nothing; print the JSON of contracts/scanner-cli.md. T017–T019 turn green
- [ ] T021 [US3] Teach `scripts/validate-package.py` the payload `scripts/` root: `EXACT_DIRECTORY_FILES["scripts"] = {"scripts/scan-lexicon.py"}` for staged payloads and archives only; in a source checkout require only that `scripts/scan-lexicon.py` exists; make the `copied_payload != PACKAGE_COPY_SOURCES` check accept the file-level source `scripts/scan-lexicon.py` so a copy of the whole `scripts/` folder still fails (research R3)
- [ ] T022 [US3] Stage only `scripts/scan-lexicon.py` into the payload in `scripts/package-skill.sh`; leave `scripts/package-plugin.py` unchanged (plan "Source code")
- [ ] T023 [US3] Update `tests/test_package_security.py`: the payload accepts exactly `scripts/scan-lexicon.py` and `references/ai-error-lexicon.md` as new files and still rejects any other code file, any other file under `scripts/`, and a whole-folder copy; run `python3 -m unittest tests.test_package_security` green
- [ ] T024 [US3] Make `.plugin-skills/vietnamizer/SKILL.md` resolve `scripts/` from the plugin root like `profiles/` and `references/`
- [ ] T025 [US3] Write the scanner invocation rules for the agent in `references/writing-workflow.md` inventory section (or a short subsection it points to), per contracts/scanner-cli.md "Invocation by the agent": paths in POSIX single quotes with `'` written as `'\''`; a user-named file via `< '<path>'`; pasted text written with the host's file-write tool to a new scratch file, scanned, then deleted; without such a tool and at most 100,000 bytes, the single-quoted here-document with delimiter `VNZ_END_OF_TEXT_036` only when no line equals it; never an argument, `echo`, double quotes or unquoted here-document; any failure or more than 20 s means the reading path, at most one retry, no request to enable or install, no mention of the path unless asked (FR-014). Add the matching guards to `tests/test_skill_contract.py`, including FR-019 (no instruction waits on the scanner; the skill text works with the file absent)
- [ ] T026 [US3] Build and check: `python3 scripts/validate-package.py`, then `bash scripts/package-skill.sh`, then `python3 -B scripts/package-plugin.py`, then `python3 -B scripts/package-plugin.py --check`, then `claude plugin validate .`; both archives list `scripts/scan-lexicon.py` and `references/ai-error-lexicon.md` and nothing else under `scripts/` (quickstart.md §2)

**Checkpoint**: scanner in the package; tests green; FR-021 consumers (Phase 8) must land in the same PR.

---

## Phase 6: User Story 4 - Voice is applied after errors are fixed, and the result is rescanned (P2)

**Goal**: order errors → voice → rescan on every long-form edit.

**Independent test**: a fixture where the profile's preferred phrasing would produce a lexicon form; the rescan catches it (spec US4).

### Tests for User Story 4

- [ ] T027 [US4] Add red guards to `tests/test_skill_contract.py`: `references/writing-workflow.md` states the order once (errors, then voice, then rescan of the lexicon, the touched paragraphs and the five chốt; the rescan also runs without a profile, after the error pass and after review edits) (FR-015); it says the error fix wins and a profile makes a form acceptable only when the row's **Không flag** covers that register (FR-016); the apply steps of `references/voice-from-samples.md` and `references/voice-profile.md` point to that order

### Implementation for User Story 4

- [ ] T028 [US4] Write the order and rescan rules in `references/writing-workflow.md`, next to the inventory section; voice adjustments stay distinguishable from error fixes (Principle II); a voice adjustment that recreates a lexicon form outside its **Không flag** sends the row back to `sửa` and is reverted (data-model "Inventory row" state transitions)
- [ ] T029 [P] [US4] Point the apply step of `references/voice-from-samples.md` to the order in `references/writing-workflow.md`
- [ ] T030 [P] [US4] Point the apply step of `references/voice-profile.md` to the order in `references/writing-workflow.md`; run `python3 -m unittest tests.test_skill_contract` green

**Checkpoint**: all P1 and P2 stories in place.

---

## Phase 7: User Story 5 - Maintainers grow the lexicon from evidence only (P3)

**Goal**: an entry without evidence cannot pass validation.

**Independent test**: a contract test rejects an entry without a pattern, a source case, a fix or a **Không flag** condition (spec US5).

- [ ] T031 [US5] Add negative tests to `tests/test_scan_lexicon.py` (class `LexiconGrowthTest`) that feed `LexiconTableTest`'s checker a table copy with a row missing `Pattern`, `Ca`, `Sửa` or `Không flag`, with `Ca` holding no guard case, or with a fix equal to the form, and expect each to fail
- [ ] T032 [US5] Add an evidence row to `calibration/LOG.md` for the lexicon seed (HF01–HF18 sources) and for the Sonnet 5.5 V20 miss on 0.16.2 (it never opened `missing-words.md`; Orrery memory `01M7EZ2JW53X6TRFSA515G4RVK`)
- [ ] T033 [US5] Add block LX to `calibration/test-cases.md` mirroring `tests/fixtures/lexicon/fixtures.json` as agent-judgment cases, and a note under the HF block that HF01–HF18 are development cases, never proof (FR-020)

**Checkpoint**: growth rule enforced.

---

## Phase 8: Polish & cross-cutting (same PR as Phase 5 for FR-021)

- [ ] T034 [P] Rewrite `AGENTS.md` "Không có evaluator ngoài" and its file table for the 2.9.0 Principle V: one optional offline script and one data table in the package (FR-021, plan Governance row)
- [ ] T035 [P] Update the package-contents statements in `README.md` ("Nền tảng hỗ trợ"), `docs/architecture.md`, `PRIVACY.md` and `SECURITY.md`: the scanner reads only stdin and the lexicon, writes nothing, calls no network, and is optional; mention the lexicon in `docs/patterns.md` and `docs/usage.md`. Public Vietnamese text through Vietnamizer in Fio's voice
- [ ] T036 Bump to 0.17.0 in `SKILL.md` metadata, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.antigravity-plugin/plugin.json` and every other file the versioning contract and AGENTS.md "Version" name, and add the 0.17.0 entry under `Unreleased`/dated heading in `docs/changelog.md` (FR-022); run `python3 -m unittest tests.test_distribution`
- [ ] T037 Run the README checklist: `readme_check.py` from the `plugin-packaging` skill (its `scripts/` folder; the repository has no copy) on the release branch and fix each failure or record why not in the PR
- [ ] T038 Review every product description against what ships (diagrams, README, docs, in-product help) before asking for the release; list drift fixed or left with reason in the PR

## Phase 9: Evidence before release (after the PR merges; plan steps 7–9)

- [ ] T039 Agent runs of HF01–HF18 and block LX on Claude Code with the scanner, then with `scripts/` removed from a copy of the installed skill; record candidate sets and outputs in `docs/benchmarks.md` as a development result (SC-004, SC-006)
- [ ] T040 Live probes per research.md R1 protocol on Claude Code, Codex (after 17/11/2026 10:16), Antigravity (when a Gemini pool has quota; Gemini weekly pool out until 21/11/2026), Claude.ai and Cowork with the 0.17.0 candidate package; record host, version, model id, date and result in `docs/benchmarks.md` (O3)
- [ ] T041 Parity runs (FR-018, SC-002, SC-003): the same fixtures on Claude.ai with a test package built without `scripts/` (plan P8) and with the full package; record every difference with fixture, host, model id and date; a release needs no difference or Fio's written acceptance of each
- [ ] T042 Implement `benchmarks/holdout_036.py` (source only, never packaged): NFC-normalise sheet, article and output; align each marked sentence with `difflib`; fixed, broken and out-of-span rules of contracts/holdout-marking-sheet.md "What counts"; report per model recall on lexicon kinds and other marked errors, guard breaks, judged over-corrections, time and tokens, with model ids, corpus manifest hash, lexicon hash and package versions
- [ ] T043 Generate the 20 holdout articles per research.md R6 after the lexicon and skill text are frozen, store them outside Git with a committed SHA-256 manifest, and hand them to Fio for marking (O2); no agent that edits the lexicon sees them
- [ ] T044 After Fio marks the articles, run 0.16.2 and 0.17.0 on every available P2 model; Sonnet 5.5 and Opus 5.5 on Claude Cowork are required (O6), Argon, Flash and GPT run when quota allows and are reported as not run otherwise; write the report to `docs/benchmarks.md` (SC-005); release only on Fio's go (O7)

---

## Dependencies & execution order

### Phase dependencies

- **Setup (Phase 1)**: none.
- **Foundational (Phase 2)**: after Setup; T003 before any other change; T004 → T005 → T006 → T007.
- **US1 (Phase 3)**: after Phase 2.
- **US2 (Phase 4)**: after Phase 2; independent of US1 in files except `tests/test_skill_contract.py` (serialise edits to that file).
- **US3 (Phase 5)**: after Phase 2; T025 edits the US2 section in `references/writing-workflow.md`, so after T016.
- **US4 (Phase 6)**: after T016 (same file, next to the inventory section).
- **US5 (Phase 7)**: after Phase 2.
- **Polish (Phase 8)**: after US3; must land in the same PR as Phase 5 (FR-021).
- **Evidence (Phase 9)**: after the PR merges; T043 after the skill text is frozen; T044 after Fio's marking.

### User story dependencies

- US1, US2, US5: only Phase 2.
- US3: Phase 2, and T016 for T025.
- US4: T016.

### Within each story

Red test first, then the file that turns it green; one test module per command, `uptime` first.

### Parallel opportunities

- T010, T011, T012 (three catalog files).
- T029, T030 (two voice references).
- T034, T035 (different documents).
- US5 (T031–T033) beside US1 once Phase 2 is done, except edits to the same test file.

## Parallel example: User Story 1

```text
T010 references/missing-words.md   V20 pointer line
T011 references/sentence-structure.md   V9 pointer line
T012 references/terms-and-lead-ins.md   V19 pointer line
```

## Implementation strategy

### MVP first (US1 + US2)

1. Phase 1 and Phase 2 (constitution 2.9.0 committed first).
2. US1 reading path, then US2 inventory.
3. Stop and validate on the HF fixtures with no scanner: this already serves Chat, Cowork and every host.

### Incremental delivery

1. MVP (US1 + US2).
2. US3 scanner with its package changes and Phase 8 documents in the same PR (FR-021).
3. US4 order and rescan.
4. US5 growth rule.
5. Phase 9 evidence; release 0.17.0 only on Fio's go (O7).

All of Phases 1–8 form one pull request (plan "Delivery order": steps 1–6 together), with one reviewable commit per step and its check output. Phase 9 produces evidence in `docs/benchmarks.md` before a separate release pull request.

## Notes

- [P] tasks touch different files with no unfinished dependency.
- Vietnamese text in the package and public documents goes through Vietnamizer's own review before commit.
- No tag, release, catalog pin or publish without Fio's explicit go.
