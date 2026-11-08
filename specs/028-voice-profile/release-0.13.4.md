# Release preparation: 0.13.4

## Scope and version choice

Patch 0.13.4 under phase 0 (`0.y.z`): compatible additions only. The 55 pattern IDs and bodies, the Jev runner and its input contract, and the five meaning-preservation rules are unchanged. New: the opt-in voice-profile route (`references/ho-so-giong.md`, `references/phan-tich-giong-viet.md`, one routing row in `SKILL.md`). Changed packaging: release archives no longer contain `calibration/`. Includes the catalog distribution change already on main (PR #30, #31). Version is recorded in `SKILL.md`, the three plugin manifests, README and docs/changelog.md.

Breaking-change check: external readers that expect `calibration/` inside an installed package would find it missing. No repository consumer reads it at run time; manual-install docs were updated.

## Local verification (2026-11-08)

- `python3 scripts/validate-package.py` pass (v0.13.4, 55 patterns).
- `python3 -m unittest tests.test_package_security tests.test_distribution`: 51 tests OK.
- `claude plugin validate .` passes. Offline `python3 -B -m jev status` from the extracted `.skill` returns `key_absent` with a cleaned environment.
- No `calibration/` entry in any of the three archives.

## Candidate assets (local, unpublished)

Hashes describe these local builds only; the final assets must be rebuilt and verified against the merged release commit.

| Candidate | Bytes | SHA-256 |
|---|---:|---|
| vietnamizer.skill | 138717 | `51868594859b858a014fdcce2da3c949aeaad711d2879b785a87a00200d4b293` |
| vietnamizer-claude-org.zip | 137485 | `744d41eeacde110aebf8a3ca3d637a40f927db9371652fe5260f554d06a839ec` |
| vietnamizer-plugin.zip | 141442 | `a09a4be47872fe767663bb9dc484d2b71dc9897204f91a77e96e8c9dd05a78b0` |

## Not verified

No agent has executed the voice-profile route end to end; reviews were of the text. Voice quality is not evaluated and there is no held-out set. SKILL.md grew by about 275 characters for every route.

## Remaining external gates

Push the branch, open the release pull request, follow CI, obtain the required reviews, merge. Then tag `v0.13.4` on the merged commit, publish the three assets and verify their hashes. None of these has been done or authorized.
