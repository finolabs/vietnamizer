# Research: spec 031

Each item: Decision, Rationale, Alternatives considered. Nothing here was checked on live pages: Fio named no page to open, and the browser is used only on pages he names (brief of 14/11/2026).

## R1. URL shapes and page signs (open decision O2, settled 2026-11-14)

- **Decision** (Fio approved on 14/11/2026, "Duyệt đề xuất", as checked against platform conventions, not on live pages):
  - **Facebook fanpage**: `facebook.com/<tên-trang>` or `facebook.com/profile.php?id=<số>`, where `id` is the only query parameter allowed; hosts `www.facebook.com`, `m.facebook.com`, `web.facebook.com`. The posts view is the page itself (no separate tab is opened).
  - **LinkedIn company page**: `linkedin.com/company/<slug>/` (host `www.linkedin.com`) and its posts view `linkedin.com/company/<slug>/posts/`. `/in/`, `/showcase/` and `/school/` paths are not accepted.
  - **Page signs**: a fanpage shows "Trang · <hạng mục>" ("Page · <category>") and a Like or Follow button, with no "Thêm bạn bè"/"Add friend" button and no friends count; a company page shows Follow, an industry and a follower count, with no Connect button.
  - Anything else stops before reading (FR-008), so a shape the platforms change later fails closed.
- **Rationale**: these are the public URL forms both platforms use for brand pages; the personal path of spec 030 already uses the same hosts. `profile.php?id=` is how Facebook addresses pages without a vanity name in the new Pages experience; allowing only `id` keeps the query-string surface to one known parameter.
- **Alternatives**: verify on a live fanpage and company page Fio names first (offered; Fio chose to approve the conventions); drop `profile.php?id=` (offered; a page without a vanity name would then need paste or export).

## R2. Where the brand browser rules live

- **Decision**: `references/voice-sources.md` mục 4 splits into "4a. Tài khoản cá nhân" (the current text, unchanged in substance) and "4b. Trang thương hiệu" (the new route: accepted URLs, consent, terms warning, fixed route, website limits, shared platforms, the one click, stops, cap). `references/brand-voice.md` mục 1 points to 4b; `references/voice-profile.md` mục 2 states the brand consent question and points to 4b for the route.
- **Rationale**: one owner for browser behaviour; FR-016 asks for "a brand subsection beside the personal one"; no new file keeps the inventory, adapters and line limits unchanged.
- **Alternatives**: a new `references/brand-pages.md` (one more file to route and package for about 40 lines); putting the route in `brand-voice.md` (splits browser rules across two files).

## R3. Consent question for a brand page

- **Decision**: the one consent question of `references/voice-profile.md` mục 2, filled for a brand page: it names the brand, the exact URL it will open, asks the user to state they may speak for that brand, and says the skill cannot verify that. Example: “Tôi sẽ mở `<URL>` qua trình duyệt và đọc các bài thương hiệu <tên> đã đăng ở đó để tạo toàn bộ hồ sơ giọng thương hiệu để bạn xem lại. Bạn xác nhận mình được nói thay thương hiệu <tên> chứ? Tôi không kiểm được điều này.” One question per URL; with several URLs of the same brand, the second and third questions sit outside the six-question budget (decision 5). For Facebook and LinkedIn, the terms warning stands right before the first consent question of that platform in the run, once per platform (FR-004); no warning for the brand's own website (decision 7).
- **Rationale**: keeps spec 028's single-question gate; the brand name in the question is what the brand-name check (FR-008) compares against.
- **Alternatives**: one consent for all URLs (rejected in review of PR #47: each page is a separate read).

## R4. Website route

- **Decision**: the URL must be a listing page of posts, not the site root (path `/` or empty). The "path prefix" is the listing page's whole path with a `/` appended when missing, so `https://brand.vn/blog` and `https://brand.vn/blog/` both give `/blog/`; a prefix of only `/` counts as the root (security audit 14/11/2026: cutting at the last `/` turned `/blog` into `/`, opening the whole host). Each post page is checked like the first page: a redirect to another host or outside the prefix drops that page. The skill opens only post pages linked from that listing page, on the same host (exact match, `www.` included), whose path starts with that prefix and is longer than it. It does not follow pagination ("Trang 2", "Xem thêm bài"), so a run reads at most the posts one listing page shows. It never opens login, account, contact, search or comment pages, PDFs or any URL with a query string, and never a link from inside a post.
- **Rationale**: decision 6 and FR-005–FR-006; no pagination is the lower bound FR-011 allows and needs no counting rule of its own.
- **Alternatives**: follow pagination up to the cap (more pages opened for little gain over 10–20 posts the route needs); same registrable domain instead of exact host (lets a subdomain the brand does not run in).

## R5. Shared publishing platforms and the brand's own space

- **Decision**: as decision 9. On Medium, Substack, Blogspot, WordPress.com and hosted Ghost, the URL must be the brand's own space (`medium.com/@<brand>`, `<brand>.substack.com`, `<brand>.blogspot.com`, `<brand>.wordpress.com`, `<brand>.ghost.io` or the like) and the space must carry the brand name; the route stays inside it. On news and information sites (VnExpress, Tuổi Trẻ, CafeF, Kenh14 and the like) and forums or community sites (Spiderum, Viblo and the like) the skill stops unless the user gives an official account or channel the brand operates there (forums) or the brand owns the domain (news sites: always stop otherwise). A tag, topic, category or search page is never the brand's own space. A brand domain served by such a platform counts as the brand's own site.
- **Rationale**: decision 9; a tag page on a news site lists articles about the brand written by others.
- **Alternatives**: none open; the list is the owner's.

## R6. Reading bounds on Facebook and LinkedIn

- **Decision**: read the page's own post feed by scrolling; stop at the 80-post cap across the run (FR-011), or when a scroll shows no new brand post. Only "See more" ("Xem thêm") inside the body of a post the brand published may be clicked, once per post; if the click changes the URL, opens a dialog or overlay, or shows comments, read nothing from that view, keep only the text already visible, and do not click again on that post (decision 8, FR-010).
- **Rationale**: matches the personal path's scroll-to-cap rule; the click guard keeps the one allowed action from becoming navigation.
- **Alternatives**: a fixed scroll count (host-dependent and meaningless across page sizes).

## R7. Tests and evidence

- **Decision**: red first: replace the two asserts that pin the old phrases (`tests/test_skill_contract.py:173` "không mở link bằng công cụ trình duyệt hay công cụ tải trang nào" and `:225` "không đưa lựa chọn trình duyệt") with guards for the new rules and run them red before the references change. Add phrase guards for FR-002–FR-010 in a new `test_brand_page_browser_rules`. Behaviour stays manual evidence: calibration block BP01–BP20, run by hand.
- **Rationale**: the repository guards rule text with phrase tests (spec 030 precedent); they prove the text ships, not that an agent follows it.
- **Alternatives**: no new guard (the old asserts would simply be deleted, leaving the new rules unguarded).
