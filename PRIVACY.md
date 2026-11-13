# Dữ liệu và quyền riêng tư

`vietnamizer` là bộ hướng dẫn biên tập chạy trong agent mà người dùng chọn. Quy trình Markdown
cốt lõi không có máy chủ riêng, telemetry hoặc bước gửi văn bản đến dịch vụ của maintainer.
Plugin không khai báo MCP server, hook hay quyền đăng nhập vào dịch vụ bên ngoài.

Văn bản đưa vào Claude hoặc Codex vẫn được xử lý theo cấu hình, quyền truy cập và chính sách dữ
liệu của nền tảng đó. Cài skill không làm văn bản trở thành dữ liệu chỉ xử lý trên máy.

## Dữ liệu đầu vào và quyền kiểm soát

Quy trình dùng văn bản người dùng chủ động cung cấp, yêu cầu biên tập, ngữ cảnh tối thiểu và
mẫu giọng tùy chọn cho đúng tác vụ. Những phần này có thể chứa dữ liệu cá nhân; người dùng nên
ẩn danh trước khi gửi. Vietnamizer không yêu cầu hồ sơ cá nhân, vị trí, lịch sử hội thoại hoặc
dữ liệu khác chỉ để dự phòng. Mục đích sử dụng là biên tập và đối chiếu ý, giọng của văn bản.

Không cung cấp dữ liệu thẻ thanh toán thuộc PCI DSS, thông tin sức khỏe cá nhân được bảo vệ
(PHI), định danh do chính phủ cấp, mật khẩu, API key, mã MFA/OTP hoặc secret xác thực khác.
Nếu nhận thấy các dữ liệu này, skill dừng biên tập đầu vào đó và yêu cầu bản đã che hoặc ví dụ
giả lập; không trích lại hay lưu thành ca hiệu chuẩn. Consent không gỡ bỏ
giới hạn này. Ví dụ giả lập hoặc nội dung nói chung về sức khỏe và giấy tờ không bị cấm chỉ vì
chủ đề. Việc biên tập không cần thu thập thêm dữ liệu cá nhân nhạy cảm; ưu tiên bản đã ẩn danh.

Người dùng có thể không cung cấp mẫu giọng hoặc dùng bản giả lập
mà vẫn dùng được quy trình cốt lõi. Skill không tự lưu phản hồi hoặc sửa quy tắc; hồ sơ giọng chỉ
được lưu khi người dùng yêu cầu rõ theo tuyến bên dưới. Ghi nhật ký hiệu chuẩn cần một tác vụ
bảo trì và quyền ghi file cụ thể. Xóa hội thoại hoặc file được host
lưu phải thực hiện qua cơ chế của host; Vietnamizer không điều khiển hay bảo đảm thời hạn xóa
của nền tảng đó.

## Hồ sơ giọng

Tuyến hồ sơ giọng chỉ chạy khi người dùng yêu cầu tạo, cập nhật hoặc áp dụng hồ sơ giọng.
Trước khi đọc mẫu, skill nêu rõ nguồn sẽ đọc và chờ người dùng đồng ý. Mẫu chỉ là văn bản người
dùng dán hoặc file người dùng chỉ định trong tác vụ; skill không tự tìm mẫu trong memory, lịch
sử, email, connector hay kho lưu trữ. Khi áp dụng, skill chỉ đọc hồ sơ được người dùng dán hoặc
chỉ định, không tự liệt kê hay chọn hồ sơ.

Hồ sơ có thể gồm tên do người dùng chọn, ngày cập nhật, số mẫu theo kênh, đặc tính giọng, cách
viết theo kênh và người đọc, điều nên/không nên dùng, cùng căn cứ ngắn đã loại dữ liệu cá nhân.
Hồ sơ không được chứa dữ liệu cá nhân hoặc bí mật: tên người, thông tin liên hệ, mã định danh,
chi tiết sức khỏe/tài chính, điều khoản giao dịch, công việc chưa công bố hay nhận xét về người
khác. Agent được chỉ dẫn bỏ các dữ liệu này, nhưng v1 không có bộ lọc bằng mã: người dùng đọc toàn bộ dự thảo trước khi lưu là bước kiểm chính. Hồ sơ chỉ giữ trích đoạn ngắn đã lược chi tiết riêng, không chép nguyên mẫu.

