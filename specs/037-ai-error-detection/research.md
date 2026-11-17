# Research: Detect AI errors in fresh Vietnamese text

**Date**: 2026-11-17. Inputs: `docs/benchmarks.md` "Holdout 036" (main `ccfe199`), spec 036 (spec, plan, research R6, tasks T039–T044, contracts), `references/ai-error-lexicon.md`, `scripts/scan-lexicon.py`, `references/writing-workflow.md`, `SKILL.md`, the V9/V20 catalog text, `calibration/test-cases.md` (HF01–HF18, LX01–LX29), `benchmarks/holdout_036.py`, `benchmarks/holdout_marker.py`, Orrery memory "Vietnamizer 0.17.0 holdout: lexicon does not generalize" (17/11/2026) and the `typesafe-ai` skill. The author of this file read no holdout article or sheet; the holdout facts below are the counts the coordinator relayed.

## R1. Why fixed-form lookup did not reach the holdout errors

**Finding**: the 8 rows were seeded from HF01–HF18, which came from one set of articles and one README sentence. The holdout's 33 lexicon-kind errors share none of those surface forms; the 11 table forms present in the holdout are correct there. The scanner therefore returned nothing useful, and the agent, reading the table, looked for the same eight strings.

**Consequence**: a known-form list is exhaustive only for forms already seen. Calques (an English collocation rendered word for word) and clipped compounds (a two-syllable word cut to one) are open classes: each article brings new members. Detection must work from the shape of the error, which is what a recognition test states.

**Detection first, reluctance not ruled out**: the follow-up prompt "sửa lỗi tiếng Việt, không viết lại" removed any licence to restyle and still left 16–17 of 18 lexicon-kind errors untouched on Opus, and edited even less. Both models changed very few characters per article (`docs/benchmarks.md` "Holdout 036"). Not seeing the error certainly fails; reluctance to edit may add to it, and T044 cannot separate the two. The detection pass makes detection visible in the transcript, so the next batch counts detected-but-unfixed errors apart from undetected ones (spec FR-017).

## R2. Recognition tests, one per kind

**Decision**: each kind gets a short sequence of questions about one phrase in context, ending in a candidate or not, followed by that pattern's **Không flag**. Draft shape (final Vietnamese wording is written in the implementation, from development examples only, and goes through Vietnamizer's own review):

| Kind | Where it lives | Questions (draft) | Fix rule | Không flag (draft) |
|---|---|---|---|---|
| Calque (*dịch sát*) | V9, `references/sentence-structure.md` | 1. Put the phrase back into English word for word: does it give one ordinary English collocation or idiom (verb–object, adjective–noun, a fixed connective)? 2. For the same meaning, does a Vietnamese writer in this genre normally use a different phrase? 3. Would a reader who knows no English find the phrase odd or have to translate it back to understand it? Candidate when 1 and 2 hold, or 3 holds. | Replace the phrase with the common Vietnamese phrase of the same meaning, at the smallest unit; keep the sentence | Calques that are now standard in the genre; trade terms for in-trade readers (V19); quoted English; deliberate effect; literal meaning |
| Clipped compound (*từ ghép bị cắt*) | V20 case 1–3, `references/missing-words.md` | 1. Is this a one-syllable content word (adjective, verb, noun) in written prose? 2. In this role and meaning, does written Vietnamese of this register normally use a two-syllable word that contains it? 3. Do two-syllable words of the same kind stand beside it, so it reads cut off? Candidate when 1 and 2 hold. | Complete the word; never restructure | V20's existing **Không flag** (valid single words, chat, UI labels, formal sentences already complete, style pairs like *sạch / sạch sẽ*) |
| Bare collective noun (*danh từ tập thể đứng trơ*) | V20 case 3, same file | 1. Is a collective noun (*đội, nhóm, bên, phía, ban, team*) the subject or object? 2. Does it lack a determiner, a name or an earlier mention that says which group? Candidate when both hold. | Use the group's name from context, *đội ngũ*, or *cả đội* only when the text means the whole team | A determiner or earlier referent exists; the word is a verb (*đội mũ*); fixed names |

**Rationale**: a model fluent in both languages can answer each question about one phrase, while "does this read naturally?" asked of a whole paragraph returns yes for the same model's own output (R1). The back-translation question turns the model's bilingual knowledge from the cause of the error into its detector. Questions are ordered so the cheap one (1) filters most phrases.

**Alternatives considered**: a larger table of forms built from non-holdout sources (Fio chose not to, decision 1; it fails for the same reason as R1, only later); a list of "suspect English collocations" in Vietnamese (a word list again); one generic question "is this a calque?" (no shape for the model to check).

## R3. A detection pass before any fix

**Decision**: on the whole-article and writing routes, the agent walks the text sentence by sentence and applies the three tests to every sentence, writing inventory rows, and starts fixing only after the walk ends. The walk extends the existing inventory step (spec 036 FR-006 to FR-010); it does not replace the paragraph-level checks of the workflow.

**Rationale**: T044 shows models read the inventory instruction and then edit as they read, at paragraph level. Splitting "find" from "fix" and setting the unit to the sentence gives each sentence a fixed set of questions; the per-sentence record (visited, or rows) makes skipping visible in a transcript (spec FR-017). Asking the questions on every sentence is the only way to reach errors no list names.

