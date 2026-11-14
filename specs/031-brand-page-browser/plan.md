# Implementation Plan: Read a brand's own page through the host browser for a brand profile

**Branch**: `spec/031-brand-page-browser-impl` | **Date**: 2026-11-14 | **Spec**: [spec.md](spec.md)

**Input**: `specs/031-brand-page-browser/spec.md` (settled decisions 1–10 of 2026-11-14). Depth DEEP, trigger `privacy`. Release 0.16.0 (Fio, 14/11/2026: bundle everything into 0.16.0).

## Summary

Reverse the spec 030 FR-006 implementation decision: a `kind: brand` profile may also learn from the brand's public page, read through a browser tool the host already offers, from at most three URLs the user gives, each after its own consent question that names the brand and the URL and carries the authority statement. The route is fixed per platform (Facebook fanpage, LinkedIn company page, a listing page on the brand's own website or blog), reads only post bodies the brand published, and stops on any page it cannot tie to the named brand. The package stays Markdown only: the constitution gains the source (MINOR 2.5.0, landed first), the brand rules go into a new brand subsection of `references/voice-sources.md` mục 4, and every reference, contract, test, calibration case and doc that said "no browser for brand pages" is rewritten. No network code, no new file in the package.

## Technical Context

**Language/Version**: Markdown instructions; package checks stay Python 3 standard library (`scripts/validate-package.py`, `scripts/package-plugin.py`, `unittest`).
**Primary Dependencies**: none new. Optional host capability: a browser tool (Claude in Chrome, the in-app browser pane or an equivalent), as in spec 030.
**Storage**: unchanged; the profile's sources line counts brand posts read through the browser as `trình duyệt`, never a URL.
**Testing**: `tests/test_skill_contract.py` (the two asserts at `:173` and `:225` that pin the old no-browser phrases are replaced, and new phrase guards cover FR-002–FR-010); `tests/test_package_security.py`; `tests/test_distribution.py`; `scripts/validate-package.py`; `claude plugin validate .`; manual cases in `calibration/test-cases.md` (VM05, VM11, VM15 and VM31 rewritten; new block BP01–BP27).
**Target Platform**: Claude Code, Codex, Antigravity, standalone skill installs.
**Project Type**: agent skill (Markdown) with packaging scripts.
**Performance Goals**: the default editing path reads nothing new; onboarding keeps at most 6 questions before rating (FR-013).
**Constraints**: `SKILL.md` ≤ 550 lines and unchanged; no new reference file (the inventory in `scripts/validate-package.py` stays as it is); Principle V: no network code in the package.
**Scale/Scope**: ≤ 3 brand URLs per run; ≤ 80 posts across them (FR-011); on a website, only post pages linked from the given listing page, no pagination.

## Constitution Check

| Gate | Result |
|---|---|
| I. Vietnamese evidence first | Only Vietnamese text in brand posts counts as evidence (unchanged rule, `references/voice-sources.md` mục 3). Pass. |
| II. Meaning and voice before polish | A brand profile still applies only under the five chốt; nothing in the apply path changes (FR-014). Pass. |
| III. General rules vs genre profiles | Brand voice stays in user profiles; no V/T/B/K change. Pass. |
| IV. Labelled evidence | Brand pages feed one user's profile only; nothing enters `calibration/LOG.md`. Pass. |
| V. Self-contained Markdown | No build, network call, secret or runner in the package; the brand path uses a host browser tool and the route works without it (paste and export first). Pass. |
| Package constraint "Tuyến hồ sơ giọng" | Version 2.4.1 forbade reading another party's page and kept the browser to the user's own account. **Gate met**: MINOR amendment 2.4.1 → 2.5.0 applied verbatim from the spec's "Constitution amendment" text, Fio's approval of 14/11/2026 recorded in the Sync Impact Report, pending line replaced by the reversal (commit `4569441`, before any reference change; FR-015). Second MINOR 2.5.0 → 2.6.0 for the shared-platform post paths of decision 12, exact sentence approved by Fio on 14/11/2026. |
| Personal Page route (decision 11) | `references/voice-sources.md` mục 4c reads a Facebook Page named for the user for a `kind: personal` profile. The constraint already allows "trang của chính người dùng ... sau câu đồng ý đọc và lời khẳng định chủ tài khoản"; no amendment. Only spec 030's fixed own-account URL rule gets an exception (FR-007 note). Pass. |
| Governance | The amendment keeps "MUST NOT đọc trang của người khác, kể cả trang thương hiệu người dùng không được nói thay"; FR-007 (competitor decline) implements it. Pass. |

