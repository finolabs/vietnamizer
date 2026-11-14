# Lịch sử phiên bản Vietnamizer

[← README](../README.md)

## Lịch sử phiên bản

### 0.16.0 (14/11/2026)

Spec 031, đọc trang thương hiệu qua trình duyệt: hồ sơ `kind: brand` đọc được trang công khai của thương
hiệu qua công cụ trình duyệt host sẵn có (fanpage Facebook, trang công ty LinkedIn, trang danh sách bài
trên website hay blog riêng của thương hiệu), từ tối đa ba URL người dùng đưa trong một lượt, mỗi URL một
câu đồng ý gọi tên thương hiệu và URL kèm lời khẳng định được nói thay mà skill không kiểm được. Đường đọc
cố định, chỉ thân bài thương hiệu đã đăng, chỉ được bấm “Xem thêm” trong thân bài; từ chối trang đối thủ;
dừng khi trang chuyển hướng, không mang tên thương hiệu người dùng nêu, là trang cá nhân, nằm ngoài không
gian riêng của thương hiệu trên nền tảng dùng chung, hay gặp màn đăng nhập, captcha, tường trả phí, banner
che nội dung hoặc trang chặn. Facebook và LinkedIn có cảnh báo điều khoản, website riêng thì không. Quy tắc
nằm ở `references/voice-sources.md` mục 4b; mục 4a giữ đường tài khoản cá nhân. Dạng URL và dấu hiệu trang
theo quy ước nền tảng, chưa đối chiếu trên trang thật. Substack, Medium, Blogspot và WordPress.com đọc
qua trang danh sách và đường bài riêng của từng nền tảng; Ghost bản host sẵn, diễn đàn và trang cộng đồng
không mở. Fanpage của một
người (nghệ sĩ, người nổi tiếng) không đọc như trang thương hiệu; Trang của chính người dùng học được thành
hồ sơ cá nhân sau cảnh báo và xác nhận (mục 4c); `/vietnamizer:help` có lựa chọn Trang ở bước nguồn của
giọng Cá nhân. Constitution lên 2.5.0 (MINOR): ràng buộc “Tuyến hồ
sơ giọng” thêm nguồn trang thương hiệu, đảo lại quyết định triển khai của spec 030 FR-006; rồi lên 2.6.0
(MINOR): câu về đường đọc cố định nêu đường bài riêng của Substack, Blogspot và WordPress.com; rồi lên 2.6.1
(PATCH): nêu rõ những gì không tính là chuyển hướng: đổi giữa ba host Facebook, chỉ thêm `/` ở cuối, và
`profile.php?id=` sang tên trang. Thêm ca
BP01–BP29, sửa VM05, VM11, VM15, VM31. Chưa chạy agent trên các ca mới; chưa có bằng chứng cải thiện chất
lượng.

Spec 032, gọi lại hồ sơ đã lưu bằng tên: người dùng gõ `/vietnamizer <tên>` hay `/vietnamizer:vietnamizer <tên>`, cùng lệnh ấy với `cá nhân`
(`personal`), `$vietnamizer <tên>` trên Codex, câu “theo hồ sơ <tên>” hoặc “theo giọng của tôi”, và skill
tìm đến chỗ lưu qua sổ hồ sơ `~/.agents/vietnamizer/registry.md`. Sổ chỉ ghi tên, loại, hồ sơ cá nhân mặc
định, kho và vị trí, không chứa nội dung hồ sơ; mỗi dòng chỉ được ghi khi người dùng đồng ý sau lúc lưu.
Lời gọi do người dùng tự gõ là câu đồng ý đọc sổ và đúng một hồ sơ khớp; không khớp thì skill đưa các tên
trong sổ hoặc hỏi vị trí, không dò kho. Sau khi lưu, skill in đúng câu cần gõ lần sau; `/vietnamizer:help`
nêu các dạng câu gọi. Bước lưu không còn đề nghị kho mà quy tắc của host hay chỉ dẫn của người dùng đã cho
ngừng dùng (ví dụ Obsidian). “Theo giọng của tôi” giờ dùng hồ sơ cá nhân mặc định nếu sổ có (đảo ca 5 của
route hồ sơ giọng). Constitution lên 2.7.0 (MINOR): ràng buộc “Tuyến hồ sơ giọng” thêm đường gọi lại qua
sổ. Trên Chat không có file (claude.ai, Desktop, Mobile, Cowork chạy trên cloud), hồ sơ lưu được dưới
dạng bản gọn khoảng 1.200 ký tự trong bộ nhớ của Chat, có câu chặn phạm vi, sau khi người dùng xem đúng
văn bản và đồng ý; host khác không ghi hồ sơ vào bộ nhớ của agent. Tạo hồ sơ không bắt buộc: chưa có hồ
sơ thì skill vẫn sửa bài ngay và nhắc một dòng, tối đa một lần mỗi phiên, tắt được hẳn. Constitution lên
2.8.0 (MINOR) cho bộ nhớ của Chat và lời nhắc. Thêm ca PR01–PR26. Chưa chạy agent trên các ca mới.

