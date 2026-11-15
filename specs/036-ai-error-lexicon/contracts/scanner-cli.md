# Contract: `scripts/scan-lexicon.py`

## Interface

```text
python3 -I <skill-dir>/scripts/scan-lexicon.py [--help]  < text
```

- **Input**: the text to scan on standard input, UTF-8, optional BOM. Nothing on the command line except `--help`. Any other argument exits 2.
- **Lexicon**: `<skill-dir>/references/ai-error-lexicon.md`, found relative to the script file. The only file the script opens.
- **Output** (stdout, exit 0), one JSON object, UTF-8, `ensure_ascii=False`:

```json
{
  "schema": 1,
  "lexicon_sha256": "<first 12 hex of the lexicon file's SHA-256>",
  "candidates": [
    {"entry": "L01", "text": "rườm", "line": 3, "column": 41, "paragraph": 2, "zone": null}
  ]
}
```

Candidates are ordered by position, then by entry id. Overlapping matches of different entries are all reported.

- **Exit codes**: 0 scanned (with or without candidates); 2 bad input (argument other than `--help`, empty input, invalid UTF-8, more than 1,000,000 bytes); 3 lexicon missing or malformed. On 2 or 3 one line goes to stderr, nothing to stdout.
- **Runtime**: Python 3.9+, standard library only; no environment variable is read; `-I` keeps the current directory and user site packages out of the import path.

## Invocation by the agent

- Text in a file the user named: `python3 -I "<skill-dir>/scripts/scan-lexicon.py" < "<path>"`, the path quoted as the host's shell requires.
- Pasted text: a quoted here-document with a random delimiter of 32 hex characters, generated per call and checked absent from the text:

```text
python3 -I "<skill-dir>/scripts/scan-lexicon.py" <<'VNZ_<32hex>'
<text>
VNZ_<32hex>
```

The quoted delimiter stops expansion; the absence check stops the text from closing the document early. The agent never puts the text in an argument, an `echo`, or an unquoted here-document.

- Any failure (no Python, no shell tool, permission refused, non-zero exit, unparsable JSON, more than 20 s) means the reading path; the agent does not retry more than once, does not ask the user to enable or install anything, and says nothing about the path unless asked (FR-014).

## Principle V mapping (2.9.0 text)

| Condition | How the scanner meets it | Test |
|---|---|---|
| Skill works without the script | Reading path in the skill text; package built without `scripts/` still edits | `test_skill_contract` phrase guard; SC-003 run |
| Standard library only | Imports limited to an allow-list | Test parses the AST and rejects any other import |
| No network | No `socket`, `urllib`, `http`, `ssl`, `subprocess` import | Same AST test |
| No secret or API key | No `os.environ` / `os.getenv` access | AST test rejects attribute access to `environ`, `getenv` |
| No file write | No `open(..., "w"/"a"/"x")`, no `pathlib` write methods, no `tempfile`, `shutil` | AST test; runs under a read-only temp dir in the test |
| Reads only the task text and package data | stdin plus the one lexicon path | Test with `sys.argv` paths rejected; lexicon path fixed |
| Prints candidates only, agent decides | Output schema has no fix field applied to text; the script never echoes the edited text | Output schema test |
