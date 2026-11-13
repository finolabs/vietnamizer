# Quickstart: validating spec 030

Prerequisites: a checkout with the implementation, Claude Code with the plugin installed from that checkout (`claude plugin install` from the local path or a fresh session reading the folder), optionally a browser tool and a test LinkedIn/Facebook export with synthetic content.

## Package checks

```bash
python3 -B scripts/validate-package.py
python3 -B -m unittest tests.test_skill_contract tests.test_distribution
claude plugin validate .
npx --yes skills@1.5.20 add . --list
```

Expected: package valid; tests pass; the plugin lists `vietnamizer` and `help`; the skills CLI lists the root skill.

## Behaviour walk-through (manual, cases VM01–VM16 in `calibration/test-cases.md`)

1. Run `/vietnamizer:help`: one-screen overview, no file read, offer to start (contract help-onboarding).
2. Accept, pick Cá nhân → Dán bài, paste 12 synthetic posts, consent: a full draft profile with `kind` absent or `personal`.
3. Choose 3 paragraphs; rate Tốt, Kém, Khá: one reason question for the Kém paragraph, a proposed diff, nothing written.
4. Save to a temporary folder outside any git tree: the file ends with one `Lịch sử chấm` line with counts 1/1/0/1 and the fixed label.
5. Brand: pick Thương hiệu, state authority, give a 5-line guide and 10 posts with one post breaking a rule: `Quy tắc thương hiệu` lists guide rules; the conflict appears in `Điểm chưa quyết`; no names.
6. Export: give a synthetic LinkedIn export with own posts, reshares and others' comments: kept and dropped counts reported; only own posts cited.
7. Browser (if available): name a page without stating ownership → the skill asks and reads nothing; on LinkedIn, the terms warning appears before any read.
8. Edit a draft naming both profiles: the skill asks which one.

Results are manual evidence only; record them in the PR, not as quality claims.
