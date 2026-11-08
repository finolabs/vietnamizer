# Implementation Plan: Voice-profile route for Vietnamizer

**Branch**: not created (current branch kept) | **Date**: 2026-11-08 | **Spec**: [spec.md](spec.md)

**Input**: `specs/028-voice-profile/spec.md` (clarified 2026-11-08). Depth DEEP, trigger `privacy`.

## Summary

Add an opt-in route that builds, stores and reuses named Vietnamese writing-style profiles. v1 is Markdown only: two new reference files (workflow, analysis guide), a small routing row and rule amendment in `SKILL.md`, a profile format contract, and coordinated edits to the constitution and privacy-facing docs. The route reads only pasted or named text, saves only on explicit request to a store the user picks (Orrery, Obsidian, or a Markdown path), and applies a profile only inside the existing five-chốt and genre gates. No code, no connector, no new network path.

## Technical Context

**Language/Version**: Markdown instructions; package checks stay Python 3 standard library (`scripts/validate-package.py`, `unittest`).
**Primary Dependencies**: none new. Optional host tools used only if present: Orrery MCP note tools, Obsidian CLI.
**Storage**: user-chosen: Orrery note, Obsidian note, or a plain `.md` file. Nothing stored by the skill otherwise.
**Testing**: `python3 scripts/validate-package.py`, targeted `tests/test_package_security.py` and `tests/test_distribution.py` for the new files; manual cases added to `calibration/ca-kiem-thu.md`.
**Target Platform**: Claude Code, Codex, Antigravity, Claude org zip (existing packaging).
**Project Type**: agent skill (Markdown) with packaging scripts.
**Performance Goals**: mandatory reads of the three existing routes unchanged (SC-007).
**Constraints**: `SKILL.md` ≤ 550 lines (now 135); no secrets, network or build for the route; machine-path scan in the payload must still pass.
**Scale/Scope**: 5–30 pasted pieces per profile; bulk corpora out of scope.

## Constitution Check

| Gate | Result |
|---|---|
| I. Vietnamese evidence first | The analysis dimensions come from observable Vietnamese features (xưng hô, particles, code-switching, diacritics). Marked as inference where not source-backed; no English rule imported. Pass, with research.md R3 recording the status of each dimension. |
| II. Meaning and voice before polish | The route applies profiles only under the five chốt; current request overrides profile (FR-013, FR-014). Pass. |
| III. General rules vs genre profiles | No V/T/B/K numbering change. Personal voice stays out of shared profiles and the calibration log. Pass. |
| IV. Labelled evidence | Personal preference stays in the user's own profile, never in `calibration/LOG.md`. Quality claims are not made: behavior stays "pending" until a held-out set exists. Pass. |
| V. Self-contained Markdown | No build, network or secret. Pass. |
| Package constraints | Two new reference files must be added to `REFERENCE_FILES` and the archive tests; `SKILL.md` stays under 550. Pass once tasks cover it. |
| Governance | The feature changes a stated owner rule ("không tự lưu hồ sơ"). Needs a constitution MINOR amendment (2.1.0 → 2.2.0) with reason, impact report and owner approval. The owner decision of 2026-11-08 exists in this conversation; the amendment text must cite it. **Gate: amendment lands before or with the SKILL.md change.** |

Post-design re-check: pass, no new violations. One residual risk is recorded under Risks.

## Project Structure

### Documentation (this feature)

```text
specs/028-voice-profile/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── route-contract.md      # triggers, consent, read/write boundaries
│   └── profile-format.md      # file format, naming, store mapping
└── tasks.md                   # from speckit-tasks
```

### Source (repository root)

```text
SKILL.md                              # + 1 routing row, amended wording about saving profiles
references/ho-so-giong.md             # NEW: route workflow (consent, intake, save, reuse, update, calibration)
references/phan-tich-giong-viet.md    # NEW: Vietnamese analysis guide + profile template
references/giu-giong-tu-mau.md        # wording: points to the route; keeps "no auto-save"
calibration/ca-kiem-thu.md            # + manual cases for the route
.specify/memory/constitution.md       # 2.1.0 -> 2.2.0
AGENTS.md, PRIVACY.md                 # file table and data section
docs/style-and-voice.md, docs/usage.md, docs/architecture.md, README.md
scripts/validate-package.py           # REFERENCE_FILES += 2
tests/test_package_security.py        # assert 2 new files in archives
tests/test_distribution.py            # as needed for file inventory
```

