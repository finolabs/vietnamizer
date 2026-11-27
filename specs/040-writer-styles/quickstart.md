# Quickstart: validating spec 040

Run everything from the worktree `.claude/worktrees/040-writer-styles`.

- Check the load average with `uptime` before each step.
- Run at most two test modules per command.
- Run every paid run through the heavy-job lock.

## 1. Static checks (SC-001, SC-002, SC-005)

```bash
python3 -B scripts/validate-package.py
```
**Expected:** the package is valid, with 11 style cards, and no failure line.

```bash
python3 -B -m unittest tests.test_skill_contract tests.test_package_security
```
**Expected:** every test passes, including the new card-list and card-field tests from [contracts/card-list.md](contracts/card-list.md).

```bash
python3 -B -m unittest tests.test_route_budget
```
```bash
python3 scripts/route_budget.py
```
**Expected:**
- every route is at or under its `max_bytes`;
- `git diff main -- benchmarks/route-budget.json` shows no `max_bytes` raised;
- `wc -c SKILL.md` is at most 14,428.

## 2. Probe before the full run (research R4)

Build the base zip (v0.16.3) and the candidate zip into `.finolabs/harness-040/`. Then run WS01, WS04, WS07 and WS10 on the base arm only, 5 reps per model. (Run on 27/11/2026 on both arms, 2 reps per model.)

The base arm has no new card, so this step does not test whether those cards are picked. It counts how often a run reads any card at all.

Record the rate; it is not a gate. Fio settled on 27/11/2026 that the full run follows the probe whatever the rate, and that SC-004 counts only runs that read a card.

## 3. Early model run (SC-003, SC-004)

All arms run in one batch, as research R6 sets out:
- D11–D34 on both arms;
- MS01–MS14 on both arms;
- WS01–WS12 on the candidate.

Score the edits:

```bash
python3 benchmarks/holdout_036.py score <index>
```
Count card picks from the read log of each run.

**Pass, per model (Opus 5.5 and Sonnet 5.5):**
- fixes and guard breaks are each no worse than the base arm by more than 2 (fewer fixes or more guard breaks), as spec 038 FR-004; fixes are summed, lexicon-kind plus other, per the SC-003 exception of 27/11/2026;
- mean cost per run is at most 5% above the base arm;
- in every WS and MS run that reads a card, the card is the expected one, and no run reads a wrong card;
- the card-read rate per model and arm is recorded beside it.

## 4. Record

Write the counts to `docs/benchmarks.md` with the fields listed in [data-model.md](data-model.md) "Benchmark record".
