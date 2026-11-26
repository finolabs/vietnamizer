# Feature Specification: AI-error lexicon, phrase inventory and optional scanner

**Feature Branch**: `spec/036-ai-error-lexicon`
**Created**: 2026-11-15
**Status**: Removed from main on 26/11/2026 and never released (Fio: "Gỡ, không release"; see spec 037 Closure). Before that: implemented on main, not released. T001–T038 merged in PR 68 (zone fix PR 69); constitution 2.9.0 applied. The holdout (T044, PR 74) did not meet SC-005, so 0.17.0 is deferred (Fio, 17/11/2026: "Hoãn, mở spec mới") and detection moved to [spec 037](../037-ai-error-detection/spec.md). Spec 037 US5 (PR 76) took `scripts/scan-lexicon.py` out of the package; it stays a source-only maintainer tool, so FR-012, FR-014 and FR-018 no longer describe the shipped package. The lexicon, the phrase inventory and the errors-voice-rescan order still ship. The constitution amendment text was approved by Fio on 15/11/2026 (decision 6, shared with spec 033).
**Input**: Fio, 15/11/2026, after marking errors in sample AI articles that 0.16.2 (PRs 59 and 60) fixed one by one: the next version should have the agent build an explicit structure of the source's words and phrases, flag the wrong ones, fix the AI errors, apply the user's voice profile, then reassemble; it must run on cloud Chat and Cowork (a native sandbox at most) and may run extra scripts on Claude Code, with both paths error-free. Scope agreed in the coordinator's discussion with Fio the same day (session `local_c94f3fc0-fa20-4142-8374-d4a879f60b8f`). Router depth DEEP, triggers `contract` and `security`: the package would ship executable code for the first time since 0.14.0 (spec 029 removed the Jev runner), which needs a Principle V amendment, and every whole-article edit gains a mandatory step.

## Background

0.16.2 added T2 (mid-sentence colon), V20 cases for clipped compounds and bare *đội*, V9 calques and V19 misread trade jargon. Each fix widened a pattern's **Dấu hiệu**, but nothing makes the agent look at every phrase of a long article: it still reads the text as a whole, so errors it does not happen to notice pass through. Fio's marked articles show the same small set of AI errors recurring by exact surface form (*rườm* for *rườm rà*, *bỡ* for *bỡ ngỡ*, *giữ nghĩa* for *giữ ngữ nghĩa*, *gọi tên được lỗi*, *bản dịch sát*, sentence-initial *Đội*). A known surface form can be found by lookup, which the constitution's development gate 1 puts in code ("Parsing, tính toán và policy tất định nằm trong code; model chỉ làm phán đoán ngữ nghĩa"), while deciding whether a hit is an error in context stays a semantic judgment under each pattern's **Không flag**.

## Settled scope (coordinator with Fio, 2026-11-15)

1. **A curated lexicon of known AI errors ships as a data file.** Four kinds: clipped compounds (*rườm* → *rườm rà*, *nghĩa* → *ngữ nghĩa*), calques (*gọi tên được lỗi*), misread trade jargon (*bản dịch sát*) and bare collective nouns (*đội*). Seeded from calibration cases HF01–HF18 in `calibration/test-cases.md` (HF11–HF18 arrived with PR 60, released in 0.16.2).
2. **A mandatory internal phrase inventory for long-form edits**, pure Markdown, working on Claude.ai Chat and Cowork: for each suspect phrase, the phrase, the suspected pattern, the evidence, the fix and the **Không flag** check.
3. **An optional scanner** over the lexicon, Python standard library only, that returns candidates with positions. It runs on Claude Code and wherever a code sandbox exists and is never required: with no sandbox the agent scans the same lexicon by reading.
4. **Order:** fix errors, then apply the voice profile, then a final rescan.

Out of scope (same discussion): a full Vietnamese grammar matrix; external NLP libraries (underthesea, pyvi); reassembling sentences from the inventory in edit mode (edit mode edits in place; assembly from the inventory only when writing new text).

## Settled decisions (owner, 2026-11-15)

