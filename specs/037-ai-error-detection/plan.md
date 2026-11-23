# Implementation Plan: Detect AI errors in fresh Vietnamese text

**Branch**: `spec/037-ai-error-detection` | **Date**: 2026-11-17 | **Spec**: [spec.md](spec.md)

**Input**: `specs/037-ai-error-detection/spec.md` (settled decisions 1–7). Depth DEEP, trigger `uncertainty`. Next release keeps the number 0.17.0 (spec FR-018).

## Summary

Teach the agent to recognise three kinds of AI error by their shape instead of by known strings. V9 gets a calque test and V20 gets a clipped-compound test and a bare-collective test: each a short sequence of questions about one phrase, with **Không flag** and worked examples from a new development pool only. The whole-article and writing routes gain a detection pass that applies the three tests to every sentence before the first fix and writes hits into spec 036's phrase inventory. The scanner leaves the package (kept in source as a maintainer tool); the lexicon stays as known examples. Proof is a rerun of the 14-article holdout against 0.16.2 in the same batch on Cowork, with a fixed bar (Opus ≥ 17/33, Sonnet ≥ 11/33, no more guard breaks or wrong edits), and a fresh 6-article Gemini holdout reported beside it.

## Technical Context

**Language/Version**: Markdown instructions; checks are Python 3.9+ standard library (`unittest`).
**Primary Dependencies**: none new.
**Storage**: none in the package. Development and holdout articles and sheets live outside Git under `artifacts/` (gitignored) with committed SHA-256 manifests.
**Testing**: `tests/test_skill_contract.py` (phrase guards for the tests, the pass, the scanner sentence removed); `tests/test_package_security.py` (payload `scripts/` rejected again); `scripts/validate-package.py`; `tests/test_scan_lexicon.py` stays green unchanged (maintainer tool); development runs scored by `benchmarks/holdout_036.py`; calibration cases run by hand. One test module per command, `uptime` first (owner rule).
**Target Platform**: Claude Code, Codex, Antigravity, Claude.ai Chat and Org upload, Cowork; the proof host is Cowork.
**Project Type**: agent skill package (Markdown only after this change).
**Performance Goals**: none capped; time per article (tokens where shown; Cowork shows none) reported against 0.16.2 (spec SC-005).
**Constraints**: `SKILL.md` ≤ 550 lines (139 today); pattern count 55; constitution 2.9.0 unchanged; holdout isolation (spec FR-011); at most two holdout runs (FR-012).
**Scale/Scope**: three recognition tests; one detection pass; 10 development articles; 56 holdout outputs on H01–H14 and 24 on H15–H20 per batch.

## Plan decisions (plan author, reviewable in this PR)

| # | Decision | Why |
|---|---|---|
| P1 | Development pool D01–D10 as research.md R5: two articles per holdout genre, D01–D05 by `claude-opus-5-5`, D06–D10 by `gpt-6.1-sol` (research R5), pre-marked by a fresh agent, reviewed by Fio or a marker Fio names (decision 5) | Mirrors the holdout's public shape without its content; keeps Gemini unseen for H15–H20 |
| P2 | Split the pool: D01–D03 and D06–D08 (6 articles) are for writing and tuning the tests; D04–D05 and D09–D10 (4 articles) are the development gate, never read by the person writing tests. Amended 23/11/2026 (spec decision 8): all of D01–D10 tune; the gate pool is D11–D22 | Principle IV inside the development set: a threshold is not proven on the cases that tuned it, and the holdout should not be the first unseen text |
| P3 | Development gate before the holdout run: on the 4 gate articles, scored with `holdout_036.py`, Opus fixes at least half and Sonnet at least a third of the lexicon-kind errors, and neither breaks more guards than 0.16.2 on the same articles. Amended 23/11/2026 (spec decision 8): gate pool D11–D22 with at least 20 lexicon-kind errors, two runs per model per article, ratios over the pooled count | The same ratios as the release bar; failing them on development text means the holdout run would be wasted |
| P4 | Tests live in the pattern catalogs: a **Phép thử nhận diện** paragraph in V9 (`references/sentence-structure.md`) and in V20 (`references/missing-words.md`, covering clipped compounds and bare collectives); the long-form routing row of `SKILL.md` names both catalogs so the pass always has them | Principle III (V patterns own general errors); the pass needs the tests loaded, and loading on suspicion is the 0.16.2 behaviour that missed |
| P5 | The pass is a new paragraph at the head of "Kê cụm khi biên tập toàn bài" in `references/writing-workflow.md`: walk sentence by sentence, apply the three tests, record hits or "đã xem", fix only after the walk | Reuses spec 036's inventory fields and output rules; one place states the order |
| P6 | Scanner stays in source, leaves the payload (research.md R7) | Keeps the table parser and LXF fixture tests; removes code and shell commands from every host |
| P7 | Holdout runner is a fresh session started for the batch that edits no skill file; it reports counts only in the shape of contracts/holdout-report.md | Spec FR-011; the maintainer never sees the holdout |
| P8 | Development iteration runs on Claude Code headless with the plugin installed from the worktree, Opus 5.5 and Sonnet 5.5; the gate run (P3) and the holdout run are on Cowork with test skills uploaded to Fio's account and disabled after. Amended 21/11/2026 (Fio): the gate runs on Claude Code `-p` with the plugin ZIP, not on Cowork | Cheap iteration where scripts can drive it; the proof host is the one Fio named |