Skill hiển thị toàn bộ hồ sơ trước khi lưu; chỉ lưu hoặc cập nhật khi người dùng yêu cầu rõ.
Người dùng đặt tên từng hồ sơ và chọn Orrery, Obsidian hoặc đường dẫn file Markdown. Skill chỉ
đề nghị Orrery/Obsidian nếu thấy công cụ tương ứng trong danh sách công cụ của agent; nếu không
có, skill hỏi đường dẫn và gợi ý `~/.agents/vietnamizer/profiles`. Tạo thư mục và ghi đè một hồ sơ đã có cũng cần người dùng
đồng ý riêng; đích là file chỉ dẫn của agent bị từ chối, và đích trong cây Git cần người dùng xác nhận rõ. Không ghi được thì báo lỗi, không tự lưu sang nơi khác.

Người dùng có thể đọc, sửa hoặc xóa file/ghi chú hồ sơ tại nơi đã chọn; bản người dùng sửa là
bản chuẩn. Skill không tự cập nhật từ phản hồi, tự nạp hồ sơ ở phiên sau hay ghi hồ sơ vào nhật
ký hiệu chuẩn chung. Nếu cần bản mẫu tạm ngoài hội thoại, skill đặt ngoài cây thư mục Git và
xóa khi quy trình kết thúc hoặc người dùng dừng.

Skill không gửi hồ sơ hay mẫu giọng tới dịch vụ ngoài: chúng chỉ nằm trong ngữ cảnh hội thoại
của agent mà người dùng chọn.

Từ bản 0.14.0, Vietnamizer không còn runner đánh giá ngoài (Jev/TypeSafe) và không đọc
`TYPESAFE_API_KEY`. Các bản cũ hơn có tuyến đó; lịch sử nằm trong `docs/changelog.md`.

Ngoài tuyến hồ sơ giọng được người dùng yêu cầu rõ ở trên, skill chỉ dùng mẫu giọng hoặc hồ sơ
người dùng chủ động cung cấp trong tác vụ, không tự truy xuất hay cập nhật memory. Việc lưu hội
thoại hoặc file bởi host vẫn theo chính sách host.

## Issue, pull request và ca sửa sai

Issue và pull request của repo công khai có thể được người khác đọc. Chỉ gửi nội dung mày có
quyền công bố; thay tên, dữ kiện nội bộ và thông tin cá nhân bằng ví dụ giả lập. Không gửi API key
hoặc credential qua issue. Hướng dẫn ca hiệu chuẩn nằm trong [`CONTRIBUTING.md`](CONTRIBUTING.md).

Maintainer và người đọc GitHub có thể tiếp cận nội dung mày chủ động đăng để hỗ trợ hoặc xem
ca sửa sai. Nội dung công khai không có thời hạn tự xóa do Vietnamizer đặt; lịch sử Git, bản
fork và bản sao có thể vẫn còn sau khi chỉnh sửa. Có thể sửa bài đăng hoặc liên hệ maintainer
để yêu cầu gỡ nội dung trong phạm vi kiểm soát của repo; không bảo đảm xóa mọi bản sao trên
GitHub hoặc do người khác giữ. Ca hiệu chuẩn được duyệt chỉ dùng ví dụ được phép công bố,
đã loại dữ liệu cá nhân và nhạy cảm, để bảo trì quy tắc biên tập.

Liên hệ về quyền riêng tư qua [GitHub Issues](https://github.com/finolabs/vietnamizer/issues),
chỉ mô tả vấn đề chung đã loại dữ liệu nhạy cảm. Không đăng thêm dữ liệu cá nhân
để yêu cầu gỡ nội dung. Nếu vấn đề liên quan đến lộ dữ liệu hoặc lỗi bảo mật, dùng
[kênh báo riêng](SECURITY.md); không gửi credential hoặc dữ liệu nhạy cảm trong báo cáo.
