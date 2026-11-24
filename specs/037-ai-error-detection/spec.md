# Feature Specification: Detect AI errors in fresh Vietnamese text

**Feature Branch**: `spec/037-ai-error-detection`
**Created**: 2026-11-17
**Status**: Planned ([plan.md](plan.md)); tasks in [tasks.md](tasks.md); no implementation yet.
**Input**: Fio, 17/11/2026, after the spec 036 release proof (T044): hold 0.17.0 and open a new spec that makes Vietnamizer actually detect AI errors in fresh Vietnamese text, chiefly calques (*dịch sát*), and also clipped compounds (*từ ghép bị cắt*) and bare collective nouns (*danh từ tập thể đứng trơ*). Delegated by the coordinator session `local_c94f3fc0-fa20-4142-8374-d4a879f60b8f`. Router depth DEEP, trigger `uncertainty`: no measured mechanism yet makes a model notice an error it writes itself, and every whole-article edit changes.

## Background: what the 036 holdout showed

Spec 036 (merged on main, unreleased as 0.17.0) added an 8-row lexicon of known AI error forms, a phrase inventory step on the whole-article route and an optional scanner. Its release proof ran on 17/11/2026 on claude.ai Cowork: 56 runs over 14 fresh holdout articles H01–H14 (H01–H07 by `claude-opus-5-5`, H08–H14 by `gpt-6`), which Fio marked with 48 errors, 33 of them of the lexicon kinds (23 calques, 9 clipped compounds, 1 bare collective noun), and 38 guards.

| Model | Version | Lexicon-kind fixed | Other errors fixed | Guards broken | Mean time per article |
|---|---|---|---|---|---|
| Opus 5.5 | 0.16.2 | 3/33 | 2/15 | 0/38 | 57 s |
| Opus 5.5 | 0.17.0 | 2/33 | 2/15 | 1/38 | 76 s |
| Sonnet 5.5 | 0.16.2 | 0/33 | 1/15 | 0/38 | 43 s |
| Sonnet 5.5 | 0.17.0 | 0/33 | 1/15 | 0/38 | 39 s |

Source: `docs/benchmarks.md` "Holdout 036" (main `ccfe199`). Out-of-span edits (95–97 per Opus set, 31–37 per Sonnet set) are not yet judged; Cowork shows no token counts. The mechanism ran: every run loaded the skill, 0.17.0 read the lexicon in 24 of 28 runs and ran the scanner in 6 (exit 0, no candidate). But the table's fixed surface forms match 0 of the 33 marked errors; the 11 forms it does find in the corpus are not errors Fio marked. A follow-up prompt "sửa lỗi tiếng Việt, không viết lại" on 4 articles with Opus still left 16–17 of the 18 lexicon-kind errors there untouched.

**Detection is the part that certainly fails.** The editing model reads the calque as fluent, as the generating model did. Both models also edit very little (Opus about 50–60 characters per article, Sonnet about 9), and the T044 record notes that reluctance to edit may contribute; that run could not separate the two causes. This spec targets detection and measures both (FR-017). A list of fixed forms does not reach new errors of the same kind, because calques and clipped compounds are open classes. This spec changes how the agent looks at each sentence, not which strings it looks for.

## Settled decisions (Fio, 17/11/2026, native question tool)

