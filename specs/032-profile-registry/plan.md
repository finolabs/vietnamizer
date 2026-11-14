# Implementation Plan: Find a saved voice profile again by its name

**Branch**: `spec/032-profile-registry` | **Date**: 2026-11-14 | **Spec**: [spec.md](spec.md)

**Input**: `specs/032-profile-registry/spec.md` (settled decisions 1–8, plan decisions P1–P4). Depth DEEP, trigger `privacy`. Release 0.16.0 (decision 8).

## Summary

Add a fixed profile registry, `~/.agents/vietnamizer/registry.md`, that records where each saved profile lives (name, slug, kind, default flag, store, location; no content). A save asks one question to add the row and prints the call sentence for the host. A call (`/vietnamizer <tên>`, `cá nhân`, `personal`, `$vietnamizer <tên>`, "theo hồ sơ <tên>", "theo giọng của tôi") is the read consent for the registry and exactly one matching profile. No store, memory or history is ever searched. The save step stops offering a store that a host or user rule retires (F13). The package stays Markdown only.

## Technical Context

**Language/Version**: Markdown instructions; checks stay Python 3 standard library (`unittest`, `scripts/validate-package.py`).
**Primary Dependencies**: none new.
**Storage**: one new user-side file, `~/.agents/vietnamizer/registry.md`, written only after the user's yes; nothing new in the package.
**Testing**: phrase guards in `tests/test_skill_contract.py` (old guard "không tạo chỉ dẫn tự nạp hồ sơ ở phiên sau" kept, its sentence extended; new guards for FR-002–FR-012); manual cases in `calibration/test-cases.md` (route case 5 rewritten; new block PR01–PR16); `scripts/validate-package.py`; `tests/test_distribution.py` for the adapter.
**Target Platform**: Claude Code, Codex, Antigravity, Skills CLI installs.
**Constraints**: `SKILL.md` ≤ 550 lines; no new reference file (the registry rules live in `references/voice-profile.md` mục 4 and 5); Principle V: no network code, no script in the package.
**Scale/Scope**: one registry per user home; a call reads at most the registry and one profile.

## Constitution Check

| Gate | Result |
|---|---|
| I. Vietnamese evidence first | No pattern change. Pass. |
| II. Meaning and voice | The apply path (five chốt, current request first, one profile) is unchanged (FR-013). Pass. |
| III. General rules vs profiles | No V/T/B/K change. Pass. |
| IV. Labelled evidence | Profiles and the registry stay with the user; nothing enters `calibration/LOG.md`. Pass. |
| V. Self-contained Markdown | No code or network; the registry is a local Markdown file the agent reads and writes with host file tools. Pass. |
| Constraint "Tuyến hồ sơ giọng" | 2.6.1 forbade any lookup beyond what the user pasted or pointed to. **Gate met**: MINOR 2.6.1 → 2.7.0 applied verbatim from Fio's approved text (commit `9dc02a1`, before any reference change; FR-014). |
| Constraint, second change | Chat memory and the reminder needed 2.7.0 → 2.8.0; applied verbatim from Fio's approved text (commit `b390f18`) before the reference change. |
| Governance (`AGENTS.md` vs constitution) | `AGENTS.md` "không tự liệt kê, chọn hay nạp ở phiên sau" conflicts with 2.7.0 once applied; rewritten in this pull request (T006). |

Post-design re-check: pass. Residual risks: a hand-edited registry could point at a file the user did not mean (mitigated by the mục 4 location checks and by the answer naming the location read); the "theo giọng của tôi" call reads a profile on a looser phrase (Fio's decision 6; the answer always names what was read).

## Project Structure

```text
specs/032-profile-registry/
├── spec.md
├── plan.md      # this file
└── tasks.md

.specify/memory/constitution.md   # 2.7.0 (landed first)
references/voice-profile.md        # mục 1, 2, 4 (F13, registry, call sentence), 5 (call and resolution)
references/help.md                 # item 2 call forms, step 6 registry and sentence
SKILL.md                           # line 24 pointer, routing row
.plugin-skills/vietnamizer/SKILL.md  # text after the command is part of the request
AGENTS.md                          # file-map row, "Hồ sơ văn phong cá nhân"
PRIVACY.md, docs/style-and-voice.md, docs/changelog.md
specs/028-voice-profile/contracts/route-contract.md  # read-boundary note
calibration/test-cases.md, tests/test_skill_contract.py
```

Handed over, not edited here: `README.md` (README session), `docs/usage.md` and `docs/installation.md` (docs worktree `030-t035-docs`).

## Path choice (Spec Kit depth gate)

The change crosses a `security-review-gate` trigger (private data, a new read path and consent form), so it runs `speckit-tasks` and the tasks below; no direct path.

## Design notes

- **Registry format** (FR-001): front matter `type: vietnamizer-profile-registry`, `schema: 1`; one table `Tên | Slug | Loại | Mặc định | Kho | Vị trí`. `Kho` is `orrery`, `obsidian` or `markdown`. `Vị trí` is an absolute file path (`markdown`), `space:<space> note:<path>` (`orrery`) or `vault:<vault> file:<path>` (`obsidian`).
- **Write** (FR-002, P1, P2): one question after a successful save; re-read the registry right before writing and change only the asked row.
- **Read** (FR-003–FR-008): only on a call, a row write or the no-match path; location checks of mục 4 before reading; the answer names profile and location.
- **F13** (FR-011): the store offer drops a store a host or user rule in context retires; naming it anyway gets the reason and the other stores.
- **No draft with the call**: the skill resolves and reads the profile, says which one matched, and asks for the text or brief.
