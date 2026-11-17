# Contract: holdout report the runner returns (counts only)

The runner (plan P7) is a session that edits no skill text, rule, lexicon, calibration or test file. It runs the batch, scores it with `benchmarks/holdout_036.py`, gets Fio's blind judgments of out-of-span edits, and returns only the table below. No sentence, span, row id or article excerpt leaves the runner; the maintainer and every agent that edits the skill see this table and nothing else.

## Header

```text
Batch: <date>   Host: Claude Cowork   Runner session: <id>   Runner edited no skill file: yes
Corpus manifest SHA-256: <hex> (H01–H14) / <hex> (H15–H20)
Prompt: T044 prompt, unchanged   Outputs per article, version and model: 1   Labels: random
Version A: 0.16.2 (tag v0.16.2)   Version B: candidate <commit>
```

## Table (one row per holdout, model and version)

| Holdout | Model id | Version | Lexicon-kind fixed / 33 (H01–H14) or / n | of which calques / clipped / collective | Other errors fixed / n | Guards broken | Out-of-span `sai` | Out-of-span `không cần` | Runs with detection pass seen | Median seconds | Median tokens |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Verdict lines

- Bar (spec FR-014): Opus ≥ 17, Sonnet ≥ 11, guards and `sai` ≤ 0.16.2 per model → `đạt` or `không đạt`, with the numbers.
- H15–H20 (FR-015): reported, no verdict; a gap of more than 15 percentage points in lexicon-kind recall between the two holdouts is named.
- Models not run and why.
