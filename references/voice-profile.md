# Xây dựng và dùng hồ sơ giọng

Tuyến này chia theo việc. Đọc file này trước, rồi chỉ đọc phần của việc đang làm:

| Việc | Phần cần đọc | Mục |
|---|---|---|
| Học hồ sơ mới: xin đồng ý đọc, soạn và trình hồ sơ | `references/voice-profile-learn.md` | 2, 3 |
| Lưu hồ sơ đã trình, ghi sổ, in câu gọi lần sau | `references/voice-profile-save.md` | 4 |
| Gọi và áp hồ sơ đã lưu | `references/voice-profile-apply.md` | 5 |
| Cập nhật hồ sơ, chấm đoạn mẫu, kiểm A/B | `references/voice-profile-update.md` | 6, 7 |
| Nhắc tạo hồ sơ khi chưa có, tắt lời nhắc | `references/voice-profile-reminder.md` | 8 |

Số mục dùng chung cho cả tuyến: “mục 5” là mục 5 ở file ghi trong bảng. Việc này dẫn sang việc khác (học
xong thì lưu, gọi xong thì cập nhật) thì đọc phần kia khi tới bước ấy, không đọc trước.

## 1. Chọn đúng tuyến (FR-001, FR-020)

Chỉ mở tuyến này khi người dùng yêu cầu học, xây dựng, cập nhật hoặc áp dụng hồ sơ giọng
viết cá nhân, hoặc dựng, cập nhật hay áp dụng một hồ sơ thương hiệu họ gọi bằng tên. Yêu cầu lưu hồ sơ đã được xem
lại đi tiếp ở mục 4. Không tự mở tuyến vì một
yêu cầu sửa bài thông thường hoặc vì tác vụ có mẫu giọng; giữ tuyến do `SKILL.md` chọn.
Chỉ nạp hướng dẫn phân tích khi xây dựng hồ sơ; dùng lại hồ sơ không cần phân tích lại mẫu.

Hồ sơ ngắn dán thẳng trong yêu cầu biên tập vẫn đi tuyến “Theo mẫu” với `references/voice-from-samples.md`,
không qua tuyến này và không cần câu xin đồng ý đọc. Tuyến này dành cho học, lưu, cập nhật hoặc áp
dụng hồ sơ lấy từ nơi lưu. Lời gọi một hồ sơ đã lưu (`/vietnamizer <tên>` hay `/vietnamizer:vietnamizer <tên>`, `cá nhân`, “theo hồ sơ
<tên>”, “theo giọng của tôi”; mục 5) mở tuyến này để tra sổ hồ sơ. “Theo giọng của tôi” mà sổ không có
hồ sơ cá nhân nào thì tiếp tục biên tập theo giọng hiện có, nói một dòng là sổ chưa có hồ sơ cá nhân, và
không coi việc có hồ sơ là điều kiện để sửa.

### Giọng cá nhân và giọng thương hiệu (spec 030)

Hồ sơ có hai loại, ghi ở trường `kind` của đầu hồ sơ: `personal` (giọng của chính người dùng) và
`brand` (giọng một thương hiệu người dùng được nói thay). Hồ sơ không có `kind` là hồ sơ cá nhân.
Người dùng không nêu giọng thì dùng giọng cá nhân. Đó là giọng hiện có của bản nháp, hoặc hồ sơ cá nhân họ
gọi bằng tên. Chỉ áp hồ sơ thương hiệu khi người dùng gọi đúng tên hồ sơ đó để áp dụng trong yêu cầu hiện tại;
bài chỉ nhắc tới tên thương hiệu thì chưa phải là gọi hồ sơ; hồ sơ thương hiệu
được gọi cho một lời rõ là riêng tư (tin nhắn riêng, thư cho người thân) thì hỏi xác nhận trước.

Dựng hoặc cập nhật hồ sơ thương hiệu thì đọc thêm `references/brand-voice.md`, gồm tài liệu nhận được, lời
xác nhận được nói thay thương hiệu, cách tách quy tắc khỏi nét quan sát và phần phải lược.

Mỗi lần dùng chỉ áp một hồ sơ. Yêu cầu gọi hai hồ sơ trở lên thì hỏi người dùng chọn một rồi mới
sửa; không trộn nét của hai hồ sơ vào cùng một bài. Khi đã áp hồ sơ, nói ngắn trong câu trả lời đã
dùng hồ sơ nào.

### Tên hồ sơ và slug

Slug lấy từ tên do người dùng chọn, chỉ gồm chữ ASCII thường, chữ số và dấu gạch nối, tối đa 40 ký tự.
Bỏ dấu tiếng Việt và đổi `đ` thành `d` trước khi lọc (ví dụ “Giọng công việc” thành `giong-cong-viec`).
Có thể chuyển tên thành slug bằng tay; không lấy slug từ mẫu. File hồ sơ Markdown luôn tên `<slug>.md`.