Sửa câu chữ sau review 0.15.0, không đổi nghĩa vụ nào:
- Mục 7 của `references/voice-profile.md`: với hồ sơ đã lưu, dòng chấm nằm trong diff từ lý do; khi không
  có diff đó hoặc người dùng bác nó, dòng chấm thành một diff riêng.
- Ca VM30: người dùng bác diff thì vẫn trình lại toàn bộ bản sẽ lưu, có dòng chấm, trước câu hỏi lưu.
- Hợp đồng onboarding: cảnh báo điều khoản LinkedIn và Facebook đứng trước câu xin đồng ý đọc; câu hỏi chủ
  tài khoản hay quyền nói thay thương hiệu nằm trong chính câu đó, như `references/help.md`; lựa chọn trình
  duyệt chỉ hiện cho giọng cá nhân (spec 031 ở trên mở thêm cho giọng thương hiệu).
- Constitution lên 2.4.1: điều khoản file export nêu thêm lời khẳng định được nói thay thương hiệu cho
  export của trang thương hiệu.

### 0.15.0 (14/11/2026)

Spec 030, phần MVP (giọng cá nhân và thương hiệu, nguồn mạng xã hội): hồ sơ có trường `kind`
(`personal` mặc định, `brand`), mỗi lần chỉ áp một hồ sơ và chỉ áp hồ sơ thương hiệu khi được gọi tên;
`references/voice-sources.md` thêm hai nguồn mẫu ngoài dán bài: file export LinkedIn/Facebook người dùng
tự tải, và trang của chính người dùng qua công cụ trình duyệt host sẵn có (cảnh báo điều khoản LinkedIn và Facebook,
không xử lý mật khẩu hay cookie). Constitution lên 2.4.0. Thêm ca VM01–VM15 và fixture tổng hợp. Chưa
chạy agent trên các ca mới; chưa có bằng chứng cải thiện chất lượng.

Spec 030, phần còn lại (giọng thương hiệu, chấm đoạn mẫu, hướng dẫn):
`references/brand-voice.md` dựng hồ sơ `kind: brand` từ bộ quy chuẩn, bài thương hiệu đã đăng và tài
liệu nội bộ người dùng đưa, sau lời xác nhận được nói thay thương hiệu; quy tắc từ bộ quy chuẩn nằm ở mục
mới `Quy tắc thương hiệu`, chỗ bài đăng làm khác quy tắc vào `Điểm chưa quyết`, và hồ sơ không ghi tên
người viết, nhân viên hay khách hàng. Đường trình duyệt vẫn chỉ cho tài khoản cá nhân. Mục 7 của
`references/voice-profile.md` thêm bước chấm đoạn mẫu: hỏi số đoạn (0–10), từng đoạn một với bốn mức Kém,
Trung bình, Khá, Tốt; số lượt chấm chỉ vào mục mới `Lịch sử chấm` khi người dùng lưu, ghi là đánh giá của
người dùng; skill không tự tính điểm giống giọng. Kiểm A/B ẩn chế độ giữ lại như lựa chọn tùy chọn.
Plugin có thêm skill `help` (`/vietnamizer:help`, adapter `.plugin-skills/help/SKILL.md`) trỏ tới
`references/help.md`: hướng dẫn một màn hình và bước thiết lập giọng, không đọc file của người dùng. Thêm ca
VM16–VM33. Chưa chạy agent trên các ca mới; chưa có bằng chứng cải thiện chất lượng.