1. **The scanner ships inside the package** (skill ZIP and plugin), beside the lexicon, so Claude Code and any Chat or Cowork sandbox can run it. This needs the Principle V amendment (O1) and the consumer changes of FR-021. Not taken: keeping it in the source repo outside the package like `scripts/check-consistency.py`, which no Chat or Cowork sandbox could reach.
2. **The lexicon is one Markdown table** in `references/`, with fixed columns, read directly by the agent and parsed by the scanner from the same file. A test checks the table's structure. Not taken: a JSON file plus a generated Markdown view, which adds a generation step and a second copy that can drift.
3. **Proof comes from a fresh holdout of AI articles Fio marks** before release, never used to build or tune the lexicon; 0.17.0 and 0.16.2 run on the same model over it. The number of articles is set in the plan. Not taken: development set only; re-marking the 20 public sources of 0.11.0.
4. **One shared Principle V sentence with spec 033.** Principle V allows optional offline scripts under fixed conditions; a script that must read other files on the user's machine (spec 033's history reader) needs its own, stricter clause on top. Whichever spec lands first applies the shared sentence. Not taken: a named exception per script.
5. **Version 0.17.0, released before spec 033.** This spec applies the shared Principle V sentence; spec 033 later adds only its own clause and drops "ngoại lệ duy nhất". Not taken: 033 first.
6. **Principle V text (Fio, 15/11/2026: "Bản mày sửa").** The approved text is the one in section "Constitution amendment". It also rewrites the first sentence of Principle V in plain Vietnamese without MUST/MUST NOT, so the whole principle reads one way. Not taken: the first draft, which kept MUST in the first sentence and packed every script condition into one sentence.

7. **Scanner drops zoned matches (Fio, 17/11/2026: "Bỏ mọi zone").** After the PR 68 code review, the scanner drops every match inside frontmatter, code, link targets, quotation marks and blockquotes, and the candidate no longer carries `zone`. Reading-path parity (FR-018) is measured outside those zones; the agent still judges quoted emphasis and blockquote notes by reading. Not taken: reporting every match with a zone hint (the 15/11 design), or dropping only frontmatter, code and link targets.

## Open decisions

| # | Decision | Owner | Unblocks when |
|---|---|---|---|
| O1 | Exact text of the constitution amendment (section "Constitution amendment" below), reconciled with spec 033's O1 into one Principle V text | Fio | Resolved 15/11/2026: Fio approved the revised text (decision 6) |
| O2 | Size of the holdout (decision 3) and how Fio marks it (which errors count, guard spans) | Plan author, then Fio | Size settled 15/11/2026: 20 articles (plan P1); amended 17/11/2026: 14 articles (H01–H14, Claude and GPT) for 0.17.0, the six Gemini articles move to the next version (research.md R6); marking sheet in `contracts/holdout-marking-sheet.md`; Fio marks the articles before the release benchmark |
| O3 | Which hosts the parity check (FR-018) covers: whether Claude.ai Chat with code execution and Cowork's sandbox can run a script shipped in a skill and read its files | Plan author | Documentation checked 15/11/2026 (`research.md` R1). Claude.ai Chat and Cowork resolved 15/11/2026 by a live probe: a script shipped in a skill ran there and read the skill's data file. Codex and Antigravity probes remain before the parity run; a host that cannot is covered by the reading path only |
| O4 | Spec 033 updated to drop "ngoại lệ duy nhất" and keep only its own clause on top of the shared sentence (decision 4) | Session of spec 033, then Fio | Spec 033's amendment section rewritten on 15/11/2026 to sit on top of the shared text; the exact words of its own clause stay spec 033's O1 |
| O5 | PR 60 (`fix/035-calques`, HF11–HF16, V9/V19/V20 widening) merged into main | Fio | Resolved 15/11/2026: PR 60 merged (main `823ce7a`); the plan seeds the lexicon from merged text only |

## Plan amendments (15/11/2026)

Three LOW findings from the spec review, settled in the plan: HF17 joins the guard cases and calibration is HF01–HF18 (FR-003, FR-020, SC-004; plan P7); the lexicon file is `references/ai-error-lexicon.md` (plan P5); the scanner reads text only on standard input (FR-012; plan P6).

## Clarifications

### Session 2026-11-15

- Q: Does the scanner ship inside the skill package so a Chat or Cowork sandbox can run it, or stay in the source repo outside the package? → A: Inside the package (decision 1).
- Q: Is the lexicon one Markdown table both the agent and the scanner read, or JSON plus a generated Markdown view? → A: One Markdown table (decision 2).
- Q: Which set proves the lexicon helps, given HF01–HF16 built it (HF01–HF18 since 0.16.2)? → A: A fresh holdout of AI articles Fio marks (decision 3).
- Q: Do specs 033 and 036 share one Principle V sentence, or does each add its own exception? → A: One shared sentence; 033 adds a stricter clause on top (decision 4).
- Q: Is this 0.17.0 and released before spec 033? → A: Yes (decision 5).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Known AI errors are caught in a long article on any host (Priority: P1)

