# Plan: 034 colon and compound

**Path**: direct (Spec Kit depth gate). One seam: catalog text in `references/typography.md` (T2) and `references/missing-words.md` (V20), two sentences of the gate in `SKILL.md`, the T2 row and gate note in `docs/patterns.md`. Consumers known: the agent reading these files; `tests/test_skill_contract.py` and `tests/test_distribution.py`. No task ordering or parallel split, no security trigger (no new input, network, data exposure or consent path), no migration or dependency.

**Changes**: FR-001–FR-003 in T2; FR-004 and FR-005 in `SKILL.md`; FR-005–FR-006 in V20; FR-007 in `calibration/test-cases.md` and `tests/test_skill_contract.py`. Version 0.16.2 in `SKILL.md`, three manifests, README, installation, changelog; `docs/architecture.md` source version corrected. Social preview JSON and README banner per decision 3.

**Proof**: `python3 -m unittest tests.test_skill_contract`, then `tests.test_distribution`; packaging checks (`package-plugin.py --check`, `validate-package.py`, `claude plugin validate .`).
