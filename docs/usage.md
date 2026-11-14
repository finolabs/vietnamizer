# Sử dụng, phạm vi và dữ liệu

[← README](../README.md)

## Dùng ngay

Gọi skill rồi dán đoạn cần sửa ngay bên dưới. Cài qua plugin Claude Code thì lệnh là `/vietnamizer:vietnamizer`.

```text
/vietnamizer

[văn bản cần biên tập]
```

Muốn sửa thẳng trên file thì bạn nêu rõ phạm vi, để agent biết phần nào không được đụng tới:

```text
Dùng vietnamizer để sửa phần văn xuôi trong docs/bai-viet.md.
Giữ nguyên code, bảng tham số và các trích dẫn.
```

Không cần hồ sơ giọng hay bước thiết lập nào. Mặc định, Vietnamizer giữ giọng sẵn có của bản bạn
đưa và chỉ sửa chỗ có lỗi.

### Viết từ ý hoặc biên tập bản có sẵn

Cả hai việc đều đi qua bốn bước: tách ý, chọn giọng, khai triển, rồi rà lại nghĩa và cách viết.
Biên tập thì lấy ý từ bản gốc đầy đủ; viết mới thì lấy từ brief hoặc dữ kiện được giao. Outline
không thay được nguồn đối chiếu, và bạn không cần đưa qua một nháp AI trung gian. Người đọc, mục
đích và phạm vi ảnh hưởng tới cách viết thì nên nói rõ. Thiếu mẫu giọng không có nghĩa là skill
được tự tìm hồ sơ hay bịa trải nghiệm.

```text
Dùng Vietnamizer viết một thông báo cho nhóm phát triển từ các ý sau:
- Bản thử mở thứ Hai, tối đa 20 người.
- Chưa chốt ngày kết thúc.
Giọng ngắn gọn cho công việc. Không tự thêm giờ, hạn chót hoặc lời hứa.
Chỉ trả thông báo cuối.
```

Chỉ sửa một cụm hay một câu thì skill chỉ làm trong đúng phạm vi đó. Nó đọc đoạn xung quanh để hiểu,
không tự viết lại cả bài. Giao biên tập toàn bài thì skill tách ý và sắc thái trước khi chọn cách
diễn đạt, và không mặc định phải thay mọi câu. Bản tách ý không phải đầu ra bắt buộc.

### Ba prompt dùng thử trên Claude

Dán từng prompt bên dưới sau khi chọn skill Vietnamizer. Với Claude Code, thêm
`/vietnamizer:vietnamizer` trước prompt. Đây là mẫu thử và tiêu chí mong đợi, không phải cam kết
mọi lần chạy model sẽ trả cùng một câu.

1. **Hoàn chỉnh ý:** “Sửa câu sau trong bài kể trải nghiệm; chỉ trả câu cuối: Đã thử ba cách mà
   vẫn không giải quyết vấn đề.” Kết quả mong đợi thêm “được” sau “giải quyết”, giữ “ba cách”.
2. **Giữ câu vốn tự nhiên:** “Rà câu sau trong chat công việc; nếu đã tự nhiên thì giữ nguyên.
   Chỉ trả câu cuối: Tôi rời công ty lúc sáu giờ.” Kết quả mong đợi giữ nguyên câu.
3. **Giữ code trong README:** dùng mẫu dưới đây. Kết quả mong đợi thêm “là” sau “đơn giản nhất”
   và giữ nguyên khối code từng byte.

````text
Biên tập phần văn xuôi sau trong README; giữ nguyên khối code từng byte:
Cách xử lý đơn giản nhất tăng số worker.

```bash
WORKERS=3 ./run-worker.sh --dry-run
```
````

## Tùy chọn: hồ sơ giọng