Đổi tên file và thư mục sang tiếng Anh (nội dung vẫn tiếng Việt, không đổi chữ nào ngoài đường dẫn):
`references/` (`bang-tra-cuu` → `function-words`, `bo-giai-phong-cach` → `style-resolution`,
`giu-giong-tu-mau` → `voice-from-samples`, `han-viet-thuan-viet` → `sino-vietnamese`, `ho-so-giong` →
`voice-profile`, `loi-cau-va-quan-he` → `sentence-structure`, `loi-thieu-tu` → `missing-words`,
`loi-tu-va-loi-dan` → `terms-and-lead-ins`, `nguon-van-phong` → `style-sources`, `phan-tich-giong-viet` →
`voice-analysis`, `quy-trinh-viet` → `writing-workflow`, `thuat-ngu-va-nhat-quan` → `terminology-consistency`);
`profiles/blog-ca-nhan` → `profiles/personal-blog` (style `chuyen-mon-cong-khai` → `public-expertise`,
`ke-trai-nghiem` → `personal-narrative`, `marketing-thuyet-phuc` → `persuasive-marketing`,
`phoi-hop-cong-viec` → `work-coordination`); `profiles/ky-thuat-doanh-nghiep` → `profiles/enterprise-technical`
(`hoc-thuat-phan-tich` → `academic-analysis`, `huong-dan-ky-thuat` → `technical-guide`,
`van-hanh-doanh-nghiep` → `business-operations`); `calibration/ca-kiem-thu` → `test-cases`,
`ghi-chu-ngu-vuc` → `register-notes`. Spec cũ, `calibration/LOG.md`, tài liệu có ngày và các runner benchmark đã
đóng băng (`benchmarks/`, đọc artifact cũ) giữ tên cũ như lịch sử. Người dùng không cần làm gì; ai trỏ thẳng tới đường dẫn file trong gói thì đổi theo bảng trên.

Hồ sơ giọng, học ý tưởng từ một plugin brand voice (viết lại cho tiếng Việt, không chép): mỗi nét ở
Giọng chung, Theo kênh và mục `Nên:` có thể kèm `ranh giới`, là trần khi áp để tránh áp quá tay; mục
`Điểm chưa quyết` (hồ sơ mới luôn có, ghi “Không có.” khi trống) giữ chỗ mẫu mâu thuẫn kèm đề xuất, và đề xuất không được áp cho tới khi người dùng
chốt khi xem bản nháp hoặc qua cập nhật có diff. Hồ sơ `schema: 1` cũ thiếu hai phần này vẫn hợp lệ. Thêm ca
HG01–HG11 và test giữ quy tắc. Chưa chạy agent trên các ca mới; chưa có bằng chứng cải thiện chất lượng.

### 0.14.0 (13/11/2026)

Gỡ Jev (evaluator TypeSafe) khỏi Vietnamizer, theo spec `specs/029-remove-jev/`. Đã bỏ: package `jev/`
(runner, transport, chuẩn bị/coverage, registry 55 pattern), `references/typesafe-advisor.md`,
`scripts/build-jev-registry.py`, đoạn "Evaluator" trong `SKILL.md`, mọi xử lý `register`/ngữ cảnh phong
cách gửi sang evaluator trong tuyến hồ sơ giọng, các benchmark và test chỉ phục vụ Jev, và `eval/guard/`.
Gói phát hành nhỏ hơn khoảng 211KB (chưa nén).

Học từ nghiên cứu một kho skill viết học thuật công khai (ý tưởng viết lại, không chép): thêm `references/thuat-ngu-va-nhat-quan.md` (bảng thuật ngữ, xưng hô, cách viết số và quét lại cho bài dài hoặc nhiều vòng sửa), một câu trong `SKILL.md` về chế độ ghi chú sửa khi người dùng yêu cầu rõ, test giữ bất biến Markdown (`tests/test_skill_contract.py`), script đếm nhất quán tùy chọn ngoài gói (`scripts/check-consistency.py`), ca CN01–CN06 và mẫu ghi chú ngữ vực chưa có số đo (`calibration/ghi-chu-ngu-vuc.md`). Chưa chạy agent trên các ca mới; chưa có bằng chứng cải thiện chất lượng. Năm chốt bảo toàn nghĩa và 55 pattern không đổi; hồ sơ giọng vẫn là tuyến opt-in.

Việc người dùng cần làm: không bắt buộc. Skill không còn đọc `TYPESAFE_API_KEY`; nếu đã đặt key riêng
cho Vietnamizer thì có thể xóa. Agent hoặc script gọi `python3 -B -m jev …` phải bỏ lời gọi đó. Spec cũ,
`calibration/` và `docs/benchmarks.md` còn là hồ sơ lịch sử về Jev, không phải runtime hiện hành.

### 0.13.4 (08/11/2026)

