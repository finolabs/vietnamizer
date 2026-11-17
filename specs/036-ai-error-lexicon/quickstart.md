# Quickstart: validating spec 036

Run from the repository root. Check `uptime` first and run one test module per command (owner rule). Commands below are the targets the implementation must satisfy; they fail until the matching step of plan "Delivery order" lands.

## 1. Lexicon and scanner (deterministic; SC-001, FR-005, FR-017)

```bash
python3 -m unittest tests.test_scan_lexicon
```

Expected: every fixture returns exactly its expected candidates; table structure checks pass; refusal cases exit 2 or 3; the AST allow-list test passes.

```bash
printf 'Quy trình còn rườm và dễ làm nhân viên mới bỡ.\n' | python3 -I scripts/scan-lexicon.py
```

Expected: two candidates, `L01` *rườm* and `L02` *bỡ*.

```bash
printf 'Quy trình rườm rà làm nhân viên bỡ ngỡ.\n' | python3 -I scripts/scan-lexicon.py
```

Expected: `"candidates": []` (lexical guard).

## 2. Package (FR-021, development gate 5)

```bash
python3 -m unittest tests.test_package_security
```

```bash
python3 scripts/validate-package.py
```

```bash
bash scripts/package-skill.sh
```

Expected: both archives list `scripts/scan-lexicon.py` and `references/ai-error-lexicon.md`, and no other file under `scripts/`.

## 3. Skill text (FR-006–FR-016, FR-019)

```bash
python3 -m unittest tests.test_skill_contract
```

Expected: the guards of contracts/skill-text.md pass.

## 4. Agent runs (by hand; SC-002, SC-003, SC-004, SC-006)

1. Block LX and HF01–HF18 on Claude Code with the scanner, then with `scripts/` removed from a copy of the installed skill; record per fixture the candidate set from the shown inventory and the output. Development result only.
2. The same fixtures on Claude.ai with the test package built without `scripts/` (plan P8), and once with the full package.
3. Live probes per host (research.md R1 protocol).
4. Record every difference with fixture, host, model id and date in `docs/benchmarks.md`; a release needs no difference or Fio's written acceptance of each (FR-018).

## 5. Holdout (SC-005)

After Fio marks the 20 articles (contracts/holdout-marking-sheet.md), run `benchmarks/holdout_036.py` for each model under plan P2 and O6, both versions, then review the out-of-span list. The report goes to `docs/benchmarks.md` with model ids, corpus manifest hash, lexicon hash and package versions.
