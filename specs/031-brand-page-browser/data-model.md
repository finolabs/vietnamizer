# Data model: spec 031

Nothing here is stored except the counts in the profile's sources line. The entities describe what the skill holds in the conversation during one learning run.

## Brand page source

| Field | Values | Rule |
|---|---|---|
| platform | `facebook`, `linkedin`, `website` | from the URL check (contract `brand-page-route.md`) |
| url | the URL the user gave | never stored; named in the consent question only |
| brand | the brand name the user stated | compared with the page (FR-008); one brand per profile |
| authority | yes, with the date of the run | asked in the consent question; a no declines the brand profile |
| terms_warned | per platform, once per run | Facebook and LinkedIn only (FR-004) |
| kept, dropped | approximate counts, main drop reason | reported to the user; counts reach the sources line |

Validation: at most 3 sources per run, all with the same `brand`; the post cap (80) counts across all of them.

## URL check (before any page is opened)

1. Given in the current request by the user (FR-002); not searched, guessed or fetched.
2. Platform shape accepted (contract, "Accepted URLs"); otherwise stop.
3. Not a competitor or another party's page by the request's own wording (FR-007); otherwise decline.
4. For a website: not the root, no query string, not a login, account, contact, search or comment page; on a shared platform, inside the brand's own space, with the platform's listing and post paths (FR-006, FR-018).

## Page check (after opening, before reading posts)

1. No redirect to another page or host. Not a redirect: a move between `www.`, `m.` and `web.facebook.com` on the same path with the same query string, an added trailing `/`, or `profile.php?id=<số>` to a one-segment `facebook.com/<tên-trang>` on one of those hosts; every other check still runs on the page reached.
2. Brand page signs present, personal profile signs absent (research R1). A fanpage whose category marks a person stops the brand route; the user's own one may go to the personal Page route (FR-017, mục 4c).
3. The page carries the brand name the user stated.
4. No login wall, captcha, paywall, blocking consent or cookie banner, rate-limit or block page.

## Stop event

`condition` ∈ {person's fanpage, login wall, other account or page, redirect, brand-name mismatch, personal profile, captcha, paywall, consent banner, rate limit or block, shared platform outside the brand space, tag/topic/search page, competitor}. Shown to the user with what the skill saw, followed by the paste or export offer. Not stored.

## Sources line (profile)

`references/voice-analysis.md` template: brand posts count by source, for example `bài đăng: dán 4 / export 0 / trình duyệt 18`. No URL, page name, host or post link is recorded.
