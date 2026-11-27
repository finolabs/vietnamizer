---
description: "Task list for spec 040, style cards for common Vietnamese writer types"
---

# Tasks: Style cards for common Vietnamese writer types

**Input**: `specs/040-writer-styles/` (spec.md, plan.md, research.md, data-model.md, contracts/card-list.md, quickstart.md)

**Tests**: The spec and constitution gate 1 require tests. Each behavior starts from a contract test that fails on main.

**Format**: `[ID] [P?] [Story] Description`. Tasks marked [P] touch different files and need nothing unfinished.

Run tests at most two modules per command, and check `uptime` first.

## Phase 1: Setup

- [x] T001 Build the base zip from main `de8a2ba` (v0.16.3) with `python3 scripts/package-plugin.py` into `.finolabs/harness-040/v0163.zip`. Record its SHA-256 in `.finolabs/harness-040/README.md`.
- [x] T002 Copy `.finolabs/harness-038/run_round.py` and `rb_run.py` into `.finolabs/harness-040/`. Add a routing-case mode that reads a cases JSON (id, prompt, expected card) and records the card each run picks. A run picks a card when the only `profiles/*/styles/*.md` it reads is that card (research R4).

## Phase 2: Foundational (blocks every story)

- [x] T003 [US4] Add red tests to `tests/test_skill_contract.py`:
  - the card list block exists, per contracts/card-list.md rules 1–4 and 6;
  - `SKILL.md` holds no full `profiles/*/styles/*.md` path;
  - all 11 ids sit under their family.
  Run them and confirm they fail on main.
- [x] T004 [US4] In `scripts/validate-package.py`:
  - replace the `STYLE_CARDS[:4]`/`[4:]` slicing with an ordered `STYLE_FAMILIES`, family → ids, in the order data-model.md "Card list block" gives;
  - derive `STYLE_CARDS` and `STYLE_PROFILE_CARDS` from it;
  - replace the full-path check (``f"`{card_path}`" not in skill``) with the list parse from contracts/card-list.md;
  - fail on any card file under `profiles/*/styles/` that is missing from `STYLE_FAMILIES`.
- [x] T005 [US4] In `SKILL.md`, replace the table under "Chọn card khi làm bài" with the card list block from contracts/card-list.md. Keep the following paragraph byte-for-byte.
  - Confirm `wc -c SKILL.md` ≤ 14,428 and `python3 scripts/route_budget.py` passes with `benchmarks/route-budget.json` unchanged.
  - Until T007–T010 exist, the four new ids make the validator fail. T005 is therefore committed together with them, or the four ids are added in T011.

**Checkpoint:** the validator and T003 pass for the seven existing cards in list form.

## Phase 3: User Story 1, customer replies (P1) — MVP

**Goal:** a reply to one customer routes to `customer-reply`, keeps address forms and particles, and adds no compensation, discount, deadline, admission of fault or promise.

**Independent test:**
- WS01–WS03 are present and well-formed;
- the card passes the contract tests;
- in the model run, WS01 picks `customer-reply` in ≥9 of 10 runs per model.

- [x] T006 [P] [US1] Add red tests to `tests/test_skill_contract.py` for each new card:
  - the canonical heading and the eight fields;
  - at most 1,500 bytes;
  - "Không tự thêm" names the FR-006 items;
  - "Ca kiểm thử" cites WS ids that exist in `calibration/test-cases.md`.
  Parameterize the tests over the four ids.
- [x] T007 [US1] Write `profiles/personal-blog/styles/customer-reply.md` with the eight fields, per data-model.md.
  - Address: keep *anh/chị–em*, *dạ*, *ạ*, *chúng tôi* or *quý khách* as the source has them; when the address form is unknown and a change would shift the relationship, ask one question (MSP05).
  - Không tự thêm: compensation, discounts, deadlines, admissions of fault, promises.
  - Ca kiểm thử: WS01; WS02, WS03.
  - Cite the B14 sources or label claims *suy luận*.
- [x] T008 [US1] Add section "WS01–WS12 · card cho kiểu người viết (spec 040)" to `calibration/test-cases.md`, with the columns from data-model.md. Add WS01–WS03 there, labelled "maintainer dựng".

## Phase 4: User Story 2, internal announcements and requirements (P2)

**Goal:**
- staff announcements route to `internal-announcement`, which keeps the signer, the reason and the date;
- PRD, spec and ADR text routes to `product-requirements`, which keeps *phải/nên/có thể*, actors, numbers and conditions;
- README text still routes to `technical-guide`.

**Independent test:** WS04–WS09 route correctly; MS02, MS06, MS08, MS09 and MS11 keep their cards.

