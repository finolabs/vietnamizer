# Implementation Plan: AI-error lexicon, phrase inventory and optional scanner

**Branch**: `spec/036-plan` | **Date**: 2026-11-15 | **Spec**: [spec.md](spec.md)

**Input**: `specs/036-ai-error-lexicon/spec.md` (settled decisions 1–6, plan decisions P1–P8 below). Depth DEEP, triggers `contract` and `security`. Release 0.17.0, before spec 033 (decision 5).

## Summary

Ship a curated lexicon of known AI errors as one Markdown table, `references/ai-error-lexicon.md`, under the existing patterns V9, V19 and V20 (no new pattern number). On the whole-article and writing routes the agent builds an internal phrase inventory that visits every paragraph, takes every lexicon candidate as a row and keeps an edit only when the owning pattern's **Không flag** and the five chốt allow it. Where code can run, an optional scanner, `scripts/scan-lexicon.py` (Python standard library only, text on stdin, candidates as JSON on stdout), finds the same candidates by lookup; everywhere else the agent reads the table. Errors are fixed before any voice adjustment, and the final text is rescanned. The constitution's Principle V takes Fio's approved text (2.8.0 → 2.9.0) as the first commit of the implementation, and every document that says the package is Markdown-only changes in the same pull request as the scanner.

## Technical Context

**Language/Version**: Markdown instructions; the scanner and checks are Python 3.9+ standard library (`re`, `unicodedata`, `json`, `argparse`, `hashlib`, `unittest`).
**Primary Dependencies**: none new. No `underthesea`, `pyvi` or any package outside the standard library (spec, out of scope).
**Storage**: none. The scanner writes no file; the lexicon is a read-only data file in the package.
**Testing**: `tests/test_scan_lexicon.py` (new: scanner against fixtures, lexicon table structure, CLI contract, refusal cases); `tests/test_package_security.py` (payload accepts exactly the scanner and the lexicon, still rejects other code); `tests/test_skill_contract.py` (inventory, reading path, order and rescan phrases; no instruction waits on the scanner); `calibration/test-cases.md` block LX (agent judgment, run by hand); `scripts/validate-package.py`. One test module per command, `uptime` first (owner rule).
**Target Platform**: Claude Code, Codex, Antigravity, Skills CLI installs, Claude.ai Chat and Claude Org upload, Cowork. Per-host behaviour in [research.md](research.md) R1.
**Project Type**: agent skill package (Markdown) with one optional offline helper script.
**Performance Goals**: the scanner finishes a 1 MB input in under 2 s on a laptop; the lexicon adds at most about 2,500 tokens on the long-form route (P4).
**Constraints**: `SKILL.md` ≤ 550 lines (137 today); pattern count stays 55; Principle V as amended (no network, no secret, no file write, reads only stdin and package data); the scanner input cap is 1,000,000 bytes (R4).
**Scale/Scope**: seed lexicon of 8 entries (data-model.md "Seed entries"), growing only through FR-004; 20 holdout articles (P1); up to five model families in the release benchmark (P2).

## Plan decisions (Fio, 2026-11-15, native question tool)

| # | Question | Answer | Recorded effect |
|---|---|---|---|
| P1 | Holdout size (O2) | **20 articles** (proposal was 12) | 20 fresh AI articles, 800–1,500 words each; split in research.md R6 |
| P2 | Models for the 0.17.0 vs 0.16.2 comparison | **"Opus, Sonet, Argon, Gemini, các model GPT nếu có quota..."** | Each available model runs both versions on all 20 articles: Claude Opus, Claude Sonnet, Gemini Argon (`gemini-4-argon-high`), Gemini Flash (`gemini-3.8-flash-high`), GPT through Codex when quota allows. Which ones a release cannot skip stays open (O6) |
| P3 | Where the scanner sits in the package | **"Làm sao thì chuẩn theo agent skills và plugin packing"** | The Agent Skills layout and `plugin-packaging` both put executables in `scripts/` beside the skill: payload path `scripts/scan-lexicon.py`; the packager copies only that file from the source `scripts/` (R3) |
| P4 | Which routes read the lexicon | **Only the whole-article and writing routes** (recommended) | Small edits keep today's "luôn rà soát V20" line and do not load the table |

Decided by the plan author within the spec (reviewable in this PR, changeable by Fio at review):

