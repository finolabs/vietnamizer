# Implementation Plan: Voice profiles on Cowork and cloud hosts

**Branch**: `spec/039-cloud-voice-profiles` | **Date**: 2026-11-26 | **Spec**: [spec.md](spec.md)

**Input**: spec 039 with Fio's clarifications of 26/11/2026. Router depth DEEP, trigger `privacy`: new stores for user data (a project folder, the user's Google Drive).

## Summary

Three changes to the voice-profile route:

1. Local Cowork, or any session with an attached writable folder, saves full profiles and a registry in `.vietnamizer/`.
2. Cloud Cowork and Chat may keep a full copy in the user's Google Drive beside the compact memory copy.
3. `references/voice-profile.md` splits by task, so applying a profile reads only the apply part.

The constitution amendment ([contracts/constitution-amendment.md](contracts/constitution-amendment.md)) must be approved by Fio before any skill text changes.

## Technical Context

- **Language/Version:** Markdown skill text (Vietnamese). Python 3 standard library for tests only.
- **Primary Dependencies:** none in the package. The stores are host features: the file tools and the Google Drive connector.
- **Storage:** `.vietnamizer/registry.md` and `.vietnamizer/profiles/<slug>.md` in a project folder; one Markdown file per profile in the user's Drive; the home store `~/.agents/vietnamizer/` is unchanged.
- **Testing:**
  - `tests/test_skill_contract.py`, which follows the split and pins the new rules.
  - `scripts/route_budget.py`.
  - Manual cases PJ01–PJ08 in `calibration/test-cases.md`.
  - Runs on Claude Code with a folder that stands in for a project.
  - Runs on claude.ai through the Finos Chrome.
- **Target Platform:** local Cowork, cloud Cowork, claude.ai Chat. Claude Code, Codex and Antigravity are unchanged.
- **Constraints:**
  - Every consent, scope and privacy rule of 0.16.2 is kept.
  - One profile is read per call.
  - No store is searched on a miss.
  - No `.vietnamizer/` inside a Git work tree unless the user names it.
- **Scale/Scope:** one reference split into an index plus 5–6 parts; 4 docs updated; 8 manual cases.

## Constitution Check

| Principle | How the plan meets it | Status |
|---|---|---|
| I. Vietnamese evidence first | No pattern changes. | Pass |
| II. Meaning and voice | Profiles apply under the same five chốt; nothing changes in editing. | Pass |
| III. Rules vs profiles | Profiles stay user data. | Pass |
| IV. Labelled evidence | No threshold is tuned. | Pass |
| V. Self-contained Markdown | No script or network code. Stores are written through the host's own tools. | Pass |
| Constraint "Tuyến hồ sơ giọng" | Fixes the home registry and the Chat-only memory. | **Amendment needed** (FR-008); blocks P2 |

## Delivery order

- **P1. Amendment.** Fio approves the exact text in the contract. Then apply it to `.specify/memory/constitution.md` (2.11.0), with the Sync Impact Report.
- **P2. Red tests.** Add contract tests for:
  - the project store offer, path and creation consent;
  - registry precedence (project, then home);
  - the Drive offer only when the tools are visible;
  - Drive file naming and the compact-copy link;
  - no `.vietnamizer/` in a Git work tree;
  - the split index and the apply-only read.
- **P3. Text.**
  - Split `references/voice-profile.md`.
  - Add the project store and the Drive store to the save, registry and call parts.
  - Update `SKILL.md` pointers, `references/help.md`, `PRIVACY.md`, README and `docs/style-and-voice.md`.
  - Lower the route budget for the voice-profile route.
- **P4. Cases and runs.**
  - Write PJ01–PJ08.
  - Run the project-store cases on Claude Code with a stand-in folder.
  - Run the cloud and Drive cases on claude.ai through the Finos Chrome, with Drive on and off, and with test profiles only.
  - Report what could not be run, which is local Cowork itself.
- **P5. Reviews and release.** Code and security reviews, a drift review, then 0.17.0 on Fio's go.

## Complexity Tracking

| Item | Why | Simpler option rejected |
|---|---|---|
| Two registries (project, home) | Cowork projects are separate workspaces; one home registry cannot see a project's folder on cloud-backed sessions | Home registry only: misses the Cowork case this spec is for |
| Drive store | Only durable full-profile store on cloud hosts that the user owns | Memory only: loses evidence and open points |
