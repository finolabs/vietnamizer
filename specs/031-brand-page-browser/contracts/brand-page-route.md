# Contract: brand page through the host browser (spec 031)

Owner in the package: `references/voice-sources.md` mục 4b. `references/brand-voice.md` mục 1 and `references/voice-profile.md` mục 2 point to it.

## Offered when

A `kind: brand` profile is being learned or updated, and the agent sees a browser tool (a deferred tool counts). Third source, after pasted posts and the page's export. No browser tool: say the way is unavailable on this host. A fetch or download tool never replaces it.

## Accepted URLs (O2, settled 2026-11-14 on platform conventions)

| Platform | Accepted | Posts view |
|---|---|---|
| Facebook fanpage | `facebook.com/<tên-trang>`, `facebook.com/profile.php?id=<số>` (only `id`); hosts `www.`, `m.`, `web.` | the page itself |
| LinkedIn company page | `www.linkedin.com/company/<slug>/` | `/company/<slug>/posts/` |
| Brand website or blog | a listing page of posts on the brand's own host, not the root, no query string | post pages linked from it, same host, under its path prefix |

Not accepted: `linkedin.com/in/`, `/showcase/`, `/school/`; a Facebook personal profile; a shared publishing platform outside the brand's own space; a news or information site the brand does not own; any tag, topic, category or search page.

At most three URLs per run, all of one brand; more than three: read the first three after consent and say the rest need a later update run. URLs of two brands: ask which brand this profile is for.

## Order per URL

1. Missing URL or brand name: ask for it (the "platform when needed" slot of the onboarding budget).
2. Competitor or another party's page by the request's wording: decline, open nothing.
3. URL check (data-model): stop on a failure, say why.
4. Facebook or LinkedIn, first URL of that platform in the run: the terms warning; continue only on the user's go.
5. One consent question naming the brand and the URL, asking the authority statement, saying it cannot be verified. Read nothing before a yes.
6. Open the URL; page check (data-model); stop on a failure, say what was seen.
7. Read post bodies the brand published, up to the cap across the run; discard all other text.
8. Report approximate kept and dropped counts and the main drop reason.

## The one click

"See more" ("Xem thêm") inside the body of a post the brand published, once per post, to expand it in place. If the URL changes, a dialog or overlay opens, or comments appear: read nothing from that view, keep the text already visible, do not click again on that post. No other click, typing, scrolling into comments, or banner action.

## Never

Log in; ask for, type or read a password, cookie or token; solve a captcha; accept or dismiss a consent or cookie banner; like, comment, follow, post or send; change a setting; open comments, replies, reactions, messages, reviews, visitor or tagged posts, follower or member lists, People or employee tabs, job posts; record staff names; follow a link inside a post; store a URL.
