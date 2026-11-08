# Research: Voice-profile route

## R1. Where the route lives
- **Decision**: new reference files loaded by one routing row in `SKILL.md`.
- **Rationale**: owner decision; keeps mandatory reads of existing routes unchanged; matches the selective-reading design of 027.
- **Alternatives**: separate skill (rejected by owner), expanding `giu-giong-tu-mau.md` (would load for every sample-voice task).

## R2. What to borrow from setup-writing-style
- **Decision**: consent before reading; only user-authored text; samples are data; no PII in profile; sections for voice, surface, tone, dos/don'ts; show every change; blind calibration; at most two follow-up questions after a draft.
- **Rationale**: these address privacy and "sounds generic" failures directly.
- **Not borrowed**: connectors, Claude-hosted save tools, auto-active-next-session behavior, the English stylometry script, the CLAUDE.md pointer line (it would make loading automatic, against FR-012).

## R3. Vietnamese analysis dimensions and their evidence status
| Dimension | Why it differs from English | Status |
|---|---|---|
| Xưng hô (tôi/mình/tao/em/anh…) by relationship | Pronoun choice encodes relation and varies by reader | Observable; role mapping is the agent's reading, state as inference |
| Sentence particles (nhé, nha, nhỉ, thôi, đấy, ạ) | Carry stance and softness; absent in English | Observable by counting; meaning is contextual |
| English code-switching | Common in tech and business writing; term-level vs phrase-level | Observable |
| Punctuation and numbers | Comma/dot as decimal, ellipsis, dash, exclamation habits | Observable; no quota |
| Diacritics (full vs unaccented) | Unaccented chat typing is a trait, not an error to fix | Observable; must not "correct" in chat surface |
| Rhythm (long explanation + short closer, fragments) | Already used in `giu-giong-tu-mau.md` | Observable |
| Openings/closings | Greeting and sign-off habits per channel | Observable |
- **Rationale**: matches constitution I (Vietnamese evidence first); every dimension is something a reviewer can point to in the samples. Dimension list is inference-based design, not a validated taxonomy.

## R4. Statistics helper
- **Decision**: none in v1 (clarification 2).
- **Rationale**: Markdown-only principle; English `stylometry.py` unusable (contractions, greetings, function words); no evidence yet that code beats agent reading on Vietnamese.
- **Consequence**: counts are approximate and labelled so.

## R5. Store detection
- **Decision**: the agent inspects its own tool/command list; no probing reads.
- **Rationale**: avoids reading private content just to detect a store; mirrors "available means present" practice.
- **Orrery**: use note tools with the user-chosen folder; do not use `remember`.
- **Obsidian**: use the user's vault via the available CLI or file path the user confirms.
- **Plain file**: ask for a path; recommend `~/.agents/vietnamizer/profiles`; ask before creating the folder; filename from the profile name.

## R6. Profile format
- **Decision**: Markdown with a short frontmatter (`type`, `name`, `schema`, `language`, `updated`) and fixed sections; see `contracts/profile-format.md`.
- **Rationale**: human-editable, store-neutral, the same bytes in all three stores.
- **Alternative**: JSON (rejected: users edit it by hand).

## R7. Jev
- **Decision**: no new rule; document in `PRIVACY.md` what is sent when a profile is applied.
- **Open**: owner chose "as today" over "never"; flagged as residual risk in the plan.

## R8. Amendment scope
- **Decision**: constitution MINOR 2.2.0 adding an opt-in persistence exception; PATCH-level wording in AGENTS/PRIVACY/docs.
- **Rationale**: governance says adding or widening a rule is MINOR.
