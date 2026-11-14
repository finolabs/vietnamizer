# Verification: spec 028 voice-profile

Dates are 2026-11-08. Status words: drafted, verified, integrated, delivered, parked. Nothing is committed or delivered.

## T001 Baseline (before the change, from `git show HEAD:` and specs/027 measurements)

| File | Lines | Unicode characters |
|---|---|---|
| SKILL.md (HEAD) | 135 | 9699 |
| references/giu-giong-tu-mau.md (HEAD) | 60 | 4311 |

`python3 scripts/validate-package.py` on HEAD was not re-run before the edits; the baseline is the file sizes only.

## After the change (working tree)

| File | Lines | Unicode characters | Delta |
|---|---|---|---|
| SKILL.md | 138 | 10094 | +3 lines, +395 chars (+4.1%) |
| references/giu-giong-tu-mau.md | 62 | 4436 | +2 lines, +125 chars |
| references/ho-so-giong.md (new, route only) | 174 | 10982 | n/a |
| references/phan-tich-giong-viet.md (new, build only) | 113 | 8622 | n/a |

**SC-007 finding**: mandatory reads of the existing routes did not stay identical. SKILL.md grew by 395 characters, not only by the added routing row, because two "never saves a profile" sentences were reworded. The small-edit and article routes read SKILL.md, so each pays about 400 extra characters. The supplied-sample route also pays +125 for giu-giong-tu-mau.md. The new files load only on the profile route.

## Checks run by the coordinator

- `python3 scripts/validate-package.py` → "Gói vietnamizer v0.13.3 hợp lệ, gồm 55 pattern" (after ho-so-giong.md existed).
- `python3 -m unittest tests.test_package_security tests.test_distribution` → 50 tests OK.
- Red phase: the delegate ran the new assertions before editing the validator and saw 17 failures caused by the missing/new reference files and inventory mismatch, with the files appearing during the run. This is weaker than a clean single-reason red.

## Not verified

- No behavior run of the route (consent, save, reuse, update, calibration). The seven manual cases exist in calibration/ca-kiem-thu.md but have not been walked (T018 pending).
- No voice-quality evaluation and no held-out set.
- T016 (docs) still running at the time of writing; docs/usage.md, docs/style-and-voice.md, docs/architecture.md, README.md nav line and changelog are not yet changed.
- Reviews (T019) not run.
- Delegation: ledger `finish` lines for T002/T004, T003, T005/T007, T006/T008/T009/T012, T010/T011, T013, T014/T015 use `--accept-unverified` because the work is uncommitted (no head SHA). Log scans flagged a `private_key` pattern in the T005 and T006 logs; the source was not chased (likely the validator's own regex text).

## T016–T019 update (2026-11-08, after reviews)

- T016 docs done by Antigravity flash; coordinator read the diff. Overclaims about privacy filtering were reworded (v1 filters by agent instruction only; the user reading the full draft is the check).
- T017: validator pass, targeted package tests 51 OK, SKILL.md 139 lines, new files free of machine paths and secret patterns.
- T018: case walk by Codex read-only: 4 PASS, 3 WEAK (cases 4, 5, 7). It was a reading of the text, not an agent run. Fixes: SKILL.md note that a profile pasted inline stays on the sample route and "theo giọng của tôi" without a profile opens no route; case 4 and 7 inputs/expectations corrected; spec US4 AC1 given its precondition; cases 8 and 9 added (overwrite, instruction-file target).
- T019: code review (Claude subagent) and security review (Claude subagent): no blocking findings. Fixed in ho-so-giong.md: existence check before write, path rules (directory + slug.md, absolute `~`, refuse `..`, symlinks, Git work tree without confirmation, agent instruction/memory files), Orrery space confirmation and `base_revision`, slug diacritic folding, v1 no temp copies, header check and instruction-line rule for profiles, Jev `register` limited to trait statements and scope without quoted evidence, update only when a profile is in scope, re-read before update, store detection counts declared-but-unloaded tools. Also: SKILL.md description mentions the opt-in profile route (trigger change, owner to confirm), .plugin-skills adapter no longer lists calibration/, README and claude-marketplace-checks (removed; see [blob at 87f4744](https://github.com/finolabs/vietnamizer/blob/87f4744/docs/claude-marketplace-checks.md)) carry the opt-in exception, secret-test message assertion tightened.
- Still not verified: no run of the route by an agent; no test for the source-checkout secret scan of calibration/; no test that an archive containing calibration/ is rejected against a clean payload root; code-review items left open: docs/usage.md duplicates the SKILL.md routing table, the PHI gate in SKILL.md vs "cut the quote" wording in ho-so-giong.md, style cards cite MS01–MS14 that now live only in the repo.
- SC-007 after trimming: SKILL.md 137 lines, 9974 characters (HEAD 135 and 9699: +2 lines, +275 characters, +2.8%, almost all of it the routing row and the description phrase); giu-giong-tu-mau.md +52 characters. The deviation from "only one row" is accepted by the owner as a trim target met in part; the reworded save sentences were reverted to the original wording plus one parenthetical. Validator pass; 51 package tests OK.
