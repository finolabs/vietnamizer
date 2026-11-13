# Research: spec 030

Each item: Decision, Rationale, Alternatives considered. Platform facts were not re-checked against live pages on 2026-11-13; the implementation task re-reads the platforms' help pages before writing the export steps.

## R1. Where help and onboarding live

- **Decision**: one reference file `references/tro-giup.md` holds the overview and the onboarding flow. A second plugin adapter `.plugin-skills/help/SKILL.md` points to it (plugin users get `/vietnamizer:help`); a routing row in `SKILL.md` sends "giúp", "hướng dẫn", "bắt đầu" requests there (standalone installs).
- **Rationale**: one source of text; the adapter pattern already exists for the main skill; standalone `npx skills add` installs only the root skill.
- **Alternatives**: a separate `help/` skill directory with its own copy (drift); help only as a route (no `/vietnamizer:help` in plugins, against decision 8).

## R2. Onboarding trigger

- **Decision**: onboarding runs only when the user asks (help, "bắt đầu", "thiết lập giọng"). No first-run detection.
- **Rationale**: the skill keeps no state between sessions and must not auto-load or write anything; detecting "first use" would need stored state.
- **Alternatives**: a marker file after first use (adds silent writes, against the explicit-save rule).

## R3. Profile kind and schema

- **Decision**: add `kind: personal | brand` to the frontmatter; a missing `kind` reads as personal; `schema` stays `1` because every addition is optional and old profiles stay valid. Brand profiles add a `## Quy tắc thương hiệu` section before `## Giọng chung`; every profile may end with `## Lịch sử chấm` after `## Điểm chưa quyết`.
- **Rationale**: same additive approach as PR #39; no migration for existing users.
- **Alternatives**: `schema: 2` (forces a migration path for no behaviour gain).

## R4. Export reading

- **Decision**: LinkedIn: the user requests "Get a copy of your data" and picks posts; the skill reads the posts file (`Shares.csv` at the time of writing) and keeps rows whose author is the account owner, dropping reshares without own text, comments, messages and connections. Facebook: "Download your information", posts only, JSON; the skill keeps the user's own posts and drops tagged posts by others, comments and messages. Cap: the most recent 80 owned posts with Vietnamese text; the skill states how many it kept and dropped.
- **Rationale**: exports are the reliable, terms-compliant path; a cap keeps context bounded while 80 posts is well above the 10–20 the route needs.
- **Alternatives**: read everything (context blow-up); ask the user to pre-filter (more effort, against "đơn giản hóa").

## R5. Browser path

- **Decision**: only through a browser tool the host already lists, on the user's logged-in session, on a page the user names and states is theirs. Before LinkedIn, show the terms warning and continue only on the user's go. Stop on a login wall, a different account, a captcha or a rate-limit page; never type credentials, solve captchas or read cookies. Read at most the same cap as R4 by scrolling the user's own activity page.
- **Rationale**: settled decisions 5 and FR-007; host safety rules already forbid credentials and captchas.
- **Alternatives**: fetch public URLs (blocked by login walls, and LinkedIn forbids it).

## R6. Brand sources

- **Decision**: three inputs (guide, published posts, internal documents). Guide statements become `Quy tắc thương hiệu` entries with their source label; observed patterns become traits as in spec 028, with evidence from posts or documents. A post that breaks a guide rule goes to `Điểm chưa quyết`. Text by many authors is allowed only for brand profiles, after the user states they may speak for the brand.
- **Rationale**: decisions 3 and 4; keeps written rules authoritative but visible when practice differs.
- **Alternatives**: merge guide and posts into one list (hides conflicts).

## R7. Rating session

- **Decision**: ask the count first (0–10, default suggestion 5); for each paragraph, show it in the message, then one question with exactly four options in the owner's order: Kém, Trung bình, Khá, Tốt, with none marked recommended. Without a form the user replies with the level word. After the last paragraph, for Kém and Trung bình ask at most two reason questions in total, then propose a diff (spec 028 mục 6). On save, append one line to `## Lịch sử chấm`: date, count, counts per level, unrated count, and the fixed label "đánh giá của người dùng, không phải điểm chất lượng". Paragraph text is never stored.
- **Rationale**: decision 6 and 7; a four-option question fits every known host form; fixed label keeps the README claim honest.
- **Alternatives**: a 1–5 scale (does not fit four-option forms); storing the paragraphs (privacy and size).

## R8. Doc and constitution amendments

- **Decision**: constitution 2.4.0 (MINOR): the voice-profile constraint allows the browser source on the user's own pages and multi-author material for brand profiles; ratings by the user may be stored in their profile; the skill still never scores similarity. Update README, PRIVACY ("Hồ sơ giọng"), `docs/style-and-voice.md`, AGENTS file map, changelog.
- **Rationale**: FR-017; the constitution's governance requires reason, impact and owner approval.
- **Alternatives**: none; leaving the conflict would block review.
