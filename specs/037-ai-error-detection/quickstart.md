# Quickstart: development loop, gate and holdout batch

Everything here runs one heavy job at a time, `uptime` first; no command reads `artifacts/holdout-036/` unless you are the runner.

## 1. Development pool (once)

1. A fresh agent that edits no skill file generates D01–D10 per research.md R5 into `artifacts/dev-037/articles/` and writes `Dnn.sheet.md` proposals per spec 036 `contracts/holdout-marking-sheet.md`, each row noted "AI đề xuất".
2. Fio, or a marker Fio shares the marking page with, reviews each sheet (decision 5). Locally:

   ```bash
   python3 benchmarks/holdout_marker.py artifacts/dev-037/articles
   ```

   On the shared claude.ai marking page, every row is saved to the page's store; read the store back and write the sheets through `holdout_marker.build_sheet` before the manifest. The page and its export script stay outside Git with the articles.

3. Commit the manifest:

   ```bash
   python3 benchmarks/holdout_036.py manifest artifacts/dev-037/articles > benchmarks/dev-037-manifest.json
   ```

## 2. Iterate on the tuning articles

Edit D01–D03 and D06–D08 with the plugin installed from the worktree on Claude Code (Opus 5.5, Sonnet 5.5), write their `runs.json` and score:

```bash
python3 benchmarks/holdout_036.py score artifacts/dev-037/articles/runs.json
```

Read the outputs and sheets of the tuning articles only. Since decision 8 these are D01–D10; never open D11–D34 while writing tests.

## 3. Gate (plan P3)

Run 0.16.2 and the candidate on the gate pool D11–D34 on Claude Code `-p` (decision 8; Fio, 21/11/2026), two runs per model per article, score, and compare with P3. Fail: back to step 2. Pass: record the candidate commit (freeze).

## 4. Holdout batch (runner only)

Not run: decision 3 as amended on 25/11/2026 skipped the holdout, and the spec stopped on 26/11/2026. The steps below are the original design.

The runner generates H15–H20 with Gemini after the freeze, Fio marks them, then the runner runs H01–H14 and H15–H20 with both versions on Cowork, scores with `holdout_036.py score`, collects Fio's judgments with `holdout_036.py edits`, and returns contracts/holdout-report.md.
