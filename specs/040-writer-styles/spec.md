# Feature Specification: Style cards for common Vietnamese writer types

**Feature Branch**: `spec/040-writer-styles`

**Created**: 2026-11-26

**Status**: Draft. Scope decisions settled by Fio on 26/11/2026 (see Clarifications). Plan written 2026-11-27 ([plan.md](plan.md)).

**Input**: Fio, 26/11/2026, via the coordinating session: ready-made writing styles for common Vietnamese writer types (brand and marketing content; founders and directors; PhD students, students and scientists; product builders, product owners and engineers), plus others the agent proposes (sales and customer service, HR and internal communication, teachers and trainers, journalists and editors, public-sector writing, finance and legal).

## Clarifications

### Session 2026-11-26

- Q: Which new cards does spec 040 add? → A: All four proposed: `customer-reply`, `internal-announcement`, `product-requirements`, `news-report` (Fio: "customer-reply, internal-announcement, product-requirements, news-report"). Teachers and trainers stay on the existing cards; legal, contract, public-sector official letters and regulations keep the existing T1–T6-only gate (both stated in the question; Fio did not object).
- Q: Each new card adds a row to the card table in `SKILL.md`, about 100 bytes on every route, while `route_budget.py` caps every route at its 0.16.2 bytes. How is the budget kept? → A: Compact the card table: rows carry the card id, the path is written once as a pattern, and the validator follows (Fio: "Rút gọn bảng card").
- Q: Where does the labelled Vietnamese evidence for each new card come from (principles I and IV)? → A: Maintainer-built cases plus public sources recorded in `docs/sources.md`; no samples from Fio (Fio: "Chỉ ca dựng + nguồn công khai").
- Q: How is spec 040 measured before it is accepted? → A: Static tests plus an early model run on Sonnet and Opus, on the old gate pool and the new cases, with enough runs to beat noise, compared with 0.16.2 (Fio: "Test + chạy model sớm").
- Q: What is the pass bar of the model run? → A: As in spec 038, each quality count (fixes, guard breaks) may differ by at most 2 per model; mean cost per run rises by at most 5%; each new routing case picks the right card in at least 9 of 10 runs per model (Fio: "Như 038 + chi phí ≤5%"). The routing part was amended on 27/11/2026, below.

### Session 2026-11-27

- Q: An id-only table still grows `SKILL.md` by 133 bytes (research R1). May the card table become a two-item list, one item per family, with the path pattern written once? → A: Yes (Fio: "Duyệt, làm tiếp").
- Q: In the early model run every routing miss was a run that read no card; no run read a wrong card, and 0.16.3 also read no card on 15 of 16 short probe runs. How do no-card runs count toward SC-004? → A: SC-004 counts the runs that read a card: each must read the expected card, and no run may read a wrong one. The card-read rate is reported beside it, per model and arm (Fio: "Đếm card đúng khi đọc").
- Q: Counted per kind as in spec 038, Sonnet's other fixes fell from 5 to 2 (−3), past the bar of 2; summed, its fixes went from 7 to 5 (−2). Rerun the gate once, or accept the summed count? → A: Accept, as a recorded exception decided after the results were seen: for this run SC-003 counts fixes as one sum (lexicon-kind plus other) per model (Fio: "Chấp nhận, gộp số").

## Background: what the seven cards already cover

Style cards live under `profiles/*/styles/`, are chosen from the purpose table in `SKILL.md` ("Chọn card khi làm bài") and, only when the purpose is unclear, by `references/style-resolution.md`. Each card is a contract of eight fields (Dùng khi, Thanh ngữ vực, Xưng hô, Nhịp, Thuật ngữ, Cách kết, Không tự thêm, Ca kiểm thử), pinned by `scripts/validate-package.py` and the contract tests, with positive and leak cases in `calibration/test-cases.md` (MS01–MS14).

A card describes a writing function and its reader, not a person or a company. The resolver says so: "Không tạo card cá nhân/công ty". A writer type is therefore mapped to the functions that writer actually produces.

