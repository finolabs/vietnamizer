<!--
Sync Impact Report
- Version change: 2.4.1 -> 2.5.0 (MINOR: the voice-profile constraint gains a source, public brand
  pages read through the host browser for `kind: brand`; no principle's obligation is removed).
- Owner approval: 2026-11-14, Fio approved the "Constitution amendment" text of spec 031
  (`specs/031-brand-page-browser/spec.md`), applied verbatim as the first sentence of the constraint.
- Modified constraint "Tuyến hồ sơ giọng": a `kind: brand` profile may also read the brand's public
  page (Facebook fanpage, LinkedIn company page, listing page on the brand's own website or blog)
  through the host browser tool, from at most three URLs the user gives per run, each after a consent
  question naming the brand and the URL with the authority statement; the route is fixed, reads only
  brand post bodies, opens no comments, messages, reviews or follower lists, records no staff names,
  and stops on a redirect or a brand-name mismatch. The rest of the constraint is unchanged.
- Reversal (replaces the pending line of 2.4.1): the 2026-11-13 implementation choice of spec 030
  FR-006, "brand pages are not read through the browser", is reversed by the owner on 2026-11-14
  (spec 031 settled decision 1).
- Principle V unchanged: the package still ships no network code; the brand browser path uses a host
  tool and the route works without it.
- No meaning-preservation chốt, protected span or pattern changed.
- Previous amendment: 2.4.0 -> 2.4.1 (below).
- Version change: 2.4.0 -> 2.4.1 (PATCH: wording only, no obligation added or removed).
- Owner approval: 2026-11-14, Fio's go on the parked follow-ups of release 0.15.0.
- Clarified constraint "Tuyến hồ sơ giọng": the export clause also names the brand authority
  statement for a brand page's export, as `references/brand-voice.md` already requires (security
  review LOW, PR #43).
- Previous amendment: 2.3.0 -> 2.4.0, spec 030 (below).
- Version change: 2.3.0 -> 2.4.0 (MINOR: the voice-profile constraint gains two sources and a
  stored user rating; no other principle's obligation changes).
- Owner approval: 2026-11-13, spec 030 settled decisions 3, 5 and 7 ("Tao muốn Vietnamizer hỗ trợ
  cả brand voice và personal voice", learning from LinkedIn/Facebook, "Lưu cả điểm vào hồ sơ").
- Reason: users learn their voice from their own social posts and teams keep a brand voice.
- Modified constraint "Tuyến hồ sơ giọng": samples may also come from a platform export the user
  supplies or from the user's own page through a browser tool the host offers, after consent and
  an ownership statement; a profile of `kind: brand` may draw on material by several authors after
  the user states they may speak for the brand; the user's own ratings may be stored in their
  profile, while the skill never scores voice similarity itself.
- Now used (2026-11-13, spec 030 US3–US4): `references/brand-voice.md` relies on the brand
  multi-author allowance (after the user states they may speak for the brand; no author, staff or
  customer names stored), and `references/voice-profile.md` mục 7 relies on stored ratings (one
  `Lịch sử chấm` line per saved session, labelled as the user's judgement; the skill computes no
  similarity score). The browser source stays limited to the user's own personal account; brand
  pages are not read through the browser or any fetch tool (implementation choice 2026-11-13,
  pending the owner's confirmation; spec FR-006).
- Browser rules aligned with `references/voice-sources.md` (2026-11-13 review): no captcha, no
  like/comment/post/send, no account settings change; stop on a login wall, another account, a
  captcha or a rate-limit page.
- Principle V unchanged: the package still ships no network code; the browser path uses a host
  tool and the route works without it.
- No meaning-preservation chốt, protected span or pattern changed.
- Previous amendment: 2.2.0 -> 2.3.0, spec 029 (Jev removed).
-->
# Constitution của vi-humanizer

## Core Principles

### I. Bằng chứng tiếng Việt đứng trước convention

Mỗi quy tắc MUST mô tả một lỗi tiếng Việt cụ thể, giải thích vì sao đó là lỗi, nêu cách sửa
và chỉ rõ khi nào MUST NOT flag. Quy tắc từ humanizer tiếng Anh, nhận định chung về model và
lựa chọn phong cách không tự trở thành bằng chứng. Nguồn bên ngoài MUST được ghi trong
`README.md` đúng với mức độ tin cậy; suy luận MUST được gọi đúng là suy luận.

### II. Giữ nghĩa và giọng trước khi làm câu hay hơn

Mỗi edit MUST giữ dữ kiện, chủ thể, thời điểm, quan hệ nhân quả, mức chắc chắn, mức cam kết,
thứ tự, quan hệ đồng thời, thể loại và giọng ổn định của bản gốc, trừ khi yêu cầu hiện tại của
người dùng chủ động thay đổi một yếu tố. Sửa lỗi ngôn ngữ MUST gọi tên được pattern và loại trừ mục **Không flag**. Khi người dùng
chủ động yêu cầu theo giọng mẫu, điều chỉnh phong cách MAY đổi cấu trúc câu đúng nếu có căn cứ
trong mẫu đúng phạm vi và giữ mọi bất biến về nghĩa, thể loại cùng vùng bảo toàn. Điều chỉnh
này MUST được phân biệt với sửa lỗi; có mẫu đơn thuần không cấp quyền chuyển giọng. Edit thiếu
căn cứ tương ứng MUST bị bỏ hoặc chuyển cho người xem. Bản trôi chảy nhưng đổi nghĩa vẫn là lỗi.

### III. Tách quy tắc chung khỏi profile thể loại

V-series và T-series trong `SKILL.md` MUST chỉ chứa những lỗi áp dụng được trên mọi thể loại
mà cổng đầu vào cho phép. Phán đoán phụ thuộc thể loại, người đọc hoặc thanh ngữ vực MUST nằm
trong profile tương ứng. Chỉ được chuyển pattern qua ranh giới này khi có bằng chứng gắn nhãn,
các ca chống sửa quá tay và thay đổi đồng bộ trong inventory của `README.md`.

### IV. Hiệu chỉnh từ bằng chứng có nhãn

Mọi thay đổi quy tắc dùng chung MUST bắt đầu từ bằng chứng ở đơn vị nhỏ nhất còn đủ nghĩa:
đoạn gốc, edit đề xuất, ngữ cảnh, phán đoán mong đợi, nguồn nhãn và pattern liên quan. Sở thích
cá nhân MUST nằm trong hồ sơ riêng của đúng người dùng, không nằm trong calibration log dùng
chung. Ngưỡng số MUST được chọn trên tập phát triển có nhãn và đánh giá trên tập holdout tách
biệt; cùng một ca MUST NOT vừa dùng để chỉnh ngưỡng vừa dùng để chứng minh ngưỡng.

### V. Giữ skill Markdown tự đứng được

`SKILL.md` và các profile MUST dùng được mà không cần build, dịch vụ mạng, secret hoặc runner. Gói
phát hành MUST NOT chứa mã gọi dịch vụ ngoài hay đọc API key, và MUST NOT phụ thuộc một repo local khác.
Evaluator ngoài (Jev/TypeSafe) đã bị gỡ theo quyết định owner ngày 13/11/2026; thêm lại cần amendment.

## Ràng buộc về gói và dữ liệu

- `SKILL.md` là nguồn chuẩn cho workflow, V-series và T-series.
- Số hiệu V, T, B và K MUST liên tục. Khi thêm, bỏ hoặc đổi số pattern, `README.md` MUST đổi
  trong cùng commit.
- `metadata.version` trong `SKILL.md`, mục lịch sử mới nhất của `README.md` và
  `.claude-plugin/plugin.json` MUST giống nhau.
- Giới hạn dòng giữ nguyên: `SKILL.md` 550, profile blog 320, profile kỹ thuật 220.
- Tuyến hồ sơ giọng trong `SKILL.md` MAY tạo và dùng lại hồ sơ có tên từ văn bản người dùng dán
  hoặc chỉ định trong tác vụ, từ file export nền tảng người dùng tự đưa, hoặc từ trang của chính
  người dùng qua công cụ trình duyệt host sẵn có, sau câu đồng ý đọc và lời khẳng định chủ tài
  khoản (với file export của trang thương hiệu: lời khẳng định được nói thay thương hiệu). Với
  hồ sơ `kind: brand`, tuyến MAY đọc thêm trang công khai của thương hiệu qua công cụ trình
  duyệt đó (fanpage Facebook, trang công ty LinkedIn, hoặc trang danh sách bài trên website hay
  blog riêng của thương hiệu), từ tối đa ba URL người dùng đưa trong một lượt, mỗi URL sau một
  câu đồng ý đọc gọi tên thương hiệu và URL cùng lời khẳng định được nói thay thương hiệu đó;
  trang của thương hiệu người dùng được nói thay không phải trang của người khác. Đường đọc ấy
  MUST cố định: chính trang đó và mục bài đăng của nó, với website thêm các trang bài cùng host,
  dưới tiền tố đường dẫn của trang danh sách (trang danh sách không phải trang gốc); MUST NOT
  theo link nào khác; chỉ đọc thân bài thương hiệu đã đăng; MUST NOT mở bình luận, tin nhắn,
  đánh giá hay danh sách người theo dõi; MUST NOT ghi tên nhân viên; và MUST dừng khi trang
  chuyển hướng sang trang hay host khác hoặc không mang tên thương hiệu người dùng nêu. Tuyến
  MUST NOT lấy mẫu qua connector khác, MUST NOT đọc trang của người khác, kể cả trang thương
  hiệu người dùng không được nói thay, và MUST NOT xử lý mật khẩu, cookie hay token. Trên trình duyệt, skill MUST giữ các điều cấm: không giải
  captcha; không bấm thích, bình luận, đăng hay gửi; không đổi cài đặt tài khoản; và MUST dừng khi
  gặp màn đăng nhập, tài khoản khác, captcha hoặc trang giới hạn truy cập. Hồ sơ `kind: brand` MAY dùng tài liệu của nhiều người viết sau
  khi người dùng khẳng định được nói thay thương hiệu; dữ liệu riêng vẫn phải được lược. Hồ sơ MAY
  lưu số lượt người dùng tự chấm, ghi rõ là đánh giá của người dùng; skill MUST NOT tự tính điểm
  giống giọng. Hồ sơ MUST chỉ được lưu
  khi người dùng yêu cầu rõ, tại kho hoặc đường dẫn do họ chọn. Skill MUST NOT tự tìm hồ sơ
  hoặc mẫu trong memory hay lịch sử; chỉ đọc hồ sơ người dùng dán hoặc chỉ định. Ngoại lệ lưu
  này MUST giữ nguyên năm chốt và vùng bảo toàn trong `SKILL.md`; sở thích cá nhân MUST nằm
  trong hồ sơ riêng của đúng người dùng, MUST NOT ghi vào `calibration/LOG.md`.
- Production evaluator MUST chỉ gửi phần văn bản cần cho phán đoán. Raw prose MUST NOT xuất
  hiện trong telemetry hoặc báo cáo health. Lọc credential không thay thế cho phân loại dữ liệu
  và tối thiểu hóa trường gửi đi.
- Mọi kết quả eval MUST ghi model version và corpus version. Judgment run tạo trước khi fit policy
  MUST ghi evaluation-config version và MUST ghi `policy_version=null`; report hoặc run áp dụng
  policy MUST ghi decision-policy version. Typed output chỉ đảm bảo interface, không chứng minh
  phán đoán là đúng.

## Cổng phát triển và phát hành

1. Hành vi mới bắt đầu từ một ca kiểm thử đỏ và test được độc lập. Parsing, tính toán và policy
   tất định nằm trong code; model chỉ làm phán đoán ngữ nghĩa.
2. Mỗi task MUST tạo một deliverable review được và có verification riêng. Checkbox không kèm
   output mới của lệnh kiểm tra không phải bằng chứng.
3. Behavioral eval MUST báo harmful-edit recall, valid-edit false-block rate, review rate, lỗi
   dịch vụ, latency và cost. Số lượt guard bắn chưa chứng minh guard đúng.
4. Không có evaluator ngoài trong gói. Agent MUST kiểm năm chốt chặn trước khi giữ edit; không có
   policy số tự động quyết định edit. Quyết định owner ngày 16/10/2026 trong spec 007 (nhánh có key
   tự động thử Jev) bị thay thế bởi quyết định ngày 13/11/2026 và chỉ còn là lịch sử.
5. Trước khi phát hành, MUST chạy và đọc output của `python3 scripts/validate-package.py`,
   `npx skills add . --list` và `claude plugin validate .`. Sau đó cài lại gói cho mọi runtime
   đang dùng bản chép và đối chiếu bytes đã cài.

## Governance

Constitution này chi phối spec, plan và implementation trong repo. `AGENTS.md` vẫn là hợp đồng vận
hành; nếu hai tài liệu xung đột thì MUST dừng và giải quyết trước khi làm tiếp. Mỗi amendment cần
lý do bằng văn bản, impact report, owner approval và semantic version bump: MAJOR khi thay đổi
không tương thích một principle, MINOR khi thêm hoặc mở rộng governance, PATCH khi chỉ làm rõ.
Mọi spec và review MUST kiểm tra các principle này. Complexity không truy ngược được tới outcome
hoặc acceptance criterion MUST bị bỏ.

**Version**: 2.5.0 | **Ratified**: 2026-09-26 | **Last Amended**: 2026-11-14
