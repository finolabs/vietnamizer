# Tasks: Find a saved voice profile again by its name

**Input**: [spec.md](spec.md), [plan.md](plan.md). Tests are phrase guards plus manual calibration cases; a guard is written red first, then the reference text turns it green.

## Phase 1 — Gate

- [x] T001 Constitution 2.6.1 → 2.7.0 with Fio's approved text and Sync Impact Report (`.specify/memory/constitution.md`, commit `9dc02a1`). FR-014.

## Phase 2 — Guards first (red)

- [ ] T002 Add guards in `tests/test_skill_contract.py` for the registry path and its data rule, the call-is-consent rule, resolution order, no-match without search, location checks, row write only on yes, printed call sentence, F13 store rule, help call forms; run and see them fail. FR-001–FR-012.

## Phase 3 — US1–US4 references (green)

- [ ] T003 `references/voice-profile.md` mục 1 and 2: calls open the route; call = consent for registry and one profile; "theo giọng của tôi" with no personal row keeps the shipped behaviour. FR-004, FR-005, FR-009.
- [ ] T004 `references/voice-profile.md` mục 4: F13 store rule; registry subsection (format, write question, default, repoint, refusals); call sentence per host. FR-001, FR-002, FR-010, FR-011, P1, P2.
- [ ] T005 `references/voice-profile.md` mục 5: call forms, resolution steps, no match, location checks, missing profile, registry as data, show or remove a row. FR-004–FR-008, FR-012, P3, P4.
- [ ] T006 `SKILL.md` line 24 pointer and routing row; `.plugin-skills/vietnamizer/SKILL.md` arguments sentence; `AGENTS.md` file map row and "Hồ sơ văn phong cá nhân". FR-015.
- [ ] T007 `references/help.md` item 2 call forms and step 6 registry question and sentence. FR-010.

## Phase 4 — Cases and docs

- [ ] T008 `calibration/test-cases.md`: rewrite route case 5; add block PR01–PR16. SC-001–SC-006.
- [ ] T009 `PRIVACY.md`, `docs/style-and-voice.md`, `docs/changelog.md` (0.16.0), `specs/028-voice-profile/contracts/route-contract.md` note. FR-015.
- [ ] T010 Hand-over note for `README.md`, `docs/usage.md`, `docs/installation.md` in the shared notes folder. FR-015.

## Phase 5 — Checks and PR

- [ ] T011 `uptime` below 15, then `python3 -m unittest tests.test_skill_contract`, `python3 -m unittest tests.test_distribution`, `python3 scripts/validate-package.py` (one per command).
- [ ] T012 Open the PR with the router marker, fresh code and security reviews posted through `review-gate`; no merge without Fio's go.
