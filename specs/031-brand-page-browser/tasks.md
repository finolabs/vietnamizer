# Tasks: Read a brand's own page through the host browser for a brand profile

**Input**: `specs/031-brand-page-browser/` (spec.md, plan.md, research.md, data-model.md, contracts/, quickstart.md)
**Tests**: required. New behaviour starts from a red guard in `tests/test_skill_contract.py` that fails before the Markdown change, plus manual calibration cases in `calibration/test-cases.md`. Guards prove the rule text ships, not agent behaviour.
**Organization**: by phase; US1–US3 share the route text in `references/voice-sources.md` mục 4b, so they land together; US4 is onboarding.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel (different files, no dependency on an unfinished task)
- **[Story]**: US1–US4 from spec.md

## Path Conventions

Repository root of `finolabs/vietnamizer`. Run tests with `python3 -B -m unittest <module>`, one module per command; check `uptime` first.

---

## Phase 1: Foundational (blocks every reference change)

- [x] T001 Amend `.specify/memory/constitution.md` to 2.5.0 (MINOR) with the spec's "Constitution amendment" text verbatim; record Fio's approval of 14/11/2026 in the Sync Impact Report and replace the 2.4.1 pending line with the reversal (FR-015; commit `4569441`)
- [x] T002 Settle open decision O2 with Fio and record it as decision 10 in `spec.md` and R1 in `research.md` (approved 14/11/2026, platform conventions, not live pages)

## Phase 2: Red guards

- [x] T003 In `tests/test_skill_contract.py`, replace the old phrase at `:173` ("không mở link bằng công cụ trình duyệt hay công cụ tải trang nào") with the new `references/brand-voice.md` phrases, and the one at `:225` ("không đưa lựa chọn trình duyệt") with the new onboarding phrase; add `test_brand_page_browser_rules` covering FR-001–FR-012 in `references/voice-sources.md` mục 4b and the consent wording in `references/voice-profile.md` mục 2; run the module and confirm the new guards fail

## Phase 3: US1–US3 route (P1, P2, P1)

- [x] T004 [US1] [US2] [US3] Split `references/voice-sources.md` mục 4 into 4a (personal account, current text) and 4b (brand page): accepted URLs and page signs (R1), at most three URLs of one brand, consent per URL, terms warning per platform, fixed route, website limits (R4), shared platforms (R5), the one click (R6), stops, discard rule, cap; update mục 1 (third source for brand) and mục 2 (brand pages read only under 4b)
- [x] T005 [US1] [US3] Update `references/brand-voice.md` mục 1 (item 2 and the links paragraph: the browser path of mục 4b, competitor decline) and mục 3 (pages read through the browser: discard non-post text, no staff names; sources line `trình duyệt`)
- [x] T006 [US1] Update `references/voice-profile.md` mục 2: the brand page consent question names the brand and the exact URL, asks the authority statement, says it cannot be verified; one per URL; terms warning per platform before the first one
- [x] T007 [P] [US1] Update `references/voice-analysis.md` sources line: brand posts count by `dán / export / trình duyệt`, no URL

## Phase 4: US4 onboarding (P3)

- [x] T008 [US4] Update `references/help.md`: help item 3 (brand page through the browser), onboarding step 2 (Thương hiệu offers the browser source after paste and export when a browser tool is seen), step 3 (terms warning for Facebook and LinkedIn only, consent with brand and URL), budget line (URL and brand name take "nền tảng khi cần"; the second and third consent questions sit outside the 6)

## Phase 5: Spec 030 artifacts

- [x] T009 [P] Update `specs/030-voice-modes/contracts/profile-format.md:15` (brand posts may count `trình duyệt`) and `contracts/help-onboarding.md` (help item 3, onboarding steps 2 and 3, budget line), each with a dated pointer to spec 031
- [x] T010 [P] Update the FR-006 delivery note in `specs/030-voice-modes/spec.md`: the brand-page decision was reversed by spec 031 on 14/11/2026

## Phase 6: Calibration

- [x] T011 In `calibration/test-cases.md`: VM05 keeps its fetch-tool half and gains the browser-tool brand path; VM11, VM15 and VM31 say they apply when the voice kind is Cá nhân; add block BP01–BP20 (FR-002–FR-010, the competitor case, a "See more" that does not expand in place, a news-site tag page)

## Phase 7: Docs

- [x] T012 [P] Update `AGENTS.md` file map rows for `references/voice-sources.md` and `references/brand-voice.md`
- [x] T013 [P] Update `PRIVACY.md` (brand pages through the browser, what is read and discarded, authority not verified)
- [x] T014 [P] Update `README.md` voice section and `docs/style-and-voice.md` sources line
- [x] T015 [P] Update `docs/architecture.md` line for `references/voice-sources.md`

## Phase 8: Release 0.16.0

- [x] T016 Bump to 0.16.0 per `finolabs-vibecode:versioning`: `SKILL.md` metadata.version, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.antigravity-plugin/plugin.json`, README version line and history, `docs/installation.md`; turn "Chưa phát hành" in `docs/changelog.md` into "### 0.16.0" and fold in the 031 work
- [x] T017 Review everything that describes the product against what ships (diagrams, README, docs, help) and fix drift or record why not

## Phase 9: Checks and gates

- [ ] T018 `uptime`, then `tests.test_skill_contract`, `tests.test_package_security`, `tests.test_distribution` (separate commands), `python3 -B scripts/validate-package.py`, `claude plugin validate .`
- [ ] T019 `security-audit` on the change (new trust boundary: pages from URLs the user gives)
- [ ] T020 Open the PR with `<!-- fnl-router depth=DEEP trigger=privacy -->`; fresh-context `fnl-reviewer` and `fnl-security-reviewer`; post both with `review-gate`'s `post_review.py`; `merge_check.py --repo finolabs/vietnamizer <PR>`
- [ ] T021 Build archives in `dist/` and list their SHA-256 in `.finolabs/release-0.16.0.md`; no merge, tag, release or catalog pin without Fio's go

## Dependencies

T001 → everything. T003 before T004–T008. T004 before T005–T006 (they point to mục 4b). T009–T015 after T004. T016–T017 after T015. T018–T021 in order.
