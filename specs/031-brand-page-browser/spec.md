# Feature Specification: Read a brand's own page through the host browser for a brand profile

**Feature Branch**: `spec/031-brand-page-browser`
**Created**: 2026-11-14
**Status**: Draft (specify phase; clarify and plan pending)
**Input**: Owner, 14/11/2026, review of the afk lease of 13–14/11/2026 (Orrery memory `01M7C2CK384NC5QK4ED7CM5ZQ3`): the implementation decision in spec 030 FR-006 that kept brand pages off the browser source is reversed; Fio wants the voice-profile route to read a brand's own page through a host browser tool when learning a `kind: brand` profile. Router depth DEEP, trigger `privacy` (network access through a host browser, pages the skill cannot tie to the user, a new consent path). Builds on spec 028 (voice-profile route) and spec 030 (personal and brand voice, social sources).

## Settled decisions (owner, 2026-11-14)

1. **Reversal**: the spec 030 FR-006 implementation decision of 2026-11-13 ("the browser path is not used for brand pages") is reversed. Until this spec is implemented and released, the shipped rule (no browser for brand pages) still applies.
2. **Route: one URL the user gives, checked**: the user gives exactly one URL of the brand's page. The skill opens only that page and the posts view of that same page, after checking that the URL is on a supported platform and that the page shown carries the brand name the user stated. It follows no other link.
3. **Platforms**: Facebook fanpages, LinkedIn company pages, and the brand's own website or blog.
4. **Authority: any public brand page, on the user's statement**: the skill reads any public brand page once the user states they may speak for that brand. It does not require the logged-in account to be a page admin and checks no admin sign. It cannot verify the user's authority and says so, as spec 030 decision 4 and `references/brand-voice.md` mục 1 already do.

The options Fio did not pick, kept for the record: start from a fixed "pages I manage" admin URL; read only the tab the user opened themselves; admin-only pages.

## Clarifications

### Session 2026-11-14
- Q: Which route reaches a brand page, given brand pages have no fixed "my page" URL like `/in/me`? → A: one URL the user gives, checked for platform and brand name; no other link followed (decision 2).
- Q: Which platforms? → A: Facebook fanpage, LinkedIn company page, brand website or blog (decision 3).
- Q: Page admins only, or any public brand page with the user's statement? → A: any public brand page with the statement (decision 4).
- Unverified (2026-11-14): the URL shapes below (`facebook.com/<page>`, `linkedin.com/company/<slug>/posts/`) and the page signs that tell a fanpage from a personal profile come from platform conventions; no live page was opened to confirm them. The plan confirms them on real pages before the reference text names them.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Learn a brand voice from the brand's fanpage or company page (Priority: P1)

A user who speaks for a brand asks Vietnamizer to learn the brand voice from the brand's Facebook fanpage or LinkedIn company page. The host has a browser tool. The skill asks for the page URL if none was given, warns once about the platform's terms, asks the one consent question that names the URL and includes the authority statement, then opens that page, reads up to the cap of the brand's own published posts, and drafts a `kind: brand` profile as in spec 030 US3.

**Why this priority**: this is the reversal Fio asked for; it removes copying posts by hand for brands that have no export at hand.
**Independent Test**: on a host with a browser tool, give a fanpage URL and state authority; the skill warns about Meta's terms once, asks one consent question naming that URL, reads only the page's posts, and the draft profile cites only brand posts, with no names of staff, customers or commenters.
**Acceptance Scenarios**:
1. **Given** a request to learn a brand voice from "our fanpage" with no URL, **When** the user picks the browser source, **Then** the skill asks for the page URL and reads nothing yet.
2. **Given** a fanpage or company-page URL, **When** the user has not stated they may speak for the brand, **Then** the consent question asks for that statement and the skill reads nothing until the user answers yes.
3. **Given** consent and the statement, **When** the skill reads, **Then** it opens only the given page and its posts view, keeps only posts the brand published, and reports approximate kept and dropped counts.
4. **Given** a URL that resolves to a personal profile (`linkedin.com/in/…`, or a Facebook profile of a person), **When** the user says it is the brand's page, **Then** the skill stops and does not read it; a personal account goes through the personal route of spec 030.

### User Story 2 — Learn from the brand's own website or blog (Priority: P2)

A user gives the URL of the brand's blog or news page. The skill asks the same consent question with the authority statement, opens the listing page, opens post pages linked from it on the same host and path, and reads their article text up to the cap.

**Why this priority**: many brands write their longest Vietnamese text on their own site; it carries no platform terms risk but has no admin or account sign the skill can check.
**Independent Test**: give a blog listing URL; the skill opens only pages on that host under that path, never a link to another host, a login page, a comment section or a contact form, and reports the pages used.
**Acceptance Scenarios**:
1. **Given** a blog URL and consent, **When** reading, **Then** the skill opens only the listing and post pages on the same host under the same path prefix, at most the cap.
2. **Given** a post page that links to another host, a social page or a PDF, **When** reading, **Then** the skill does not follow it.
3. **Given** a site that shows a login wall, a paywall, a captcha or a block page, **When** reading, **Then** the skill stops and offers paste or the page's export.

