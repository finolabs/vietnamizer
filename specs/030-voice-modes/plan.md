# Implementation Plan: Personal and brand voice, social sources, user rating, help and onboarding

**Branch**: `spec/030-voice-modes` | **Date**: 2026-11-13 | **Spec**: [spec.md](spec.md)

**Input**: `specs/030-voice-modes/spec.md` (owner decisions and clarifications of 2026-11-13). Depth DEEP, trigger `privacy`.

## Summary

Extend the opt-in voice-profile route (spec 028, PR #39) with a profile `kind` (personal or brand), three learning sources (paste, platform export, the user's own page through a host browser tool), a rating session of four levels whose counts are stored in the profile, and a help and onboarding entry. The package stays Markdown only: three new reference files, edits to `references/voice-profile.md` and `references/voice-analysis.md`, two routing rows in `SKILL.md`, one plugin adapter for `help`, and coordinated amendments to the constitution, README, PRIVACY and `docs/style-and-voice.md`. No code in the package, no network call of its own, no evaluator; the browser path uses only a tool the host already has.

## Technical Context

**Language/Version**: Markdown instructions; package checks stay Python 3 standard library (`scripts/validate-package.py`, `scripts/package-plugin.py`, `unittest`).
**Primary Dependencies**: none new. Optional host capabilities used only when present: a question form (`AskUserQuestion`, `request_user_input`, `ask_question`), a browser tool (Claude in Chrome, the in-app browser or an equivalent), Orrery or Obsidian for storage as in spec 028.
**Storage**: unchanged from spec 028; the profile file the user chooses now also holds `kind`, brand rules and rating history.
**Testing**: `tests/test_skill_contract.py` guards for the new rules; `tests/test_package_security.py` and `tests/test_distribution.py` for the new files and the second plugin skill; `scripts/validate-package.py`; `claude plugin validate .`; `npx skills add . --list`; manual cases in `calibration/test-cases.md` (new block VM01–VM16).
**Target Platform**: Claude Code, Codex, Antigravity, standalone skill installs.
**Project Type**: agent skill (Markdown) with packaging scripts.
**Performance Goals**: the default editing path reads nothing new (SC-001); onboarding to a drafted profile in under 10 minutes and at most 6 questions before rating (SC-003).
**Constraints**: `SKILL.md` ≤ 550 lines (now 128); every new reference listed in `REFERENCE_FILES`; no secrets, credentials or cookies handled; payload machine-path scan still passes.
**Scale/Scope**: paste 10–20 posts; exports capped to the most recent 80 owned posts (research R4); rating sessions 0–10 paragraphs.

## Constitution Check

| Gate | Result |
|---|---|
| I. Vietnamese evidence first | Only Vietnamese text in a source counts as evidence; export and page filtering is a data rule, not a style rule. Pass. |
| II. Meaning and voice before polish | Profiles of both kinds apply only under the five chốt; one profile per use; generated rating paragraphs obey the chốt. Pass. |
| III. General rules vs genre profiles | Brand voice lives in user profiles, not in `profiles/` (genre profiles). No V/T/B/K change. Pass. |
| IV. Labelled evidence | Ratings are the user's judgement of their own profile and stay in that profile; they never enter `calibration/LOG.md` and are not used as quality evidence for the skill. Pass. |
| V. Self-contained Markdown | No build, network call, secret or runner in the package. The browser path uses a host tool and works without it (paste and export remain). Pass, with the amendment below. |
| Package constraints | "v1 MUST NOT lấy mẫu qua connector" conflicts with the browser source; the multi-author brand source conflicts with "chỉ phần do người dùng tự viết". **Gate: constitution MINOR amendment 2.3.0 → 2.4.0 with reason, impact report and the owner approval of 2026-11-13, landing before or with the route change.** |
| Governance | `references/voice-profile.md` mục 7 and README/style docs say the skill does not score similarity; decision 7 stores user ratings. The amendment keeps "the skill never scores" and adds "user ratings may be stored, labelled as the user's judgement". Pass with FR-017 tasks. |

Post-design re-check: pass; residual risks listed below.

## Project Structure

### Documentation (this feature)

```text
specs/030-voice-modes/
├── spec.md
├── plan.md            # this file
├── research.md        # R1–R8 decisions
├── data-model.md      # profile v1 additions, source, rating session, brand rule
├── quickstart.md      # validation walk-through
├── contracts/
│   ├── profile-format.md   # additive fields on top of spec 028's contract
│   ├── rating-session.md   # the question flow and the stored line
│   └── help-onboarding.md  # help output and onboarding steps
└── checklists/requirements.md
```

### Source (repository root)

```text
SKILL.md                                  # 2 routing rows: help/onboarding, brand voice; one sentence on kind
.plugin-skills/help/SKILL.md              # new plugin adapter → references/help.md
references/
├── voice-profile.md                        # kind, one-profile rule, source step, rating step (mục 7 rewritten)
├── voice-analysis.md               # kind field, brand rules section, rating history section
├── voice-sources.md                          # new: paste, export (LinkedIn, Facebook), browser path, ownership, filtering
├── brand-voice.md                  # new: brand sources, guide rules vs observed traits, redaction
└── help.md                           # new: help overview and onboarding flow
calibration/test-cases.md                # VM01–VM16
.specify/memory/constitution.md           # 2.4.0 amendment
README.md, PRIVACY.md, docs/style-and-voice.md, docs/changelog.md, AGENTS.md
scripts/validate-package.py, scripts/package-plugin.py   # inventory and second adapter
tests/test_skill_contract.py, tests/test_distribution.py, tests/test_package_security.py
```

**Structure Decision**: keep one plugin; add `help` as a second adapter so the plugin exposes `/vietnamizer:help`. The help and onboarding text lives once in `references/help.md`, reached both from the adapter and from a routing row in `SKILL.md`, so standalone skill installs get the same help by asking for it.

## Phases

- **Phase 0** (research.md): R1–R8 below; no open unknowns.
- **Phase 1** (data-model.md, contracts/, quickstart.md): written with this plan.
- **Phase 2** (`/speckit-tasks`): order is constitution amendment → data model and contract text in references → sources → brand → rating → help adapter and packaging → docs → calibration and guards.

## Risks

- **Browser path on LinkedIn**: the user may get their account restricted; mitigated by the warning and the user's decision (FR-007), and by keeping paste and export first.
- **Ratings read as quality evidence**: mitigated by the label in the profile, the README wording and the rule that ratings never enter calibration.
- **Brand material carries third-party personal data**: same redaction as personal samples; calibration cases with staff and customer names.
- **No runtime evidence**: as in spec 028, the cases are manual until an agent runs them; release notes must say so.

## Complexity Tracking

None beyond the constitution amendment above.