| # | Decision | Why |
|---|---|---|
| P5 | Lexicon file name `references/ai-error-lexicon.md` (spec review LOW 2) | English file names in the package (memory "Vietnamizer naming"); says what the table holds; sorts beside the other references |
| P6 | The scanner reads the text only from standard input, never from command-line arguments or a path it opens (spec review LOW 3; narrows FR-012) | Text in an argument leaks into process lists and shell history and breaks on quoting; a path option would let the script open files Principle V does not list. A file the user named reaches the scanner as `< path`, opened by the host shell |
| P7 | Guard fixtures include HF17 (spec review LOW 1); calibration is HF01–HF18 | HF17 (*giữ nghĩa* in a formal report) is the guard for lexicon entry L03; HF18 is a profile-routing case with no lexicon form and stays out of the lexicon fixtures |
| P8 | A parity run "without code execution" on Chat uses a test-only package built without `scripts/` | Claude.ai loads skills only with code execution on (R1), so no real Chat session has the skill without a sandbox; removing the scanner from a test upload is the faithful way to exercise the reading path there (also proves SC-003) |

## Constitution Check

| Gate | Result |
|---|---|
| I. Vietnamese evidence first | Every entry ties to an HF case marked by Fio and to an existing pattern; the lexicon adds no rule, only known surface forms. Pass. |
| II. Meaning and voice | A hit is a candidate; an edit is kept only after **Không flag** and the five chốt (FR-002). Order errors → voice → rescan keeps voice adjustments distinguishable from error fixes (FR-015). Pass. |
| III. General rules vs profiles | Entries sit under V9/V19/V20; register-bound judgments stay in each entry's **Không flag** column, not in B/K. Pass. |
| IV. Labelled evidence | HF01–HF18 are development cases; proof is the sealed holdout (P1, R6), never used to build or tune the lexicon. Pass. |
| V. Self-contained Markdown | **Gate met by amendment**: 2.8.0 → 2.9.0 with Fio's approved text (spec decision 6), applied verbatim as the first commit of the implementation, before any package change. The scanner satisfies each condition of the new text (contracts/scanner-cli.md "Principle V mapping"). |
| Development gate 1 | Lookup of known surface forms is deterministic and lives in code (scanner); the error judgment stays with the model. Pass. |
| Development gate 5 | Release runs `validate-package.py`, `npx skills add . --list`, `claude plugin validate .`, reinstall and byte comparison; the scanner is part of the compared bytes. Pass. |
| Eval constraint (model and corpus version) | The holdout run records model id, corpus hash, lexicon hash and package version per output (R6). Pass. |
| Governance (`AGENTS.md` vs constitution) | `AGENTS.md` "Không có evaluator ngoài" says the package is Markdown only; it conflicts with 2.9.0 once applied and is rewritten in the same pull request (FR-021). |

Post-design re-check: pass. Residual risks: (1) a host shell may prompt for permission to run Python, which interrupts the user although the skill itself asks nothing; mitigated by falling back to the reading path on any refusal (FR-014) and by never suggesting the user enable anything. (2) Untrusted text or a user-named path reaching a shell; mitigated by single-quoted paths, by writing pasted text with the host's file tool instead of the shell, and, only without such a tool, a single-quoted here-document with a fixed delimiter refused when any line equals it, bounded at 100,000 bytes under `ARG_MAX` (contracts/scanner-cli.md "Invocation by the agent"). (3) A model may skip the inventory on a long article as Sonnet skipped V20 on 0.16.2; measured on the holdout (SC-005), not assumed away.

## Project Structure

### Documentation (this feature)

```text
specs/036-ai-error-lexicon/
├── spec.md                 # amended in this PR: HF01–HF18, HF17 guard, stdin only
├── plan.md                 # this file
├── research.md             # R1 hosts (O3), R2–R5 scanner design, R6 holdout (O2)
├── data-model.md           # lexicon entry, candidate, inventory row, fixture, seed entries
├── quickstart.md           # validation scenarios
├── contracts/
│   ├── lexicon-table.md    # column contract of references/ai-error-lexicon.md
│   ├── scanner-cli.md      # stdin/stdout/exit-code contract, Principle V mapping
│   ├── skill-text.md       # inventory, reading path, order and rescan wording contract
│   └── holdout-marking-sheet.md  # Fio's marking sheet (O2)
├── checklists/requirements.md
└── tasks.md                # task list (speckit-tasks, 16/11/2026)
```

### Source code (repository root)

