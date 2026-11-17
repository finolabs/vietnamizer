# Quickstart: development loop, gate and holdout batch

Everything here runs one heavy job at a time, `uptime` first; no command reads `artifacts/holdout-036/` unless you are the runner.

## 1. Development pool (once)

1. A fresh agent that edits no skill file generates D01–D10 per research.md R5 into `artifacts/dev-037/` and writes `Dnn.sheet.md` proposals per spec 036 `contracts/holdout-marking-sheet.md`, each row noted "AI đề xuất".
2. Fio reviews each sheet:

   ```bash
   python3 benchmarks/holdout_marker.py artifacts/dev-037
   ```

3. Commit the manifest:

   ```bash
   python3 benchmarks/holdout_036.py manifest artifacts/dev-037 > benchmarks/dev-037-manifest.json
   ```

## 2. Iterate on the tuning articles

Edit D01–D03 and D06–D08 with the plugin installed from the worktree on Claude Code (Opus 5.5, Sonnet 5.5), write their `runs.json` and score:

```bash
python3 benchmarks/holdout_036.py score artifacts/dev-037/runs.json
```

Read the outputs and sheets of the tuning articles only. Never open D04–D05 or D09–D10 while writing tests.

## 3. Gate (plan P3)

Run 0.16.2 and the candidate on D04–D05 and D09–D10 on Cowork, score, and compare with P3. Fail: back to step 2. Pass: record the candidate commit (freeze).

## 4. Holdout batch (runner only)

The runner generates H15–H20 with Gemini after the freeze, Fio marks them, then the runner runs H01–H14 and H15–H20 with both versions on Cowork, scores with `holdout_036.py score`, collects Fio's judgments with `holdout_036.py edits`, and returns contracts/holdout-report.md.
