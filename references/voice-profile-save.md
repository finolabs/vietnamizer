# Hồ sơ giọng: lưu hồ sơ

## 4. Lưu theo lựa chọn rõ ràng (FR-010, FR-011, FR-012; spec 039)

Chỉ lưu khi người dùng yêu cầu rõ ràng sau khi đã thấy toàn bộ hồ sơ. Đồng ý với nội dung
không tự thành yêu cầu lưu. Không tự lưu cuối tác vụ, không lưu như tác dụng phụ của sửa
bài và không tạo chỉ dẫn tự nạp hồ sơ ở phiên sau. Sổ hồ sơ là dữ liệu để tìm lại hồ
sơ khi người dùng gọi hồ sơ bằng tên, không phải chỉ dẫn tự nạp.

Xác định khả năng lưu từ danh sách công cụ, lệnh và thư mục mà chính agent đang thấy, không từ tên sản phẩm;
tên công cụ đã khai báo nhưng chưa nạp schema cũng tính là thấy (nạp schema khi người dùng chọn). Người dùng luôn có
thể tự nêu tên nơi lưu. Chỉ đề nghị
Orrery khi có công cụ note tương ứng; chỉ đề nghị Obsidian khi thấy công cụ hoặc lệnh
Obsidian dùng được. Không đọc note, dò vault, liệt kê thư mục hay chạy truy vấn thử chỉ để
phát hiện kho. Không suy rằng cài đặt được nhắc trong tài liệu đồng nghĩa với có khả năng dùng.
Không đề nghị kho mà quy tắc của host hoặc chỉ dẫn của người dùng trong ngữ cảnh của agent đã cho ngừng dùng hay cấm
(ví dụ chỉ dẫn ghi vault Obsidian đã ngừng dùng cho agent), kể cả khi thấy công cụ của kho đó. Người dùng
tự nêu tên kho ấy thì nói quy tắc nào chặn, đưa các kho còn lại và không ghi vào đó.

Host có hai loại:

- **Có thư mục ghi được:** phiên có thư mục mà agent ghi được bằng công cụ file của host, như thư mục
  người dùng gắn vào Cowork trên máy hay thư mục làm việc của Claude Code. Thư mục ấy là thư mục project.
  Đề nghị thêm kho “thư mục project này (`.vietnamizer/`)” theo đoạn **Kho project** dưới đây.
- **Không có thư mục ghi được:** Chat và các host không đọc được file trên máy, thường là claude.ai bản
  web, Desktop, Mobile và Cowork chạy trên cloud. Đề nghị thêm “Bộ nhớ của Chat” theo mục “Bản gọn trong
  bộ nhớ của Chat” dưới đây, và “Google Drive” theo đoạn **Google Drive** khi thấy công cụ của nó.

“Bộ nhớ của Chat” chỉ dành cho host không có thư mục ghi được. Trên mọi host khác không đề nghị kho này và không ghi hồ sơ vào bộ nhớ của agent
(`MEMORY.md` của Claude Code, memories của Codex, `AGENTS.md`, `CLAUDE.md`). Không ghi hồ sơ vào bộ nhớ project
của Cowork; đó là kho của host.

Đưa ra những kho vừa xác định được và để người dùng chọn; có nhiều kho thì đưa đủ, không
chọn sẵn. Quyền truy cập hay hạn chế của host vẫn áp dụng; thấy công cụ không cấp quyền
đọc/ghi. Nếu không thấy kho nào mà host ghi được file, hỏi đường dẫn file Markdown và đề nghị thư mục
`~/.agents/vietnamizer/profiles`. Đề nghị này không phải lựa chọn đã được chấp thuận.
Người dùng cũng có thể chủ động chọn file Markdown khi có kho khác.

Hỏi tên hồ sơ và vị trí còn thiếu, không suy từ nội dung mẫu. Cho phép nhiều hồ sơ có tên
riêng; không ghi đè một hồ sơ khác để giữ một bản duy nhất. Slug và tên file theo mục 1.
Nếu tên chuyển thành slug rỗng hoặc đụng tên đã biết, hỏi tên khác hay yêu cầu ghi đè rõ
ràng; không liệt kê các hồ sơ khác để chọn thay người dùng.

Đường dẫn file: nhận một thư mục cộng `<slug>.md`, không nhận đường dẫn đầy đủ tùy ý. Đổi `~` thành
đường dẫn tuyệt đối của thư mục home rồi nêu đường dẫn đó cho người dùng xem trước khi ghi; từ chối
`..` và liên kết tượng trưng. Từ chối đích nằm trong cây làm việc Git, trừ khi người dùng xác nhận rõ
sau khi được báo hồ sơ có thể bị commit. Từ chối đích là file hoặc thư mục chỉ dẫn/bộ nhớ của agent
(`AGENTS.md`, `CLAUDE.md`, `.claude/`, thư mục skill và các file/thư mục tương đương của Codex, Gemini). Hồ sơ ở đó sẽ tự nạp, trái với tuyến này.