1. **Recognition tests plus a per-sentence pass.** The skill teaches, for each of the three kinds, a short recognition test the agent applies to phrases (for a calque: does a word-for-word back-translation give one English collocation, and would a Vietnamese writer in this genre say it another way?), and the whole-article route adds one detection pass that visits every sentence for these three kinds before any fix. Pure Markdown; runs on Cowork and every host. Examples come only from sources outside the holdout. Not taken: a larger example table on top; asking Jev/TypeSafe per sentence (needs network code in the package, against Principle V; Jev was removed in 0.14.0 and is not validated on Vietnamese); Jev at maintainer time only.
2. **Keep the lexicon and the inventory, drop the scanner from the package.** The phrase inventory stays as the place where recognition-test hits are recorded; the 8 lexicon rows stay as known examples, no longer described as the way errors are found. `scripts/scan-lexicon.py` leaves the package (it matched 0 of 33, ran in 6 of 28 runs, and adds a shell command and a code surface to every long edit). Constitution 2.9.0 stays: it allows a script, it does not require one. Not taken: keep all three; drop the lexicon and the scanner and return to the 0.16.2 base.
3. **Release bar on the same 14-article holdout**: Opus 5.5 fixes at least 17 of the 33 lexicon-kind errors and Sonnet 5.5 at least 11, on Cowork; per model, guard breaks and edits Fio judges `sai` are no more than 0.16.2's in the same batch (0.16.2 broke 0 of 38 guards in T044, so in practice this asks for no guard break). Not taken: only "clearly better than 0.16.2" (+8 errors); a higher bar (25 and 17).
4. **Plan and tasks in the same pull request as this spec.**
5. **Development labels: an agent proposes, a human marker reviews.** A fresh agent that edits no skill text proposes error and guard rows for the new development articles, as for the holdout; Fio, or a marker Fio shares the marking page with, reviews each sheet, and that marker's reviewed sheet is the label without a second review by Fio (amended 18/11/2026, Fio: "Tính thẳng làm nhãn"). Each sheet names its marker. Review runs in `benchmarks/holdout_marker.py` on Fio's machine or on a shared claude.ai marking page that starts from the agent's rows and exports through the same sheet builder. Not taken: agent-only labels (they share the model's blind spot); Fio marking alone; two markers per article.
6. **0.16.2 is rerun in the same batch** as the candidate, same models and settings, outputs labelled at random. Not taken: reusing the T044 scores as the baseline.
7. **H15–H20 are generated after the text freeze and reported beside the bar.** The six Gemini articles that spec 036 moved to the next version are generated after this version's skill text is frozen, marked by Fio and run in the same batch; they are reported separately as a fully fresh holdout and do not count toward the bar of decision 3. Not taken: folding them into a 20-article bar; keeping them for a later version.

## Settled decisions after the T022 gate (Fio, 23/11/2026, native question tool)

8. **Second development round, designed from a root-cause review.** The T022 gate failed (Opus 1/4, Sonnet 0/4 lexicon-kind errors). An advisor review, read-only and by a Claude reviewer on a separate install, found that the test examples quote 7 of the 11 tuning errors word for word, that keep rules in the same catalogs likely veto 3 of the 4 gate errors (its reading from the sheets and the rules; the raw outputs were lost), that no test reaches V19 (trade terms read the wrong way), that tuning and gate articles differ in genre, and that a 4-error gate cannot tell a working change from noise. Fio chose to follow its plan:
   - D04, D05, D09 and D10 become tuning articles, so all of D01–D10 tune.
   - The round starts with a diagnostic run on D01–D10 that records, for every marked error, whether the phrase was not flagged, flagged and kept (with the reason given), or fixed; raw outputs are kept.
   - Tests change by structure, not by more examples from scored articles: a question on ambiguity that also reaches V19 trade terms, asked only when the text itself shows a second meaning or a reader outside the trade could take the everyday one; keep rules for operational genres narrowed to labels, table cells and bullets; the V15 keep rule for *việc* plus a clause no longer protects a causal *Với việc X, Y*; examples written as rule-based fix and keep pairs; no example quoted from an article that is scored.
   - A new gate pool D11–D22: twelve articles, six by `claude-opus-5-5` (D11–D16) and six by `gpt-6.1-sol` (D17–D22), across the five genres, marked as decision 5 says. The gate needs at least 20 lexicon-kind errors across the pool and at least 4 per kind; when the marked sheets hold fewer, more articles are added before the gate runs. D11–D14 were written on 23/11/2026 by a fresh `claude-opus-5-5` subagent that loaded no skill and read no file, with research R5's prompt, and count toward the six by Opus; the coordinating session has not read them, and no session that has read D11–D22 edits skill text, rules, calibration or tests.
   - The gate runs on Claude Code `-p` (Fio, 21/11/2026), two runs per model per article, raw outputs kept; P3's ratios apply to the pooled count; a person judges near-miss fixes that the accepted-fix match does not count.

   Not taken: another wording round on D01–D10 alone; a four-article gate written by Opus alone.

## Open decisions

| # | Decision | Owner | Unblocks when |
|---|---|---|---|
| O1 | Release go for the next version (merge, tag, release, catalog pin) | Fio | After the holdout report (FR-016); never on a relayed yes |
| O2 | Fio's written acceptance of any recognition-test example or **Không flag** he disagrees with in the development review | Fio | Development sheets reviewed (FR-010) |