A user pastes a 1,500-word AI draft into Vietnamizer on Claude.ai Chat with no code execution and asks for an edit. The agent reads the lexicon, finds every known error form in the text, checks each against its **Không flag**, fixes the real ones in place and returns the article.

**Why this priority**: This is the error class Fio keeps marking by hand, and Chat users have no scripts at all. Without the reading path the lexicon helps nobody on Chat.

**Independent Test**: Run the edit on the HF fixture articles with the scanner unavailable; compare the set of fixed spans with the expected set.

**Acceptance Scenarios**:

1. **Given** an article containing *các thao tác quá rườm* and *giữ nghĩa và giọng* in a product description, **When** the user asks for an edit on a host without a sandbox, **Then** the output has *rườm rà* and *giữ ngữ nghĩa và giọng văn*, and nothing else in those sentences changes.
2. **Given** a chat message *“Sửa giúp mình mà vẫn giữ giọng mình nhé.”* (HF12) inside the article, **When** the lexicon entry for clipped *giọng* matches, **Then** the **Không flag** check keeps it and the text is unchanged.
3. **Given** an article with no lexicon hit, **When** the user asks for an edit, **Then** the agent still checks the other patterns as today; no lexicon hit is not treated as a clean article.

---

### User Story 2 - Every paragraph of a long edit is examined (Priority: P1)

A user asks Vietnamizer to edit a whole article. Before editing, the agent builds an internal phrase inventory: it walks the article paragraph by paragraph and records each suspect phrase with its suspected pattern, the evidence from context, the proposed fix and the result of the **Không flag** check. It edits only the rows that survive the check, in place.

**Why this priority**: The inventory is Fio's "explicit structure" request. It turns "read the whole and notice" into "visit every paragraph and justify every edit", which is what catches the errors that read fluently.

**Independent Test**: On a fixture article, ask for the inventory to be shown (a user may request it) and check that every paragraph appears, every lexicon hit appears as a row, and every edit in the output traces to a kept row.

**Acceptance Scenarios**:

1. **Given** a whole-article edit, **When** the agent returns the article, **Then** by default only the article is returned; the inventory stays internal, as the terminology table does today.
2. **Given** the user asks to see the edits, **When** the agent returns, **Then** it may show the inventory rows that led to edits, within the existing limit of the "Trả kết quả" section (at most 5 lines of notes or the Gốc/Đã sửa/Vì sao table).
3. **Given** a row whose **Không flag** check keeps the phrase, **When** the article is returned, **Then** that phrase is byte-identical to the source.
4. **Given** a one-sentence edit, **When** the agent works, **Then** no inventory is built; the small-edit path stays as it is.

---

### User Story 3 - Claude Code and sandbox hosts use the scanner, with the same result (Priority: P2)