Trước khi ghi, kiểm tồn tại đúng một đích (đường dẫn file, tiêu đề note Orrery, file Obsidian, file trong Drive),
không liệt kê nơi khác. Nếu đã có, hỏi tên khác hoặc một câu đồng ý ghi đè riêng, hoặc, nếu người dùng
nêu tên đúng file đó là hồ sơ cần cập nhật và đồng ý đọc (mục 2), đi tuyến cập nhật ở mục 6. Bản đã có do người dùng sửa tay là bản có thẩm quyền.

Chốt đích cụ thể trước khi ghi. Nếu phải tạo thư mục mới, hỏi một câu đồng ý **riêng** cho
việc tạo thư mục, kể cả đã được yêu cầu lưu. Không tạo thư mục trước câu trả lời đó.

- **Orrery:** tạo note trong thư mục người dùng chọn, tiêu đề `Hồ sơ giọng — <tên>` và nội
  dung theo template. Xác nhận space với người dùng trước khi ghi, không mặc định sang space dùng chung; cập nhật dùng
  `base_revision`. Dùng công cụ note; không dùng `remember`, không đưa hồ sơ vào memory.
- **Obsidian:** ghi cùng nội dung Markdown vào file trong vault/thư mục người dùng chỉ
  định, bằng khả năng host cho phép. Không tự chọn vault hoặc chuyển sang vault khác.
- **File Markdown:** ghi đúng đường dẫn người dùng đã chọn với quy tắc tên trên; không
  tự thay bằng thư mục đề nghị nếu đường dẫn đã chọn không dùng được.
- **Kho project:** theo đoạn dưới.
- **Google Drive:** theo đoạn dưới; ghi toàn bộ hồ sơ.
- **Bộ nhớ của Chat:** chỉ trên host không có thư mục ghi được; ghi bản gọn theo mục dưới, không ghi toàn bộ hồ sơ.

Nếu kho không truy cập được hoặc thao tác ghi bị từ chối, báo kết quả và không ghi ở nơi
nào khác. Giữ bản đã trình trong hội thoại để người dùng tự quyết bước tiếp. Chỉ báo đã
lưu khi thao tác ghi thực sự thành công; nêu đúng tên hồ sơ và đích đã ghi.

**Kho project.** Hồ sơ ghi vào `<project>/.vietnamizer/profiles/<slug>.md`, dòng sổ ghi vào
`<project>/.vietnamizer/registry.md`; `<project>` là đường dẫn tuyệt đối của thư mục project. Hồ sơ và sổ cùng định
dạng với kho ở home. Phiên gắn nhiều thư mục thì câu chọn kho hỏi luôn lưu vào thư mục nào. Câu chọn kho nêu
đường dẫn tuyệt đối sẽ ghi. Thư mục chưa có `.vietnamizer/profiles/` thì câu ấy nói sẽ tạo nó, và câu trả lời đồng ý là câu đồng ý riêng cho việc tạo đúng thư mục `.vietnamizer/profiles/` đó.
Không đề nghị kho project khi thư mục nằm trong cây làm việc Git, khi `.vietnamizer/` hay thư mục project là liên
kết tượng trưng, hay khi thư mục ấy là thư mục chỉ dẫn, bộ nhớ của agent. Người dùng tự nêu đúng chỗ đó thì đi như
file Markdown với các điều kiện đích ở trên, và dòng sổ ghi vào sổ ở home, không tạo sổ trong thư mục đó.

**Google Drive.** Chỉ trên host không có thư mục ghi được, và chỉ khi agent thấy công cụ tạo và đọc file của connector Google Drive.
Không thấy công cụ Drive thì không nhắc tới Drive. Câu chọn kho nêu tên file `<slug>.md` và thư mục `Vietnamizer` trong
Drive của chính người dùng; người dùng có thể đổi thư mục. Kiểm đích là kiểm đúng file `<slug>.md` trong đúng thư mục
đó, không tìm hay liệt kê gì khác trong Drive. Chưa có thư mục thì câu chọn kho nói sẽ tạo nó; câu trả lời đồng ý là
câu đồng ý riêng cho việc tạo đúng thư mục ấy. File chứa toàn bộ hồ sơ, đúng nội dung đã trình, ở dạng Markdown.
Chỉ ghi sau câu đồng ý của người dùng và hộp duyệt của host. Người dùng từ chối ở hộp duyệt hay ghi lỗi thì nói chưa
lưu vào Drive và không ghi nơi khác; bản gọn vẫn có thể lưu như dưới đây. Chỉ báo đã lưu khi connector trả về file đã
tạo, rồi nêu thư mục và tên file. Không chia sẻ file và không đổi quyền của file.

Lưu vào Drive xong, host có bộ nhớ của Chat thì hỏi một câu có lưu thêm bản gọn trỏ tới file đó không (mục dưới).
Bản gọn ấy giúp lần gọi sau tìm đúng file.

### Ghi sổ và câu gọi lần sau (spec 032)