Post-design re-check: pass; residual risks below.

## Project Structure

### Documentation (this feature)

```text
specs/031-brand-page-browser/
├── spec.md
├── plan.md            # this file
├── research.md        # R1–R7 decisions, O2 settled
├── data-model.md      # brand page source, URL check, stop event, sources line
├── quickstart.md      # validation walk-through
├── contracts/
│   └── brand-page-route.md   # accepted URLs, consent, fixed route, stops, the one click
└── checklists/requirements.md
```

### Source (repository root)

```text
.specify/memory/constitution.md            # 2.5.0 (landed first)
references/
├── voice-sources.md                         # mục 1 (brand browser source), 2 (brand pages), 4 split: 4a personal, 4b brand
├── brand-voice.md                           # mục 1 item 2 and links paragraph; mục 3 pages read through the browser
├── voice-profile.md                         # mục 2: brand page consent question
├── voice-analysis.md                        # sources line: trình duyệt for brand posts
└── help.md                                  # help item 3, onboarding steps 2–3, budget line
specs/030-voice-modes/spec.md                # FR-006 delivery note
specs/030-voice-modes/contracts/{profile-format,help-onboarding}.md
tests/test_skill_contract.py                 # replace :173 and :225, add 031 guards
calibration/test-cases.md                    # VM05, VM11, VM15, VM31; BP01–BP27
AGENTS.md, PRIVACY.md, README.md, docs/style-and-voice.md, docs/architecture.md
docs/changelog.md, docs/installation.md, SKILL.md metadata, three plugin.json   # 0.16.0
```

**Structure Decision**: keep the browser rules in one place, `references/voice-sources.md` mục 4, with two subsections (personal account, brand page), as FR-016 asks ("a brand subsection beside the personal one"). `references/brand-voice.md` and `references/voice-profile.md` point to it instead of repeating the route. No new file, so the package inventory, adapters and line limits stay as they are.

## Tasks path

The Spec Kit depth gate does not allow a direct path: the change accepts new input (pages from URLs the user gives), which is a `security-review-gate` trigger, and touches about twenty files across references, contracts, tests, calibration and docs. `speckit-tasks` runs, then `speckit-implement`.

## Phases

- **Phase 0** (research.md): R1–R7; O2 settled by Fio on 14/11/2026 (decision 10).
- **Phase 1** (data-model.md, contracts/, quickstart.md): written with this plan.
- **Phase 2** (`/speckit-tasks`): constitution (done) → red guards in `tests/test_skill_contract.py` → references → spec 030 contracts and note → calibration → docs → release 0.16.0 → checks, security audit, PR and reviews.

## Risks

- **A false authority statement**: the skill cannot verify it (decision 4); mitigated by the competitor decline (FR-007), the brand-name check (FR-008) and saying plainly that it cannot verify. Residual and accepted by the owner.
- **Page text reaching the profile**: comments, reviewer names and "people also viewed" arrive in the same page read; mitigated by the discard rule (FR-009), the redaction of `references/brand-voice.md` mục 3 and calibration case BP14.
- **Platform terms and account restriction**: the warning once per platform before its first consent question (FR-004); paste and export stay first.
- **Prompt injection from pages**: page text is data (FR-012); no link inside a post is followed (FR-005); calibration case BP20.
- **URL shapes drift**: O2 was settled on platform conventions, not checked on live pages; the page-type and brand-name checks stop on anything that does not match, so drift fails closed.
- **No runtime evidence**: the cases are manual until an agent runs them on a host with a browser; release notes say so.

## Complexity Tracking

None beyond the constitution amendment above.
