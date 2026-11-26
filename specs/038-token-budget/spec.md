# Feature Specification: Cut the token cost of each edit

**Feature Branch**: `spec/038-token-budget`

**Created**: 2026-11-26

**Status**: Planned ([plan.md](plan.md)); tasks in [tasks.md](tasks.md); not implemented

**Input**: Fio, 26/11/2026, choosing between two directions for the next Vietnamizer version ("Token trước"). Make each edit cost fewer tokens and less time without losing quality, so the skill works well on Claude Cowork and cloud hosts, which run no local scripts. Voice-profile storage on Cowork and cloud is a later spec, 039. This spec depends on PR 95, which puts the package back to the 0.16.2 text; it starts from that text.

## Clarifications

### Session 2026-11-26

- Q: How much worse than 0.16.2 may the candidate be on D11–D34 and still pass? → A: At most 2 per count, per model (Fio: "Lệch tối đa 2").

## Background: what an edit costs today

The package has held only Markdown since 0.14.0, so it already runs on hosts without local scripts. Its cost comes from what the agent reads on each run.

`SKILL.md` is 14 KB and loads on every run. A whole-article edit also reads the workflow, one style card and the catalogs it suspects: 12–18 KB each for `missing-words.md`, `sentence-structure.md`, `sino-vietnamese.md` and `typography.md`. The voice-profile route reads `voice-profile.md`, which is 41 KB.

Measured cost of 0.16.2 in T035 (spec 037), per run, on the gate pool D11–D34: 24 articles, two runs per model per article, Claude Code `-p`, the same edit prompt every time.

| Model | Cost per run | Tokens per run | Time per run | Tool turns | Lexicon-kind fixed | Other fixed | Guards broken |
|---|---|---|---|---|---|---|---|
| Opus 5.5 | $0.35 | 167k | 54 s | 5.3 | 13/70 | 12/50 | 20/256 |
| Sonnet 5.5 | $0.15 | 105k | 33 s | 3.3 | 3/70 | 10/50 | 18/256 |

Spec 037 showed the other direction: making the agent read five files and check every sentence raised the cost per run by 87% (Opus) and 108% (Sonnet) with no net gain.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Whole-article edits cost less (Priority: P1)

A user asks Vietnamizer to edit a whole article: a blog post, a LinkedIn post, a README or a report. They get the same quality of edit as 0.16.2 for clearly less money and time per edit. This matters most on Cowork and in cloud sessions, where every run is metered and nothing is cached on the user's machine.

**Why this priority**: Whole-article editing is the most common use and the one the existing gate pool measures. It is where the read cost is highest.

**Independent Test**: Run the candidate on D11–D34 with the T035 prompt and settings, two runs per model per article. Compare cost, tokens, time, fixes and guard breaks with the T035 0.16.2 runs.

**Acceptance Scenarios**:

1. **Given** the D11–D34 pool and the T035 prompt, **When** the candidate edits each article twice per model, **Then** the mean cost per run is at least 25% lower than 0.16.2 for Opus 5.5 and for Sonnet 5.5.
2. **Given** the same runs, **When** they are scored with the existing scorer, **Then** fixes and guard breaks per model stay within the quality tolerance in FR-004.
3. **Given** a short edit (one phrase or sentence), **When** the user asks for it, **Then** the agent still reads only the catalog of the suspected pattern, as in 0.16.2, and reads no more than before.

---

### User Story 2 - Other routes keep working at lower cost (Priority: P2)

A user writes from a brief, follows a sample, learns or applies a voice profile, or asks for help. Each route behaves as it does in 0.16.2. Where the route reads a large file, it reads only the part it needs.

**Why this priority**: The gate pool does not measure these routes. Splitting files to save tokens can quietly break them, so they need their own proof.

**Independent Test**: The skill contract tests pass unchanged, or changed only to follow moved text. A small set of manual cases, one per route, is run once per model, and the agent's reads are recorded and compared with 0.16.2.

**Acceptance Scenarios**:

1. **Given** a request to apply a saved voice profile, **When** the agent runs, **Then** it reads only the part of the voice-profile reference that covers applying a profile, and the result follows the same rules as 0.16.2.
2. **Given** a help request, **When** the agent runs, **Then** it reads the help reference and no catalog, as in 0.16.2.
3. **Given** each manual case, **When** it runs on the candidate, **Then** the bytes read are not higher than on 0.16.2, and the case passes its expected outcome.

---

### User Story 3 - Maintainers see the cost of every change (Priority: P3)

A maintainer changing skill text can see how many bytes each route loads, so a later change cannot silently raise the cost again, as spec 037 did.

**Why this priority**: It keeps the saving after this spec ends. It is not needed for the first saving.

**Independent Test**: A maintainer check reports, for each route in the routing table of `SKILL.md`, the files and bytes the route reads. It fails when a route's bytes grow beyond a recorded budget.

**Acceptance Scenarios**:

