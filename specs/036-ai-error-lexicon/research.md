# Research: AI-error lexicon, phrase inventory and optional scanner

**Date**: 2026-11-15. Sources were read on this date; host behaviour changes often, so each live probe below records its own date.

## R1. Which hosts can run a script shipped in the skill (O3)

**Decision**: the scanner path covers Claude Code, Codex, Antigravity, Claude.ai Chat and Claude Org uploads (skills there always run with code execution), and Cowork. Claude.ai, in its "Claude" mode (page radio value `cowork`), was confirmed by a live probe on 15/11/2026; Codex and Antigravity still need theirs before the parity run, and every host repeats the probe with the real 0.17.0 package. The reading path is the baseline everywhere and the only path on ChatGPT surfaces that receive Codex plugin skills, and on any host where a probe fails.

| Host | What the documentation says | Local evidence | Scanner path | Live probe still needed |
|---|---|---|---|---|
| Claude Code (CLI, desktop) | Skills may bundle scripts; the skill's base directory is given when the skill loads | This session received "Base directory for this skill: …" on skill load; plugin copies of Vietnamizer under `~/.claude/plugins/cache/` | Yes, through Bash; a permission prompt may appear, and a refusal means the reading path | Run `scripts/scan-lexicon.py --help` from the installed plugin copy |
| Codex (CLI, app) | A skill folder may hold an optional `scripts/` with executable code; skills load from `.agents/skills`, `~/.agents/skills` and plugins. "Prefer instructions over scripts unless you need deterministic behavior" | Fiomac config `sandbox_mode = "workspace-write"`, `approval_policy = "on-request"` | Yes, inside its sandbox; reading package files outside the workspace is allowed by the read-only default, unverified for plugin installs | After quota returns (17/11/2026 10:16) |
| ChatGPT Chat/Work receiving Codex plugin skills | "Skills bundled in plugins are also available in Chat and Work across ChatGPT" | none | No evidence of code execution with skill files; reading path | Optional; out of the parity set |
| Antigravity (App, CLI, IDE) | Skills may include "helper scripts … the agent can execute" in `scripts/`; advice to run them with `--help` first; plugin skills at `~/.gemini/config/plugins/<plugin>/skills/` | `~/.gemini/config/plugins/vietnamizer` exists | Yes, through its terminal tool, subject to its terminal policy | With `gemini-3.8-flash-high` (Argon out of quota) |
| Claude.ai Chat (web, desktop, mobile) and Claude Org upload | "Skills require the code execution environment to function"; Team and Enterprise need both "Code execution and file creation" and "Skills" on | **Live probe 15/11/2026** (main coordinator session, on Fio's go): a throwaway skill `o3-probe` uploaded to Fio's account, run in a new session with Sonnet 5.5. Its bundled Python script ran on a here-document with no permission prompt, received Vietnamese stdin intact (NFC, first word *Đội*), and read a data file shipped in the same skill. Linux VM, Python 3.13.18, skills synced under `/root/.claude/skills/synced/…`. No mode without code execution was offered | Yes, confirmed. A Chat with code execution off has no skills, so Vietnamizer reaches it only as text the user pastes or adds to a Project, where only the reading path exists | Only the per-release probe with the 0.17.0 package |
| Cowork | Runs in a sandboxed Linux VM on the user's machine with code execution; skills and plugins load there (third-party guides; Anthropic's page names Cowork only for sharing) | **Same live probe, 15/11/2026**: claude.ai's selected "Claude" mode carries the radio value `cowork` in the page and showed the connected desktop and a permission mode, so the run above is a Cowork session | Yes, confirmed for Cowork reached through claude.ai's "Claude" mode; Python 3.13.18 present and package data readable | Only the per-release probe with the 0.17.0 package |

**Consequences for the spec**: US1's "Claude.ai Chat with no code execution" is reachable only through pasted or Project text, not an installed skill. The reading path still matters there and on every host where Python, the shell or a permission is missing. SC-002's "Chat or Cowork host without code execution" is exercised with a test package without `scripts/` uploaded to Claude.ai (plan P8).

