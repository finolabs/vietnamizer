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

Candidates are ordered by position, then by entry id. Overlapping matches of different entries are all reported; the agent merges them into one inventory row (data-model "Inventory row").

- **Exit codes**: 0 scanned (with or without candidates); 2 bad input (argument other than `--help`, empty input, invalid UTF-8, more than 1,000,000 bytes); 3 lexicon missing or malformed. On 2 or 3 one line goes to stderr, nothing to stdout.
- **Runtime**: Python 3.9+, standard library only; no environment variable is read; `-I` keeps the current directory and user site packages out of the import path.

## Invocation by the agent

Every path in the command is wrapped in POSIX single quotes, with each `'` inside the path written as `'\''`. Double quotes are never used for a path or for text: they still expand `$(…)`, backticks and `$VAR`.

1. **Text already in a file the user named**: `python3 -I '<skill-dir>/scripts/scan-lexicon.py' < '<path>'`.
2. **Pasted text, host has a file-write tool** (Claude Code, Codex, Antigravity, Chat and Cowork sandboxes): write the text unchanged with that tool, never through the shell, to a new file in the host's own scratch or temp folder, run form 1 on it, then delete the file. This is the default for pasted text, because no shell ever parses the text.
3. **Pasted text, no file-write tool, text at most 100,000 bytes**: a single-quoted here-document with the fixed delimiter `VNZ_END_OF_TEXT_036`, used only when no line of the text equals the delimiter; otherwise the reading path.

```text
python3 -I '<skill-dir>/scripts/scan-lexicon.py' <<'VNZ_END_OF_TEXT_036'
<text>
VNZ_END_OF_TEXT_036
```

A fixed delimiter with an exact-line absence check replaces a "random" one: a model asked for randomness may copy a template value, and the attack (a line equal to the delimiter) is exactly what the check refuses. The 100,000-byte bound keeps the command under the host's argument size limit (`ARG_MAX` is 1 MiB on macOS), since a tool call passes the command string as an argument. Above it, form 2 or the reading path.

The agent never puts the text in an argument, an `echo`, a double-quoted string or an unquoted here-document.

- Any failure (no Python, no shell tool, permission refused, non-zero exit, unparsable JSON, more than 20 s) means the reading path; the agent does not retry more than once, does not ask the user to enable or install anything, and says nothing about the path unless asked (FR-014).

## Principle V mapping (2.9.0 text)

| Condition | How the scanner meets it | Test |
|---|---|---|
| Skill works without the script | Reading path in the skill text; package built without `scripts/` still edits | `test_skill_contract` phrase guard; SC-003 run |
| Standard library only | Imports limited to the closed set `__future__`, `argparse`, `hashlib`, `json`, `pathlib`, `re`, `sys`, `unicodedata` | Test parses the AST and rejects any other import, including `os`, `io`, `importlib`, `builtins` and dynamic `__import__` |
| No network | No `socket`, `urllib`, `http`, `ssl`, `subprocess` import | Same AST test |
| No secret or API key | No `os.environ` / `os.getenv` access | AST test rejects attribute access to `environ`, `getenv` |
| No file write | No `open` call except the lexicon read in mode `"r"` or `"rb"`; no `pathlib` write, `unlink`, `rename`, `mkdir` or `touch` methods; no `tempfile` or `shutil` | AST test; runs under a read-only temp dir in the test |
| Reads only the task text and package data | stdin plus the one lexicon path | Test with `sys.argv` paths rejected; lexicon path fixed |
| Prints candidates only, agent decides | Output schema has no fix field applied to text; the script never echoes the edited text | Output schema test |
