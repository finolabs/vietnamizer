# Feature Specification: Remove Jev (TypeSafe evaluator) from Vietnamizer

**Created**: 2026-11-13
**Status**: Specify + plan accepted by owner decisions below; implementation on branch `refactor/remove-jev`
**Input**: Owner: "Tao muốn gỡ bỏ Jev khỏi Vietnamizer". Router depth DEEP, trigger `contract` (removes a documented public surface; touches packaging and privacy docs).

## Settled decisions (owner, 2026-11-13)

1. **Scope**: remove the whole `jev/` package (runner, transport, preparation, coverage, registry, `__main__`), `references/typesafe-advisor.md`, `scripts/build-jev-registry.py`, and the `register`/style-context handling that fed the evaluator. Nothing in the shipped skill runs Python or reads `TYPESAFE_API_KEY` afterwards.
2. **Benchmarks**: remove `benchmarks/jev_*.py`, `benchmarks/public_*.py`, their tests and `eval/guard/`. Specs 001–028, `calibration/` and `docs/benchmarks.md` stay as dated history with a note that the evaluator no longer exists (same approach as `docs/typesafe-removal-2026-10-03.md`).
3. **Docs**: constitution principle V is rewritten to "no external service, no key"; README and PRIVACY stop mentioning the evaluator except one line saying it was removed; `CHANGELOG`/`docs/changelog.md` record the removal and the consumer action.

## Requirements

- FR-001: No runtime path, package payload entry, doc claim or test depends on Jev or `TYPESAFE_API_KEY`.
- FR-002: The five meaning-preservation rules and the 55 patterns (`references/*`, `profiles/*`) are byte-unchanged.
- FR-003: The voice-profile route stays; its docs (PRIVACY, AGENTS, `references/ho-so-giong.md` §5, spec 028 FR-021 note) no longer say a profile may enter the Jev `register` context.
- FR-004: `scripts/validate-package.py` passes without the registry parity check; `PACKAGE_PAYLOAD` and `REFERENCE_FILES` drop `jev` / `typesafe-advisor.md`; `package-skill.sh`, `package-plugin.py`, and `scan-tells.sh` hold no Jev dependency. `scan-tells.sh` keeps working as a human-review aid.
- FR-005: Release archives are smaller (jev ≈ 211 KB of ≈ 425 KB uncompressed).
- FR-006: Version: phase 0, removing a documented feature = MINOR (0.14.0). The release itself is the owner's decision; this change prepares the version and changelog only if the owner asks.

## Consumer action

Users who set `TYPESAFE_API_KEY` for the skill: nothing breaks; the key is simply unused. Remove it from the skill's environment if it was added only for Vietnamizer. Agents that called `python3 -m jev …` must stop; the Markdown core is unchanged.

## Out of scope

Rewriting historical specs, `calibration/`, `docs/benchmarks.md`, or deleting local ignored `artifacts/` and `output/`.
