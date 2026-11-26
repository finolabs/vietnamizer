# Research: Cut the token cost of each edit

## R1. Where the money goes

**Finding**: Most of the cost is new text entering the context, not the number of turns.

A least-squares fit of `costUSD` over the 48 T035 0.16.2 runs per model gives these prices per million tokens and cost shares:

| Model | Cache read | Cache write (1 h) | Output | Share: read / write / output |
|---|---|---|---|---|
| Opus 5.5 | $0.20 | $8.00 | $20.00 | 5% / 64% / 31% |
| Sonnet 5.5 | $0.10 | $4.00 | $10.00 | 5% / 66% / 29% |

A cache write is every new block that enters the context: the prompt with the article, each file the agent reads, and each of its own earlier outputs that the next turn carries. Re-reading cached context costs almost nothing.

**Decision**: Measure and cut new context, meaning the bytes of skill text read and the text the agent writes between tool calls. Do not optimise for the turn count by itself.

**Rationale**: Cutting a turn saves only its re-read (5% of cost) unless the turn also brings in a file or produces text.

**Alternatives considered**: Count only bytes read. Rejected, because output is 30% of the cost and each intermediate turn's text is written to the cache again.

## R2. What one run reads today (probe, 26/11/2026)

One Claude Code `-p` run per model on D02 (a development article) with the 0.16.2 ZIP, logged with `--output-format stream-json`:

| Model | Cost | Turns | Cache write | Cache read | Output | Reads |
|---|---|---|---|---|---|---|
| Opus | $0.327 | 6 | 22.0k | 180k | 5.7k | Skill load (`SKILL.md`), `writing-workflow.md`, card `public-expertise.md`, a Grep into `missing-words.md` |
| Sonnet | $0.109 | 3 | 13.2k | 75k | 4.8k | Skill load only |

The first call writes about 5.9k tokens (prompt, article and skill listing) and reads about 35k cached tokens: the host's system prompt and tools, plus the runner's `CLAUDE.md`. That part is fixed, cheap and outside the skill.

On Opus, the skill-driven writes are about 16k tokens after the first call. They are `SKILL.md` (14 KB), the workflow, the card, the grep result, and the agent's own text between turns.

**Decision**: The levers, in expected order of saving:
1. Shrink `SKILL.md`. Every run loads it in full through the Skill tool.
2. Make the whole-article route read fewer and smaller files.
3. Cut text the agent writes between tool calls. For example, tell it to read what the route needs in one step, then write the article once.

**Feasibility**: SC-001 asks for 25%, about $0.08 per Opus run. Saving half of the Opus skill-driven writes (about 8k tokens at $8/M) gives about $0.064, or 20%. A further 1k of output gives about $0.02. 25% is reachable but tight. The plan therefore puts an early check on D01–D10 (P4) before any gate run.

## R3. Other installs leak into the runs

**Finding**: The runner's machine also has `vietnamizer@finolabs` installed as a user plugin. In a probe run without `--plugin-dir`, the agent still found and used a Vietnamizer skill; one model even globbed the repository's main checkout. With `--plugin-dir`, the probe runs read only from the ZIP's install path. T035 did not log reads, so it cannot show which install each of its runs used.

**Decision**: Every spec 038 run logs `stream-json`. A run is valid only when every skill load and read comes from its own ZIP's install path. 0.16.2 runs again in the same batch as the candidate (spec Assumptions: rerun when the host or the setup changes), instead of reusing the T035 runs.

**Rationale**: The baseline must be clean as well. It costs 96 more runs, about $24 and about 30 minutes with three workers.

**Alternatives considered**: Reuse the T035 0.16.2 runs. Rejected, because they cannot be shown clean.

## R4. Which text can leave the always-loaded part

`SKILL.md` sections in 0.16.2, in bytes:

| Section | Bytes |
|---|---|
| Front matter and intro | about 900 |
| Trước khi làm | 1,778 |
| Chọn đúng tuyến đọc | 4,822 |
| Chọn card khi làm bài | 1,271 |
| Năm chốt giữ mọi lúc | 3,021 |
| Làm và kiểm lại | 630 |
| Trả kết quả | 2,007 |

**Decision**:
- Keep in `SKILL.md`: the scope, the data boundary and frozen zones, the five gates and a routing table that only names files. These apply to every task.
- Move route-specific text to the file that route already reads: the long per-row read lists, the card table (whole-article and writing routes only) and the return-format details of rare routes.
- Write the routing rows as short pointers.
- Target: always-loaded text at most 10 KB, which is SC-005's 30% cut.

**Alternatives considered**:
- Drop the five gates from `SKILL.md`. Rejected: they guard every route.
- Merge catalogs. Rejected: one owner per rule is a core rule.

## R5. Large references

`voice-profile.md` (41 KB) mixes learning, saving, applying and updating a profile. `voice-sources.md` (20 KB) covers three sources.

**Decision**: Split `voice-profile.md` by task (learn, apply, update, registry) behind a short index, so applying a saved profile reads only the apply part. Leave the catalogs whole in this spec: a whole-article route reads a catalog only when it suspects a pattern, and a short edit reads one catalog.

**Alternatives considered**: Split the catalogs by pattern. Deferred: it adds many files for a small saving, since the probe read at most one catalog, through a grep.

## R6. Bytes-per-route check

**Decision**: Add a repository check, `scripts/route_budget.py`, run from the test suite. It is not in the package. It reads the routing table of `SKILL.md`, resolves the files each row names, sums their bytes plus `SKILL.md`, and compares each sum with `benchmarks/route-budget.json`. It fails when a route exceeds its budget.

**Rationale**: It keeps the saving after this spec ends (User Story 3). It is a proxy: a route read at run time can differ from the table, which is why P4 and P5 log real reads.
