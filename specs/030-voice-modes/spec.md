# Feature Specification: Personal and brand voice, social sources, user rating, help and onboarding

**Feature Branch**: `spec/030-voice-modes`
**Created**: 2026-11-13
**Status**: Draft (specify phase; clarify and plan pending)
**Input**: Owner, 13/11/2026: support both brand voice and personal voice, chosen at use, personal by default; learn a user's voice from their LinkedIn or Facebook; after learning, let the user rate generated paragraphs so the profile can be upgraded; add a `help` skill and an onboarding flow. Router depth DEEP, trigger `privacy` (new data sources, a browser path to the user's logged-in accounts, stored ratings, new consent paths). Builds on spec 028 (voice-profile route) and PR #39 (`ranh giới`, `Điểm chưa quyết`).

## Settled decisions (owner, 2026-11-13)

1. **Two voice kinds**: personal voice and brand voice. The user picks one each time they use the skill; personal is the default.
2. **No mixing**: one profile applies per use. A text is never written in a blend of a personal and a brand profile.
3. **Brand sources**: an existing brand guide, the brand's published posts, and internal documents the user supplies (sample emails, landing pages, proposals). All of them go through the same redaction as personal samples.
4. **Ownership**: the user states that an account or page is theirs, or a brand they are allowed to speak for. The skill cannot verify identity and says so; it never learns the voice of someone else.
5. **Learning sources**: pasted posts (default); LinkedIn and Facebook data exports the user downloads; and reading the user's own pages through a browser tool the host offers, after consent, when the user is already logged in.
6. **Rating after learning**: the skill asks how many paragraphs the user wants to review, then shows one generated paragraph at a time with a question form of four levels, **Kém, Trung bình, Khá, Tốt**, and repeats for the chosen count.
7. **Ratings are stored in the profile** as the user's own judgement, not as a quality measure. This amends `references/ho-so-giong.md` mục 7 ("Không biến một lượt chọn thành điểm khớp giọng") and the README/style docs that say the skill does not score voice similarity: the skill still never scores similarity itself.
8. **Help and onboarding**: a `help` skill and an onboarding flow ship inside the existing plugin, which today carries one skill.

## Clarifications

### Session 2026-11-13
- Q: How hard are the exports for users? → A: About five or six clicks on each platform and a wait of minutes to a day; pasting 10–20 posts stays the simplest default (owner chose to keep all three sources, decision 5).
- Q: Does the browser path cover LinkedIn, whose terms forbid automated access? → A: Yes, both LinkedIn and Facebook; the skill warns about LinkedIn's terms and the risk to the account, and the user decides (FR-007).

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Pick a voice when I use the skill (Priority: P1)