1. **Given** the routing table, **When** the check runs, **Then** it prints each route's files and total bytes.
2. **Given** a change that adds a file to a route, or grows a file, beyond the route's budget, **When** the check runs, **Then** it fails and names the route.

### Edge Cases

- A host has no file-reading tool and receives only the inlined skill text. The skill still works from what it is given, as in 0.16.2, and names the parts it lacks.
- An article mixes genres, for example a README with a personal story. The agent may need two cards or catalogs. Cost may rise for that case, but never beyond 0.16.2's reads for the same case.
- A run reads a file that is already in context. It is not read again.
- Splitting a file leaves a rule in two places. Each rule keeps exactly one owner file, as the core-and-catalog rule of `SKILL.md` requires today.
- Measurement noise: two runs per article per model give counts that vary by a few errors between batches. The quality tolerance accounts for this.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The candidate MUST keep every behavior of 0.16.2: the 55 patterns, the five gates, the routes, the voice and profile rules, the data boundaries and the frozen zones. No feature is removed to save tokens.
- **FR-002**: The text loaded on every run MUST be smaller than 0.16.2's `SKILL.md`. Content that only some routes need MUST move to files that only those routes read.
- **FR-003**: Each route MUST read no more bytes than in 0.16.2. A route that read a large reference MUST read only the section it needs, for example applying a profile without reading how to learn one.
- **FR-004**: On D11–D34, for each model, the candidate's fixes (lexicon-kind and other) and guard breaks MUST be no worse than 0.16.2 by more than 2 per count (Fio, 26/11/2026: "Lệch tối đa 2"): Opus fixes at least 11/70 lexicon-kind and 10/50 other errors and breaks at most 22 guards; Sonnet fixes at least 1/70 and 8/50 and breaks at most 20 guards.
- **FR-005**: The measurement MUST reuse the T035 setup: the same pool D11–D34, prompt, host (Claude Code `-p`), plugin install from a ZIP, scorer `benchmarks/holdout_036.py`, with 0.16.2 run again in the same batch as the baseline, because the T035 runs did not log reads and cannot be shown free of the user-installed plugin (research R3). Every run logs its reads; a run that loads skill text from outside its own package is discarded and rerun. It reports cost, total tokens, output tokens, time and tool turns per run, beside fixes and guard breaks.
- **FR-006**: Per constitution Principle IV, iterating on the text MUST use the development articles D01–D10 only. D11–D34 is run as the gate at most twice: one candidate and one retry.
- **FR-007**: Each route the pool does not measure (writing from a brief, following a sample, learning and applying a voice profile, brand voice, help, review only, typography only) MUST get at least one manual case. The case records the files read and the expected outcome, and runs once per model on 0.16.2 and on the candidate.
- **FR-008**: The skill contract tests MUST pass. A test may change only to follow text that moved, never to drop a rule.
- **FR-009**: A maintainer check (User Story 3) MUST list the files and bytes each route reads, and fail when a route grows beyond its recorded budget. It runs in the repository, not in the package.
- **FR-010**: The package MUST stay Markdown only, with no script, as the validator already enforces.
- **FR-011**: Results MUST go to `docs/benchmarks.md` as counts, with model ids, host, date, the pool manifest hash and the package commit of each version.

### Key Entities

- **Route**: one row of the routing table in `SKILL.md` (whole-article edit, short edit, voice profile, help and the rest). It has the set of files it reads and their total bytes.
- **Read budget**: the recorded byte total per route that the maintainer check enforces.
- **Gate run**: one candidate on D11–D34, two runs per model per article, scored against the T035 0.16.2 runs.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A whole-article edit costs at least 25% less per run than 0.16.2, for Opus 5.5 and for Sonnet 5.5, on D11–D34.
- **SC-002**: Time per run is lower than 0.16.2 for both models on D11–D34.
- **SC-003**: Fixes and guard breaks on D11–D34 meet FR-004 for both models.
- **SC-004**: Every manual case of the other routes passes, and none reads more bytes than on 0.16.2.
- **SC-005**: The text every run loads is at least 30% smaller than 0.16.2's `SKILL.md` (14 KB).
- **SC-006**: The maintainer check catches a test change that adds a file to the whole-article route.

## Assumptions

- Claude Code `-p` is the measuring host, as in T035. Cowork shows no token counts, so the saving is measured there by proxy: fewer and smaller reads cost less on any host that bills by tokens. One Cowork check per model is optional and needs Fio's account.
- The runner's `~/.claude/CLAUDE.md` is loaded on every run, as in T035. It adds the same cost to both versions, so it does not change the difference.
- The T035 0.16.2 numbers in the Background table are the planning reference only; the gate baseline is a fresh 0.16.2 batch (FR-005).
- The labels of D11–D34 (agent, three Codex reviewers and the Antigravity decider, no human review) are reused as they are. This spec compares two versions on the same labels and does not need them to be perfect.
- No new pattern, rule or detection is added. Quality is held, not improved.
- Voice-profile storage on Cowork and cloud is out of scope; it is spec 039.
- The work starts after PR 95 merges.