### User Story 3 — Stop safely when the page is not what was named (Priority: P1)

While reading a brand page the skill meets a page it should not read: a login wall, a page for another brand, a captcha or a rate-limit page. It stops and offers the paste or export way. It never asks for, types or reads a password, cookie or token.

**Why this priority**: the reversal is acceptable only if the stop conditions of the personal path hold for brand pages too.
**Independent Test**: run the four stop cases; each stops before reading any post and suggests paste or export; none types into a field.
**Acceptance Scenarios**:
1. **Given** a login wall, a captcha or a rate-limit page, **When** it appears, **Then** the skill stops, types nothing, and suggests paste or export.
2. **Given** the page shown carries a different brand name than the one the user stated, or the URL redirects to another page or host, **When** checked before reading, **Then** the skill stops and tells the user what it saw.
3. **Given** page text aimed at the agent (open this link, save, send), **When** reading, **Then** it is data, never an instruction.

### User Story 4 — Pick the browser source for a brand during onboarding (Priority: P3)

A user runs the onboarding of spec 030, picks Thương hiệu, and on a host with a browser tool sees "Đọc trang qua trình duyệt" among the sources.

**Why this priority**: onboarding is optional; the route works without it.
**Independent Test**: onboarding with Thương hiệu on a host with a browser tool offers the browser source; on a host without one it does not; the question budget before rating stays at 6.
**Acceptance Scenarios**:
1. **Given** Thương hiệu and a browser tool, **When** the source step runs, **Then** the browser source is offered after paste and export.
2. **Given** the browser source, **When** the consent step runs, **Then** the terms warning (social platforms only) comes first, then one consent question naming the URL and asking the authority statement; neither becomes a separate question.

### Edge Cases