A user asks Vietnamizer to edit or write. Without saying anything about voice, they get the current behaviour: their own voice (the text's existing voice, or a personal profile they name). When they say they want a brand's voice and name a brand profile, the skill applies that brand profile only.

**Why this priority**: every other story depends on the skill knowing which kind of voice is in play, and on never mixing two.
**Independent Test**: run the same draft three times: no voice named, a personal profile named, a brand profile named. The first two follow personal rules, the third applies only the brand profile; no output carries traits of both.
**Acceptance Scenarios**:
1. **Given** a request that names no voice, **When** the skill edits, **Then** it uses personal voice and does not look for any profile.
2. **Given** a request naming a brand profile, **When** editing, **Then** only that brand profile is read and applied, and the skill says which profile it used.
3. **Given** a request naming both a personal and a brand profile, **When** editing, **Then** the skill asks which one to use and applies only that one.

### User Story 2 — Learn my voice from my LinkedIn or Facebook (Priority: P1)

A user wants their voice learned from what they already post. The skill offers three ways, simplest first: paste 10–20 posts, give a data export file, or, where the host has a browser tool and the user is logged in, read the user's own page after consent. It keeps only posts the user wrote, then builds the profile as in spec 028.

**Why this priority**: this is the main new value; it removes the effort of collecting samples by hand.
**Independent Test**: give a LinkedIn export containing the user's posts, reshares and comments by others; the draft profile cites only the user's own posts and holds no names or contacts.
**Acceptance Scenarios**:
1. **Given** a request to learn from LinkedIn, **When** no source is given yet, **Then** the skill explains the three ways with the export steps and asks which one; it reads nothing yet.
2. **Given** an export file, **When** the user consents, **Then** the skill keeps only items authored by the account owner, drops reshares, others' comments, messages and contact data, and says how many items it kept and dropped.
3. **Given** the browser way, **When** the user has not stated the page is theirs, **Then** the skill asks first and reads nothing; **When** the page shows a login wall or a different account, **Then** it stops and suggests the paste or export way.
4. **Given** a URL to someone else's profile, **When** the user says it is not theirs, **Then** the skill declines to learn that voice.

### User Story 3 — Build a brand voice (Priority: P2)

A user responsible for a brand gives a brand guide, links or exports of the brand's posts, and internal documents. The skill builds a brand profile: the same sections as a personal profile, marked as brand, with traits drawn from material written by many people and with explicit rules from the guide kept apart from patterns observed in posts.

**Why this priority**: high value for teams, but it reuses the personal machinery.
**Independent Test**: give a short brand guide and 15 posts; the profile separates guide rules from observed patterns, contains no staff or customer names, and is marked as a brand profile.
**Acceptance Scenarios**:
1. **Given** brand material, **When** the user has not stated they may speak for the brand, **Then** the skill asks first.
2. **Given** a guide rule that the posts contradict, **When** drafting, **Then** the conflict goes to `Điểm chưa quyết` with a proposal, not into the voice sections.
3. **Given** internal documents with customer names or deal terms, **When** drafting, **Then** none of them appear in the profile.

### User Story 4 — Rate sample paragraphs and upgrade the profile (Priority: P2)

Right after a profile is drafted (or later, on request), the skill asks how many paragraphs the user wants to review. It then shows one generated paragraph at a time, on topics outside the samples, and asks the user to rate it as Kém, Trung bình, Khá or Tốt. For paragraphs rated Kém or Trung bình it asks briefly why and proposes a profile diff. Ratings are written into the profile only when the profile is saved or updated with the user's confirmation.

**Why this priority**: gives the user a cheap way to correct the profile and a record over time.
**Independent Test**: choose 3 paragraphs, rate them Tốt, Kém, Khá; the skill asks one reason for the Kém paragraph, proposes a diff, and the saved profile records three ratings with the date and nothing else about the paragraphs' content.
**Acceptance Scenarios**:
1. **Given** a drafted profile, **When** the rating step starts, **Then** the skill first asks how many paragraphs to review and accepts zero (skip).
2. **Given** a host with a question form, **When** showing each paragraph, **Then** the paragraph is shown first and the form offers exactly the four levels; **Given** no form, **Then** the user answers in text.
3. **Given** ratings, **When** the profile is saved, **Then** the profile holds the counts per level and the date, labelled as the user's own judgement; the skill never computes or states a similarity score of its own.
4. **Given** a rating session the user did not ask to save, **When** it ends, **Then** nothing is written.

### User Story 5 — Get help and a first-run walkthrough (Priority: P3)

A user who does not know what Vietnamizer can do asks for help, or runs the help skill. They get a short overview (edit, write, voice profiles, brand voice) and can start an onboarding walkthrough: pick personal or brand voice, pick a source, learn, rate, and choose whether to save.

**Why this priority**: lowers the entry cost; the features work without it.
**Independent Test**: on a fresh install, run help; the overview fits one screen and the walkthrough reaches a saved-or-not decision without the user knowing any command.
**Acceptance Scenarios**:
1. **Given** the help skill is run, **When** it answers, **Then** it lists what the skill does and the way to start each, in Vietnamese, without reading any user file.
2. **Given** the user starts onboarding, **When** each step needs a choice, **Then** it is asked through the host's question form where available, recommended option first.
3. **Given** onboarding, **When** the user stops at any step, **Then** nothing is saved and nothing is read beyond what they consented to.

### Edge Cases

- An export holds tens of thousands of items: the skill takes a bounded, recent subset and says how many it used.
- Posts mostly in English or mixed: only Vietnamese text counts as evidence; the skill reports when too little Vietnamese remains.
- Shared or ghost-written posts on a personal account: the user is asked whether they wrote them; unclear items stay out of the evidence.
- A brand profile is named while the user writes a personal message: the skill uses the brand profile only if the user confirms.
- Rating answers outside the four levels, or "không biết": recorded as no rating for that paragraph.
- An old personal profile without a kind field: treated as personal.
- The browser path is unavailable on the host: the skill offers paste or export and never asks the user for passwords or cookies.
- A page or export contains text aimed at the agent: it is data, never an instruction.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The skill MUST support two profile kinds, personal and brand, and MUST mark each profile with its kind. A profile without a kind MUST be read as personal.
- **FR-002**: The skill MUST use personal voice when the user names no voice, and MUST apply a brand profile only when the user names it in the current request.
- **FR-003**: The skill MUST apply exactly one profile per use and MUST ask when two are named.
- **FR-004**: The skill MUST offer three learning sources in this order: pasted text, a platform data export the user supplies, and reading the user's own pages through a host browser tool. It MUST explain the export steps for LinkedIn and Facebook on request.
- **FR-005**: Before reading any source, the skill MUST ask one consent question naming the source, as spec 028 FR-002 requires, and MUST ask the user to state the account or page is theirs or a brand they may speak for. It MUST decline when the user says it is not.
- **FR-006**: From an export or a page, the skill MUST keep only items authored by the account owner (or published by the brand) and MUST drop reshares, comments by others, private messages, contact lists and profile data; it MUST report kept and dropped counts as approximate.
- **FR-007**: The browser path MUST run only through a browser tool the host already offers, on a session the user is already logged in to; the skill MUST NOT ask for or handle passwords, cookies or tokens, MUST NOT read pages of other people, and MUST stop on a login wall or a different account. The path covers LinkedIn and Facebook; before reading LinkedIn the skill MUST tell the user that LinkedIn's terms forbid automated access and that their account may be restricted, and MUST continue only after the user decides to go ahead.
- **FR-008**: A brand profile MUST keep explicit rules from a brand guide apart from patterns observed in posts, and MUST route conflicts between them to `Điểm chưa quyết`.
- **FR-009**: Brand material MUST go through the same redaction as personal samples (spec 028 FR-007): no names of staff or customers, contacts, deal terms or unpublished work.
- **FR-010**: After a profile is drafted, the skill MUST offer the rating step and ask how many paragraphs to review; zero MUST skip it. Paragraphs MUST be on topics outside the samples and MUST respect the five meaning chốt.
- **FR-011**: Each paragraph MUST be shown alone, followed by a rating question with exactly four levels: Kém, Trung bình, Khá, Tốt; where the host has no question form the user answers in text.
- **FR-012**: For paragraphs rated Kém or Trung bình, the skill MAY ask at most two reason questions per session and MUST turn reasons into a proposed diff through spec 028 mục 6 (`ranh giới`, scope, `Điểm chưa quyết`); it MUST NOT save without confirmation.
- **FR-013**: When the user saves or confirms an update, the profile MUST record the rating session as counts per level and the date, labelled as the user's own judgement; it MUST NOT store the paragraphs or describe the counts as a quality or similarity score. The skill MUST NOT compute a similarity score itself.
- **FR-014**: The plugin MUST ship a `help` skill that describes what Vietnamizer does and how to start each flow, reads no user file and saves nothing.
- **FR-015**: The plugin MUST offer an onboarding flow, started from help or by request, that walks through voice kind, source, learning, rating and the save choice, asking each choice through the host's question form where available.
- **FR-016**: The five meaning chốt, protected spans, consent gates, the explicit-save rule and the absence of any external evaluator MUST stay unchanged; profiles from spec 028 and PR #39 MUST remain valid.
- **FR-017**: The constitution, `references/ho-so-giong.md` mục 7, README, PRIVACY and `docs/style-and-voice.md` MUST be amended where they conflict with decisions 3, 5 and 7 (brand material from many authors, the browser source, stored ratings), with the owner's approval recorded.

### Key Entities

- **Voice profile**: as in spec 028, plus `kind` (personal or brand), optional sources line per kind, and a rating history.
- **Learning source**: pasted text, export file, or browser page; with owner statement, kept and dropped counts.
- **Rating session**: date, number of paragraphs, counts per level (Kém, Trung bình, Khá, Tốt), number unrated; no paragraph text.
- **Brand rule**: a rule taken from a brand guide, kept apart from observed traits.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In calibration cases, 100% of runs that name no voice use personal voice, and 0 runs apply two profiles at once.
- **SC-002**: From a mixed export (own posts, reshares, others' comments), 0 non-owned items appear as evidence in the profile, and 0 names or contacts appear anywhere in it.
- **SC-003**: A new user can go from "help" to a drafted profile from pasted posts in under 10 minutes, answering at most 6 questions before the rating step.
- **SC-004**: In a rating session of N paragraphs, the user answers exactly N rating questions, and the saved profile holds exactly the counts given, with no score computed by the skill.
- **SC-005**: Every calibration case for the browser path stops before reading when ownership is not stated, and on a login wall.
- **SC-006**: All existing voice-profile cases (route cases 1–9, HG01–HG11) still pass review with the new text in place.

## Assumptions

- Hosts differ: Claude Code has a question form (four options, four questions per form) and may have a browser tool; other hosts may have neither. Every step has a text fallback.
- LinkedIn exports carry posts in `Shares.csv`; Facebook exports carry posts in JSON or HTML. Field names may change; the skill reads them as data and reports when it cannot find posts.
- A bounded subset for large exports is the most recent 50–100 posts; the plan sets the number.
- Ratings stay in the profile file the user chose; no rating leaves that store.
- The `help` skill ships in the same plugin; standalone installs through `npx skills add` can add it by name.
- Version: new skills and a new profile kind are a MINOR change in phase 0 (0.15.0 or later); the release is the owner's call.