| Writer type | Covered by | Gap |
|---|---|---|
| Brand and marketing content | `persuasive-marketing` (offer pages, CTA); `public-expertise` (brand thought pieces) | None for the function. A brand's own voice is user data: a `kind: brand` voice profile (`references/brand-voice.md`). |
| Founders and directors | `public-expertise` (LinkedIn, opinion); `work-coordination` (messages to the team); `business-operations` (reports) | A letter or announcement to the whole company, see `internal-announcement`. A founder's personal voice is a voice profile. |
| PhD students, students, scientists | `academic-analysis` (theses, proposals, papers, đề án); `public-expertise` (popular science written for outsiders) | None. |
| Product builders, product owners, engineers | `technical-guide` (README, API prose, setup); `work-coordination` (chat); changelog, commit, error and UI text stay T1–T6 only | Requirements documents (PRD, spec, feature proposal, ADR, acceptance criteria), see `product-requirements`. |
| Sales and customer service | `persuasive-marketing` covers one-to-many offers only; `work-coordination` covers colleagues, not customers | One-to-one replies to a customer, see `customer-reply`. |
| HR and internal communication | `business-operations` covers SOP and minutes; JDs and recruiting posts fit `persuasive-marketing` | Announcements and policy explanations to staff, see `internal-announcement`. |
| Teachers and trainers | `academic-analysis` (giáo trình, lesson content); `technical-guide` (step-by-step exercises, lab guides) | None for now. |
| Journalists and editors | No card. `references/style-sources.md` lists press sources for sample work only | News, reportage, press releases, see `news-report`. |
| Public sector | Công văn and quy chế are in the core gate: T1–T6 only, no card | Out of scope; changing the gate is a separate decision. |
| Finance and legal | Contracts and pháp quy are in the same gate; financial reports fit `business-operations`, analysis fits `academic-analysis` | Out of scope. |

**Ready-made voice profiles.** A writer type with a recognisable personal voice (a founder who writes short and direct, a brand that says *mình*) is a preference, not a rule. Principle IV and the voice-profile constraint put preferences in that user's own profile, saved only on their request. This spec ships no preset profiles. Users build theirs through the existing voice-profile route, which spec 039 is changing; nothing here touches that route.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Customer replies get a fitting card (Priority: P1)

