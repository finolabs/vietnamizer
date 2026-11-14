<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/icon-dark.svg">
    <img src="assets/icon.svg" alt="Biểu tượng Vietnamizer: chữ ă" width="88">
  </picture>
</p>

<h1 align="center">Vietnamizer</h1>

<p align="center"><strong>Biên tập tiếng Việt rõ ý, giữ nghĩa và giọng người viết.</strong><br>
Skill cho Claude Code, Codex, Antigravity và các agent đọc được Agent Skills, dùng để rà bản nháp AI, bản dịch sát và văn bản tiếng Việt đọc chưa thuận. Gói chỉ có Markdown, nên mọi quy tắc là hướng dẫn cho agent chứ không có mã nào ép buộc. Agent chọn quy tắc theo thể loại, chỉ sửa khi gọi tên được lỗi và kiểm lại nghĩa trước khi giữ thay đổi.</p>

<p align="center">
  <a href="https://github.com/finolabs/vietnamizer/releases/latest"><img src="https://img.shields.io/github/v/release/finolabs/vietnamizer" alt="Bản phát hành mới nhất"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/finolabs/vietnamizer" alt="Giấy phép: MIT"></a>
  <a href="https://github.com/finolabs/vietnamizer/actions/workflows/validate.yml"><img src="https://github.com/finolabs/vietnamizer/actions/workflows/validate.yml/badge.svg?branch=main" alt="CI"></a>
  <a href="#claude-code-plugin"><img src="https://img.shields.io/badge/Claude%20Code-plugin-7FE2CE" alt="Claude Code plugin"></a>
  <a href="#codex-plugin"><img src="https://img.shields.io/badge/Codex-plugin-7FE2CE" alt="Codex plugin"></a>
  <a href="#antigravity-plugin"><img src="https://img.shields.io/badge/Antigravity-plugin-7FE2CE" alt="Antigravity plugin"></a>
</p>

<p align="center">
  <img src="docs/figures/banner.png" alt="Banner Vietnamizer: câu gốc “Đã tìm khắp nhà nhưng vẫn không tìm chìa khóa.” được sửa thành “… không tìm thấy chìa khóa.”, ca MR04 thiếu bổ ngữ, bản 0.12.1 trên Codex đạt." width="920">
</p>

Tôi viết Vietnamizer riêng cho tiếng Việt chứ không phải dịch lại từ một skill tiếng Anh nào cả. Dù sao
thì các LLM phần lớn được build với rất nhiều data tiếng Anh, ít tiếng Việt, còn những bên làm model cũng
chưa thật sự tập trung vào tokenizer cho tiếng Việt, càng chưa hiểu ngữ nghĩa tiếng Việt. Do đó văn từ,
câu cú AI viết ra thường thô cứng.

