# Vietnamizer

![Vietnamizer — Giúp AI viết tiếng Việt giống con người hơn.](assets/wordmark.svg#gh-light-mode-only)
![Vietnamizer — Giúp AI viết tiếng Việt giống con người hơn.](assets/wordmark-dark.svg#gh-dark-mode-only)

> **Biên tập tiếng Việt rõ ý, giữ nghĩa và giọng người viết.**

Vietnamizer hướng dẫn Claude, Codex và các agent tương thích biên tập tiếng Việt:
tìm câu thiếu từ, cách diễn đạt gượng hoặc cấu trúc dịch sát, rồi sửa theo thể loại.
Mỗi chỗ sửa đều phải được đối chiếu với bản gốc để tránh làm đổi ý.

**Dùng được ngay, không cần API key.** Skill mặc định giữ giọng bản gốc. Nếu muốn viết
theo mẫu, hãy nói rõ yêu cầu và gửi mẫu kèm theo. Khả năng này vẫn cần được kiểm chứng thêm.

[Cài nhanh](#cài-nhanh) · [Xem bằng chứng](#bằng-chứng-và-kiểm-thử) · [Dùng ngay](#dùng-ngay) · [Tài liệu](#tài-liệu-chi-tiết)

## Vietnamizer hữu ích ở đâu?

| Khi cần | Skill hướng agent làm gì? |
|---|---|
| Rà bản nháp AI hoặc bản dịch sát | Tìm lỗi cụ thể về từ, bổ ngữ và cấu trúc câu |
| Biên tập blog, bài chuyên môn | Giữ ý người viết, độ chắc chắn của lời nói, câu rút gọn và nhịp dấu câu |
| Rà README, báo cáo, tài liệu công việc | Giữ thuật ngữ và giọng theo thể loại |
| Biên tập theo giọng mẫu | Học cách diễn đạt từ mẫu, kiểm tra xem bản sửa có thêm, bỏ hoặc đổi ý không |

Có thể dùng Vietnamizer để rà bài trước khi gửi hoặc xuất bản. Vẫn cần đọc lại những chỗ
đổi xưng hô, cấu trúc câu và dấu câu. Skill không kiểm chứng các thông tin trong bài.

## Trước/sau: sửa chỗ cần sửa, giữ chỗ đã đúng

Trích đầu ra thật trên cùng Codex trong lượt hồi quy **0.12.0/0.12.1** ngày 27/10/2026.
Bảng chỉ hiển thị phần liên quan; kết quả này không phải phép đo mới cho 0.13.2.

| Ca | Bản gốc | Sau biên tập với 0.12.1 |
|---|---|---|
| MR04 · thiếu bổ ngữ | Đã tìm khắp nhà nhưng vẫn không tìm chìa khóa. | Đã tìm khắp nhà nhưng vẫn không tìm **thấy** chìa khóa. |
| MR05 · điểm ngắt có chức năng | Tất cả – chỉ khác là… | Giữ nguyên điểm ngắt; 0.12.0 đã đổi thành dấu phẩy. |
| MR12 · đối tượng đã rõ | Tôi đang soạn hướng dẫn bàn giao. Soạn xong rồi dừng. | Giữ nguyên; 0.12.0 đã thêm “bản hướng dẫn” vào câu sau. |

Ở MR04, ngữ cảnh là đã tìm nhưng chưa thấy. MR05 không có quy chuẩn buộc đổi dấu;
MR12 đã rõ đối tượng từ câu trước. [Xem đủ ca và tiêu chí](specs/018-mr-version-comparison/results.md).

## Bằng chứng và kiểm thử

**Các ca kiểm thử cho thấy một số lỗi sửa quá tay đã được khắc phục. Chưa có đánh giá độc lập từ người đọc.**
Các phép so sánh dưới đây dùng cùng agent biên tập, không xếp hạng Codex với Gemini.

### Hồi quy: hai ca sửa quá tay đã được khắc phục trong lượt đối chiếu

<picture>
  <source media="(max-width: 600px)" srcset="docs/figures/regression-cases-mobile.svg">
  <img src="docs/figures/regression-cases.svg" alt="Cùng Codex: 0.12.0 đạt 10/12 ca, 0.12.1 đạt 12/12; MR05 và MR12 chuyển sang đạt.">
</picture>

**12 ca, 14 tình huống × 2 phiên bản = 28 đầu ra.** MR05 và MR12 chuyển từ chưa đạt sang đạt;
không ca nào chuyển ngược trong lượt này. Các ca này cũng đã được dùng để sửa skill, nên chưa cho biết kết quả trên văn bản mới.
Mỗi tình huống chỉ chạy một lần với từng phiên bản; agent đối chiếu kết quả và một agent khác rà lại.
**12/12 không có nghĩa 100% văn bản sẽ được sửa đúng.**
[Xem báo cáo hồi quy](specs/018-mr-version-comparison/results.md).

### Theo giọng mẫu: có tín hiệu tốt, kết quả còn trái chiều

<picture>
  <source media="(max-width: 600px)" srcset="docs/figures/reference-voice-mobile.svg">
  <img src="docs/figures/reference-voice.svg" alt="Pilot 0.13.2 so với prompt dùng cùng mẫu: Codex chấm 5 thắng, 3 hòa; Gemini chấm 3 thắng, 1 hòa, 3 thua và thiếu 1 phiếu.">
</picture>

Codex và Gemini ở đây là **hai model chấm bài**, không biết bản sửa dùng chế độ nào.
Tất cả bản sửa đều do **cùng Codex biên tập**, với cùng bản gốc, mẫu giọng và yêu cầu theo mẫu.
Mỗi model được giao tám nguồn; phiếu V2 của Gemini bị loại vì trích dẫn sai, nên còn thiếu một phiếu.

Hai model chọn giống nhau ở **4/7 nguồn có đủ phiếu**. Bộ văn bản này đã được dùng để
điều chỉnh skill; điểm do model chấm cũng không thay thế nhận xét của tác giả hoặc người đọc.
Kết quả chưa cho thấy Vietnamizer luôn tốt hơn một prompt thông thường có cùng mẫu giọng.
[Xem pilot 0.13.2](specs/025-section-voice-pilot/results.md) · [Phương pháp, dữ liệu và mọi đợt đánh giá](docs/benchmarks.md).

Vietnamizer đáng thử nếu cần rà lỗi diễn đạt và hạn chế những thay đổi không cần thiết.
Riêng việc viết theo giọng mẫu, vẫn cần đọc lại từng bản sửa. Bài ngắn hơn, đổi nhiều chữ hơn
hay dùng ít token hơn đều chưa đủ để kết luận chất lượng tốt hơn.

## Cài nhanh

Bản hiện tại là **0.13.2**. [Tải các gói từ GitHub Release](https://github.com/finolabs/vietnamizer/releases/latest).

### Skills CLI

```bash
npx skills add finolabs/vietnamizer --skill vietnamizer
```

### Codex plugin

```bash
codex plugin marketplace add finolabs/plugins
codex plugin add vietnamizer@finolabs
```

Đã đăng ký catalog `Finolabs` cũ hoặc `vietnamizer@vietnamizer`? Đọc
[hướng dẫn chuyển](docs/installation.md#codex-plugin) trước khi đổi đăng ký.
**Finolabs** là catalog dùng chung; không phải chứng nhận từ OpenAI.

### Claude Code plugin

```bash
claude plugin marketplace add finolabs/plugins
claude plugin install vietnamizer@finolabs
```

### Antigravity plugin

```bash
agy plugin install https://github.com/finolabs/vietnamizer
```

Mở session mới sau khi cài. [Claude web/Desktop, Claude Org, cài thủ công và đóng gói](docs/installation.md).

## Dùng ngay

Gọi `Vietnamizer`, gửi bản nháp và cho biết bài viết dành cho ai, thuộc thể loại nào,
có phần nào cần giữ nguyên. Ví dụ:

```text
Use Vietnamizer to copyedit the Vietnamese draft below for a personal blog.
Preserve its meaning, level of certainty, terminology and existing voice.
Keep quotations and code unchanged. Return only the edited article.

<draft>Paste your draft here.</draft>
```

Có thể yêu cầu bảng trước/sau và lý do thay đổi. [Prompt theo tình huống và cách trả kết quả](docs/usage.md).

## Giữ giọng khi có mẫu

Nếu chỉ gửi mẫu mà không yêu cầu đổi giọng, skill vẫn giữ giọng bản gốc. Muốn biên tập
theo mẫu, hãy nói rõ và gửi mẫu hoặc bản mô tả giọng văn trong cùng yêu cầu. Skill có thể
đổi cách diễn đạt và cấu trúc câu, nhưng phải giữ đủ ý, điều kiện, mức độ chắc chắn
và những phần được yêu cầu giữ nguyên.

Skill không tự tìm hay lưu hồ sơ cá nhân, cũng không bịa trải nghiệm cho người viết.
[Xem hai chế độ, ví dụ prompt và bảy style card](docs/style-and-voice.md).

## Phạm vi

- Tự chọn profile theo thể loại; công văn, hợp đồng, thơ và changelog chỉ rà typography.
- Bảo toàn dữ kiện, thuật ngữ, code và trích dẫn nguyên văn; không suy tác giả AI từ lỗi ngôn ngữ.
- Nếu môi trường chạy có API key và cho phép gửi văn bản, skill tự động thử dùng Jev để hỗ trợ rà lỗi. Không có key hoặc dịch vụ lỗi thì vẫn biên tập bằng quy tắc Markdown.
- Chỉ cung cấp văn bản được phép chia sẻ, không chứa credential hoặc dữ liệu bị hạn chế.

[Xem xử lý dữ liệu và Jev](docs/usage.md) · [Quyền riêng tư](PRIVACY.md) · [Báo lỗi bảo mật](SECURITY.md).

## Danh mục pattern

| Nhóm | Số lượng | Phạm vi |
|---|---:|---|
| V1–V25 | 25 | Cách dùng từ và cấu trúc câu |
| T1–T6 | 6 | Typography |
| B1–B17 | 17 | Blog, bài cá nhân, nội dung công việc và marketing |
| K1–K7 | 7 | Tài liệu kỹ thuật, doanh nghiệp và học thuật |

**55 pattern.** [Danh mục đầy đủ](docs/patterns.md); quy tắc chuẩn nằm trong `SKILL.md` và `profiles/`.

## Tài liệu chi tiết

| Cần tìm | Tài liệu |
|---|---|
| Cài đặt theo nền tảng, marketplace và đóng gói | [Cài đặt](docs/installation.md) |
| Prompt, phạm vi, dữ liệu và tư vấn Jev | [Sử dụng](docs/usage.md) |
| Giữ giọng gốc, theo mẫu và chọn phong cách | [Giọng và phong cách](docs/style-and-voice.md) |
| Cây nguồn, các tầng quy tắc và thành phần | [Kiến trúc](docs/architecture.md) |
| Tên và vai trò của từng pattern | [Danh mục 55 pattern](docs/patterns.md) |
| Phương pháp, giới hạn và các kết quả benchmark | [Benchmark](docs/benchmarks.md) |
| Tài liệu tham khảo và mức độ tin cậy | [Nguồn và ghi nhận](docs/sources.md) |
| Thay đổi qua từng phiên bản | [Changelog](docs/changelog.md) |

## Lịch sử phiên bản

- **0.13.2** (28/10/2026) — Ưu tiên giữ nghĩa, chọn nét giọng theo chức năng từng phần; không mặc định cấm câu hỏi hay “bạn”. [Lịch sử đầy đủ](docs/changelog.md).

## Đóng góp

[Gửi ca sửa sai hoặc góp mã](CONTRIBUTING.md) · [Issues](https://github.com/finolabs/vietnamizer/issues) · [Điều khoản](TERMS.md).

## Giấy phép

Fioenix / FINOLABS · [Giấy phép MIT](LICENSE).