Khung sổ và điều kiện đọc sổ ở mục 5. Sau khi lưu thành công, hỏi đúng một câu có ghi dòng của hồ sơ vào sổ không. Chỉ hỏi câu này trên host ghi được file; Chat không có file thì bỏ qua. Hồ sơ ở kho project thì sổ là sổ của
thư mục project đó; hồ sơ ở kho khác thì sổ là `~/.agents/vietnamizer/registry.md`. Câu ấy nêu đường dẫn tuyệt
đối của sổ và dòng sẽ ghi. Thư mục `~/.agents/vietnamizer/` chưa có thì câu ấy nói sẽ tạo nó; câu trả lời đồng ý là câu đồng ý riêng cho việc tạo đúng thư mục đó. Lựa chọn là “Ghi” (đề xuất) và “Không ghi”;
hồ sơ cá nhân mà sổ đã có một dòng cá nhân mặc định thì thêm “Ghi và đặt làm mặc định”. Dòng cá nhân đầu tiên trong sổ là mặc định, không cần hỏi.

Chỉ ghi dòng sau câu trả lời đồng ý. Đọc lại sổ ngay trước khi ghi; chỉ thêm hoặc sửa đúng dòng đã
hỏi, giữ nguyên các dòng khác. Slug đã có trong sổ với vị trí khác thì hỏi tên khác hoặc một câu đồng ý
riêng để trỏ dòng sang vị trí mới. Không thêm vào file chỉ dẫn nào một
dòng trỏ tới sổ.

Sau khi lưu, in đúng câu người dùng gõ lần sau, theo host đang chạy: Claude Code cài qua plugin `/vietnamizer:vietnamizer <slug>`,
Claude Code cài skill riêng `/vietnamizer <slug>`, Codex `$vietnamizer <slug>`, host khác “Sửa bài này theo hồ sơ <slug>”.
Dòng vừa ghi là hồ sơ cá nhân mặc định thì nói thêm cùng lệnh ấy với `cá nhân` thay cho slug, hay câu “theo
giọng của tôi”, cũng gọi được hồ sơ này.
Người dùng không ghi vào sổ, hoặc host không ghi được file, thì câu ấy kèm vị trí: “Sửa bài này theo
hồ sơ ở <vị trí>”. Bản gọn trong bộ nhớ của Chat thì câu ấy là “Sửa bài này theo hồ sơ <tên>”. Chỉ lưu vào
Drive, không có bản gọn, thì câu ấy là “Sửa bài này theo hồ sơ ở Google Drive <thư mục>/<slug>.md”.

### Bản gọn trong bộ nhớ của Chat (spec 032)

Chỉ dùng trên Chat không đọc được file trên máy. Bản gọn dài khoảng 1.200 ký tự, viết ở ngôi thứ ba như
dữ liệu, theo đúng khung này:

```text
Hồ sơ giọng Vietnamizer “<tên>” (<personal|brand>). Chỉ dùng khi người dùng gọi hồ sơ “<tên>” với Vietnamizer; không dùng cho yêu cầu khác.
Giọng chung: <nét> (ranh giới: <…>); … (tối đa năm nét)
Nên: <…>. Không nên: <…>.
Theo kênh: <kênh>: <một dòng>; …
Bản đầy đủ: Google Drive, <thư mục>/<slug>.md (id: <id file>)
```

Câu đầu là câu chặn phạm vi, giữ nguyên chữ. Với hồ sơ `personal`, câu chặn thêm “ hoặc gọi hồ sơ cá nhân”
ngay sau “với Vietnamizer”. Dòng cuối chỉ có khi hồ sơ đã lưu vào Drive thành công: `Bản đầy đủ: Google Drive, <thư mục>/<slug>.md`, kèm id file connector trả về khi có. Bản gọn không chứa trích đoạn làm căn cứ, nguồn, lịch sử
chấm, `Điểm chưa quyết` hay chỉ dẫn nào khác cho agent. Hồ sơ thương hiệu giữ thêm tối đa ba quy tắc thương
hiệu trong cùng giới hạn.

Trước khi ghi, trình đúng văn bản sẽ ghi, nói rõ bộ nhớ của Chat được nạp vào mọi cuộc trò chuyện, và gợi
ý lưu trong một Project (bộ nhớ của Project tách khỏi phần còn lại) để thu hẹp phạm vi. Chỉ ghi khi người
dùng đồng ý, bằng khả năng ghi bộ nhớ của chính host; host không cho ghi, bộ nhớ đang tắt hoặc đang ở
cuộc trò chuyện ẩn danh thì nói không lưu được và để bản gọn trong hội thoại cho người dùng tự giữ. Chỉ
báo đã lưu khi host xác nhận đã ghi, rồi nói người dùng xem, sửa hay xóa bản gọn ở phần cài đặt bộ nhớ của
Chat. Chat có thể viết lại mục nhớ theo cách của nó, nên nhờ người dùng xem câu đầu, tên hồ sơ và dòng `Bản đầy đủ` còn nguyên
trong phần cài đặt đó. Không ghi bản gọn thứ hai cùng tên; cập nhật thì trình bản mới và thay đúng bản cũ khi người dùng
đồng ý. Tác vụ đặt lịch chỉ đọc được bộ nhớ thì không đề nghị lưu. Bộ nhớ tắt mà không có Drive thì trình hồ sơ để người dùng tự giữ.