**Structure Decision**: two reference files rather than one, so that building loads both analysis and workflow, applying a stored profile loads the workflow only, and a profile pasted inline in an edit request stays on the existing sample route and loads neither; the existing `giu-giong-tu-mau.md` stays the guide for applying evidence.

## Design

1. **Trigger (FR-001)**: `SKILL.md` gains one routing row: asked to learn/build/update/apply a personal writing-style profile → read `references/ho-so-giong.md`. Applying a profile also reads `giu-giong-tu-mau.md` as today. Ordinary edit requests do not hit the row.
2. **Consent first (FR-002/003)**: step 1 of the workflow is one question naming exactly what will be read (what the user pasted or named) and what will be produced; nothing is read before the yes.
3. **Analysis (FR-005–008)**: `phan-tich-giong-viet.md` lists the dimensions, how to count them approximately, what counts as evidence, what to exclude (quoted text, other authors, unmarked AI drafts), and the PII rule with a trim procedure. Counts are labelled approximate (FR-018).
4. **Profile (FR-006)**: fixed sections defined in `contracts/profile-format.md`; each trait carries scope, a short trimmed fragment or count, and a confidence note.
5. **Review then save (FR-009–011)**: show the whole profile; save only on an explicit ask. Store discovery: the agent checks its own tool list for Orrery note tools and for an Obsidian CLI; it never runs a search or reads content to detect. It offers only what it found, picks none for the user, and with none found asks for a path and recommends `~/.agents/vietnamizer/profiles`. It asks before creating a folder.
6. **Reuse (FR-012–014)**: the user names or pastes the profile; the skill reads that one item only. Profile traits are applied through the existing sample-voice rules; the user's current request wins.
7. **Feedback and calibration (FR-015/016)**: show the exact diff; save only on confirmation. Blind pair on an unrelated topic; route each reaction to a section.
8. **Jev (FR-021)**: building a profile does not call Jev (nothing to evaluate). Applying a profile goes through the unchanged edit path; profile text is style context added to `register` as today (`typesafe-advisor.md` line 40). The implementation task states the fields in `PRIVACY.md`. Residual risk: the owner chose "as today", so a profile excerpt may reach Jev when a key and permission exist; it contains no personal data by FR-007.
9. **Temporary files (FR-017)**: the route works in conversation context by default; if it needs a file, only outside any git work tree, deleted at the end.
10. **Docs (FR-019)**: constitution, `AGENTS.md` (roles table and the "không lưu hồ sơ" wording), `PRIVACY.md` new section "Hồ sơ giọng", `docs/style-and-voice.md`, `docs/usage.md`, `README.md` index, and `SKILL.md` / `giu-giong-tu-mau.md` wording change together.

## Verification plan

- Red first: add the two files to `REFERENCE_FILES` and the archive assertions; tests fail until the files exist and are packaged.
- Structural: `validate-package.py`, targeted package tests, line budget, machine-path and secret scan on the new files, link check from `SKILL.md`.
- Footprint: re-measure mandatory reads for the three existing routes against `specs/027-selective-reading/measurements.json`; expect unchanged except the added routing row.
- Behavior: manual cases (consent gating, no-save default, PII trimming, unnamed-profile refusal, store offer with none/one/both, meaning conflict) added to `calibration/ca-kiem-thu.md` and run by hand. No claim of voice quality; held-out evaluation stays pending.
- Reviews: independent code review and security review (privacy trigger) before merge.

## Risks and open points

- **Jev residual** as in Design 8; revisit if the owner wants a stricter rule.
- **Detection of Orrery/Obsidian** is judged from the agent's tool list; hosts differ. The contract says: offer only what is present, otherwise ask for a path.
- **Amendment ordering**: constitution change must not trail the SKILL.md change.
- **Quality unproven**: v1 shows a workflow and guardrails, not improved voice match.