**Cost**: about 60–100 sentences in a 1,500-word article. The pass adds output tokens (internal reasoning or notes) per sentence; the plan measures it (spec SC-005) rather than caps it.

**Alternatives considered**: running the tests only on sentences the model flags as suspicious (that is the 0.16.2 behaviour that missed 30 of 33); a separate second agent for detection (not available on every host, and the user does not see a second agent on Chat).

## R4. Jev/TypeSafe as a judge

**Read**: the `typesafe-ai` skill. A per-sentence Noul ("Is the phrase `x` in `sentence` a word-for-word rendering of an English expression that a Vietnamese writer would say differently?") fits its "find and judge evidence" and line-by-line search cookbook pattern, with code collecting candidate phrases and Jev judging each. The skill asks for live probes on representative, hard and negative cases and for validating Vietnamese behaviour first.

**Decision**: not used (Fio, decision 1). At runtime it needs network code and an API key in the package, against Principle V (Jev removed in 0.14.0, spec 029; adding it back needs an amendment), and Cowork may block outbound calls. As a maintainer tool it was offered and not chosen.

## R5. Development pool

**Decision**: 10 fresh AI articles D01–D10, 800–1,500 words, two per genre of the holdout's five (personal blog, expertise post, product or marketing copy, guide or README prose, operations report), topics from Fio's domains (retail, fashion, supply chain, SaaS). Generators: D01–D05 `claude-opus-5-5`, D06–D10 `gpt-6` through Codex (Gemini is out until 21/11/2026 and is kept for H15–H20, so the fresh holdout also tests a generator the development pool never saw). Prompts ask for an article, never for errors. A fresh agent that edits nothing in the skill generates and pre-marks them with the holdout sheet contract; Fio reviews each sheet in `benchmarks/holdout_marker.py` (decision 5). Files live outside Git in `artifacts/dev-037/`; `benchmarks/dev-037-manifest.json` commits ids and SHA-256 of article and sheet.

**Rationale**: the holdout's shape (genres, length, generators) is public in spec 036 R6 without its content, so mirroring it does not leak anything and keeps development and proof comparable. Ten articles at 3–6 marked errors each give 30–60 development errors, enough to write three tests with several worked examples and still keep part of the pool unseen for the gate (P2 in the plan).

**Alternatives considered**: published Vietnamese AI text from the web (unknown generator and date, may be edited by humans; allowed only as cited extra examples, spec FR-009); reusing HF/LX only (47 short cases from one source, the set that built the failed table).

## R6. Holdout rerun and overfitting control

**Decision**: the runner reruns H01–H14 with 0.16.2 and the frozen candidate in one batch on Cowork (Opus 5.5 and Sonnet 5.5 required), one output per article, version and model (56 outputs), with the T044 prompt and settings, output labels drawn at random, scored by `benchmarks/holdout_036.py`; Fio judges out-of-span edits blind. H15–H20 run in the same batch (24 outputs) once generated and marked. The holdout runs at most twice for this version; the second run is allowed only after a development-only change.

**Rationale**: the H01–H14 counts already shaped this spec (they showed detection is the bottleneck). Further rounds that read counts and tune can still fit the holdout through its counts. Two runs bound that, and H15–H20, generated after the freeze by a generator the development pool lacks, checks the result on text nobody has used.

**Who runs it**: a session started for the batch that edits no skill file, works from the spec 036 holdout procedure, and reports counts only (contracts/holdout-report.md). It enables the two test skills on Fio's account only for the batch and disables them after, as in T044.

## R7. Removing the scanner from the package

**Decision**: `scripts/scan-lexicon.py` stays in the source tree as a maintainer tool (like `scripts/check-consistency.py`), because `scripts/lexicon_check.py` and `tests/test_scan_lexicon.py` use its table parser and the LXF fixtures keep checking the table's neighbour and case columns. It leaves the payload: `package-skill.sh` stops copying it, `validate-package.py` drops `scripts` from the payload roots so any file under payload `scripts/` fails again, and the four scanner tests in `tests/test_package_security.py` flip to that rule. `SKILL.md` and `references/writing-workflow.md` lose the scanner sentence and section; the inventory and reading path stay.

**Consumers** (from `git grep scan-lexicon` at `448efb3`): `SKILL.md`, `references/writing-workflow.md`, `AGENTS.md`, `README.md`, `docs/architecture.md`, `docs/usage.md`, `docs/plugin-distribution.md`, `docs/changelog.md`, `PRIVACY.md`, `SECURITY.md`, `calibration/LOG.md` (history, unchanged), `scripts/validate-package.py`, `scripts/package-skill.sh`, `scripts/lexicon_check.py` (docstring), `tests/test_package_security.py`, `tests/test_skill_contract.py`, `tests/test_scan_lexicon.py`. The constitution's principles name no script and stay at 2.9.0; its sync impact report names the scanner as the first user of the 2.9.0 clause, which stays true as history. Spec 036 files are history and stay unchanged.

**Alternatives considered**: deleting the scanner and its tests (moves the parser into `lexicon_check.py` and rewrites tests for no user gain); keeping it in the package (Fio, decision 2).