**Alternatives considered**: covering only Claude Code (rejected, Fio's input names cloud Chat and Cowork); relying on documentation without probes (rejected, two of the five rows rest on third-party guides).

Sources: [Using Skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude), [Build skills (Codex)](https://learn.chatgpt.com/docs/build-skills.md), [Antigravity agent skills](https://antigravity.google/docs/skills.md), [Cowork features overview (third-party)](https://fast.io/resources/claude-cowork-features-overview/).

### Live probe protocol (each host)

1. Install the 0.17.0 candidate package as that host installs it.
2. Ask: "Chạy `scripts/scan-lexicon.py --help` của skill Vietnamizer và cho tao xem kết quả." Record whether it ran, the Python version and any permission prompt.
3. Run fixture `LXF01` through the scanner with the here-document form; compare the JSON with `tests/fixtures/lexicon/fixtures.json`.
4. Record host, host version, model id, date and result in `docs/benchmarks.md` (parity section). A failure is not a bug to fix in the host; the host is then covered by the reading path only.

## R2. Matching on Vietnamese syllables

**Decision**: normalise the input to NFC, map U+00AD (soft hyphen) and zero-width characters to nothing and any run of whitespace inside a paragraph (line breaks included) to one space, keeping an offset map back to the original text. Tokenise syllables with `[^\W\d_]+` (as `scripts/check-consistency.py` does). An entry form is a sequence of one to four syllables; it matches when the same sequence occurs with `str.casefold()` equality (unless the entry's case column says `đầu câu`: data-model "Sentence start", which also covers list items, blockquotes, headings and clauses after `:`, `;` or `—`), the syllable after the match is not in the entry's "Sau không là" list and the one before is not in "Trước không là".

**Rationale**: Vietnamese words are syllable sequences separated by spaces, so syllable boundaries are word-safe without segmentation: *rườm* never matches inside *rườmrà* (not a word) and the completing neighbour *rà* is excluded by the list. NFC plus casefold handles NFD input, combining marks typed separately and *Đội* vs *đội* (casefold maps Đ to đ).

**Alternatives considered**: plain substring search (no syllable boundary, so *bỡ* would match inside *bỡn*, and no neighbour lists); a POS tagger (out of scope, needs libraries outside the standard library).

## R3. Payload layout for the scanner (P3)

**Decision**: source file `scripts/scan-lexicon.py`; the staged payload and both archives hold `scripts/scan-lexicon.py` and nothing else under `scripts/`. `validate-package.py` adds `scripts` to the payload roots with `EXACT_DIRECTORY_FILES["scripts"] = {"scripts/scan-lexicon.py"}` for staged payloads and archives only; in a source checkout `scripts/` is the maintainer folder and only the scanner file is required to exist. `package-skill.sh` copies that one file, and the validator's static check of that script (`copied_payload != PACKAGE_COPY_SOURCES`, `validate-package.py` line 601 at `d2b21e0`) learns that the `scripts` payload root is satisfied by the file-level source `scripts/scan-lexicon.py`, so a `cp` of the whole `scripts/` folder still fails. The plugin adapter resolves `scripts/` from the plugin root like `profiles/` and `references/`. Inside the skill the scanner sits at `scripts/scan-lexicon.py` relative to the skill directory in every layout (repo root, `vietnamizer/` archive root, Org upload root, `skills/vietnamizer/` in the plugin ZIP).

**Rationale**: Fio chose the standard layout (P3). Agent Skills and the `plugin-packaging` skill put executables in `scripts/` beside the skill; a hyphenated name matches the repo's other scripts.

**Alternatives considered**: a new `tools/` folder (no packaging exception, but off-convention); moving maintainer scripts elsewhere (an unrequested refactor touching CI, docs and contributors' habits).

## R4. Input, output and failure

**Decision**: text only on stdin, UTF-8 (BOM stripped); cap 1,000,000 bytes, read as `sys.stdin.buffer.read(1_000_001)`; over the cap, invalid UTF-8 or empty input exit 2 with one line on stderr. The lexicon is read from `../references/ai-error-lexicon.md` relative to the script file; a missing or malformed table exits 3. Output is one JSON object on stdout (contracts/scanner-cli.md). Exit 0 whether or not candidates exist. No other option than `--help`.

**Rationale**: stdin keeps the text out of argv and shell history (P6); a fixed lexicon path means the script opens exactly one file, the one Principle V allows. A cap of 1 MB is about 150,000 words, far above an article, so it only stops misuse.

**Alternatives considered**: a `--lexicon` path option for tests (rejected: tests import the module and call `scan(text, entries)` directly); exit 1 on candidates like a linter (rejected: candidates are not errors).

## R5. Protected zones

**Decision** (amended 17/11/2026, spec decision 7): the scanner drops every match inside `frontmatter` (a leading `---` block), `code` (fenced block or inline backticks), `link-url` (the target of `[text](url)` or an autolink), `quote` (inside “…” or "…" on one paragraph) or `blockquote` (a `>` line), and reports the rest without a zone field. The 15/11 decision reported every match with a `zone` hint and dropped nothing; the rationale below explains why the agent still reads quoted emphasis and blockquotes itself.

**Rationale**: SKILL.md freezes code, frontmatter, link addresses and verbatim quotations, but also says a term put in quotes for emphasis is not a quotation, which only the agent can tell. Reporting the zone keeps the scanner deterministic and leaves the judgment where Principle II puts it. `zone` is a hint, not a verdict: only `frontmatter`, `code` and `link-url` are always frozen; `quote` is frozen when verbatim, and `blockquote` marks structure (callouts, notes) and is judged like ordinary prose unless it is a quotation (data-model "Zone semantics"). This reads the spec's edge case "quotation" as verbatim quotation, not every quote mark or `>` line.

**Alternatives considered**: dropping matches in zones (hides quoted emphasis that should be edited); flagging link text as protected (link text is prose; only the address is frozen).

## R6. Holdout for the release proof (O2)

**Decision**: 20 fresh AI articles (P1), 800–1,500 words, prose genres that get V patterns, four articles in each of five genres: personal blog, expertise post (LinkedIn style), product or marketing copy, guide or README prose, operations report. Generators rotate across Claude, GPT and Gemini (7, 7, 6; GPT articles wait for Codex quota or come from another GPT surface Fio uses). Amended 17/11/2026 (Fio, "dời qua phiên bản sau"): the 0.17.0 proof uses the 14 Claude and GPT articles H01–H14 (three per genre, two operations reports); the six Gemini articles H15–H20 move to the next version's holdout, because the Gemini pools are out until 21/11/2026. Topics come from Fio's domains (retail, fashion, supply chain, SaaS). Prompts ask for an article, never for errors. Articles are generated after the lexicon and skill text for 0.17.0 are frozen, stored outside Git under the benchmark's local raw folder with a SHA-256 manifest committed, and not shown to any agent that edits the lexicon.

Fio marks each article with the sheet in contracts/holdout-marking-sheet.md before any run over it. Every model available under P2/O6 runs 0.16.2 and 0.17.0 once per article (up to 5 × 2 × 14 = 140 outputs for 0.17.0), same prompt and settings, outputs labelled A/B at random. `benchmarks/holdout_036.py` scores deterministically after NFC-normalising the sheet, the article and every output: every source sentence is aligned one-to-one, in order, to output sentences with `difflib`; each aligned pair is diffed by token with character offsets; the error counts as fixed when the diff changes the marked span and an accepted fix appears at the span's place; a guard counts as broken when any character of its span changes (rules in contracts/holdout-marking-sheet.md "What counts"). Edits outside marked spans are listed for Fio to judge blind to the A/B label. Reported per model: recall on lexicon-kind errors and on other marked errors, guard breaks, judged over-corrections, time and tokens per article, model id, corpus manifest hash, lexicon hash, package version.

**Marking (17/11/2026)**: Fio marked H01 alone with `benchmarks/holdout_marker.py`. For H02–H14 a fresh Claude agent (`claude-opus-5-5`) that had not edited the lexicon and loaded no Vietnamizer file or skill proposed rows from Fio's H01 sheet and the contract, noted "AI đề xuất"; it recalibrated twice on Fio's corrections of H02 and H03–H05. Fio reviewed every article, corrected and added rows where needed, and set each sheet to `xong`. Not used: pre-marking with Vietnamizer itself, which would bias the labels toward what the system under test already finds. Labels can still miss errors neither the agent nor Fio saw; that miss applies to 0.16.2 and 0.17.0 alike.

**Rationale**: about 3–6 marked errors per article gives roughly 36–72 errors at 12 articles and 60–120 at 20, enough that one unusual article does not decide the comparison; the 14 articles of the 0.17.0 proof give about 42–84, still more than the 12-article proposal. Deterministic span scoring keeps Fio's effort to the marking and the out-of-span edits.

**Alternatives considered**: 12 articles (Fio chose 20); re-marking the 0.11.0 public sources (spec decision 3 rejects it); LLM judging of fixes (no; Fio's marks are the label).