## Constitution Check

| Gate | Result |
|---|---|
| I. Vietnamese evidence first | Each test states the error, why, the fix and **Không flag**, with examples from development sources reviewed by a human marker (decision 5). Pass. |
| II. Meaning and voice | A hit is a candidate; edits pass **Không flag** and the five chốt; guard breaks and judged wrong edits are part of the bar. Pass. |
| III. General rules vs profiles | Tests sit under V9 and V20; register-bound exceptions stay in **Không flag**. Pass. |
| IV. Labelled evidence | Tests are tuned on D01–D03/D06–D08, gated on D04–D05/D09–D10, proven on H01–H14 and checked on H15–H20; no case tunes and proves. Pass. |
| V. Self-contained Markdown | The package becomes Markdown only again; 2.9.0 permits a script and does not require one. Pass. |
| Development gate 1 | Detection is a semantic judgment and stays with the model; no deterministic step is moved into prose. Pass. |
| Development gate 5 | Release runs `validate-package.py`, `npx skills add . --list`, `claude plugin validate .`, reinstall and byte comparison. Pass. |
| Eval constraint (model and corpus version) | Reports carry model ids, corpus and development manifest hashes and package commits (spec FR-016). Pass. |

Post-design re-check: pass. Residual risks: (1) the pass may raise over-correction on single syllables and English-shaped phrases; measured by guards and Fio's blind judgment (SC-003), not assumed away. (2) Sonnet may skip the pass as it skipped V20 on 0.16.2; the transcript check (FR-017) tells a skip from a miss. (3) Cost per article rises; time is reported (SC-005), tokens only where the host shows them. (4) The bar may not be reachable by skill text alone; then the report says so and Fio decides the next step (O1), with no third holdout run. (5) Reluctance to edit may cap the gain even when detection works; FR-017's detected-but-unfixed count shows it, and a fix for it would be a separate change.

## Project Structure

### Documentation (this feature)

```text
specs/037-ai-error-detection/
├── spec.md
├── plan.md                  # this file
├── research.md              # R1–R7
├── quickstart.md            # how to run the development loop, the gate and the batch
├── contracts/
│   ├── skill-text.md        # where each obligation lives and what the phrase guards check
│   └── holdout-report.md    # counts-only report the runner returns
├── checklists/requirements.md
└── tasks.md
```

### Source (repository root)

```text
references/sentence-structure.md     # V9: calque recognition test, examples, Không flag
references/missing-words.md          # V20: clipped-compound and bare-collective tests
references/writing-workflow.md       # detection pass; scanner section removed
references/ai-error-lexicon.md       # intro: rows are known examples, not the detector
SKILL.md                             # long-form row names both catalogs; scanner sentence removed
.plugin-skills/vietnamizer/SKILL.md  # no packaged scripts/ path
scripts/validate-package.py          # payload roots without scripts/; staged scripts/ rejected; source keeps the scanner
scripts/package-skill.sh             # no scripts/ in the stage
scripts/lexicon_check.py             # docstring: scanner is a maintainer tool
tests/test_skill_contract.py, tests/test_package_security.py
calibration/test-cases.md            # new block DT (development cases from D01–D03/D06–D08)
calibration/LOG.md                   # T044 finding and this change
benchmarks/dev-037-manifest.json     # NEW, ids and SHA-256 of D01–D10
benchmarks/holdout_036.py, benchmarks/holdout_marker.py   # accept D-ids; tests beside them
AGENTS.md, README.md, docs/architecture.md, docs/usage.md, docs/plugin-distribution.md,
docs/changelog.md, PRIVACY.md, SECURITY.md, docs/benchmarks.md
```

`benchmarks/holdout_036.py` and `benchmarks/holdout_marker.py` score and mark both sets; today they accept only `H` + two digits as article ids (`holdout_036.py` lines 106, 140, 164; `holdout_marker.py` line 29), so they learn `D` + two digits for the development pool, with tests in `tests/test_holdout_036.py` and `tests/test_holdout_marker.py` (red first). Holdout scoring is otherwise unchanged.

## Path choice (Spec Kit depth gate)

DEEP, several seams (catalogs, workflow, packaging, evidence) with ordering between them (development pool before tests, freeze before H15–H20): `speckit-tasks` runs; no direct path.

## Delivery order

1. Scanner out of the package with its consumer documents and tests (one pull request; red first: the payload test that rejects `scripts/` fails before the validator change).
2. Development pool: generate D01–D10, pre-mark, human review (decision 5), commit the manifest.
3. Recognition tests and the detection pass, written from D01–D03/D06–D08; calibration block DT; phrase guards (red first).
4. Development iteration on Claude Code; then the gate run on Cowork (P3).
5. Freeze: record the candidate commit; generate H15–H20; Fio marks them.
6. Holdout batch by the runner (P7); report counts in `docs/benchmarks.md`.
7. Release documents (changelog, README version notes) and Fio's go (O1).

Steps 1 and 3 are separate pull requests with their own reviews; steps 2, 4, 5 and 6 produce evidence recorded before the release pull request.

## Complexity Tracking

| Addition | Why needed | Simpler alternative rejected because |
|---|---|---|
| A split development pool (tune / gate) | A gate on unseen development text before spending a holdout run | Tuning and gating on the same articles proves nothing (Principle IV) |
| A separate runner session | Holdout isolation (spec FR-011) | The maintainer running the batch would see outputs and spans |