Khó nhất là sửa sao cho giữ được trọn vẹn ý nghĩa, nhưng “con người” nhất có thể. Vì vậy, Vietnamizer
mặc định giữ giọng của người viết và chỉ sửa chỗ nó nhận ra pattern lỗi. Khi bạn yêu cầu, nó học giọng văn
của bạn, hoặc của thương hiệu bạn được nói thay, đóng gói thành hồ sơ giọng văn rồi viết theo hồ sơ đó
(README này cũng đã qua tay nó, theo hồ sơ giọng của tôi). Khi học giọng văn của bạn, nó đưa bạn xem bản
nháp hồ sơ và vài đoạn viết thử để cùng hiệu chỉnh. Tôi tin rằng càng kiên nhẫn làm bước này đủ sâu, đủ
kỹ, AI viết càng gần với “người” và với chính bạn hơn. Đó là niềm tin của tôi, chưa phải số đo
([xem giới hạn](#hồ-sơ-giọng-chưa-có-số-đo)), nên bạn vẫn hãy đọc lại từng bản sửa.

**Không cần API key, không gọi dịch vụ ngoài.**

[Cài nhanh](#cài-nhanh) · [Dùng ngay](#dùng-ngay) · [Thiết lập giọng](#thiết-lập-giọng-của-bạn) · [Xem bằng chứng](#bằng-chứng-và-kiểm-thử) · [Tài liệu](#tài-liệu-chi-tiết)

## Vietnamizer hữu ích ở đâu?

| Khi cần | Skill hướng agent làm gì? |
|---|---|
| Rà bản nháp AI hoặc bản dịch sát | Tìm lỗi cụ thể về từ, bổ ngữ và cấu trúc câu |
| Biên tập blog, bài chuyên môn | Giữ ý định, mức khẳng định, câu rút gọn và nhịp dấu câu |
| Rà README, báo cáo, tài liệu công việc | Giữ thuật ngữ và giọng theo thể loại |
| Viết theo giọng của bạn hoặc của thương hiệu | Học hồ sơ giọng từ bài bạn đưa, cho bạn chấm đoạn mẫu, chỉ lưu khi bạn yêu cầu; bắt đầu bằng `/vietnamizer:help` hoặc câu “thiết lập giọng” |

Hãy coi Vietnamizer là một bước biên tập có kiểm soát trước khi gửi hay đăng bài, không phải người kiểm
chứng. Skill không xác minh sự thật trong bài, nên bạn vẫn cần đọc lại những chỗ nó đổi xưng hô, cấu trúc
và dấu câu.

## Cài nhanh

Gõ một lệnh trong terminal, theo host bạn dùng, rồi mở session mới:

Claude Code:

```bash
claude plugin marketplace add finolabs/plugins && claude plugin install vietnamizer@finolabs
```

Codex:

```bash
codex plugin marketplace add finolabs/plugins && codex plugin add vietnamizer@finolabs
```

Antigravity:

```bash
agy plugin install https://github.com/finolabs/vietnamizer
```

Agent khác đọc được Agent Skills:

```bash
npx skills add finolabs/vietnamizer --skill vietnamizer
```

Chỉ chọn một cách, plugin hoặc skill lẻ. Chi tiết từng host ở [Cài đặt theo nền tảng](#cài-đặt-theo-nền-tảng).

## Dùng ngay

1. Nhờ trợ lý AI của bạn cài Vietnamizer từ repo này, hoặc chạy lệnh ở mục [Cài nhanh](#cài-nhanh).
2. Mở session mới. Trên Claude Code, gõ `/vietnamizer:help`; ở host khác, hỏi “Vietnamizer làm được gì?”.
   Bạn sẽ thấy một màn hình giới thiệu bốn việc: biên tập và viết, chọn giọng, học giọng, kiểm giọng.
3. Giao một bản nháp như ví dụ dưới. Bạn nhận lại bản đã biên tập mà dữ kiện và thuật ngữ vẫn nguyên,
   tức là skill đã chạy.

Nói rõ bản nháp dùng cho đâu, ai đọc và phần nào không được đổi. Ví dụ:

```text
Dùng Vietnamizer biên tập bài blog cá nhân dưới đây.
Giữ nguyên ý, mức chắc chắn, thuật ngữ và giọng hiện có.
Không sửa trích dẫn và code. Chỉ trả lại bài đã biên tập.

<draft>Dán bản nháp vào đây.</draft>
```

Prompt tiếng Anh cũng được, ví dụ `Use Vietnamizer to copyedit the Vietnamese draft below for a personal
blog.` Có thể xin thêm bảng trước/sau và lý do từng chỗ sửa.
[Prompt theo tình huống và cách trả kết quả](docs/usage.md).

## Thiết lập giọng của bạn

Phần này là tùy chọn. Chưa có hồ sơ giọng thì Vietnamizer vẫn biên tập như ở mục [Dùng ngay](#dùng-ngay),
và bạn có thể dựng hồ sơ lúc nào cũng được.

Mặc định Vietnamizer giữ giọng sẵn có của bài. Gửi kèm mẫu cũng chưa đổi giọng, trừ khi bạn nói rõ là
muốn viết theo mẫu. Còn muốn skill nhớ giọng qua nhiều lần dùng thì bạn dựng một hồ sơ giọng. Chỉ việc mở
đầu bằng một trong các câu sau là được:

- “Thiết lập giọng.”
- “Học giọng của tôi từ mấy bài này.” (rồi dán bài)
- “Học giọng viết LinkedIn của tôi.”

`/vietnamizer:help` chỉ có trong plugin Claude Code. Trên Codex, Antigravity hay khi cài bằng Skills CLI,
bạn hỏi bằng lời như trên. Các bước bạn sẽ gặp:

1. **Loại giọng.** Cá nhân (giọng của chính bạn, là lựa chọn đề xuất) hoặc Thương hiệu (giọng một thương
   hiệu bạn được nói thay).
2. **Nguồn mẫu.** Dán 10–20 bài bạn tự viết; đưa file export LinkedIn hoặc Facebook bạn tự tải; hoặc để
   skill đọc trang của chính bạn qua trình duyệt, nếu host có công cụ trình duyệt. Với giọng thương hiệu,
   bạn đưa bộ quy chuẩn, tài liệu nội bộ và bài đã đăng; bài đã đăng cũng đọc được từ tối đa ba URL
   fanpage, trang công ty LinkedIn hay blog của thương hiệu.
3. **Đồng ý đọc.** Skill hỏi đúng một câu, gọi tên nguồn sẽ đọc. Với file export hay trang, câu đó hỏi
   luôn tài khoản có phải của bạn không; với thương hiệu, hỏi bạn có được nói thay không. Skill không kiểm
   được những điều này và tin lời bạn. Trước khi đọc Facebook hay LinkedIn qua trình duyệt, skill báo rằng
   điều khoản của hai nền tảng này có thể cấm thu thập tự động.
4. **Xem hồ sơ nháp.** Skill trình toàn bộ hồ sơ: mỗi nét giọng có phạm vi, căn cứ và mức chắc chắn, kèm
   những điểm còn chờ bạn chốt. Bạn sửa tới khi ưng.
5. **Chấm thử.** Chọn từ 0 đến 10 đoạn mẫu; mỗi đoạn bạn chấm Kém, Trung bình, Khá hoặc Tốt. Chọn 0 là bỏ
   qua. Đây là đánh giá của bạn; skill không tự tính điểm giống giọng.
6. **Lưu hay không.** Chỉ lưu khi bạn bảo lưu. Bạn chọn nơi lưu: Orrery hay Obsidian nếu host có công cụ
   tương ứng, không thì một thư mục Markdown (skill gợi ý `~/.agents/vietnamizer/profiles`), và đặt tên
   hồ sơ. Không lưu thì hồ sơ chỉ nằm trong cuộc trò chuyện đó.

Trước bước chấm, skill hỏi không quá sáu câu. Dừng ở bước nào cũng được, và dừng thì không có gì được lưu.

Lần sau, gọi hồ sơ bằng tên kèm chỗ lưu, ví dụ “Viết lại bài này theo hồ sơ `giong-cong-viec` trong
`~/.agents/vietnamizer/profiles`.”
Skill xin đồng ý đọc hồ sơ đó, mỗi lần chỉ áp một hồ sơ và không tự nạp hồ sơ nào ở phiên sau. Hồ sơ không
được đổi nghĩa, mức chắc chắn hay điều kiện của bài.
[Hai chế độ giữ giọng, ví dụ prompt và bảy style card](docs/style-and-voice.md).

## Trước/sau: sửa chỗ cần sửa, giữ chỗ đã đúng

Trích đầu ra thật trên cùng Codex trong lượt hồi quy **0.12.0/0.12.1** ngày 27/10/2026.
Bảng chỉ hiển thị phần liên quan; các bản sau 0.12.1 chưa được đo lại trên những ca này.

| Ca | Bản gốc | Sau biên tập với 0.12.1 |
|---|---|---|
| MR04 · thiếu bổ ngữ | Đã tìm khắp nhà nhưng vẫn không tìm chìa khóa. | Đã tìm khắp nhà nhưng vẫn không tìm **thấy** chìa khóa. |
| MR05 · điểm ngắt có chức năng | Tất cả – chỉ khác là… | Giữ nguyên điểm ngắt; 0.12.0 đã đổi thành dấu phẩy. |
| MR12 · đối tượng đã rõ | Tôi đang soạn hướng dẫn bàn giao. Soạn xong rồi dừng. | Giữ nguyên; 0.12.0 đã thêm “bản hướng dẫn” vào câu sau. |

Ở MR04, ngữ cảnh là đã tìm nhưng chưa thấy. MR05 không có quy chuẩn buộc đổi dấu;
MR12 đã rõ đối tượng từ câu trước. [Xem đủ ca và tiêu chí](specs/018-mr-version-comparison/results.md).

## Bằng chứng và kiểm thử

**Có bằng chứng hồi quy về sửa lỗi và tránh sửa quá tay; chưa có chấm người độc lập.**
Các phép so sánh dưới đây dùng cùng agent biên tập, không xếp hạng Codex với Gemini.

### Hồi quy: hai ca sửa quá tay đã được khắc phục trong lượt đối chiếu

<picture>
  <source media="(max-width: 600px)" srcset="docs/figures/regression-cases-mobile.svg">
  <img src="docs/figures/regression-cases.svg" alt="Cùng Codex: 0.12.0 đạt 10/12 ca, 0.12.1 đạt 12/12; MR05 và MR12 chuyển sang đạt.">
</picture>

**12 ca, 14 tình huống × 2 phiên bản = 28 đầu ra.** MR05 và MR12 chuyển từ chưa đạt sang đạt;
không ca nào chuyển ngược trong lượt này. Đây là tập phát triển đã dùng để sửa skill,
mỗi điều kiện sinh một lần; nhãn do agent đối chiếu và reviewer kiểm tra.
**12/12 không có nghĩa 100% văn bản sẽ được sửa đúng.**
[Xem báo cáo hồi quy](specs/018-mr-version-comparison/results.md).

### Theo giọng mẫu: có tín hiệu tốt, kết quả còn trái chiều

<picture>
  <source media="(max-width: 600px)" srcset="docs/figures/reference-voice-mobile.svg">
  <img src="docs/figures/reference-voice.svg" alt="Pilot 0.13.2 so với prompt dùng cùng mẫu: Codex chấm 5 thắng, 3 hòa; Gemini chấm 3 thắng, 1 hòa, 3 thua và thiếu 1 phiếu.">
</picture>

Cả hai hàng là **model chấm ẩn nhãn**, cùng đánh giá đầu ra do **Codex biên tập**.
So sánh dùng cùng bản gốc, mẫu giọng và yêu cầu theo mẫu. Mỗi hàng có tám nguồn dự kiến;
phiếu V2–Gemini bị loại do trích dẫn sai và giữ ở trạng thái thiếu.

Hai giám khảo đồng ý lựa chọn ở **4/7 nguồn cùng có phiếu**. Corpus đã được dùng để
hiệu chỉnh skill; model chấm không thay thế tác giả hoặc người đọc. Chưa đủ bằng chứng
Vietnamizer luôn tốt hơn prompt thông thường kèm mẫu.
[Xem pilot 0.13.2](specs/025-section-voice-pilot/results.md) · [Phương pháp, dữ liệu và mọi đợt đánh giá](docs/benchmarks.md).

### Hồ sơ giọng: chưa có số đo

Tuyến hồ sơ giọng của 0.15.0 và 0.16.0 có ca kiểm thử viết tay (HG, VM và BP), nhưng agent
chưa chạy các ca đó, nên chưa có bằng chứng hồ sơ giúp bản viết giống giọng hơn. Dạng URL và
dấu hiệu nhận ra fanpage, trang công ty hay blog đi theo quy ước của nền tảng, chưa đối chiếu
trên trang thật. [Xem changelog](docs/changelog.md).

💡 Tôi nghĩ rằng Vietnamizer đáng thử khi bạn cần một quy trình rà tiếng Việt có quy tắc rõ và biết
dừng tay trước khi sửa quá tay. Còn với yêu cầu theo giọng mẫu hay theo hồ sơ, bạn vẫn nên đọc lại từng
bản sửa. Đừng lấy mức đổi ký tự, độ dài hay token làm điểm chất lượng.

## Cho AI agent: cài và thiết lập

Người dùng đưa link repo này và nhờ bạn cài. Làm theo thứ tự:

1. **Xác định host**: Claude Code, Codex, Antigravity hoặc một agent khác đọc được Agent Skills.
2. **Hỏi người dùng trước khi cài.** Plugin áp dụng cho mọi dự án của họ. Chỉ cài một trong hai cách, plugin hoặc skill lẻ, vì cài cả hai thì skill sẽ hiện hai lần.
3. **Kiểm tra bản đã cài**: chạy `claude plugin list` hoặc `codex plugin list`. Nếu `vietnamizer` đã có từ catalog khác (`vietnamizer@vietnamizer` hoặc catalog `Finolabs` cũ), dừng lại và hỏi người dùng; các bước nằm trong [hướng dẫn chuyển](docs/installation.md#codex-plugin).
4. **Cài** bằng lệnh của host:

   | Host | Lệnh |
   | --- | --- |
   | Claude Code | `claude plugin marketplace add finolabs/plugins`, rồi `claude plugin install vietnamizer@finolabs` |
   | Codex | `codex plugin marketplace add finolabs/plugins`, rồi `codex plugin add vietnamizer@finolabs` |
   | Antigravity | `agy plugin install https://github.com/finolabs/vietnamizer` |
   | Agent khác | `npx skills add finolabs/vietnamizer --skill vietnamizer` |

5. **Kiểm tra** `claude plugin list`, `codex plugin list` hoặc `agy plugin list` đã liệt kê `vietnamizer`, rồi báo nguyên văn kết quả cho người dùng, kể cả khi lỗi.
6. **Bàn giao**: nhắc người dùng mở session mới, rồi giao một bản nháp như ví dụ ở mục [Dùng ngay](#dùng-ngay), hoặc nói “thiết lập giọng” nếu muốn dựng hồ sơ giọng ([Thiết lập giọng của bạn](#thiết-lập-giọng-của-bạn)).

Xong khi host liệt kê `vietnamizer` và người dùng biết phải mở session mới.

## Nền tảng hỗ trợ

Gói không phụ thuộc hệ điều hành. Nó chỉ gồm Markdown, không có mã chạy riêng, nên host chạy ở đâu thì
skill chạy ở đó (macOS, Linux hay Windows, tùy host). Script đóng gói trong repo cần Bash và Python 3.

| Host | Cách cài | Ghi chú |
| --- | --- | --- |
| Claude Code | Plugin từ catalog `finolabs/plugins` | Có thêm `/vietnamizer:help` |
| Codex | Plugin từ catalog `finolabs/plugins` | |
| Antigravity | Plugin từ URL repo | Không có catalog |
| Claude web, Claude Desktop, Claude Org | Skill lẻ hoặc marketplace | Xem [Cài đặt](docs/installation.md) |
| Agent khác đọc được Agent Skills | `npx skills add` | |

## Cài đặt theo nền tảng

Bản hiện tại là **0.16.0**. [Tải các gói từ GitHub Release](https://github.com/finolabs/vietnamizer/releases/latest).

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

## Quyền riêng tư

Skill không có mã gọi mạng và không đọc API key. Văn bản bạn giao đi qua host bạn đang dùng, theo chính
sách của host đó. Hồ sơ giọng chỉ được lưu khi bạn yêu cầu rõ, tại nơi bạn chọn.

Đường đọc trang qua trình duyệt chỉ chạy khi host có công cụ trình duyệt và sau câu đồng ý của bạn. Gói
không có mã mạng, nhưng công cụ trình duyệt của host thì mở trang bên ngoài: Facebook, LinkedIn hay
website của thương hiệu. Trước khi đọc Facebook hay LinkedIn, skill cảnh báo rằng điều khoản của Meta và
LinkedIn có thể cấm thu thập tự động. Skill không kiểm được tài khoản có phải của bạn, Trang Facebook có
mang tên bạn hay bạn có quyền nói thay một thương hiệu hay không, nên nó tin lời bạn. Không muốn thì
bạn đừng dùng tuyến hồ sơ giọng, hoặc chọn dán bài. [Chi tiết trong PRIVACY.md](PRIVACY.md).

## Phạm vi

- Tự chọn profile theo thể loại; công văn, hợp đồng, thơ và changelog chỉ rà typography.
- Bảo toàn dữ kiện, thuật ngữ, code và trích dẫn nguyên văn; không suy tác giả AI từ lỗi ngôn ngữ.
- Không gọi dịch vụ ngoài và không đọc API key; Jev/TypeSafe đã gỡ từ 0.14.0.
- Chỉ cung cấp văn bản được phép chia sẻ, không chứa credential hoặc dữ liệu bị hạn chế.

[Xem xử lý dữ liệu](docs/usage.md) · [Quyền riêng tư](PRIVACY.md) · [Báo lỗi bảo mật](SECURITY.md).

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
| Prompt, phạm vi và dữ liệu | [Sử dụng](docs/usage.md) |
| Giữ giọng gốc, theo mẫu, tuyến hồ sơ giọng tùy chọn và chọn phong cách | [Giọng và phong cách](docs/style-and-voice.md) |
| Cây nguồn, các tầng quy tắc và thành phần | [Kiến trúc](docs/architecture.md) |
| Tên và vai trò của từng pattern | [Danh mục 55 pattern](docs/patterns.md) |
| Phương pháp, giới hạn và các kết quả benchmark | [Benchmark](docs/benchmarks.md) |
| Tài liệu tham khảo và mức độ tin cậy | [Nguồn và ghi nhận](docs/sources.md) |
| Thay đổi qua từng phiên bản | [Changelog](docs/changelog.md) |

## Lịch sử phiên bản

- **0.16.0** — Hồ sơ giọng thương hiệu đọc được fanpage Facebook, trang công ty LinkedIn hoặc blog của thương hiệu qua trình duyệt của host, từ tối đa ba URL bạn đưa, mỗi URL một câu đồng ý gọi tên thương hiệu và URL; chỉ đọc thân bài thương hiệu đã đăng, từ chối trang đối thủ, dừng khi trang không mang tên thương hiệu bạn nêu. Trang Facebook mang tên chính bạn học được thành hồ sơ cá nhân sau cảnh báo và xác nhận. Constitution lên 2.6.1. Chưa chạy agent trên các ca mới. [Lịch sử đầy đủ](docs/changelog.md)
- **0.15.0** — Hồ sơ giọng có hai loại, cá nhân (mặc định) và thương hiệu, mỗi lần chỉ áp một; học giọng từ bài dán, file export LinkedIn/Facebook hoặc trang của chính bạn qua trình duyệt (có cảnh báo điều khoản nền tảng); chấm đoạn mẫu bốn mức sau khi học; thêm skill `help` và bước thiết lập; hồ sơ giọng có `ranh giới` và `Điểm chưa quyết`; tên file trong gói đổi sang tiếng Anh (xem bảng trong changelog). Giữ 55 pattern và năm chốt. [Lịch sử đầy đủ](docs/changelog.md)
- **0.14.0** — Gỡ Jev (evaluator TypeSafe): skill không còn gọi dịch vụ ngoài hay đọc API key; gói chỉ gồm Markdown và script đóng gói. Giữ 55 pattern, năm chốt và tuyến hồ sơ giọng opt-in. [Lịch sử đầy đủ](docs/changelog.md)
- **0.13.4** — Thêm tuyến hồ sơ giọng cá nhân tùy chọn (chỉ lưu khi bạn yêu cầu rõ); gói phát hành bỏ `calibration/`; phân phối qua catalog `finolabs/plugins`. Giữ 55 pattern và runtime. [Lịch sử đầy đủ](docs/changelog.md)

## Đóng góp

[Gửi ca sửa sai hoặc góp mã](CONTRIBUTING.md) · [Issues](https://github.com/finolabs/vietnamizer/issues) · [Điều khoản](TERMS.md).

## Giấy phép

MIT. Xem [LICENSE](LICENSE). Fioenix / FINOLABS.
