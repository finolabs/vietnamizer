# Quickstart: measure and gate spec 038

Prerequisites:
- PR 95 is merged, so the package text equals 0.16.2.
- The Claude Code CLI is logged in.
- Load is at or below 25.
- One heavy job at a time.

1. **Build the two packages.**
   - `python3 scripts/package-plugin.py` on the candidate commit.
   - Copy `dist/vietnamizer-plugin.zip` to `.finolabs/harness-038/cand-<sha>.zip`.
   - The 0.16.2 package is the existing `v0162.zip`, built from tag `v0.16.2`.
2. **Check the budgets.** Run `python3 scripts/route_budget.py`. Every route must be within budget, and the whole-article route below its 0.16.2 bytes.
3. **Early check (P4).**
   - Run the harness on D01–D10 with both versions, two runs per model per article.
   - The harness discards and reruns invalid runs (contract [run-record](contracts/run-record.md)).
   - Compare mean cost per model. Under a 15% saving for a model: stop and report to Fio.
4. **Manual route cases (P5).** Run RB01–RB08 from `calibration/test-cases.md` once per model per version. Record pass or fail and the bytes read.
5. **Gate (P6).**
   - Run the harness on D11–D34 with both versions in one batch, two runs per model per article.
   - Score with `python3 benchmarks/holdout_036.py score <index>`.
   - Pass when, for each model:
     - mean cost is at least 25% lower;
     - mean time is lower;
     - lexicon-kind fixes, other fixes and guard breaks are within 2 of 0.16.2.
6. **Report.** Put the counts in `docs/benchmarks.md`: model ids, host, date, manifest hash and package commits.
