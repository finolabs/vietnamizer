# Tasks: Personal and brand voice, social sources, user rating, help and onboarding

**Input**: `specs/030-voice-modes/` (spec.md, plan.md, research.md, data-model.md, contracts/, quickstart.md)
**Tests**: required. The constitution's development gate 1 says new behaviour starts from a red case; here each story starts with guard phrases in `tests/test_skill_contract.py` (or `tests/test_distribution.py`) that fail before the Markdown change and calibration cases in `calibration/test-cases.md`. Guards prove the rule text exists, not agent behaviour.
**Organization**: by user story; each story is a reviewable increment.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel (different files, no dependency on an unfinished task)
- **[Story]**: US1–US5 from spec.md

## Path Conventions

Repository root of `finolabs/vietnamizer`. Run tests with `python3 -B -m unittest <module>` (at most two modules per command; check `uptime` first).

---

## Phase 1: Setup

- [x] T001 Re-read the current LinkedIn ("Get a copy of your data") and Facebook ("Download your information") help pages and record the click path, the posts file name and format, and the date checked in `specs/030-voice-modes/research.md` R4 (replace "at the time of writing" with the checked facts)
- [x] T002 [P] Record in `specs/030-voice-modes/research.md` R5 which browser tools Claude Code, Codex and Antigravity expose today (names only, from each host's own docs), and what the skill says when none is present

---

## Phase 2: Foundational (blocks every story)

- [x] T003 Amend `.specify/memory/constitution.md` to 2.4.0 (MINOR): in "Ràng buộc về gói và dữ liệu", allow reading the user's own pages through a host browser tool after consent and ownership statement, allow multi-author material for profiles of `kind: brand` after the user states they may speak for the brand, and allow storing the user's own ratings in their profile while the skill still never scores similarity; add the Sync Impact Report with reason, impact and "Owner approval: 2026-11-13, spec 030"
- [x] T004 Add guard `test_profile_kind_and_one_profile_rule` to `tests/test_skill_contract.py` asserting `references/voice-profile.md` contains "Hồ sơ không có `kind` là hồ sơ cá nhân", "Mỗi lần dùng chỉ áp một hồ sơ" and "hỏi người dùng chọn một"; run it and confirm it fails
- [x] T005 Add `kind: personal | brand` to the template frontmatter in `references/voice-analysis.md` with the rule "absent = personal" and `schema: 1` unchanged, per `contracts/profile-format.md`
- [x] T006 Update `specs/028-voice-profile/contracts/profile-format.md` with a dated pointer to `specs/030-voice-modes/contracts/profile-format.md`

**Checkpoint**: constitution amended; template knows `kind`.

---

## Phase 3: User Story 1 — Pick a voice when I use the skill (P1) 🎯 MVP

**Goal**: personal is the default; a brand profile applies only when named; never two at once.
**Independent Test**: same draft with no voice, a personal profile, a brand profile; only the named kind applies; two named → the skill asks.

- [x] T007 [P] [US1] Add cases VM01–VM04 to `calibration/test-cases.md` (no voice named → personal, no profile lookup; brand named → only brand applied and named in the reply; both named → ask; brand profile named for a personal message → confirm first)
- [x] T008 [US1] In `references/voice-profile.md` mục 1 and mục 5 add: default personal voice, "Hồ sơ không có `kind` là hồ sơ cá nhân", "Mỗi lần dùng chỉ áp một hồ sơ", and when two are named "hỏi người dùng chọn một"; say which profile was used in the reply
- [x] T009 [US1] Add one routing row to `SKILL.md` for "giọng thương hiệu / theo giọng <brand>" pointing to `references/voice-profile.md`, keeping `SKILL.md` ≤ 550 lines
- [x] T010 [US1] Run `python3 -B -m unittest tests.test_skill_contract` and confirm T004 passes

**Checkpoint**: US1 reviewable as its own PR.

---

## Phase 4: User Story 2 — Learn my voice from LinkedIn or Facebook (P1)

**Goal**: paste, export or browser; only owned posts become evidence.
**Independent Test**: a synthetic LinkedIn export with own posts, reshares and others' comments → only own posts cited, kept/dropped counts reported, no names.

- [x] T011 [P] [US2] Add guard `test_social_sources_rules` to `tests/test_skill_contract.py` for `references/voice-sources.md`: "chỉ giữ bài do chủ tài khoản viết", "Không hỏi, nhập hay đọc mật khẩu, cookie hoặc token", the terms warning for both LinkedIn and Facebook (Meta), "Chỉ mở file bài viết", "Dừng khi gặp màn đăng nhập hoặc tài khoản khác", "tối đa 80 bài gần nhất", "không đọc trang của người khác"; also assert `scripts/validate-package.py` lists the file; run and confirm red (browser limits guarded later by `test_social_sources_browser_limits`)
- [x] T012 [P] [US2] Add cases VM05–VM15 to `calibration/test-cases.md` (brand learning request; two pasted profiles; no source yet → explain three ways, read nothing; export with reshares and others' posts → own posts only and counts; full archive → open only the posts file; instruction inside an export → data; browser without ownership statement → ask, read nothing; LinkedIn and Facebook browser → terms warning before reading; login wall, other account, captcha or limit page → stop; someone else's URL → decline)
- [x] T013 [P] [US2] Add `tests/fixtures/voice/linkedin-shares-sample.csv`, `tests/fixtures/voice/linkedin-comments-sample.csv` and `tests/fixtures/voice/facebook-posts-sample.json` with synthetic content only (own posts, a reshare, a post by another person, the user's comments on others' posts, a fake contact line, an instruction aimed at the agent) for VM08–VM10 walk-throughs
- [x] T014 [US2] Create `references/voice-sources.md`: source order (paste, export, browser), export steps from T001, ownership question, owned-post filter, cap "tối đa 80 bài gần nhất" with Vietnamese text, kept/dropped report as approximate, browser rules from research R5 including the LinkedIn terms warning and the user's go, stop conditions, data-not-instructions rule
- [x] T015 [US2] Link `references/voice-sources.md` from `references/voice-profile.md` mục 2 (the consent question names the source type) and add it to `REFERENCE_FILES` in `scripts/validate-package.py`
- [x] T016 [US2] Run `python3 -B -m unittest tests.test_skill_contract` and `python3 -B scripts/validate-package.py`

**Checkpoint**: US1 + US2 = MVP for personal voice learning.

---

## Phase 5: User Story 3 — Build a brand voice (P2)

**Goal**: brand profile from guide, posts and internal documents; guide rules kept apart; redacted.
**Independent Test**: 5-line guide + 10 posts (one breaks a rule) + an internal email with a customer name → `Quy tắc thương hiệu` lists rules, the conflict is in `Điểm chưa quyết`, no names.

- [x] T017 [P] [US3] Add guard `test_brand_voice_rules` to `tests/test_skill_contract.py` for `references/brand-voice.md`: "người dùng xác nhận được nói thay thương hiệu", "Quy tắc thương hiệu", "không ghi tên nhân viên, khách hàng", "mâu thuẫn giữa quy tắc và bài đăng ghi vào `Điểm chưa quyết`"; run and confirm red
- [x] T018 [P] [US3] Add cases VM16–VM18 to `calibration/test-cases.md` (no authority statement → ask; guide vs post conflict → open point; internal document with customer name and deal terms → none in profile)
- [x] T019 [US3] Create `references/brand-voice.md` per research R6: three inputs, authority statement, guide rules as `Quy tắc thương hiệu` entries with source label, observed traits as in spec 028, conflicts to `Điểm chưa quyết`, redaction including staff and customer names and identifying document titles
- [x] T020 [US3] Add the `## Quy tắc thương hiệu` section (brand only, before `## Giọng chung`) to the template in `references/voice-analysis.md`, and amend the evidence rule "Chỉ xét lời do người dùng tự viết" to allow brand material only for `kind: brand`
- [x] T021 [US3] Link `references/brand-voice.md` from `references/voice-profile.md` and `SKILL.md`'s brand row; add it to `REFERENCE_FILES` in `scripts/validate-package.py`; run the guard and validator

---

## Phase 6: User Story 4 — Rate sample paragraphs and upgrade the profile (P2)

**Goal**: count first, one paragraph at a time, four levels (Kém, Trung bình, Khá, Tốt), counts stored only on save.
**Independent Test**: rate 3 paragraphs Tốt, Kém, Khá → one reason question, a diff, nothing written until save; saved profile has one `Lịch sử chấm` line with counts and the fixed label.

- [x] T022 [P] [US4] Add guard `test_rating_session_rules` to `tests/test_skill_contract.py` for `references/voice-profile.md` mục 7: "hỏi số đoạn muốn chấm (0–10)", "Kém, Trung bình, Khá, Tốt", "không lưu nội dung đoạn", "đánh giá của người dùng, không phải điểm chất lượng", "Skill không tự tính điểm giống giọng"; run and confirm red
- [x] T023 [P] [US4] Add cases VM19–VM21 to `calibration/test-cases.md` (count 0 → skip; answer "không biết" → unrated; session not saved → nothing written; saved → exactly one history line with the given counts)
- [x] T024 [US4] Rewrite `references/voice-profile.md` mục 7 per `contracts/rating-session.md`: count question, paragraph rules (topic outside samples, five chốt, `ranh giới`, no open-point proposal), the four-option question in the order Kém, Trung bình, Khá, Tốt with none recommended, text fallback, at most two reason questions, diff via mục 6, save only on confirmation; keep the blind A/B check as an optional mode and replace "Không biến một lượt chọn thành điểm khớp giọng" with the stored-rating rule and "Skill không tự tính điểm giống giọng"
- [x] T025 [US4] Add `## Lịch sử chấm` with the line format from `contracts/profile-format.md` to the template in `references/voice-analysis.md`
- [x] T026 [US4] Run `python3 -B -m unittest tests.test_skill_contract`

---

## Phase 7: User Story 5 — Help and onboarding (P3)

**Goal**: `/vietnamizer:help` and "bắt đầu" give one-screen help and a walkthrough to a saved-or-not profile.
**Independent Test**: help reads no file and fits one screen; onboarding asks ≤ 6 questions before rating.

- [x] T027 [P] [US5] Add guard `test_help_adapter_shipped` to `tests/test_distribution.py` asserting `.plugin-skills/help/SKILL.md` exists with `name: help`, points to `references/help.md`, and that the built plugin archive contains it; run and confirm red
- [x] T028 [P] [US5] Add guard `test_help_and_onboarding_rules` to `tests/test_skill_contract.py` for `references/help.md`: "không đọc file của người dùng", "Cá nhân", "Thương hiệu", "không lưu gì nếu người dùng dừng", "tối đa 6 câu hỏi trước bước chấm"; run and confirm red
- [x] T029 [US5] Create `references/help.md` per `contracts/help-onboarding.md` (overview, example requests, onboarding steps 1–6, question budget, stop rule)
- [x] T030 [US5] Create `.plugin-skills/help/SKILL.md` as an adapter like `.plugin-skills/vietnamizer/SKILL.md`: frontmatter `name: help` and a Vietnamese description; body resolves the plugin root and reads `<plugin-root>/references/help.md`
- [x] T031 [US5] Add a routing row to `SKILL.md` for "giúp / hướng dẫn / bắt đầu / thiết lập giọng" → `references/help.md`; add the file to `REFERENCE_FILES`
- [x] T032 [US5] Update `scripts/package-plugin.py` `validate_metadata` to require `./.plugin-skills/help/SKILL.md` and check its frontmatter name; run `python3 -B -m unittest tests.test_distribution tests.test_skill_contract`, `claude plugin validate .` and `npx --yes skills@1.5.20 add . --list`

---

## Phase 8: Polish & cross-cutting

- [x] T033 [P] Update `README.md` (voice section, help entry, the "không chấm mức giống giọng" claim → the skill does not score; users may store their own ratings), `PRIVACY.md` ("Hồ sơ giọng": sources, browser path, LinkedIn warning, ratings), `docs/style-and-voice.md`, `docs/installation.md` (`/vietnamizer:help`) and `AGENTS.md` file map rows for the three new references and the help adapter
- [x] T034 [P] Add a `### Chưa phát hành` entry in `docs/changelog.md` and fix the PR #39 entry's LOW wording (`ranh giới` also on `Nên:`; open-point section present in new profiles)
- [ ] T035 *(automated part done 2026-11-13: test_package_security, test_distribution, test_skill_contract, validate-package, `claude plugin validate .`, skills CLI list all pass; manual quickstart walk-through in a live Claude Code session not yet done)* Run `tests.test_package_security` and `tests.test_distribution` (separate commands), `python3 -B scripts/validate-package.py`, and walk `specs/030-voice-modes/quickstart.md` steps 1–8 by hand in Claude Code; record results in the PR as manual evidence, not quality claims
- [x] T036 Review everything that describes the product (README, docs, help text, feature map) against what ships, per the owner's pre-release rule (2026-11-13: README, PRIVACY, docs/usage, docs/installation, docs/architecture, docs/style-and-voice, AGENTS updated; marketplace listing text and `agents/openai.yaml` left unchanged because they do not describe voice profiles; refresh at the 0.15.0 release)

---

## Dependencies & Execution Order

- Phase 1 → Phase 2 → stories. T003 (constitution) blocks every story.
- US1 has no story dependency. US2 depends on US1's `kind` rule only through T005 (Phase 2). US3 depends on T005 and on US2's `references/voice-sources.md` for posts read from exports or pages (T014). US4 depends on Phase 2 only. US5 depends on US1–US4 text existing, because help describes them.
- Within a story: guard and cases first (red), then the reference text, then routing and inventory, then the green run.

## Parallel Opportunities

- T001 ∥ T002.
- Within each story, the guard task and the calibration task are [P] (different files).
- US1 and US4 can proceed in parallel after Phase 2 (they touch different sections of `references/voice-profile.md`; still one writer per file at a time).
- T033 ∥ T034.

## Parallel Example: User Story 2

```text
T011 guard in tests/test_skill_contract.py
T012 cases VM05–VM10 in calibration/test-cases.md
T013 synthetic fixtures in tests/fixtures/voice/
```

## Implementation Strategy

- **MVP**: Phase 1–2, US1 and US2 (personal voice from paste or export, optional browser), as one PR.
- **Increment 2**: US3 brand voice.
- **Increment 3**: US4 rating.
- **Increment 4**: US5 help and onboarding, Phase 8 docs, then the 0.15.0 release on the owner's go.
- Each increment: one PR with posted code and security reviews.

## Notes

- Calibration cases are manual until an agent runs them; changelog and PR say so.
- No task stores real user data in fixtures; fixtures are synthetic.
