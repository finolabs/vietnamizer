# Tasks: Voice-profile route for Vietnamizer

**Input**: `specs/028-voice-profile/` (spec.md, plan.md, research.md, data-model.md, contracts/, quickstart.md)
**Depth**: DEEP, trigger `privacy`. Two posted reviews (code and security) are required before merge.
**Rules**: serial by default, because the new route files and the docs overlap; `[P]` only where files differ. No commit, push, version bump or release in these tasks. A checkbox is ticked only with command output or a file diff recorded in `specs/028-voice-profile/verification.md`.

## Phase 1: Setup

- [x] T001 Record baseline in specs/028-voice-profile/verification.md: line count of SKILL.md (135), `python3 scripts/validate-package.py` output, and mandatory-read footprints for the small-edit, article and supplied-sample routes taken from specs/027-selective-reading/measurements.json.

## Phase 2: Foundational (blocks every story)

- [x] T002 Write failing tests first: add `references/ho-so-giong.md` and `references/phan-tich-giong-viet.md` to the expected payload in tests/test_package_security.py (assert both appear in vietnamizer.skill and the org zip) and in tests/test_distribution.py if it lists references; run the two files and record the red result.
- [x] T003 Amend .specify/memory/constitution.md from 2.1.0 to 2.2.0 (MINOR): add the opt-in persistence exception (explicit request only, user-chosen store, no automatic search of memory or history, five chốt unchanged), with reason, impact report, and the owner approval of 2026-11-08 from this conversation. Must land before T008.
- [x] T004 Add the two reference paths to REFERENCE_FILES in scripts/validate-package.py so the validator expects them.

## Phase 3: User Story 1 — Build a profile from my own writing (P1)

**Goal**: consent, intake of pasted or named text, Vietnamese analysis, a reviewed profile.
**Independent test**: manual cases 1, 2 and 3 in quickstart.md (consent gating, no personal data in the profile, nothing written without a save request).

- [x] T005 [US1] Create references/phan-tich-giong-viet.md: the seven dimensions from research.md R3 (xưng hô by relationship, sentence particles, English code-switching, punctuation and numbers, diacritics, rhythm, openings/closings), how to count approximately and say so, what is excluded (other authors, quoted text, unmarked AI drafts), the PII trim rule from FR-007, and the "too few samples" rule (FR-008). Vietnamese text, third-person wording for profile content.
- [x] T006 [US1] Create references/ho-so-giong.md part 1: trigger boundary (FR-001), the single consent question (FR-002), read boundary (FR-003, FR-004), no Jev call while building (plan Design 8), working-copy rule (FR-017), show-the-whole-profile step (FR-009). Link to contracts/profile-format.md content by embedding the template, not by pointing outside the package.
- [x] T007 [US1] Embed the profile template (frontmatter, five sections, trait shape {statement, scope, evidence, confidence}) from specs/028-voice-profile/contracts/profile-format.md into references/phan-tich-giong-viet.md.

## Phase 4: User Story 2 — Save where I choose (P1)

**Goal**: explicit-save only, store chosen by the user.
**Independent test**: manual cases 3 and 4 (no save without request; no stores detected → ask path, recommend the default, ask before creating the folder).

- [x] T008 [US2] Extend references/ho-so-giong.md with the save section: explicit request only (FR-010), detection from the agent's own tool and command list without probing reads, offer only detected Orrery and Obsidian and choose neither for the user, plain-file fallback with recommendation `~/.agents/vietnamizer/profiles`, separate yes before creating a folder, slug rule, unreachable store → report and write nowhere else (FR-011). Orrery: a note in the user's folder, not `remember`.

## Phase 5: User Story 3 — Edit or write with a saved profile (P2)

**Goal**: reuse a named profile under the existing safeguards, wired into SKILL.md.
**Independent test**: manual cases 5 and 6 (no profile search when none is named; meaning wins over a profile trait).

- [x] T009 [US3] Extend references/ho-so-giong.md with the reuse section: user names or pastes the profile, read only it, no listing, merging or picking among profiles (FR-012), current request overrides (FR-014), five chốt and genre gates hold and no new facts or catchphrases (FR-013), Jev unchanged with profile text only as style context (FR-021).
- [x] T010 [US3] Edit SKILL.md: add one row to the route table pointing to references/ho-so-giong.md for building, saving, updating or applying a personal profile; replace the sentences that say the skill never saves a profile ("Không tự lưu hồ sơ" in "Trước khi làm" and the feedback sentence in "Làm và kiểm lại") with wording that keeps "no automatic save" and names the opt-in route. Keep the file ≤ 550 lines. Depends on T003.
- [x] T011 [US3] Edit references/giu-giong-tu-mau.md: replace the "không lưu hồ sơ" phrasing with a pointer to the opt-in route and keep its role as the guide for applying evidence.

## Phase 6: User Story 4 — Correct the profile and check it blind (P3)

**Goal**: feedback loop with a shown diff, blind calibration.
**Independent test**: manual case 7 plus a calibration run on a topic outside the samples.

- [x] T012 [US4] Extend references/ho-so-giong.md with the update and calibration section: route each reaction to voice, surface, tone or don'ts; show the exact diff and save only on confirmation; at most two follow-up questions; no personal data or others' text added (FR-015); blind plain-vs-profiled pair on an unrelated topic, unlabeled until the user picks (FR-016); how to read a "plain wins" result (wrong move, indistinct, overdone).

## Phase 7: Polish and cross-cutting

- [x] T013 Add the seven manual cases from quickstart.md to calibration/ca-kiem-thu.md as a new section with input, expected result and reason, marking the anti-overreach cases.
- [x] T014 [P] Update PRIVACY.md: new section on voice profiles (what is read, what may be saved and where, the user's control, what reaches Jev when a profile is applied) and fix the sentence that says the skill never saves a profile.
- [x] T015 [P] Update AGENTS.md: file-table rows for the two new references, and the "không lưu hồ sơ" wording in the giu-giong-tu-mau.md row.
- [x] T016 [P] Update docs/style-and-voice.md, docs/usage.md, docs/architecture.md and README.md (navigation line only); add the Unreleased entry in docs/changelog.md without changing the version.
- [x] T017 Run `python3 scripts/validate-package.py`, the two targeted test files from T002 (now green), and a scan of the new files for machine paths and secrets; confirm SKILL.md ≤ 550 lines and the mandatory-read footprints of the three existing routes match T001 apart from the added routing row. Record outputs in verification.md.
- [x] T018 Walk the seven manual cases from calibration/ca-kiem-thu.md against the finished instructions, recording what was actually exercised; state plainly that voice quality is not evaluated and no held-out set exists.
- [ ] T019 Request the two posted reviews (code review and security review, privacy trigger) per fnl-review-gate; record findings and dispositions in verification.md.

## Dependencies and execution

T001 → T002 → T003 → T004 → T005 → T006 → T007 → T008 → T009 → T010 → T011 → T012 → T013 → (T014, T015, T016 in parallel) → T017 → T018 → T019.

- T003 must complete before T010 (constitution before the SKILL.md change).
- T006, T008, T009 and T012 edit the same file, so they run in order.
- T014–T016 touch different files and may run in parallel.
- Story order is also delivery order: US1 and US2 together are the MVP, because a profile with no save path is only half useful; US3 and US4 follow.
- No model calls, installs, commits, pushes or releases without separate authorization.

Status 2026-11-08: T001–T018 done with evidence in verification.md (T018 is a reading of the text, not an agent run). T019 is done for the first round; a re-review of the post-review fixes is in progress. Nothing is delivered or merged.