Gói phát hành không còn chứa `calibration/` (nhật ký bằng chứng và ca kiểm thử tay của maintainer, khoảng 140KB, không nạp lúc chạy). `scripts/validate-package.py` vẫn kiểm inventory và quét bí mật `calibration/` trong repo nguồn và từ chối mọi payload phát hành có thư mục này; file `.skill` nén giảm khoảng 20%.

Tuyến hồ sơ giọng cá nhân (opt-in): bổ sung `references/ho-so-giong.md` và `references/phan-tich-giong-viet.md`
để tạo, lưu và áp dụng hồ sơ văn phong có tên từ văn bản người dùng dán hoặc chỉ định. Chỉ đọc mẫu
sau khi người dùng đồng ý rõ ràng; chỉ lưu vào kho do người dùng chọn (Orrery, Obsidian hoặc Markdown
tại đường dẫn bạn chọn, gợi ý `~/.agents/vietnamizer/profiles`) khi được yêu cầu rõ; khi tái sử dụng, chỉ đọc hồ sơ được chỉ định tên.
Giữ nguyên 5 chốt bảo toàn nghĩa, vùng bảo toàn và 55 pattern; không tự động tra cứu hay lưu hồ sơ
trong memory hoặc lịch sử; các tuyến biên tập thông thường không nạp thêm tài liệu.