A sales or customer-service writer asks Vietnamizer to edit or write a reply to one customer: an answer to a complaint, a follow-up email after a quote, a message about a late delivery. The result keeps the address forms and particles the relationship already uses (*anh/chị–em*, *dạ*, *ạ*, or the company's *chúng tôi*), apologises or explains without promising more than the source says, and ends with the real next step.

**Why this priority**: The two existing personal-blog cards each get this wrong in a known way: `persuasive-marketing` pushes offer language into a reply, `work-coordination` treats the customer as a colleague. Address forms decide the relationship in Vietnamese, so a wrong card changes meaning, not only style.

**Independent Test**: The new positive and leak cases for `customer-reply` route to it and keep the address forms; the existing MS cases still route as before.

**Acceptance Scenarios**:

1. **Given** a reply to a complaint that uses *anh–em* and *dạ*, **When** the user asks for a whole-text edit, **Then** the agent picks `customer-reply`, keeps *anh–em* and *dạ*, and adds no discount, compensation, deadline or promise absent from the source.
2. **Given** the same facts written as a public offer page, **When** the user asks for an edit, **Then** the agent picks `persuasive-marketing`, not `customer-reply`, and adds no *anh/chị* or *dạ*.
3. **Given** a reply whose address form is unknown and a change from *bạn* to *anh/chị* would change the relationship, **When** the agent edits it, **Then** it asks one short question about address, as MSP05 already requires.

---

### User Story 2 - Internal announcements and requirements documents get fitting cards (Priority: P2)

An HR writer or a director edits an announcement to all staff (a new leave policy, an office move, a leadership letter after a hard quarter). A product owner or engineer edits a PRD, a spec, an ADR or a list of acceptance criteria. Each gets a card that keeps who decided, who is affected, what changes and when, and in requirements documents keeps the obligation words (*phải*, *nên*, *có thể*) and the conditions exactly.

**Why this priority**: These are frequent documents in the retail, fashion and SaaS teams Vietnamizer serves, and today they fall between `business-operations` (no author voice, no reasons) and `public-expertise` (outside readers).

**Independent Test**: Positive and leak cases for `internal-announcement` and `product-requirements` route correctly; MS02, MS06, MS08, MS09 and MS11 still route to their existing cards.

**Acceptance Scenarios**:

1. **Given** a leadership letter to staff that gives a reason and a date, **When** the user asks for an edit, **Then** the agent picks `internal-announcement`, keeps the signer's voice, the reason and the date, and adds no slogan, thanks, approval or benefit absent from the source.
2. **Given** a PRD line "Hệ thống phải khoá tài khoản sau 5 lần đăng nhập sai; quản trị viên có thể mở khoá", **When** the user asks for an edit, **Then** the agent picks `product-requirements` and keeps *phải*, *có thể*, the number and the actor exactly.
3. **Given** a README section, **When** the user asks for an edit, **Then** the agent still picks `technical-guide`.

---

### User Story 3 - News and press releases get a fitting card (Priority: P3)

A journalist, an editor or a company's PR writer edits a news item, a report from an event or a press release. The result keeps who said what, titles, places and times, the attribution words (*theo*, *cho biết*, *khẳng định*) at their original strength, and adds no opinion.

**Why this priority**: Attribution and the strength of a reporting verb carry meaning (*cho biết* is not *khẳng định*), and no current card names them. Fewer Vietnamizer users write news than the stories above.

**Independent Test**: Positive and leak cases for `news-report` route correctly; MS13 and MS14 still route as before.

**Acceptance Scenarios**:

1. **Given** a news item with "ông A cho biết", **When** the user asks for an edit, **Then** the agent picks `news-report` and does not change *cho biết* to a stronger or weaker reporting verb.
2. **Given** a press release with a quote from a director and a launch date, **When** the user asks for an edit, **Then** the quote stays byte-for-byte, the date and title stay, and no superlative or call to buy is added.

---

### User Story 4 - The skill reads no more per edit (Priority: P1)

Every user, whatever the card, pays no more per edit than on 0.16.2 beyond the agreed tolerance, and short edits read exactly what they read before.

**Why this priority**: Spec 038 showed that extra text and extra reads raise cost and the edit rate with no quality gain. Eleven cards must cost what seven cost.

**Independent Test**: `python3 scripts/route_budget.py` passes with every route at or under its current `max_bytes`; the model run meets the bar in FR-010.

**Acceptance Scenarios**:

1. **Given** the compacted card list, **When** `route_budget.py` runs, **Then** every route is at or under its current `max_bytes`, and `SKILL.md` is no larger than before.
2. **Given** a whole-article edit, **When** the agent picks a card, **Then** it reads one card file of the same size class as today (about 1.2–1.5 KB) and does not need `references/style-resolution.md` to find the card's file.

### Edge Cases

- A text mixes functions: a customer reply that quotes a policy, an announcement that contains a requirements list, a press release with an offer and CTA. The resolver's existing rule applies: one card per part, split only when purpose, reader or speaker changes.
- A customer reply that is a legal notice or a contract change is in the core gate (T1–T6 only), not `customer-reply`.
- A public-sector công văn sent to citizens stays in the gate even if it reads like an announcement; a company's internal announcement does not enter the gate because it mentions a policy.
- A PRD written as a chat thread between engineers is `work-coordination`; a PRD section that is a reference table stays a protected structure.
- A founder's LinkedIn post about the company stays `public-expertise`; the same text sent to staff only is `internal-announcement`.
- A press release used as a product page with prices and a CTA is `persuasive-marketing`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The package MUST add four cards with the eight existing fields: `customer-reply` under `personal-blog`; `internal-announcement`, `product-requirements` and `news-report` under `enterprise-technical`. The family of each is the one stated in the settled question; the plan may move a card only with Fio's yes.
- **FR-002**: Each new card MUST stay within the size class of the existing cards (no card above 1,500 bytes) and MUST own no pattern; it supports rhythm, address, terms and endings only, as the resolver already says.
- **FR-003**: The card list in `SKILL.md` MUST be one item per family, pairing each purpose with its card id, and give the path once as a pattern (shape in [contracts/card-list.md](contracts/card-list.md)), so that `SKILL.md` is no larger than its 0.16.2 size (14,444 bytes, or the size on main after spec 039 merges, whichever is smaller) and the agent can open the card without reading the resolver. Each card's family MUST be visible from the item it sits in.
- **FR-004**: `scripts/validate-package.py` MUST accept the compacted table and keep every current check: each registered card exists, has its canonical heading and the eight fields, appears in the resolver registry and in `docs/style-and-voice.md`, and the table in `SKILL.md` reaches it.
- **FR-005**: `references/style-resolution.md` MUST list the four cards in its registry and MAY gain at most one line of disambiguation per new card; its size MUST NOT grow by more than 600 bytes, since it is read only when the purpose is unclear.
- **FR-006**: Each new card's "Không tự thêm" MUST name the additions that change meaning for that function: for `customer-reply`, compensation, discounts, deadlines, admissions of fault and promises; for `internal-announcement`, approvals, benefits, dates, reasons and thanks; for `product-requirements`, obligation strength (*phải/nên/có thể*), actors, numbers, conditions and priorities; for `news-report`, reporting-verb strength, attributions, titles, opinions and superlatives.
- **FR-007**: Each new card MUST cite at least one positive case and two leak cases in `calibration/test-cases.md`, each labelled as maintainer-built, with source text, expected card, what must be kept and what must not happen. Leak cases MUST pair a new card with its nearest existing card, as MS01–MS14 do.
- **FR-008**: Any claim in a card about Vietnamese convention (address forms in customer service, reporting verbs in news, obligation words in requirements) MUST cite a public source recorded in `docs/sources.md` with its reliability, or be labelled as inference, per principle I.
- **FR-009**: `docs/style-and-voice.md` MUST list the four cards; `README.md` and `docs/architecture.md` MUST be updated where they count or name the cards.
- **FR-010**: Before acceptance, a model run MUST compare the candidate with 0.16.2 (or main after spec 039, the same base for both arms) in the same batch, on Sonnet 5.5 and Opus 5.5: D11–D34 with two runs per model per article, plus the new routing cases with ten runs per model per case. It passes when each quality count (fixes, guard breaks) is no worse than the base by more than 2 per model, as spec 038 FR-004, mean cost per run rises by at most 5% per model, and, per SC-004 as amended on 27/11/2026, every run that reads a card reads the expected one. The run happens early, on the first complete card set, before docs and release work.
- **FR-011**: Results MUST go to `docs/benchmarks.md` as counts with model ids, host, date, pool manifest hash and the package commit of each arm. Heavy runs go through the heavy-job lock, one at a time.
- **FR-012**: The work MUST NOT edit `references/voice-profile*.md` or any `.vietnamizer` store, and MUST NOT change the core gate for legal, contract, official-letter, ceremony, changelog or poetry text.

### Key Entities

- **Style card**: a Markdown file under `profiles/<family>/styles/<id>.md` with eight fields; describes a writing function and its reader, never a person or company.
- **Card list entry**: one purpose and one card id in its family's item in `SKILL.md`; the only place the agent looks when the purpose is clear.
- **Routing case**: a calibration case that names the expected card, what must be kept and what must not happen.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Eleven cards pass the validator and contract tests; `SKILL.md` is no larger than before (FR-003).
- **SC-002**: `route_budget.py` passes with no `max_bytes` raised.
- **SC-003**: On D11–D34, per model, fixes and guard breaks are no worse than the base by more than 2 (as spec 038 FR-004: fewer fixes or more guard breaks), and mean cost per run rises by at most 5%. Fixes are one sum, lexicon-kind plus other: an exception Fio accepted on 27/11/2026 after the run (Clarifications).
- **SC-004**: In every run of WS01–WS12 and MS01–MS14 that reads a card, the card read is the expected one; no run reads a wrong card. The share of runs that read a card is reported per model and arm, and no pass bar applies to it (Clarifications 2026-11-27).
- **SC-005**: No new card contains a claim about Vietnamese convention without a source in `docs/sources.md` or an inference label.

## Assumptions

- Spec 039 (`spec/039-cloud-voice-profiles`) also edits `SKILL.md`, `benchmarks/route-budget.json`, `calibration/test-cases.md`, `docs/style-and-voice.md`, `scripts/validate-package.py` and `tests/test_skill_contract.py`. Implementation of 040 starts from main after 039 merges, so the two never edit the same files at once. Until then, only this spec and its plan are written.
- Compacting the table is feasible inside the budget only as a list: measured on main after spec 039, the current table is 764 bytes, eleven id-only rows plus one path line are 897 bytes, and a two-item family list is 749 bytes ([research.md](research.md) R1; the earlier 903 and 850 byte figures were wrong).
- Teachers and trainers need no card now; a future card needs its own evidence that `academic-analysis` and `technical-guide` mislead on teaching material.
- The D11–D34 pool, the scorer and the read-logging runner from spec 038 (`.finolabs/harness-038/`, outside Git) are reused. The new routing cases are development cases, not holdout; results are reported as such.
- No new V, T, B or K pattern is added, so `docs/patterns.md` and the README pattern count do not change.
- Push, pull request, merge and release each need Fio's explicit go.