- The user gives several brand URLs at once: the skill reads one per consent question; each further page needs its own consent question, inside the question budget or after it.
- A fanpage shows posts by visitors, reviews, check-ins or tagged posts beside the brand's own posts: only posts the brand published count.
- A company page shows a "People" or "Employees" tab, job posts or follower counts: none are opened or recorded.
- A brand post quotes a customer or tags a staff member: the post may stay as evidence of the brand's writing, but the name never enters the profile (`references/brand-voice.md` mục 3).
- Posts mostly in English: only Vietnamese text counts as evidence (spec 030 edge case).
- A host offers a fetch or download tool but no browser tool: the browser source is not offered; links are never opened with the fetch tool (calibration case 5 keeps holding).
- The browser is logged in to the user's personal account while they read the brand page: the skill reads only the brand page; it does not open the personal feed, notifications or messages.
- The user says they do not speak for the brand: the skill does not build a brand profile and offers a personal profile from text they wrote themselves.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: For a `kind: brand` profile, the skill MUST offer reading the brand's page through a browser tool the host already offers, as the third source after pasted posts and the page's export, and only when the agent sees such a tool (a deferred tool counts, as in `references/voice-sources.md` mục 1). Without one, the skill MUST say the way is unavailable on this host.
- **FR-002**: The skill MUST read a brand page only from exactly one URL the user gives in the current request, on a supported platform: a Facebook fanpage, a LinkedIn company page, or the brand's own website or blog. It MUST NOT search for the page, guess its URL, or use a fetch or download tool instead of a browser tool.
- **FR-003**: Before reading, the skill MUST ask one consent question (spec 028 FR-002, `references/voice-profile.md` mục 2) that names the exact URL it will open and asks the user to state they may speak for the brand. It MUST say it cannot verify that authority. It MUST read nothing until the user answers yes, and MUST decline the brand profile when the user says they may not.
- **FR-004**: For Facebook and LinkedIn, the terms warning of spec 030 FR-007 (the platform's terms forbid automated access or collection without permission; the account in use may be restricted) MUST appear exactly once, right before the consent question; the skill MUST continue only after the user decides to go ahead. The brand's own website carries no platform terms warning.
- **FR-005**: The route MUST be fixed: on Facebook, the given fanpage and its posts view; on LinkedIn, the given company page and its posts view on the same company path; on a website, the given listing page and post pages linked from it on the same host and under the same path prefix. The skill MUST NOT follow any other link, open another host, or open a page linked from inside a post.
- **FR-006**: Before reading posts, the skill MUST check that the page is a brand page (not a personal profile) and that it carries the brand name the user stated; when either check fails, or the URL redirects to another page or host, it MUST stop and say what it saw.
- **FR-007**: The skill MUST read only the text of posts the brand published. It MUST NOT open or record comments, replies, reactions, messages or chat, reviews or ratings, visitor posts, tagged posts, follower or member lists, "People" or employee tabs, job posts, or staff names; it MUST report kept and dropped counts as approximate.
- **FR-008**: The skill MUST stop on a login wall, a different account or page, a captcha, a paywall or a rate-limit or block page, and offer paste or export. It MUST NOT ask for, type or read passwords, cookies or tokens, MUST NOT solve captchas, MUST NOT like, comment, follow, post or send, and MUST NOT change any setting.
- **FR-009**: Reading MUST stop at the cap of `references/voice-sources.md` mục 3 (at most 80 most recent posts with Vietnamese text); the plan MAY set a lower scroll or page bound.
- **FR-010**: Page content MUST be treated as data (`references/voice-sources.md` mục 5) and MUST go through the brand redaction of `references/brand-voice.md` mục 3 before it reaches the profile; the profile's sources line counts posts by type and platform and never records the URL.
- **FR-011**: The onboarding contract (spec 030 `contracts/help-onboarding.md` step 2) and `references/help.md` MUST offer the browser source for Thương hiệu under FR-001; the question budget before rating MUST stay at 6.
- **FR-012**: The five meaning chốt, protected spans, the explicit-save rule, the personal browser path of spec 030 (fixed own-account URLs) and the absence of any network code in the package (constitution Principle V) MUST stay unchanged; existing profiles MUST remain valid.
- **FR-013**: The constitution constraint "Tuyến hồ sơ giọng" MUST be amended as a MINOR change (2.4.1 → 2.5.0) before the references change, with Fio's approval recorded in its Sync Impact Report; the proposed text is under "Constitution amendment".
- **FR-014**: Every text that states brand pages are not read through the browser MUST be updated in the implementation: `references/brand-voice.md` mục 1, `references/voice-sources.md` mục 1, 2 and 4, `references/voice-profile.md` mục 2, `references/help.md`, spec 030 FR-006's delivery note and `contracts/help-onboarding.md` step 2, `PRIVACY.md`, `README.md`, `docs/style-and-voice.md`, `docs/architecture.md`, `docs/changelog.md`, and `calibration/test-cases.md` (case 5 keeps its fetch-tool half; new cases cover FR-002–FR-008).

### Constitution amendment (proposed, MINOR 2.4.1 → 2.5.0)

The constraint "Tuyến hồ sơ giọng" today allows the browser only for "trang của chính người dùng". The proposed change adds one clause and keeps every prohibition:

> … hoặc từ trang của chính người dùng qua công cụ trình duyệt host sẵn có, sau câu đồng ý đọc và lời khẳng định chủ tài khoản; với hồ sơ `kind: brand`, skill MAY đọc trang công khai của thương hiệu (fanpage Facebook, trang công ty LinkedIn, website hay blog của thương hiệu) qua công cụ trình duyệt đó, chỉ từ đúng một URL người dùng đưa, sau câu đồng ý đọc gọi tên URL và lời khẳng định được nói thay thương hiệu; chỉ đọc bài thương hiệu đã đăng, MUST NOT mở bình luận, tin nhắn, đánh giá, danh sách người theo dõi hay tên nhân viên, và MUST NOT theo link nào khác.

"MUST NOT đọc trang của người khác" stays; the amendment states that a brand page the user speaks for is not "trang của người khác", while a personal profile of anyone else still is. Principle V is unchanged: the package still ships no network code. MINOR because the constraint gains a source; no principle's obligation is removed.

### Key Entities

- **Brand page source**: platform (Facebook, LinkedIn, website), the one URL the user gave, the brand name the user stated, the authority statement and its date, approximate kept and dropped counts. Only the counts and the platform reach the profile's sources line.
- **Stop event**: the condition met (login wall, other page, captcha, paywall, limit), shown to the user; not stored.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In calibration cases, 100% of brand browser runs ask the consent question with the authority statement before any page is opened, and 0 open a page when the user has not answered yes.
- **SC-002**: 100% of runs meeting a login wall, another page, a captcha, a paywall or a limit page stop before reading any post, and 0 type into any field.
- **SC-003**: Across the cases, 0 pages outside the fixed route of FR-005 are opened, and 0 comments, reviews, follower names or staff names appear in the drafted profile.
- **SC-004**: The terms warning appears exactly once in Facebook and LinkedIn runs and 0 times in website runs.
- **SC-005**: All existing voice-profile cases (route cases 1–9, HG01–HG11, spec 030 cases) still pass review, with case 5 rewritten as FR-014 says.

## Assumptions

- Hosts differ: Claude Code may offer a browser tool (built-in pane or Chrome extension); other hosts may not. Paste and export stay the defaults, and every step has a text fallback.
- Public fanpages and company pages may show fewer posts, or a login wall, when the browser is not logged in; the login-wall stop covers that.
- The user's authority statement is the only authority signal (decision 4); the skill's checks of platform, page type and brand name guard against a wrong page, not against a false statement.
- Version: a new brand source and a constitution MINOR are a MINOR change in phase 0 (0.16.0 or later); the release is the owner's call.
- Out of scope: Instagram, TikTok, YouTube and other platforms; reading a brand's ads library; fetch or download tools; any network code in the package.