Phần này không bắt buộc. Khi muốn bài viết ra đúng giọng của mình, hoặc đúng giọng một thương hiệu
bạn được nói thay, bạn có thể cho Vietnamizer học giọng đó và lưu thành một hồ sơ có tên. Các bước
nằm ở [Thiết lập giọng của bạn](../README.md#thiết-lập-giọng-của-bạn) trong README. Trên Claude Code,
gõ `/vietnamizer:help`; ở host khác, nói “thiết lập giọng”.

Vài điều nên biết trước khi bắt đầu:

- **Nguồn mẫu.** Giọng cá nhân học từ bài bạn dán, file export LinkedIn hoặc Facebook bạn tự tải,
  hoặc trang của chính bạn qua công cụ trình duyệt của host. Giọng thương hiệu học từ bộ quy chuẩn,
  bài đã đăng và tài liệu nội bộ bạn đưa, hoặc từ tối đa ba URL fanpage, trang công ty LinkedIn hay
  blog của thương hiệu. Đường trình duyệt qua Facebook và LinkedIn có cảnh báo điều khoản trước khi đọc.
- **Skill tin lời bạn.** Skill không kiểm được tài khoản hay Trang có phải của bạn, hay bạn có được nói
  thay thương hiệu không. Nó dựa vào lời xác nhận của bạn, và học giọng của người khác là không được.
- **Đồng ý trước khi đọc.** Mỗi nguồn có một câu xin đồng ý, gọi tên nguồn sẽ đọc. Đọc qua trình duyệt
  thì mỗi URL một câu. Chưa đồng ý thì skill chưa đọc gì.
- **Hãy tự đọc kỹ hồ sơ nháp.** Skill được dặn bỏ tên người, liên hệ và chuyện riêng khỏi hồ sơ, nhưng
  không có bộ lọc bằng mã. Bạn là người kiểm cuối cùng trước khi lưu.
- **Chỉ lưu khi bạn bảo lưu.** Không lưu thì hồ sơ chỉ ở lại trong hội thoại. Để dùng lại, bạn gọi tên
  hồ sơ (`/vietnamizer:vietnamizer <tên>` trên Claude Code cài qua plugin, `$vietnamizer <tên>` trên Codex,
  hay câu “theo hồ sơ <tên>”), nói kèm chỗ lưu nếu hồ sơ chưa có trong sổ hồ sơ, hoặc dán hồ sơ vào yêu
  cầu; mỗi lần chỉ áp một hồ sơ.
- **Gọi tên là đồng ý đọc.** Lời gọi bạn tự gõ được tính là đồng ý cho skill đọc sổ hồ sơ và đúng một hồ
  sơ khớp tên, nên skill không hỏi lại; riêng hồ sơ thương hiệu áp cho văn bản riêng tư thì skill vẫn hỏi
  xác nhận trước. Yêu cầu của bạn trong lượt hiện tại luôn được ưu tiên hơn hồ sơ
  ([Giọng và phong cách](style-and-voice.md)).

## Cách hoạt động, dữ liệu và hỗ trợ

Plugin nạp hướng dẫn Markdown, profile và bảng tra đi kèm. Không có MCP server, hook, bước cài
dependency hay chương trình chạy nền. Skill chỉ xử lý phần văn bản bạn giao để biên tập, và không tự
tìm mẫu giọng trong memory hay lịch sử hội thoại. Agent có thể đọc hay sửa file bạn giao trong phạm
vi cụ thể, theo quyền và cơ chế xác nhận của host. Đó không phải quyền quét các file khác để thu
thập dữ liệu.

Maintainer không có máy chủ nhận văn bản hay telemetry của plugin. Claude vẫn xử lý và có thể lưu
hội thoại theo chính sách của nền tảng, nên dùng plugin không biến việc biên tập thành xử lý hoàn
toàn trên máy. Đừng gửi credential, định danh chính phủ, dữ liệu thẻ thanh toán hay PHI.
Xem [quyền riêng tư](../PRIVACY.md) và [điều kiện sử dụng](../TERMS.md).

- **Không thấy skill:** kiểm plugin đã bật, rồi mở phiên mới. Trong Claude Code, kiểm đúng
  marketplace `finolabs` và lời gọi `/vietnamizer:vietnamizer`.
- **Mô tả hoặc phiên bản chưa đổi:** cập nhật đúng plugin cùng tên từ nguồn đã cài, tránh cài thêm
  bản review trùng tên. ZIP upload riêng không tự cập nhật từ GitHub.
- **Sửa sai hoặc sửa quá tay:** gửi ca giả lập hoặc đã ẩn danh, kèm kết quả mong đợi, qua
  [GitHub Issues](https://github.com/finolabs/vietnamizer/issues) theo mẫu báo lỗi. Đọc
  [hướng dẫn đóng góp](../CONTRIBUTING.md) trước, và đừng gửi toàn bộ prompt, log hay tài liệu.
- **Lỗi bảo mật:** dùng [kênh báo riêng](../SECURITY.md), không đăng lên Issues công khai.
  Đừng gửi API key, token, dữ liệu cá nhân, tài liệu nội bộ hay nội dung nhạy cảm.

## Phạm vi

Skill xử lý ba lớp:

- V1–V25 kiểm tra cách dùng từ và cấu trúc câu, chẳng hạn thiếu bổ ngữ kết quả, thiếu loại từ, dịch
  sát giới từ, đặt trạng ngữ gây mơ hồ hoặc để sót lời chào của trợ lý trong tài liệu.
- B1–B17 và K1–K7 kiểm tra sự phù hợp với thể loại. Blog, tin nhắn, README và bài nghiên cứu không
  dùng cùng một giọng.
- T1–T6 kiểm tra typography. Với văn xuôi thông thường, skill chỉ áp lớp này khi có ít nhất một lỗi
  V1–V25; với thể loại chỉ rà typography thì không cần lỗi V đi kèm.

Trước khi sửa, skill xác định thể loại và phạm vi, rồi mới tra profile khi có nghi vấn phụ thuộc thể
loại. Thứ tự đọc chi tiết nằm trong [`SKILL.md`](../SKILL.md).

Skill không dùng kết quả rà soát để xác định tác giả. Người viết song ngữ cũng có thể giữ cấu trúc
tiếng Anh trong câu tiếng Việt, và LLM cũng có thể tạo ra câu hoàn toàn tự nhiên.