O2 record (Fio, 19/11/2026, relayed by the coordinator from the PR 81 Codex review, rounds 1–2):

- Kept despite Codex's objection: V20 example *"Phần nào khó nhất với đội của bạn?"* → *"...đội ngũ của bạn"* (D02 sheet #5, DT08). Codex read *của bạn* as a determiner that V20's **Không flag** keeps. Fio: keep the example as the sheet labels it. The **Không flag** now states the narrow exception: a possessive says whose team, not which group, so when the sentence speaks of a person's whole staff and of no group doing a task, *đội* falls under test question (2).
- Changed: V9 example and DT01 *"Tôi không gửi nhiều hơn một tin mỗi ngày"* now become *"Mỗi ngày tôi gửi tối đa một tin"*; *"chỉ gửi một tin"* can read as one message every day and loses the zero-message case. Fio ruled on 21/11/2026 that both wordings are correct: the D01 sheet (#4) now accepts *"Mỗi ngày tôi chỉ gửi một tin"* and *"Mỗi ngày tôi gửi tối đa một tin"*; on 24/11/2026 Fio also accepted Sonnet's T034 wordings *"Tôi chỉ gửi một tin mỗi ngày"* and *"Tôi gửi tối đa một tin mỗi ngày"* and Opus's T034a/b wording *"Tôi không gửi quá một tin mỗi ngày"*, and DT01 now accepts *chỉ gửi* and *không gửi quá*, and `benchmarks/dev-037-manifest.json` records the new sheet hash. On 23/11/2026 the pool folder was deleted by mistake during a worktree cleanup; articles and the D02–D10 sheets were restored byte for byte from agent transcripts and the marking page, and the D01 sheet was rebuilt from its reviewed 19/11 rows with this ruling applied (row #4 accepts both wordings), so its hash changed again (`1031bb82…`); the raw run outputs were lost. Runs c1–c10 were recorded against the earlier manifest (`f2cd5400…`). Rescored against the new sheet, c9 stays Opus 6/11, Sonnet 6/11; c10 becomes Opus 7/11, Sonnet 6/11; guards 0 in both.
- Changed in round 1: V9 example and DT03 *"Tôi nói trước:"* become *"Nói trước là ..."*, keeping the advance warning. The D01 sheet (#2) now accepts *"Nói thật,"* and *"Nói trước là"*; Opus fixed D01#2 in T034c with *"Tôi nói trước là ..."*.
- Kept, with the defect each one shows (safeguard 1: the author's wording is wrong, clipped or misleading):
  - V20 *"quy trình nào bị dừng"* → *"bị dừng lại"* (D07 sheet #6, DT07): marked as a clipped compound with no note; agent's reading: in a list of process events *dừng* alone reads cut off beside the two-syllable verbs around it.
  - V9 *"Bạn đặt vài quy tắc cơ bản"* → *"thiết lập vài quy tắc"* (D03, DT05): not a sheet row; taken from D03 as a word-for-word *set some rules*; Fio keeps it.
  - V9 *"...nhưng không ai cập nhật trạng thái"* → *"...không được cập nhật trạng thái"* (D02 sheet #4, DT06): marked as a calque with no note; agent's reading: *không ai* copies the English *no one updated* subject where Vietnamese writing of this kind uses the passive. On 24/11/2026 Fio ruled that the sheet and DT06 also accept *chưa được cập nhật*, the V9 example's fix since PR 90.

O2 record (Fio, 23/11/2026, native question tool, after the T030 diagnostic):

- Changed: the D01 sheet (#2) also accepts *"Nói trước là"*, and the D05 sheet (#4) also accepts *"Do TTPP Thuận An đã hoạt động đủ sáu cửa xuất hàng"*; Opus 5.5 wrote both in T030 and the sheets had counted them as unfixed. `benchmarks/dev-037-manifest.json` records the two new sheet hashes.
- Accepted risk: Fio marks the D11–D22 sheets himself and also approves examples under O2. The isolation rule binds agent sessions only, so gate content could reach skill text through the person who marks it; Fio accepts that risk rather than naming another marker.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Calques are caught in a fresh AI article (Priority: P1)

A user pastes a 1,200-word AI draft about retail operations into Vietnamizer on Cowork with Sonnet 5.5 and asks for an edit. The draft has calques none of the lexicon rows name. Before fixing anything, the agent walks every sentence and, for each verb–object pair, fixed phrase or connective that reads like a word-for-word rendering, applies the calque test. It records each hit in the inventory, checks **Không flag**, and fixes the kept ones in place with a common Vietnamese phrasing of the same meaning.

**Why this priority**: 23 of the 33 holdout errors are calques, and both models missed nearly all of them.

**Independent Test**: Run the edit on development articles with marked calques that appear in no lexicon row and no skill example; count the marked calques fixed.

**Acceptance Scenarios**:

1. **Given** a development sentence whose verb–object pair renders an English collocation word for word and has a common Vietnamese equivalent, **When** the agent edits the article, **Then** the inventory has a row for it and the output replaces only that phrase.
2. **Given** a calque that has become standard Vietnamese in the genre (for example *đóng vai trò*), **When** the test fires, **Then** **Không flag** keeps it byte-identical.
3. **Given** a term the trade uses in English or as a fixed loan translation for its readers, **When** the reader is in the trade, **Then** it is kept (V19 owns that judgment). Since decision 8 the ambiguity question still applies when the text itself shows a second meaning of the term or a reader outside the trade could take the everyday one.

---

### User Story 2 - Clipped compounds and bare collective nouns are caught (Priority: P1)

The same edit also finds single syllables standing where written prose in that register needs the two-syllable word, and collective nouns (*đội*, *nhóm*, *bên*) standing as subject with no referent, including forms no lexicon row lists.

**Why this priority**: 10 of the 33 holdout errors; V20 is the pattern the maintainer observes most often in AI text, and 0.16.2 already missed it on Sonnet.

**Independent Test**: Development articles with clipped forms and bare collectives outside the lexicon; count fixed and count guards kept.

**Acceptance Scenarios**:

1. **Given** a product description with a clipped adjective that no lexicon row names, **When** the agent edits, **Then** the inventory has a row and the output completes the word.
2. **Given** a chat line, a UI label or a formal sentence where the single syllable is complete (V20 **Không flag**), **When** the test fires, **Then** the text is unchanged.
3. **Given** *nhóm* as subject after the article has named the team, **When** the agent edits, **Then** it is kept.

---

### User Story 3 - Correct text stays correct (Priority: P1)

A user edits an article that is already natural. The per-sentence pass asks its questions everywhere; it must not turn every single syllable or every phrase with an English twin into an edit.

**Why this priority**: Principle II. A detection gain bought with over-correction fails decision 3.

**Independent Test**: Guard rows of the development sheets and LX guard cases; count guards broken; Fio's blind judgment of out-of-span edits.

**Acceptance Scenarios**:

1. **Given** a guard span on a development sheet, **When** the agent edits, **Then** no byte of it changes.
2. **Given** a sentence with no hit, **When** the agent edits, **Then** it is byte-identical.
3. **Given** a one-sentence edit request, **When** the agent works, **Then** no per-sentence pass runs over the rest of the text.

---

### User Story 4 - Maintainers improve detection without seeing the holdout (Priority: P2)

A maintainer writes or tunes a recognition test. They work only from development sources and see holdout results only as counts. A separate runner, who edits nothing, runs the holdout and returns counts.

**Why this priority**: The holdout is the only evidence the rules generalize (Principle IV); one look at it ends that.

**Independent Test**: The holdout report names the runner and states that the runner edited no skill text; every example in the skill and calibration traces to a development source listed in the development manifest.

**Acceptance Scenarios**:

1. **Given** a maintainer editing skill text, rules, the lexicon or calibration, **When** they need evidence, **Then** they use development sources only and never open `artifacts/holdout-036/` or the H15–H20 files.
2. **Given** a holdout run, **When** results return to the maintainer, **Then** they are counts per model and kind (fixed, guards broken, judged edits), never sentences, spans or row ids.

---

### User Story 5 - The package no longer ships the scanner, and nothing waits for it (Priority: P2)

A user on any host runs a whole-article edit. The package holds no executable file; the agent does all detection by reading, with no shell command and no permission prompt.

**Why this priority**: Decision 2, and every document that describes the scanner as shipped must stay true.

**Independent Test**: Build the package; the validator rejects any file under the payload `scripts/`; the skill text names no scanner command.

**Acceptance Scenarios**:

1. **Given** the built skill ZIP and plugin ZIP, **When** they are inspected, **Then** neither holds `scripts/scan-lexicon.py` or any other script.
2. **Given** a whole-article edit on Claude Code, **When** the agent works, **Then** it runs no shell command for detection.

### Edge Cases

- A phrase that is a calque and also a clipped compound (*giữ nghĩa và giọng*): one inventory row, one fix, as spec 036's overlap rule says.
- A calque inside a quotation, code, a link target, frontmatter or a proper name: protected zone, never edited (SKILL.md "Trước khi làm").
- A calque the source author clearly chose for effect (irony, a quoted English idiom marked as such): kept.
- English inline terms (*ROI*, *checkout*) are V19's question of reader and field, not the calque test; decision 8's ambiguity question covers Vietnamese trade terms a reader can take the wrong way.
- Genres that only get T1–T6 (contracts, legal, ceremonial, changelog, commit, UI strings, poetry): the three tests do not run.
- A very long article: the pass still visits every sentence in scope; the plan bounds the cost and reports time and tokens.
- A voice profile whose preferred phrasing is a calque: the error fix wins unless the test's **Không flag** covers that register (spec 036 FR-016 stays).
- A host loads the skill inline without reference files: the tests in `SKILL.md`'s routing text still apply; the agent says once that the catalog is missing, as today.

## Requirements *(mandatory)*

### Functional Requirements

**Recognition tests**

- **FR-001**: The catalog text of V9 (calques), V20 (clipped compounds and bare collective nouns) MUST state a recognition test for each of the three kinds: questions the agent answers about one phrase in context, each with its **Không flag**. A test describes a class of error, not a word list (decision 1).
- **FR-002**: Each test MUST carry at least three worked examples, positive and guard, drawn only from development sources (FR-009); no example may come from the holdout. Since decision 8 the examples are written by the maintainer to illustrate the rule, and none is quoted from a development article that is scored (D01–D22); sheet rows stay in `calibration/test-cases.md`.
- **FR-003**: The tests MUST sit under existing patterns: no new pattern number, the count stays 55, and AGENTS.md "Ngưỡng thêm pattern" holds. Each test states why the form is an error and how to fix it (Principle I).
- **FR-004**: A test hit is a candidate. An edit is kept only after the owning pattern's **Không flag** and the five chốt, as today.

**Per-sentence detection pass**

- **FR-005**: On the whole-article and writing routes, the agent MUST run a detection pass that visits every sentence in scope and applies the three tests before making the first fix. Every hit becomes an inventory row (spec 036 FR-007 fields); a sentence with no hit is recorded as visited.
- **FR-006**: Small edits MUST NOT run the pass over text outside the requested scope; within their scope the catalog's tests apply when that catalog is read.
- **FR-007**: The pass and the inventory stay internal and pure Markdown, need no tool beyond reading, and keep the output rules of "Trả kết quả".

**What happens to 0.17.0**

- **FR-008**: The lexicon file and the inventory step MUST stay. The lexicon's description MUST say its rows are known examples, not the way errors are found, and an article with no row hit is not clean. The scanner MUST leave the package, and in the same pull request every consumer that describes it as shipped MUST change: `SKILL.md`, `references/writing-workflow.md`, `.plugin-skills/vietnamizer/SKILL.md`, `AGENTS.md`, `README.md`, `docs/architecture.md`, `docs/usage.md`, `docs/plugin-distribution.md`, `PRIVACY.md`, `SECURITY.md`, `docs/changelog.md`, `scripts/validate-package.py`, `scripts/package-skill.sh` and their tests, so the validator again rejects every file under the payload `scripts/`; the source checkout keeps the scanner as a maintainer tool. The constitution stays at 2.9.0.

**Development set and isolation**

- **FR-009**: Development sources are HF01–HF18, LX01–LX29 and a new development pool of fresh AI articles generated for this spec by an agent that edits no skill text, on prompts that ask for an article and never for errors; optionally published Vietnamese sources on calques, cited in `docs/sources.md` at their reliability. The plan sets the pool's size and genres.
- **FR-010**: Development articles are marked with the holdout sheet contract (spec 036 `contracts/holdout-marking-sheet.md`): a fresh agent proposes rows, a human marker (Fio or one Fio names) reviews every sheet, and each sheet names its marker (decision 5).
- **FR-011**: Nobody who edits skill text, rules, the lexicon, calibration or tests may read `artifacts/holdout-036/`, the H15–H20 files or their sheets, and no example may come from them. Holdout runs are made by a runner who edits none of those files; the runner returns counts only (per model, version and kind: fixed, guards broken, judged edits, time, tokens).
- **FR-012**: Before any holdout run, the candidate MUST be frozen (commit recorded) and measured on the development pool with the same scorer; the plan sets the development level that allows the holdout run. The holdout runs at most twice for this version (one candidate and one retry), so counts cannot steer many rounds.

**Measurement**

- **FR-013**: The proof reruns H01–H14 with `benchmarks/holdout_036.py`: 0.16.2 and the candidate in the same batch, same prompt and settings, outputs labelled at random (decision 6). Opus 5.5 and Sonnet 5.5 on Claude Cowork are required; other models run when quota allows and are reported as not run otherwise.
- **FR-014**: The bar is decision 3: Opus at least 17 of 33 lexicon-kind errors fixed, Sonnet at least 11; per model, guard breaks and `sai` out-of-span edits no more than 0.16.2's in the same batch. Other marked errors (15), `không cần` edits, and time per article (tokens where the host shows them; Cowork does not) are reported beside it.
- **FR-015**: H15–H20 are generated after the freeze, marked by Fio, run in the same batch and reported separately as a fresh holdout (decision 7); they do not count toward FR-014.
- **FR-016**: Results go to `docs/benchmarks.md` as counts only, with model ids, host, date, corpus manifest hash, development manifest hash and the package commit of each version; no sentence or span from the holdout.
- **FR-017**: Each run records which skill files it read and whether its transcript shows a detection pass, so a miss can be told apart from a skipped step, as T044 did. Where the transcript shows inventory rows, the runner also counts, per model and version, marked lexicon-kind errors that were detected but left unfixed against those never detected (counts only), so detection and reluctance to edit are measured apart.

**Release**

- **FR-018**: The next release keeps the number 0.17.0, which was never tagged; its changelog entry describes what ships. Reports name the T044 candidate by its commit (`448efb3`) so the two candidates are never confused. Release only on Fio's go (O1).

### Key Entities

- **Recognition test**: per kind, the questions, the fix rule, **Không flag** and worked examples; lives in the owning pattern's catalog.
- **Detection pass**: one walk over every sentence in scope, before fixing, that applies the three tests and writes inventory rows.
- **Development pool**: fresh AI articles with reviewed sheets, used to write and tune tests; listed in a committed manifest of ids and SHA-256.
- **Holdout batch**: one frozen candidate and 0.16.2 run on H01–H14 (and H15–H20) by a runner who edits nothing; reported as counts.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On H01–H14, Opus 5.5 on Cowork fixes at least 17 of the 33 lexicon-kind errors (0.16.2 in T044: 3).
- **SC-002**: On H01–H14, Sonnet 5.5 on Cowork fixes at least 11 of the 33 (0.16.2 in T044: 0).
- **SC-003**: Per model, guards broken and edits Fio judges `sai` are no more than 0.16.2's in the same batch.
- **SC-004**: H15–H20 results are reported beside SC-001–SC-003 with the same measures; a large gap between the two holdouts is named in the report.
- **SC-005**: Time per article (and tokens where the host shows them) for each version and model is reported, with the ratio to 0.16.2.
- **SC-006**: The built packages contain no script, and every whole-article edit in the runs completes with no shell command for detection.
- **SC-007**: Every example in the skill text and in new calibration cases traces to a development source; the holdout report states the runner edited no skill file.

## Assumptions

- The Cowork models in the batch are the same model ids as T044 or newer; FR-013 reruns 0.16.2 so a model change does not bias the comparison.
- A detection pass over a 1,500-word article costs more tokens than 0.16.2; the cost is reported, not capped, in this version.
- "Fixed" means an accepted fix from Fio's sheet (or Fio's judgment when the cell is empty). A natural fix not listed counts as missed; this applies to both versions alike.
- The 14-article holdout was used once for T044's decision. Its counts, not its content, informed this spec; the H15–H20 report (decision 7) checks whether this version fits the first holdout too closely.

## Out of scope

- Runtime calls to Jev/TypeSafe or any external evaluator (Principle V; decision 1).
- Misread trade jargon (V19, L07) beyond keeping its current text and decision 8's ambiguity question; no holdout error was marked of that kind.
- Any new executable code in the package.
- Changes to spec 036's files (T044 and O7 are recorded by the coordinator separately).
- Code, reference or constitution changes in this pull request.