On Claude Code (or a Chat or Cowork session with code execution that can reach the package's files, O3), the agent runs the scanner on the text and gets each lexicon candidate with its position. It feeds the candidates into the inventory and makes the same judgments as on the reading path.

**Why this priority**: The scanner makes the lookup exhaustive and repeatable where code can run; the reading path already delivers the value, so this is an accelerator.

**Independent Test**: Run the scanner on the fixture set and compare its output with the expected candidate set; run the reading path on the same set and compare both sets.

**Acceptance Scenarios**:

1. **Given** the fixture set, **When** the scanner runs, **Then** it returns exactly the expected candidates (entry, matched text, position) and nothing else.
2. **Given** the scanner cannot run (no Python, no shell, sandbox off, the command fails or times out), **When** the agent edits, **Then** it falls back to the reading path without asking the user to enable or install anything, and the edit completes.
3. **Given** the same fixture, **When** the scanner path and the reading path each run, **Then** both flag the same set of candidates.

---

### User Story 4 - Voice is applied after errors are fixed, and the result is rescanned (Priority: P2)

A user calls a saved voice profile (“theo giọng của tôi”) on a long AI draft. The agent first fixes language errors (inventory, lexicon, patterns), then applies the profile as a style adjustment under Principle II, then rescans the final text against the lexicon and the five chốt before returning.

**Why this priority**: A voice pass can reintroduce clipped or calqued forms that the error pass removed, or lock in an error as "the user's style"; the order and the rescan prevent both.

**Independent Test**: A fixture where the profile's preferred phrasing would produce a lexicon form; check that the rescan catches it.

**Acceptance Scenarios**:

1. **Given** a profile is called, **When** the agent edits, **Then** error fixes happen before any voice adjustment, and voice adjustments stay distinguishable from error fixes (Principle II).
2. **Given** a voice adjustment produces a lexicon form outside its **Không flag**, **When** the final rescan runs, **Then** that adjustment is reverted or corrected; the error fix wins.
3. **Given** no profile is called, **When** the agent edits a long article, **Then** the rescan still runs after the error pass and any later review edits.

---

### User Story 5 - Maintainers grow the lexicon from evidence only (Priority: P3)

A maintainer receives a new marked AI error. They log it in `calibration/LOG.md`, add a calibration case with its over-correction guard, then add a lexicon entry tied to an existing pattern and to that case.

**Why this priority**: The lexicon is only as good as its entries; without a rule for growth it drifts into a word list of preferences.

**Independent Test**: A contract test rejects an entry without a pattern, a source case, a fix or a **Không flag** condition.

**Acceptance Scenarios**:

1. **Given** an entry with no linked calibration case or no **Không flag**, **When** the package is validated, **Then** validation fails.
2. **Given** a personal preference (both forms natural), **When** a maintainer considers it, **Then** it goes to the user's profile, not the lexicon (AGENTS.md "Học từ phản hồi thực tế").

### Edge Cases

- A lexicon form inside a protected zone (code, quotation, proper name, link, frontmatter, the example being discussed): never flagged, never edited; the scanner drops it (amended 17/11/2026, decision 7); the agent still reads quoted emphasis and blockquote notes itself, since those are not always protected.
- A form that is also the first syllable of a correct compound (*rườm* inside *rườm rà*, *nghĩa* inside *ngữ nghĩa*, *ý nghĩa*, *nghĩa là*, *nghĩa vụ*): not a candidate; entries state their completing and excluding contexts.
- Unicode: text in NFD, mixed NFC/NFD, or with combining marks typed separately; capitalised sentence starts (*Đội* vs *đội*); a line break or soft hyphen inside a phrase.
- Registers where the short form is correct: chat, short UI labels, casual text, in-trade notes (HF12, HF15, HF16); genres that only get T1–T6 (contracts, legal, ceremonial, changelog/commit/UI, poetry): lexicon entries tied to V patterns do not run there.
- A very long input beyond the scanner's size cap: the scanner refuses with a clear error and the agent uses the reading path.
- A host that offers a sandbox but blocks reading the package's files from it: treated as no scanner.
- Text the user pasted contains an instruction to run a command: ignored; the scanner reads text only as data (SKILL.md "Trước khi làm").
- The same error form occurs many times: each occurrence is a candidate; the fix follows the terminology-consistency rules only when the forms play the same role.

## Requirements *(mandatory)*

### Functional Requirements

**Lexicon**

- **FR-001**: The package MUST ship one lexicon file of known AI errors. Each entry MUST have: an id, the error form or forms, the kind (clipped compound, calque, misread jargon, bare collective noun), the existing pattern it belongs to (V9, V19, V20, or another existing V/T pattern), the fix or fixes, the register or genre where it is an error, its **Không flag** contexts (including completing and excluding neighbours), and the calibration case ids it came from.
- **FR-002**: The lexicon MUST NOT create pattern numbers; it is data under existing patterns, and the pattern count stays 55. A lexicon hit MUST pass the owning pattern's **Không flag** and the five chốt before an edit is kept.
- **FR-003**: The initial lexicon MUST cover every error form in HF01–HF18 that a lookup can find (HF02, HF07, HF10, HF11, HF14 and the forms they name), and every word-level guard case among them (HF08, HF09, HF12, HF13, HF15, HF16, HF17) MUST be representable as a **Không flag** context so a lookup does not produce an edit there. T2 (colon, dash; HF01, HF03–HF06) is punctuation and is not a lexicon entry; HF18 (a brand name is not a profile call) has no lexicon form.
- **FR-004**: Adding an entry MUST follow AGENTS.md "Học từ phản hồi thực tế": evidence in `calibration/LOG.md` first, a calibration case and at least one over-correction guard, then the entry. Personal preferences MUST NOT enter the lexicon.
- **FR-005**: The lexicon MUST be one Markdown table in `references/` with fixed columns (decision 2), the single source for both paths; a test MUST check its structure (every column filled, ids unique and continuous, pattern ids existing). It MUST be readable by the agent with its ordinary file-reading tool and, where only inline context exists, from the skill's loaded references, so the reading path works on Chat and Cowork with no code execution.

**Phrase inventory**

- **FR-006**: On the whole-article edit route and the writing route of `SKILL.md` ("Biên tập toàn bài hoặc viết từ brief/outline"), the agent MUST build an internal phrase inventory before keeping any edit. Small edits (one phrase or sentence, local review) MUST NOT build one.
- **FR-007**: The inventory MUST visit every paragraph of the text in scope (a paragraph with no suspect is recorded as visited) and record, for each suspect phrase: the phrase as written, its location (paragraph), the suspected pattern or lexicon entry, the evidence from context, the proposed fix, and the **Không flag** result (kept as an edit, or dropped with the reason).
- **FR-008**: Every lexicon candidate (from the scanner or the reading path) MUST appear as an inventory row. Suspects the agent finds from the pattern catalogs, beyond the lexicon, MUST also be rows; the lexicon does not limit what the agent checks.
- **FR-009**: In edit mode the agent MUST edit in place, at the smallest unit (chốt 4); it MUST NOT reassemble sentences from the inventory. When writing new text from a brief, the agent MAY assemble from its plan as `references/writing-workflow.md` already allows, and the rescan (FR-015) still applies.
- **FR-010**: The inventory MUST stay internal: it is not part of the returned text, and it is shown only under the existing rules of "Trả kết quả" (on the user's explicit request, within its limits) or to ask about one point the agent cannot decide.
- **FR-011**: The inventory MUST be pure Markdown instructions in the skill: it needs no file, script or tool beyond reading, and it works the same on every host.

**Scanner**

- **FR-012**: The scanner MUST ship inside the package (decision 1) and MUST use only the Python standard library, make no network call, read no secret or API key, write no file, and read only the text it is given on standard input (a file the user named reaches it through the shell's input redirection; the text is never a command-line argument) and the lexicon file. It MUST NOT edit text; it prints candidates only.
- **FR-013**: For each candidate the scanner MUST report the entry id, the matched text as written and its position (line and column, and paragraph index). It MUST match on Vietnamese syllable boundaries after Unicode normalisation, treat case as the entry says, apply the entry's completing and excluding contexts, and drop matches inside frontmatter, code spans, code blocks, link targets, quotations and blockquotes (decision 7).
- **FR-014**: The scanner MUST be optional. The agent MUST use the reading path when the scanner cannot run for any reason, MUST NOT ask the user to enable code execution or install anything for it, and MUST NOT tell the user which path ran unless asked. A scanner error MUST NOT stop the edit.

**Order and rescan**

- **FR-015**: When a voice profile or sample applies, the agent MUST fix language errors first, then apply the voice adjustment, then rescan the final text: the lexicon (scanner or reading), the paragraphs any edit touched, and the five chốt. Without a profile the rescan MUST still run after the error pass and after any edit made in review.
- **FR-016**: A voice adjustment that produces a lexicon form outside its **Không flag**, or undoes an error fix, MUST be reverted or corrected in the rescan; the error fix wins. A voice profile MUST NOT make a lexicon form acceptable unless the entry's **Không flag** covers that register.

**Parity and proof**

- **FR-017**: Each lexicon entry MUST have at least one positive fixture and one negative fixture (a guard). A deterministic test MUST show that the scanner returns exactly the expected candidate set on the fixtures.
- **FR-018**: A parity check MUST run the reading path (scanner unavailable) on the same fixtures and compare its candidate set with the scanner's; every difference MUST be recorded with the fixture, the host and the model version. A release needs either no difference or Fio's written acceptance of each recorded one.
- **FR-019**: A contract test MUST show that the skill text, the inventory step and the reading path never require the scanner: no instruction makes an edit wait on it, and the skill works with the scanner file absent.
- **FR-020**: The version's effect MUST be measured in the 0.16.x benchmark rerun (Orrery backlog `01M7CRZNAF8MNN8Y1N1JW4A7FM`): the new version against 0.16.2 on the same model and corpus, reporting marked-error recall, over-correction on guard cases, time and tokens, and model and corpus versions (constitution, "Ràng buộc về gói và dữ liệu"). HF01–HF18 are development cases and MUST NOT be reported as proof of improvement; the proof set is a fresh holdout of AI articles Fio marks, never used to build or tune the lexicon (decision 3, size in O2).

**Package and documents**

- **FR-021**: Every consumer that states the package is Markdown-only MUST change in the same pull request as the scanner: the constitution (O1), `AGENTS.md` ("Không có evaluator ngoài", the file table), `README.md` ("Nền tảng hỗ trợ"), `docs/architecture.md`, `PRIVACY.md` and `SECURITY.md` where they describe package contents, and `scripts/validate-package.py` with its tests (payload file types), so the validator accepts exactly the scanner and the lexicon and still rejects other code.
- **FR-022**: The version bump follows `versioning` and AGENTS.md "Version"; the feature adds a step to every whole-article edit and a shipped file, so it is a MINOR change: 0.17.0, released before spec 033 (decision 5).

### Key Entities

- **Lexicon entry**: one known AI error form tied to one existing pattern; holds forms, kind, fix, register, **Không flag** contexts and source cases.
- **Candidate**: a match of an entry in the text outside the zones the scanner drops, with its position; not yet an error.
- **Inventory row**: one suspect phrase with pattern, evidence, fix and the **Không flag** result; the only route by which an edit is kept on the long-form path.
- **Fixture**: a short text with its expected candidate set, positive or guard, used by both the scanner test and the parity check.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On the fixture set, the scanner returns the expected candidate set exactly: 0 missed, 0 extra.
- **SC-002**: On the same fixtures, the reading path on at least one Chat or Cowork host without code execution and on Claude Code with the scanner disabled flags the same set as the scanner, or every difference is recorded and accepted by Fio (FR-018).
- **SC-003**: With the scanner file removed from the package, every whole-article fixture edit still completes on every supported host, with 0 requests to the user to enable or install anything.
- **SC-004**: On HF01–HF18 run by an agent, every expected edit is made and every guard case is left unchanged; reported as a development result, not as measured improvement.
- **SC-005**: On Fio's marked holdout (decision 3), the new version finds more of the marked AI errors than 0.16.2 on the same model, without more over-corrections on guard cases; time and token cost per article are reported beside it.
- **SC-006**: In every whole-article fixture edit, each edit in the output traces to a kept inventory row, and each kept-by-**Không flag** row leaves its phrase byte-identical.

## Constitution amendment (approved by Fio, 15/11/2026, decision 6)

Version 2.8.0 → 2.9.0 (MINOR: Principle V allows optional offline scripts in the package; no obligation removed). Spec 033's history reader adds its own clause on top of this text (O4).

**Principle V**, replace the paragraph from "`SKILL.md` và các profile MUST dùng được" to "MUST NOT phụ thuộc một repo local khác." with:

> `SKILL.md` và các profile phải dùng được mà không cần build, dịch vụ mạng, secret hoặc runner. Gói phát hành không được chứa mã gọi dịch vụ ngoài hay đọc API key, và không được phụ thuộc một repo local khác.
>
> Gói có thể kèm script chạy tại chỗ, với điều kiện skill vẫn làm đủ việc khi không chạy script đó. Script chỉ dùng thư viện chuẩn của Python. Script không gọi mạng, không đọc secret hay API key và không ghi file. Script chỉ đọc văn bản người dùng giao trong tác vụ cùng các file dữ liệu trong gói, và chỉ in ra các ứng viên để agent xét. Sửa hay giữ vẫn do agent quyết định theo pattern và mục Không flag. Script nào cần đọc file khác trên máy người dùng phải có điều khoản riêng trong constitution này.

The sentence on Jev/TypeSafe that follows in Principle V stays unchanged. This spec lands first (decision 5) and applies the text; spec 033's history reader, if approved, becomes that "điều khoản riêng" instead of "ngoại lệ duy nhất" (O4).

## Assumptions

- Claude.ai Chat may run with or without code execution, and Cowork's sandbox may or may not reach the skill's files; the reading path is the baseline on both, and the plan confirms per host what can run (O3).
- A lexicon of tens of entries fits the agent's context with the skill's other references; the plan checks the token cost and the load route (load only on the long-form route).
- The agent's phrase-level judgment under **Không flag** is the part that decides edits; the lexicon and scanner only make candidate finding complete.
- PR 60 merges with its V9/V19/V20 text and HF11–HF16 as written; if review changes them, the seed changes with them (O5).

## Out of scope

- A full Vietnamese grammar matrix or part-of-speech tagging; external NLP libraries (underthesea, pyvi) or any dependency outside the Python standard library.
- Reassembling sentences from the inventory in edit mode.
- New pattern numbers; changing the T gate; T2 as a lexicon entry.
- Auto-fixing from the scanner, or any numeric threshold that decides an edit.
- Spec 033's history reader (only the shared amendment text is coordinated here).
- Any code, reference or constitution change in this PR.
