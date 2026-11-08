# Data Model: Voice-profile route

## Writing sample (transient)
- `surface`: email | chat | doc | post | other
- `audience`: tag by who the text was for, if the user says so; else `unknown`
- `text`: user-authored text only (quotes, signatures and other authors removed)
- `authorship`: user-written | user-edited AI draft | AI draft (the last is not evidence of voice)
- Lives in conversation context only; never written unless needed, then outside a git work tree and deleted at the end.

## Voice profile (persistent only on explicit save)
- `name`: user-chosen, unique within the store
- `schema`: integer, starts at 1
- `language`: `vi`
- `updated`: date of the last change
- `provenance`: counts per surface, approximate flag
- `voice`: 5–8 overall traits
- `surfaces[]`: one section per surface present; `sample_count`; `thin` flag when too few
- `tone_shifts[]`: only where samples show a contrast; each with a trimmed contrasting pair
- `dos[]`, `donts[]`: characteristic phrases; words and habits to avoid
- Trait = {statement, scope, evidence (trimmed fragment or approximate count), confidence note}
- Validation: no personal data (FR-007), no text authored by others, third-person style, each trait traceable.

## Profile store
- `kind`: orrery | obsidian | file
- `location`: user-chosen folder or path; recommended default `~/.agents/vietnamizer/profiles` for `file`
- Created only on explicit save; folder creation needs a separate yes.

## Calibration result (transient)
- `topic` (not in samples), `pick` (plain | profiled), `reason`, `routed_to` (voice | surface | tone | donts)

## State transitions
`none` → (consent) → `reading` → `drafted` → (user review) → `reviewed` → (explicit save) → `saved`; `saved` → (feedback + shown diff + confirm) → `saved`. Any state → `discarded` on stop; transient data cleared.