```text
.specify/memory/constitution.md       # 2.9.0, first commit (Principle V text, decision 6)
references/ai-error-lexicon.md        # NEW, the lexicon table (package)
scripts/scan-lexicon.py               # NEW, the scanner (package, staged alone into payload scripts/)
references/writing-workflow.md        # inventory step, order errors → voice → rescan
references/voice-from-samples.md      # apply step points to the order and rescan
references/voice-profile.md           # apply step points to the order and rescan
references/missing-words.md, references/sentence-structure.md, references/terms-and-lead-ins.md
                                      # V20, V9, V19: one line each pointing to the lexicon rows
SKILL.md                              # routing row for the long-form route; scanner optional line
.plugin-skills/vietnamizer/SKILL.md   # resolve scripts/ from the plugin root too
scripts/validate-package.py           # payload scripts/ = exactly {scan-lexicon.py}; lexicon in REFERENCE_FILES; table check;
                                      # its package-skill.sh copy check (`copied_payload != PACKAGE_COPY_SOURCES`) learns the file-level source scripts/scan-lexicon.py
scripts/package-skill.sh              # stage scripts/scan-lexicon.py only
tests/test_scan_lexicon.py            # NEW
tests/fixtures/lexicon/fixtures.json  # NEW, positive and guard fixtures with expected candidates
tests/test_package_security.py, tests/test_skill_contract.py
calibration/test-cases.md             # block LX (agent judgment fixtures), HF block note
calibration/LOG.md                    # evidence row for the lexicon seed and the Sonnet V20 miss
AGENTS.md, README.md, docs/architecture.md, docs/patterns.md, docs/usage.md, docs/changelog.md,
PRIVACY.md, SECURITY.md               # Markdown-only statements (FR-021), lexicon mention, 0.17.0
.claude-plugin/, .codex-plugin/, .antigravity-plugin/ plugin.json   # 0.17.0
benchmarks/holdout_036.py             # NEW, runner and deterministic span scoring for R6 (source only)
```

`scripts/package-plugin.py` needs no change: it builds the plugin ZIP from the skill archive, so `skills/vietnamizer/scripts/scan-lexicon.py` follows. `scripts/check-consistency.py` and `scripts/scan-tells.sh` stay outside the package.

**Structure decision**: the source tree keeps one `scripts/` folder; the payload gets a `scripts/` folder holding exactly one file. The validator checks the payload inventory of `scripts/` only on staged payloads and archives, so maintainer scripts never enter the package.

## Path choice (Spec Kit depth gate)

DEEP, triggers `contract` (Principle V, a mandatory step in every whole-article edit) and `security` (first executable code in the package since 0.14.0, untrusted text reaching a shell). It runs `speckit-tasks` next; no direct path.

## Delivery order

1. Constitution 2.9.0 (verbatim text, own commit).
2. Lexicon table, fixtures and the table-structure test (red first: the test fails without the file).
3. Scanner and its tests (red first on the fixtures).
4. Validator, packager and payload tests; adapter path line.
5. Skill text: inventory, reading path, order and rescan; skill-contract tests.
6. Consumer documents (FR-021), version 0.17.0 in every file the versioning contract names.
7. Calibration block LX, LOG row; agent runs of HF01–HF18 and LX (SC-004, development result).
8. Parity runs (FR-018, SC-002) and the no-scanner package run (SC-003).
9. Holdout benchmark (R6, SC-005) after Fio marks the articles; release only on Fio's go.

Each step ends in a reviewable commit with its own check output (development gate 2). Steps 1–6 land in one pull request (FR-021 requires the scanner and the consumer changes together); steps 7–9 produce evidence recorded in `docs/benchmarks.md` before the release pull request.

## Open decisions (still Fio's)

| # | Decision | Owner | Unblocks when |
|---|---|---|---|
| O2 | Fio marks the 20 holdout articles with the sheet in contracts/holdout-marking-sheet.md; sheet format confirmed at review of this PR | Fio | Articles generated (step 9 prep) and marked before any 0.17.0 run over them |
| O3 | Live probes on Codex and Antigravity (research R1 "Live probe"). Claude.ai Chat and Cowork: resolved 15/11/2026, the main coordinator's probe on Fio's go ran a bundled script with Vietnamese stdin and package data, no permission prompt (research R1) | Implementer for Codex (quota back 17/11/2026 10:16) and Antigravity | Each probe recorded with host, version and date; a failed host is covered by the reading path only. Every host repeats the probe with the 0.17.0 package |
| O4 | Spec 033's own clause on top of the shared Principle V text | Spec 033 session, then Fio | Unchanged by this plan; note that spec 033's amendment section still says "2.6.1 → 2.7.0" while the constitution is at 2.8.0 and becomes 2.9.0 here |
| O6 | Which P2 models a release cannot skip when a model has no quota at benchmark time | Fio | Resolved 16/11/2026, Fio: "Sonnet và Opus của ClaudeWork". Sonnet 5.5 and Opus 5.5, run on Claude Cowork, are required before a release; Argon, Flash and GPT run when quota allows and are reported as not run otherwise |
| O7 | Release go for 0.17.0 (merge, tag, release, catalog pin) | Fio | After step 9 evidence; never on a relayed yes |

## Complexity Tracking

| Addition | Why needed | Simpler alternative rejected because |
|---|---|---|
| Executable code in the package | Spec decision 1, settled by Fio | Keeping it outside the package leaves Chat and Cowork sandboxes without it |
| Payload-only inventory for `scripts/` | Keeps maintainer scripts out of the package while following the standard layout (P3) | A separate top-level folder breaks the Agent Skills convention Fio chose |