- [x] T009 [P] [US2] Write `profiles/enterprise-technical/styles/internal-announcement.md`. Không tự thêm: approvals, benefits, dates, reasons, thanks. Ca kiểm thử: WS04; WS05, WS06.
- [x] T010 [P] [US2] Write `profiles/enterprise-technical/styles/product-requirements.md`. Không tự thêm: obligation strength (*phải/nên/có thể*), actors, numbers, conditions, priorities. Ca kiểm thử: WS07; WS08, WS09. Cite TCVN 1-2:2008 for the obligation words, by analogy, or label the claim *suy luận* (R5).
- [x] T011 [US2] Add WS04–WS09 to `calibration/test-cases.md`. WS07 uses the spec's PRD line: "Hệ thống phải khoá tài khoản sau 5 lần đăng nhập sai; quản trị viên có thể mở khoá".

## Phase 5: User Story 3, news and press releases (P3)

**Goal:** news and press releases route to `news-report`, which keeps reporting verbs at their strength, attributions, quotes, titles and dates, and adds no opinion or superlative.

**Independent test:** WS10–WS12 route correctly; MS13 and MS14 keep their cards.

- [x] T012 [P] [US3] Write `profiles/enterprise-technical/styles/news-report.md`. Không tự thêm: reporting-verb strength, attributions, titles, opinions, superlatives. Ca kiểm thử: WS10; WS11, WS12. Cite a source for reporting-verb strength or label the claim *suy luận* (R5).
- [x] T013 [US3] Add WS10–WS12 to `calibration/test-cases.md`.

## Phase 6: Cross-cutting and User Story 4 (P1, measured)

- [x] T014 Add the four rows to the registry table in `references/style-resolution.md`, with at most one disambiguation line per new card in "Chia phần và chọn card". Confirm the file grows ≤600 bytes.
- [x] T015 [P] Add the four card paths to the expected inventory in `tests/test_package_security.py:521-528`.
- [x] T016 Record every source used in T007, T010 and T012 in `docs/sources.md`, with its reliability. Done as no-op: the cards make no convention claim beyond the meaning invariants of chốt 3; the one ranking claim (*cho biết* vs *khẳng định*) is labelled *suy luận* in `news-report`, so no source is added.
- [x] T017 Run the static checks:
  - `python3 -B scripts/validate-package.py`;
  - `python3 -B -m unittest tests.test_skill_contract tests.test_package_security`;
  - `python3 -B -m unittest tests.test_route_budget`;
  - `python3 scripts/route_budget.py`.
  Every check must pass.
- [x] T018 Commit Phase 2–6 as atomic commits, per `commit-messages`: tests, then validator and list, then each card with its cases.
- [x] T019 [US4] (Run as 2 reps on both arms, then the full run regardless, per Fio 27/11/2026.) Build the candidate zip from the branch head into `.finolabs/harness-040/cand.zip`. Run the probe: WS01, WS04, WS07 and WS10 on `v0163.zip`, 5 reps per model, through the heavy-job lock. Proceed only if at least 9 of 10 runs per model read some card. Otherwise stop and ask Fio (plan, "Open decisions").
- [x] T020 [US4] Run the full model run per research R6, in one batch, through the heavy-job lock:
  - D11–D34 on both arms, 2 reps × 2 models;
  - MS01–MS14 on both arms, 2 reps;
  - WS01–WS12 on the candidate, 10 reps.
  Log cost as it runs, and stop on a quota hit.
- [x] T021 [US4] Score the edits with `python3 benchmarks/holdout_036.py score <index>` and count card picks. Check SC-003 and SC-004 per model. If any check fails, stop before docs and report to Fio.
- [x] T022 Write the results to `docs/benchmarks.md` with the fields in data-model.md "Benchmark record".

## Phase 7: Docs and review

- [x] T023 [P] (`docs/style-and-voice.md`, `docs/architecture.md` and `AGENTS.md` done early in c34fa45, since the validator requires the docs list) Update `docs/style-and-voice.md` so it lists all 11 cards. Update `README.md` and `docs/architecture.md` where they count or name the cards (FR-009).
- [x] T024 [P] Update `references/help.md` if its feature map names the cards. Add an `Unreleased` entry to `docs/changelog.md`.
- [ ] T025 Run T017 again, then run `review-gate`: Codex code review and security review on the PR, posted through `post_review.py`. Push and open the PR only on Fio's go.

## Dependencies

- Setup T001–T002 is needed only for T019–T022.
- Foundational T003–T005 blocks every story.
- US1, US2 and US3 are independent of each other once T005 is done. T008, T011 and T013 all edit `calibration/test-cases.md`, so they run in order.
- US4's measured part (T019–T022) needs every card. Docs (T023–T024) wait for T021 to pass.

## Parallel opportunities

- Once T008 creates the section, the card files T007, T009, T010 and T012 can be written in parallel.
- T015 can run alongside the card files.
- T023 and T024 can run in parallel.

## Implementation strategy

The MVP is Phase 2 plus US1. It is not shippable alone, because FR-010 measures all four cards together. Write all four cards, then measure once. A fail at T021 sends work back to the card text, not to the docs.