Phân phối qua catalog chung `finolabs/plugins` (PR #30, sau 0.13.3): thêm manifest Antigravity, bỏ
marketplace riêng của repo. Selector cài đổi từ `vietnamizer@vietnamizer` sang `vietnamizer@finolabs`;
cách chuyển nằm trong [hướng dẫn cài](installation.md#codex-plugin). Nội dung skill không đổi.

Mô tả hiển thị của plugin dùng chung một câu tiếng Việt ở cả ba manifest và catalog, kèm bộ từ khóa thống nhất.

- **0.16.0** — Hồ sơ giọng thương hiệu đọc được fanpage Facebook, trang công ty LinkedIn hoặc blog của thương hiệu qua trình duyệt của host, từ tối đa ba URL bạn đưa, mỗi URL một câu đồng ý gọi tên thương hiệu và URL; chỉ đọc thân bài thương hiệu đã đăng, từ chối trang đối thủ, dừng khi trang không mang tên thương hiệu bạn nêu. Trang Facebook mang tên chính bạn học được thành hồ sơ cá nhân sau cảnh báo và xác nhận. Gọi lại hồ sơ đã lưu bằng `/vietnamizer:vietnamizer <tên>` hay `/vietnamizer:vietnamizer cá nhân` qua sổ hồ sơ; trên Chat lưu bản gọn trong bộ nhớ; tạo hồ sơ không bắt buộc, lời nhắc tắt được hẳn cả trên Chat. Constitution lên 2.8.0. Chưa chạy agent trên các ca mới.
- **0.15.0** — Hồ sơ giọng có hai loại, cá nhân (mặc định) và thương hiệu, mỗi lần chỉ áp một; học giọng từ bài dán, file export LinkedIn/Facebook hoặc trang của chính bạn qua trình duyệt (có cảnh báo điều khoản nền tảng); chấm đoạn mẫu bốn mức sau khi học; thêm skill `help` và bước thiết lập; hồ sơ giọng có `ranh giới` và `Điểm chưa quyết`; tên file trong gói đổi sang tiếng Anh (xem bảng trong changelog). Giữ 55 pattern và năm chốt.
- **0.14.0** — Gỡ Jev (evaluator TypeSafe): skill không còn gọi dịch vụ ngoài hay đọc API key; gói chỉ gồm Markdown và script đóng gói. Giữ 55 pattern, năm chốt và tuyến hồ sơ giọng opt-in.
- **0.13.4** — Thêm tuyến hồ sơ giọng cá nhân tùy chọn, gói phát hành bỏ `calibration/`, phân phối qua catalog `finolabs/plugins`; giữ 55 pattern, runtime Jev và năm chốt.
- **0.13.3** — Rút core thành bộ điều phối, đọc catalog/workflow/mẫu/evaluator theo tác vụ; giữ quy trình ý trước câu và 55 pattern. Thêm review-only, tách nghĩa/cách viết và harness offline gắn review với candidate hiện tại. Giữ API/runtime, metadata và gói cài đồng bộ; chưa có A/B tiếng Việt hoặc actual-read trace chứng minh cải thiện chất lượng/token.

### Chi tiết thay đổi trong 0.13.3

### 31/10/2026 · Review-only và bằng chứng candidate

Làm rõ tuyến chỉ review phải đọc chốt trước nhận xét, dùng đúng workflow/card/mẫu khi xét cả bài;
tách kết luận nghĩa/cách viết, giữ lời ai và nguồn viện dẫn. Adapter gọi core cả khi review.
Bổ sung sáu ca tổng hợp phát triển, kế hoạch heldout riêng chưa có dữ liệu và harness offline
kiểm hash candidate, quote cùng thứ tự receipt trước review. Receipt hợp lệ không chứng thực
agent thực đọc hoặc phán đoán đúng. Nghiên cứu Matt pinned là gợi ý thiết kế, chưa phải hiệu quả.

### 31/10/2026 · Tách tuyến đọc

Core chỉ giữ điều phối/chốt; chuyển nguyên nội dung V/T sang bốn catalog theo nghi vấn, giữ B/K
ở profile. Tuyến sửa nhỏ không nạp workflow bài, resolver, card hoặc guide mẫu; tuyến bài dùng
workflow/card, thêm guide khi có mẫu. Danh mục nguồn và hợp đồng evaluator nạp có điều kiện;
kiểm key/capability trước hợp đồng. Đồng bộ validator/registry với nơi sở hữu mới, không đổi
recipe hay ngưỡng. Source 0.13.3; số đo context là kích thước hướng dẫn,
không phải billing token hoặc bằng chứng chất lượng hành vi.

### 31/10/2026 · Quy trình lập ý trước khai triển

Chung quy trình tách ý có đối chiếu nguồn → chọn giọng → khai triển → kiểm nghĩa hai chiều và đọc câu/đoạn/toàn bài cho viết mới từ brief và biên tập. Outline không thay bản gốc, giữ sắc thái và phạm vi sửa nhỏ; không nhận nháp AI là giọng cá nhân. Phân biệt mẫu cá nhân với tham chiếu chuyên môn nhiều tác giả có xuất xứ; thêm danh mục khởi đầu năm bài, chỉ metadata/link và giới hạn, không tải corpus. Thêm EW01–EW16 để kiểm thủ công; giữ 55 pattern/runtime Jev, không thêm lượt gọi model. Chưa chạy pilot cũ/mới, chưa chứng minh cải thiện văn phong.

### Các phiên bản trước

- **0.13.2** (28/10/2026) – Phân biệt hình thức được phép, có căn cứ mẫu và phù hợp với chức năng phần; chọn đề mục, đại từ và đối chiếu sau khi giữ nghĩa. Không cấm câu hỏi/bạn, không đóng băng bố cục hoặc chia profile theo mỗi đoạn; làm rõ lượng với cách viết số và giữ tình thái khi đổi danh sách. Thêm SF01–SF12 để rà thủ công từ N2và phản ví dụ; giữ55pattern, quy trình skill không thêm lượt gọi model. Pilot025chạy sau đó cho N2tín hiệu tích cực nhưng chưa xác nhận nâng cấp đồng đều; xem báo cáo và phiếu thiếu ở phần giữ giọng.
- **0.13.1** (28/10/2026, mã nguồn chưa phát hành) – Giữ nghĩa trước khi theo mẫu: đối chiếu mệnh đề thêm/bỏ hai chiều, loại chú giải đúng nhưng ngoài nguồn; sửa ví dụ B tự thêm số liệu hoặc đảo/bỏ ý. Rút cách viết số, chức năng đại từ và cấu trúc hỏi có phạm vi; chọn tài liệu trước khi nạp. Thêm MS01–MS16 để rà thủ công từ V1 và các ví dụ sai; giữ 55 pattern, không thêm lượt gọi model. Đã có kiểm offline và gói; pilot023chạy sau đó được báo riêng ở phần giữ giọng, không phải bằng chứng của0.13.2.
- **0.13.0** (28/10/2026, mã nguồn chưa phát hành) – Tách giữ giọng gốc mặc định với theo giọng mẫu khi có yêu cầu rõ và mẫu/hồ sơ dùng được. Cho phép đổi cấu trúc có căn cứ mà giữ mệnh đề, điều kiện, số lượng, thứ tự và vùng bảo toàn; chọn profile theo chức năng văn bản. Thêm VC01–VC12 từ phân tích pilot019và phản ví dụ; không thêm pattern, ngưỡng hoặc lượt gọi model. Chưa chạy lại benchmark để xác nhận hiệu quả.

- **0.12.1** (27/10/2026, mã nguồn chưa phát hành) – Làm rõ giữ ý muốn, khả năng và phạm vi; giữ đối tượng lược/câu ngắn có chủ ý; T2 xét chức năng thay vì mặc định sửa theo mã ký tự. Phân biệt trích dẫn nguyên văn với thuật ngữ được nhấn, rà ứng viên lặp đoạn trong đúng phạm vi. Thêm MR01–MR12 từ phân tích Mindfio và phản ví dụ; đồng bộ tư vấn Jev, không đổi runtime hoặc ngưỡng. Đối chiếu hồi quy trên cùng Codex ghi nhận MR05/MR12 chuyển từ chưa đạt sang đạt; chưa có bằng chứng chất lượng độc lập ngoài tập phát triển.
- **0.12.0** (26/10/2026, mã nguồn chưa phát hành) – Thêm workflow có điều kiện để rút và kiểm đặc tính giọng từ mẫu được giao; phân biệt thói quen với nét thỉnh thoảng, điều cấm với phần chưa quan sát, và đổi giọng với đổi nội dung. Không tự tìm/lưu hồ sơ. Tham khảo thiết kế OSS, có 8 ca đối chiếu tổng hợp; chưa đo hiệu quả khớp giọng bằng model/người chấm.
- **0.11.1** (26/10/2026, mã nguồn chưa phát hành) – Làm rõ chốt bảo toàn hành động khi câu gốc mơ hồ; T2 chỉ cho sửa typography tối thiểu, V19 không tự dịch đồng loạt khi thiếu bằng chứng người đọc. Host vẫn rà core khi tư vấn Jev thiếu hoặc không flag. Thêm 10 ca hồi quy thủ công; chưa chạy đánh giá model sau sửa, không tuyên bố nâng chất lượng đã được kiểm chứng.
- **0.11.0** (23/10/2026) – Runner Jev đọc trọn ghi chú dài và chỉ hỏi những chỗ cần hỏi. Trên một
  ghi chú kỹ thuật khoảng 8.600 từ, bước chuẩn bị không còn vùng `preparation_limit` nào (trước đó
  có 168 vùng). Input có thể đặt số lượt gọi (`evaluation.requests`, từ 1 đến 32) và vùng cần ưu
  tiên (`focus`). Runner lập kế hoạch trước khi gửi và dùng số lượt theo thứ tự: candidate, vùng host
  chỉ định, tín hiệu từ `scripts/scan-tells.sh`, rồi rải đều. Vì vậy 32 lượt gọi chạm tới 32 đơn vị
  thay vì 9. Báo cáo có thêm khối `priority`. Phần chưa chấm vì hết lượt mang lý do
  `budget_exhausted`, thay cho `limit_exceeded`. Một lượt chạy dừng ở phản hồi không hợp lệ thứ ba,
  còn mọi lỗi khác thì dừng ngay. T4 chỉ được hỏi khi câu có `, và`. Pattern nào có **Không flag** loại trừ cả một cấu trúc thì không được hỏi
  trên cấu trúc đó: tiêu đề bỏ qua V2, V3, V5, V11 và V14, dòng nhãn–giá trị bỏ qua V11, trừ khi câu
  có dấu hiệu chuẩn của chính pattern. Dòng nhãn–giá trị gồm nhãn in đậm, danh sách trường và câu có
  nhãn đứng riêng trên dòng. Coverage thêm `excluded_subjects`, `subject_positions` cùng hai lý do
  `sign_absent` và `structure_excluded`. Mục **Không flag** của V11 thêm tiêu đề, dòng nhãn–giá trị,
  ô bảng, chú thích ảnh, mục lục và mục checklist, dựa trên bằng chứng trong `calibration/LOG.md`
  ngày 23/10/2026. Link Markdown có ngoặc đơn trong địa chỉ được chia câu bình thường. CLI báo
  `input_unreadable` khi không đọc được input. Host đang đọc `limit_exceeded` cần chuyển sang
  `budget_exhausted`.

- **0.10.6** (19/10/2026) – Cập nhật hướng dẫn cài đặt, kiểm thử và chuyển đổi hoặc hoàn tác sang
  catalog Codex dùng chung của Finolabs tại `fioenix/agybird` (bản công bố đầu từ `agybird` v0.2.1
  dùng `vietnamizer@agybird`; bản hiệu chỉnh định danh marketplace sau đó đổi tên máy sang đúng
  chữ hoa–thường `Finolabs` với selector `vietnamizer@Finolabs`), đồng thời giữ catalog độc lập
  `vietnamizer@vietnamizer` để tương thích ngược. Không đổi quy tắc biên tập hay hành vi runtime.

- **0.10.5** – Tự tách đoạn/câu từ input nguồn, giữ vị trí và nguyên đoạn/ngữ cảnh;
  đối soát từng câu, pattern và rubric qua nhiều batch. CLI có `prepare` offline, contract v2 phân biệt
  đủ câu trả lời với đủ ngữ cảnh và kiểm đầy đủ; input `sections` cũ vẫn dùng được. Phần mơ hồ hoặc
  vượt giới hạn cục bộ/dịch vụ được báo riêng; không tăng quota hay tự quyết định edit.

- **0.10.0** – Thêm runner Jev 1.14 và registry 55 pattern: tự động thử khi host cấp key và quyền gửi,
  core độc lập khi không có key hoặc dịch vụ lỗi. Kiểm tra riêng từng candidate, giữ năm chốt chặn,
  coverage và trạng thái lỗi trung thực; không tự quyết định edit theo điểm số. Gói cài chứa cùng runtime.

- **0.9.8** – Chuẩn hóa base listing Codex bằng tiếng Anh, giữ bản dịch tiếng Việt và bổ sung
  liên kết hỗ trợ. Làm rõ workflow theo thể loại, ranh giới dữ liệu bị hạn chế và quyền riêng tư;
  phản hồi biên tập không tự cấp quyền ghi nhật ký hiệu chuẩn hoặc sửa skill. Thêm gate metadata
  chặn URL hỗ trợ không an toàn, nội dung vượt giới hạn và bản dịch không hợp lệ. Giữ branding,
  pattern và TypeSafe tùy chọn; phát hành gói không thay thế xét duyệt của Directory.
- **0.9.7** – Đưa `LICENSE` vào cả hai archive, giữ MIT notice cho tooling Spec Kit và chuyển
  generated Codex integration cùng state từng checkout ra khỏi Git tracking. Bổ sung ignore
  hẹp cho tooling local, environment, scratch output và cache; thêm hướng dẫn contributor cùng
  gate CI chặn file tracked bị ignore. Thêm icon SVG sáng/tối, metadata UI, catalog Codex và ZIP plugin chung với
  Claude Code; cả hai dùng một nguồn skill chuẩn. Bổ sung thông tin quyền riêng tư, điều kiện
  sử dụng và kiểm tra asset/metadata trước đóng gói.
  Đổi thương hiệu từ vi-humanizer sang Vietnamizer, đồng bộ định danh skill/plugin/catalog,
  repo và tên gói tải thành `vietnamizer`. Quy tắc biên tập giữ nguyên. Loại CLI advisor khỏi
  ba archive và repo, cùng harness, kiểm thử và dependency SDK của nó; TypeSafe chỉ được tận
  dụng qua skill chính chủ đã có khi hữu ích và người dùng đồng ý gửi dữ liệu. Bỏ tự truy xuất/lưu hồ sơ memory; ảnh README
  dùng Markdown, giữ SVG nền trong suốt và hai biến thể violet/mint đã duyệt.
- **0.9.6** – Đóng gói optional TypeSafe advisor CLI cho host local: probe thật mới xác nhận
  readiness, assess/rank chỉ trả typed signal cho lát cắt V20, còn host Agent giữ quyền quyết định
  và viết câu cuối. Core vẫn chạy không key, không mạng và không SDK; cả `.skill` lẫn ZIP Claude
  Org chứa adapter nhưng không chứa secret hoặc mạo nhận capability của host. README đưa ba ví dụ
  đã hiệu chỉnh và các đường cài trực tiếp từ artifact phát hành lên đầu trang.
- **0.9.5** – Tổ chức hai base profile thành thư mục cha–con: `rules.md` giữ B/K pattern, còn bảy
  style card nằm trong `styles/` của profile tương thích. Gói Claude Org nay hiển thị riêng từng
  phong cách; resolver và bảng tra dùng chung vẫn nằm trong `references/`. Nếu prompt hoặc công cụ
  đang đọc trực tiếp `profiles/blog-ca-nhan.md` hay `profiles/ky-thuat-doanh-nghiep.md`, hãy chuyển
  sang file `rules.md` trong thư mục profile cùng tên.
- **0.9.1** – Sửa cổng typography-only để các thể loại bị giới hạn có thể chạy T1–T6 mà không cần
  một lỗi V đi kèm; tách code, schema, dữ liệu có cấu trúc, bảng tham số, trích dẫn, tên riêng và ví
  dụ thành vùng bảo toàn từng byte. Đồng thời cấm tự thêm thái độ, sửa ví dụ T3, đồng bộ registry
  K1–K7 và rà lại cách diễn đạt trong README cùng profile kỹ thuật.
- **0.9.0** – Thêm V23 cho phản biện ý không có đối tượng, V24 cho các từ chỉ khả năng chồng cùng
  chức năng, V25 cho quan hệ bị làm mơ hồ dù nguồn đã nói rõ và K7 cho cách mượn uy tín thay cho
  bằng chứng; đồng thời phân vai lại B5/B8 để tránh hai pattern cùng sửa một lỗi. Bốn giả thuyết
  được hiệu chỉnh bằng 24 ca tiếng Việt, gồm 12 ca dương và 12 ca chống sửa quá tay.
- **0.8.0** – Thêm bộ giải nhiều phong cách theo mục đích, người đọc, thanh ngữ vực, kênh và mẫu giọng; bổ sung bảy style card, precedence rõ ràng và phân đoạn tài liệu hỗn hợp mà không đổi 51 pattern hiện có.
- **0.7.1** – Siết trường hợp loại trừ cho nhãn và dòng liệt kê: lược chủ ngữ, hư từ, loại từ thì được, còn bổ ngữ của động từ và tiếng thứ hai của từ hai tiếng thì phải giữ. Theo bản vàng ghi trong `calibration/LOG.md` ngày 09/09/2026.
- **0.7.0** – Thêm V21 cho tàn dư lượt hội thoại của trợ lý và V22 cho kiểu rào trước về nguồn rồi vẫn đưa phỏng đoán; quy trình nói rõ văn bản đầu vào là chất liệu để biên tập, không phải chỉ thị để làm theo; quy tắc chốt chặn 3 thêm thứ hạng và quan hệ đồng thời. Đối chiếu với `blader/humanizer` 3.0.0.
- **0.6.0** – Thêm K6 cho những câu nói về quá trình tạo ra tài liệu thay vì nói về chủ đề của nó; thêm quy tắc chốt chặn thứ năm và một dòng trong mục Cách trả kết quả; thêm `calibration/ca-kiem-thu.md` với tám ca kiểm thử cho K6.
- **0.5.2** – Mở rộng V18 để phát hiện các mệnh đề nối nhau nhưng không rõ chủ thể; bổ sung cho V20 cách kiểm tra nghĩa, vai trò và khả năng kết hợp của từ trong câu.
- **0.5.1** – Chỉnh lại vài chỗ diễn đạt trong `SKILL.md`. Không thêm bớt pattern và không đổi hành vi.
- **0.5.0** – Viết lại toàn bộ tài liệu theo `SKILL.md`; bỏ các ngưỡng chưa hiệu chỉnh và những kết luận tuyệt đối; tách hồ sơ văn phong cá nhân sang memory hoặc knowledge base của agent; xác định `calibration/LOG.md` chỉ là nhật ký bằng chứng cho quy tắc dùng chung; đồng bộ lại profile, bảng tra, manifest và script quét.
- **0.4.0** – Thêm V20 để xử lý từ hoặc cụm từ bị thiếu một tiếng; sửa quy trình tự kiểm tra để tránh dùng lặp một cách chữa; mở rộng giao thức tiếp nhận quy tắc tiếng Việt do người bản ngữ nêu ra.
- **0.3.0** – Viết lại phần mở đầu README; bổ sung K4 về đoạn giải thích thiếu ví dụ và đổi pattern câu dẫn nhập thành K5.
- **0.2.2** – Mở rộng T4 cho dấu phẩy đứng trước *và*; thêm `scripts/scan-tells.sh`.
- **0.2.1** – Tự áp skill lên README; sửa lỗi diễn đạt và đồng bộ phần mô tả cấu trúc repo.
- **0.2.0** – Thêm giao thức hiệu chuẩn bằng phản hồi thực tế và `calibration/LOG.md`.
- **0.1.1** – Bổ sung các trường hợp loại trừ cho văn bản doanh nghiệp và thuật ngữ nội bộ.
- **0.1.0** – Bản đầu gồm V1–V19, T1–T6, B1–B17, K1–K4 và hai file tham chiếu.
