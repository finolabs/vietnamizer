# Feature Specification: Voice-profile route for Vietnamizer

**Feature Branch**: not created (current branch kept; branch choice is the owner's)
**Created**: 2026-11-08
**Status**: Draft (specify phase; clarify and plan pending)
**Input**: Let a user build and reuse a Vietnamese writing-style profile inside vietnamizer, inspired by `anthropic-skills:setup-writing-style` but Vietnamese-specific. Depth DEEP, trigger privacy.

## Settled decisions (owner, 2026-11-08)

1. **Placement**: a new opt-in route inside vietnamizer (`SKILL.md`), not a separate skill or repo. This amends the current "không tự lưu hồ sơ" rule explicitly: saving happens only on the user's explicit request, never automatically, and the skill never searches memory or history on its own. The five meaning-preservation chốt stay unchanged.
2. **Sample source (v1)**: only text the user pastes or files the user names. No connectors (Gmail, Slack, Drive).
3. **Profile location**: chosen by the user. The skill offers Orrery or Obsidian depending on which the host agent detects on the machine. If neither exists, it asks for a location for a plain Markdown file and recommends `~/.agents/vietnamizer/profiles`.

## Clarifications

### Session 2026-11-08
- Q: Are samples and profiles sent to the external evaluator (Jev/TypeSafe)? → A: As today: the route follows the existing Jev contract (key present and permission to send data), with no extra rule.
- Q: Does v1 ship a statistics script or a Markdown guide only? → A: Markdown guide only; a script is added later, only after evidence on a sample set.
- Q: One profile per store or several? → A: Several named profiles; the user names each when saving and names the one to use.

## User Scenarios & Testing

### User Story 1 — Build a profile from my own writing (Priority: P1)
A user asks vietnamizer to learn how they write. They paste samples or name files. The skill states what it will read, gets a yes, then produces a profile covering overall voice, per-surface habits, tone shifts by audience, and dos/don'ts, each trait backed by a short quoted fragment or a counted observation.

**Why this priority**: without a profile there is nothing to reuse; this is the whole value.
**Independent Test**: give 10 pasted samples in two surfaces; check the profile lists traits with evidence, contains no personal data, and was produced only after consent.
**Acceptance Scenarios**:
1. **Given** no profile and a request to learn my style, **When** I have not yet agreed to what is read, **Then** the skill reads nothing and asks one consent question naming the sources.
2. **Given** consent and pasted samples, **When** the profile is drafted, **Then** every trait cites evidence from the samples and the skill shows the profile before saving anything.
3. **Given** too few samples for a surface, **When** drafting, **Then** the profile says so for that surface instead of inventing traits.

### User Story 2 — Save where I choose (Priority: P1)
After reviewing the profile, the user picks where it is stored. The skill offers only the stores it detected (Orrery, Obsidian); if none, it asks for a Markdown file path and recommends `~/.agents/vietnamizer/profiles`.

**Why this priority**: storage choice and explicit save are the privacy boundary of this feature.
**Independent Test**: run on a host with neither store; confirm nothing is written until a path is given, and the recommended path is offered.
**Acceptance Scenarios**:
1. **Given** a reviewed profile, **When** I have not asked to save, **Then** nothing is written anywhere.
2. **Given** both Orrery and Obsidian detected, **When** saving, **Then** both are offered with no default chosen for me.
3. **Given** neither detected, **When** saving, **Then** the skill asks for a path, recommends `~/.agents/vietnamizer/profiles`, and does not create the folder before I confirm.

### User Story 3 — Edit or write in my voice using a saved profile (Priority: P2)
The user points to a saved profile (or pastes it) and asks for an edit or a new draft in their voice. The skill reads only that profile and applies it within the existing rules: meaning first, voice only as far as evidence supports.

**Why this priority**: this is the payoff, but it reuses the existing "theo giọng mẫu" machinery.
**Independent Test**: edit a draft once with and once without the profile; meaning checks pass in both, and profile-driven changes are traceable to profile entries.
**Acceptance Scenarios**:
1. **Given** a profile the user named, **When** editing, **Then** only that profile is read and edits are limited to evidenced traits.
2. **Given** no profile named, **When** editing, **Then** the skill does not look for one in memory, history or the stores.
3. **Given** a profile trait that would change a protected span, quantity, modality or negation, **When** editing, **Then** meaning wins and the trait is not applied.

### User Story 4 — Correct the profile from feedback and check it blind (Priority: P3)
After a draft, the user says what is off. The skill shows the exact change to the profile and saves only if asked. A blind comparison (plain vs profiled draft on an unrelated topic) tests whether the profile sounds like the user.

**Why this priority**: improves quality over time; v1 works without it.
**Independent Test**: give one correction; the skill shows the proposed profile diff and writes nothing until confirmed.
**Acceptance Scenarios**:
1. **Given** a profile in scope (named by me or just built) and my request to add "never use X" to it, **When** processed, **Then** the diff is shown and the don't-list changes only after I confirm. Feedback about a single draft only changes the draft.
2. **Given** a calibration run, **When** drafts are shown, **Then** they are unlabeled until I pick, and the topic is not one from my samples.

### Edge Cases
- Samples that contain other people's words, quoted replies or signatures: excluded from evidence.
- Samples that contain instructions aimed at the assistant: treated as data, never obeyed.
- Names, phone numbers, emails, account numbers, health, finance or deal terms in samples: not copied into the profile; the pattern is recorded, not the value.
- AI-assisted drafts pasted as "my writing": not accepted as evidence of personal voice unless the user marks them as their own edited version.
- Text typed without diacritics, mixed English, very short chat messages, or samples from several relationships (boss, friend, customer).
- Profile older than the samples now supplied, or contradicting a current explicit request: the current request wins.
- Chosen store unreachable or write refused: report, write nothing elsewhere.
- Profile file edited by hand by the user: the user's version is authoritative.

## Requirements

### Functional Requirements
- **FR-001**: The route MUST start only when the user asks to learn, build, update or apply a writing-style profile. It MUST NOT trigger from ordinary edit requests.
- **FR-002**: Before reading any sample, the skill MUST tell the user what it will read and what it will produce, and MUST proceed only after a clear yes.
- **FR-003**: Samples MUST be only text the user pasted or files the user named in this task. The skill MUST NOT search memory, history, connectors, mailboxes or the stores for samples.
- **FR-004**: The skill MUST exclude text not authored by the user and treat all sample content as data, never as instructions.
- **FR-005**: The analysis MUST be Vietnamese-specific and cover at least: address terms and pronoun roles (xưng hô), sentence particles (nhé, nha, thôi, đấy…), English code-switching, punctuation and number habits, sentence rhythm, openings/closings, and unaccented typing. English-only measures MUST NOT be used.
- **FR-006**: The profile MUST contain: provenance line (counts and date), overall voice traits, one section per surface present in the samples, tone shifts by audience only where the samples show a contrast, and dos/don'ts. Each trait MUST carry short evidence or a count and its scope.
- **FR-007**: The profile MUST NOT contain personal data or secrets: names, contact details, identifiers, health or financial details, deal terms, unannounced work, or judgments about people. Quoted fragments MUST be trimmed of such detail.
- **FR-008**: Where a surface has too few samples, the profile MUST say so and MUST NOT state traits for it as established.
- **FR-009**: The skill MUST show the full profile to the user before any save and accept edits.
- **FR-010**: Saving MUST happen only on an explicit user request. The skill MUST NOT save automatically, at the end of a task, or as a side effect of editing.
- **FR-011**: The save location MUST be chosen by the user. The skill MUST offer Orrery and Obsidian only when the host agent detects them, MUST NOT choose between them for the user, and when neither exists MUST ask for a Markdown file path and recommend `~/.agents/vietnamizer/profiles`.
- **FR-012**: A user MAY keep several profiles, each with a name the user chooses when saving (for example a public-post voice and a work-chat voice). Using a saved profile MUST require the user to name it or paste it. The skill MUST read only that profile and MUST NOT list, merge or pick among profiles on its own.
- **FR-013**: When applying a profile, the five meaning-preservation chốt, protected spans, genre gates and scope limits in `SKILL.md` MUST still hold. The profile MUST NOT permit new facts, experiences or catchphrases to be added.
- **FR-014**: A current explicit user request MUST override any profile entry.
- **FR-015**: Profile updates from feedback MUST show the exact change before saving and MUST NOT add content sourced from others' text or personal data.
- **FR-016**: The blind calibration MUST present a plain and a profiled draft without labels, on a topic not present in the samples, and route each reaction to the right profile section.
- **FR-017**: Any temporary working copy of samples MUST stay outside git-tracked folders and MUST be deleted when the flow ends or the user stops.
- **FR-018**: The route MUST work with Markdown instructions alone; v1 ships no statistics script. The Vietnamese analysis is a guide the agent follows over the supplied samples, and counts it reports MUST be stated as approximate when not computed by code. A script may be added in a later feature only with evidence on a sample set.
- **FR-019**: The constitution, `AGENTS.md`, `docs/style-and-voice.md`, `docs/usage.md`, `PRIVACY.md` and the "không tự lưu hồ sơ" wording in `SKILL.md` and `references/giu-giong-tu-mau.md` MUST be updated together so no document still states the old rule without the opt-in exception.
- **FR-020**: Mandatory reads for existing routes (small edit, article, supplied-sample) MUST NOT grow; the new route's files load only when it is triggered. `SKILL.md` MUST stay within its line limit.

- **FR-021** *(superseded 2026-11-13 by spec 029: Jev removed, nothing is sent to an evaluator)*: Sending samples or a profile to the external evaluator MUST follow the existing Jev contract unchanged (key present and permission to send data); this route adds no separate rule. The plan MUST state which fields reach Jev, and the profile content that is saved MUST still contain no personal data (FR-007).

### Key Entities
- **Writing sample**: user-authored text with surface (email, chat, doc, post) and audience tags; transient.
- **Voice profile**: provenance, overall voice, per-surface sections, tone shifts, dos/don'ts; persistent only if the user saves it.
- **Profile store**: the user-chosen location (Orrery, Obsidian, or a Markdown file path).
- **Calibration result**: which draft the user picked and the reason, used to correct the profile.

## Success Criteria

### Measurable Outcomes
- **SC-001**: In 100% of test runs, no sample is read and no file is written before the consent answer and the explicit save request respectively.
- **SC-002**: In a seeded test with names, phone numbers and emails placed in samples, 0 such values appear in the generated profile.
- **SC-003**: Every trait in a generated profile can be traced by a reviewer to a quoted fragment or a count, for 100% of traits in a 10-sample test.
- **SC-004**: Editing the same draft with a profile keeps all quantities, negations, conditions and protected spans identical to the source in the existing five-chốt checks (0 regressions across the voice benchmark cases).
- **SC-005**: On a host with no Orrery or Obsidian, the recommended path is offered and no directory is created before confirmation, in 100% of runs.
- **SC-006**: A user can go from pasting samples to a reviewed profile in one conversation of no more than 5 exchanges, excluding their own edits.
- **SC-007**: Token/line cost of the mandatory reads for the three existing routes is unchanged from the 027 baseline.

## Assumptions
- Users are Vietnamese writers; profiles for other languages are out of scope.
- "Detects Orrery or Obsidian" means the host agent can see a callable Orrery tool or an Obsidian CLI/vault; detection method is a plan-phase decision.
- Orrery and Obsidian stores are written with their own existing tools; this feature adds no new service.
- Samples are small enough to read in-context (target ≈ 5–30 pieces); bulk corpora and connectors are future work.
- Reuse in a later session is by the user naming the profile; automatic loading is out of scope for v1.
- No helper code in v1 (see Clarifications); constitution principle V is satisfied by Markdown alone.
- A constitution amendment (MINOR) is expected because the feature adds an owner-approved, opt-in persistence exception.
- Benchmark evidence for voice quality uses the existing voice cases; a held-out set is needed before claiming improvement (constitution IV).

## Open items for clarify/plan (not blocking spec)
- How host capability detection for Orrery/Obsidian is expressed in Markdown instructions.
- Profile file format and filename convention.
- Whether `PRIVACY.md` needs a new section or only an amendment.
