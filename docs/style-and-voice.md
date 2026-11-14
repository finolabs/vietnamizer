# Giọng gốc, giọng mẫu và phong cách

[← README](../README.md)

## Giữ giọng và chọn phong cách

### Giữ giọng của một người cụ thể

Có thể đưa mẫu văn ngay trong yêu cầu:

```text
Đây là hai đoạn tôi tự viết:
[mẫu văn]

Hãy sửa đoạn dưới theo cùng cách xưng hô, nhịp câu và mức độ trang trọng:
[văn bản cần sửa]
```

Mẫu văn chỉ được ưu tiên đối với thói quen xuất hiện nhất quán, như cách xưng hô, nhịp câu, cách chêm tiếng Anh hoặc dùng dấu câu. Nó không hợp thức hoá lỗi ngôn ngữ rõ ràng và không vượt qua năm quy tắc chốt chặn trong `SKILL.md`.

Có thể dán một hồ sơ phong cách ngắn trong yêu cầu thay cho mẫu văn. Hồ sơ chỉ dùng cho đúng người
và phạm vi đã nêu; yêu cầu hiện tại được ưu tiên. Skill không tự tìm hồ sơ ngoài tác vụ hay tự lưu hồ sơ;
việc tạo và lưu hồ sơ có tên chỉ diễn ra khi người dùng yêu cầu rõ qua tuyến opt-in. Hồ sơ đã lưu được
gọi lại bằng tên qua sổ hồ sơ (xem mục “Tái sử dụng” bên dưới).

### Chọn phong cách theo mục đích

`vietnamizer` không còn gom mọi văn bản vào hai giọng *cá nhân* và *trung tính*. Hai profile đó vẫn
giữ vai trò cổng pattern, còn bộ giải phong cách chọn một card theo mục đích, người đọc, quan hệ,
thanh ngữ vực, kênh và mẫu giọng. Một phần văn bản chỉ dùng tối đa một card; file pha nhiều chức
năng được chia theo phần, không ép chung một giọng.

| Style card | Dùng cho | Base profile |
|---|---|---|
| [`personal-narrative`](../profiles/personal-blog/styles/personal-narrative.md) | Blog, bài kể có người viết hiện diện | `personal-blog` |
| [`work-coordination`](../profiles/personal-blog/styles/work-coordination.md) | Chat, bình luận và lời nhờ trong công việc | `personal-blog` |
| [`public-expertise`](../profiles/personal-blog/styles/public-expertise.md) | LinkedIn, bài quan điểm hoặc chia sẻ chuyên môn | `personal-blog` |
| [`persuasive-marketing`](../profiles/personal-blog/styles/persuasive-marketing.md) | Nội dung giới thiệu có mục tiêu và CTA thật | `personal-blog` |
| [`technical-guide`](../profiles/enterprise-technical/styles/technical-guide.md) | README, văn xuôi API và hướng dẫn xử lý lỗi | `enterprise-technical` |
| [`business-operations`](../profiles/enterprise-technical/styles/business-operations.md) | SOP, báo cáo, biên bản và bàn giao | `enterprise-technical` |
| [`academic-analysis`](../profiles/enterprise-technical/styles/academic-analysis.md) | Giáo trình, đề án và nghiên cứu | `enterprise-technical` |

Card không phải khuôn để “làm màu” và không tự tạo lý do sửa. Yêu cầu hiện tại được ưu tiên;
ràng buộc thể loại và năm quy tắc chốt chặn vẫn giới hạn mọi thay đổi; mẫu/hồ sơ chỉ được dùng khi
đúng người, đúng phạm vi và có đặc tính ổn định. Chi tiết chuẩn nằm trong
`references/style-resolution.md`.

## Giữ giọng khi có mẫu

**Đã có cơ chế giúp agent biên tập theo giọng tham chiếu của người dùng.** Gửi bản
nháp cùng mẫu tự viết, bản đã sửa từ nháp AI hoặc hồ sơ phong cách được chủ động
cung cấp. Skill dùng mẫu để chọn cách sửa phù hợp, không viết lại mọi câu cho
giống một khuôn giọng.

[Hướng dẫn đọc mẫu](../references/voice-from-samples.md) yêu cầu rút đặc tính có ví dụ
và phạm vi: đại từ làm chức năng gì, dùng thuật ngữ và cách viết số nào, nhịp câu/dấu ngắt,
đề mục và mở/kết ra sao. Có thể theo cách dùng chữ số cho lượng cụ thể, giữ đề mục hỏi có
chức năng và dùng nhiều đại từ theo vai trò; không thay toàn cục hoặc đưa dữ kiện của mẫu vào bài. Agent đối chiếu bản sửa với mẫu cùng kênh và mục đích; không suy tính
cách, không rải câu cửa miệng hoặc tự thêm trải nghiệm. Một mẫu ngắn vẫn giúp
giữ đặc tính hẹp; không đặt số bài tối thiểu chưa được kiểm chứng.

Hình thức hợp lệ chưa tự là lựa chọn nên dùng. Phần giới thiệu khái niệm có thể hợp câu hỏi,
phần thao tác có thể hợp bạn, phần đối chiếu cần làm rõ những trạng thái đã có. Không cấm câu
hỏi/bạn hoặc giữ cứng bố cục nguồn; khi đổi cấu trúc vẫn kiểm phạm vi đề mục, quan hệ và tình thái.

Ví dụ lời yêu cầu, kèm bản nháp và mẫu ngay trong tác vụ:

```text
Use Vietnamizer to edit the draft below for my personal blog.
Adapt the draft toward the supplied reference voice.
You may restructure sentences, paragraphs, headings or existing lists using evidenced sample traits.
Preserve every proposition, condition, quantity, level of certainty and protected span.
Preserve my meaning, level of certainty, terminology and short-sentence rhythm.
Do not invent experiences or repeat catchphrases just to imitate the samples.
Return only the edited article.

<writing_samples>Paste your reference samples here.</writing_samples>
<draft>Paste your draft here.</draft>
```

**Hai chế độ:** yêu cầu rà lỗi, viết tự nhiên hơn hoặc chỉ đưa mẫu vẫn mặc định **giữ giọng gốc**.
Mẫu giúp đối chiếu, không tự bật chuyển giọng. Ví dụ trên chủ động chọn **theo giọng mẫu**;
chế độ này cần mẫu/hồ sơ dùng được và cho phép đổi cấu trúc câu đúng có căn cứ. Có thể tách
các định nghĩa đã có thành bullet hoặc đặt đề mục từ ý sẵn có; không thêm bước, đổi cách nhóm
mơ hồ, bỏ điều kiện hoặc sửa số liệu để giống mẫu. Nếu cần mẫu mà chưa có thì chỉ hỏi mẫu còn thiếu.

Để giữ giọng gốc dù có mẫu, dùng yêu cầu:

```text
Copyedit this draft while preserving its existing voice.
Use the supplied samples only to check consistency, not to transfer their voice.
```

Blog công nghệ có người viết hiện diện được chọn profile theo mục đích blog; README/SOP vẫn
giữ profile kỹ thuật cùng các giới hạn riêng. Không dùng giọng mẫu để đổi thể loại hoặc vùng bảo toàn.

Mẫu được khai báo đã qua AI là giọng tham chiếu người dùng chọn, chưa chứng minh
giọng tự viết không có AI. Không có mẫu và không yêu cầu theo mẫu thì biên tập giữ giọng bản gốc, viết mới theo brief/thể loại;
không khẳng định đã bắt chước đúng người. Từ source 0.13.3, workflow có nhánh viết mới từ ý được giao cùng các bước tách ý, chọn giọng và
kiểm lại như biên tập. Chưa có pilot so quy trình mới/cũ hoặc xác nhận viết mới khớp giọng.

Không tự truy xuất hoặc cập nhật hồ sơ trong HOME, memory hay nguồn ngoài tác vụ; ngoại lệ duy nhất là sổ hồ sơ, chỉ đọc khi người dùng gọi lại hồ sơ đã lưu. Việc tạo và lưu hồ sơ chỉ thực hiện khi người dùng yêu cầu rõ qua tuyến hồ sơ giọng; viết mới hay biên tập đều không tự tạo trải nghiệm hay quan điểm thay người viết. Chưa có benchmark độc lập chứng minh chất lượng giữ giọng của bản hiện tại.

## Dùng giọng để khai triển từ ý

Đọc/tách nội dung trước, chọn bằng chứng giọng phù hợp rồi mới khai triển. Giữ bản nguồn đầy đủ
để rà mọi mệnh đề, quan hệ và sắc thái; đừng biến outline thành bản tóm tắt mất điều kiện rồi
viết lại chỉ từ nó. Chọn điểm vào, chuyển ý và điểm dừng theo nội dung và giọng được giao,
không chỉ thay đại từ hoặc chèn câu cửa miệng. Review cả câu, đoạn và toàn bài; sửa tiếp thì
kiểm lại nghĩa phần bị ảnh hưởng. Quy trình đầy đủ do `SKILL.md` sở hữu.

Mẫu cá nhân được chỉ định giúp theo giọng một người. Bộ bài báo/blog/chuyên môn nhiều tác giả
là tham chiếu cách viết theo nhiệm vụ, nên chỉ chọn phần cùng thể loại, người đọc và chức năng, giữ
xuất xứ và giới hạn bằng chứng. Không trộn thành giọng trung bình hoặc mặc định bắt chước giọng
chủ. Không lấy dữ kiện, chuyện riêng hay quan điểm của mẫu sang bài. Guide mẫu mô tả cách dùng bằng chứng; danh mục nguồn ở `references/style-sources.md` chỉ đọc khi được giao tìm/chọn nguồn, gồm báo chí, blog công nghệ/nghiên cứu và giải thích phương pháp khoa học. Danh mục chỉ giữ metadata/link cùng giới hạn, không tải corpus hoặc chép toàn văn.

## Hồ sơ phong cách và nhật ký hiệu chuẩn

Hai cơ chế này phục vụ hai mục đích khác nhau.

### Hồ sơ người dùng chủ động cung cấp

Người dùng có thể tự giữ một hồ sơ và dán vào yêu cầu. Hồ sơ nên ngắn, chỉ chứa thông tin giữ giọng:

- cách xưng hô;
- nhịp và độ dài câu thường dùng;
- mức dùng từ Hán-Việt;
- cách chêm tiếng Anh;
- thói quen viết hoa và dấu câu;
- phạm vi áp dụng cùng một ví dụ ngắn.

Skill chỉ dùng hồ sơ được cung cấp hoặc được gọi lại trong tác vụ, không tự truy xuất Claude memory, lịch sử chat
hoặc dữ liệu khác, và không tự lưu hồ sơ nếu không có yêu cầu rõ. Không dùng mẫu của người này cho người khác;
yêu cầu hiện tại luôn được ưu tiên.

### Tuyến hồ sơ giọng (opt-in)

Khi người dùng yêu cầu học hoặc tạo hồ sơ phong cách viết của mình, `vietnamizer` kích hoạt tuyến opt-in
theo [`references/voice-profile.md`](../references/voice-profile.md) và [`references/voice-analysis.md`](../references/voice-analysis.md):

- **Nguồn mẫu:** chỉ đọc văn bản do người dùng dán, file chỉ định trong tác vụ (kể cả file export LinkedIn/Facebook bạn tự tải), hoặc trang của chính bạn qua công cụ trình duyệt host sẵn có, sau khi hỏi và nhận được sự đồng ý rõ ràng cùng lời xác nhận chủ tài khoản (với trang thương hiệu: lời khẳng định được nói thay, xem mục giọng thương hiệu dưới) ([`references/voice-sources.md`](../references/voice-sources.md)). Không tự tìm trong memory, lịch sử chat, hòm thư hay các đầu nối khác. Đọc LinkedIn hay Facebook qua trình duyệt có cảnh báo điều khoản trước.
- **Cá nhân hay thương hiệu:** hồ sơ có trường `kind` (`personal` mặc định, `brand`). Không nêu giọng thì dùng giọng cá nhân; hồ sơ thương hiệu chỉ áp khi bạn gọi tên; mỗi lần chỉ một hồ sơ.
- **Giọng thương hiệu:** dựng từ bộ quy chuẩn, bài thương hiệu đã đăng và tài liệu nội bộ bạn đưa, sau khi bạn xác nhận được nói thay thương hiệu ([`references/brand-voice.md`](../references/brand-voice.md)). Host có công cụ trình duyệt thì skill còn đọc được fanpage Facebook, trang công ty LinkedIn hoặc trang danh sách bài trên website hay blog riêng của thương hiệu, từ tối đa ba URL bạn đưa, mỗi URL một câu đồng ý gọi tên thương hiệu và URL; skill chỉ đọc thân bài thương hiệu đã đăng, từ chối trang đối thủ và dừng khi trang không mang tên thương hiệu bạn nêu ([`references/voice-sources.md`](../references/voice-sources.md) mục 4b). Fanpage của một người (nghệ sĩ, người nổi tiếng) không đọc như trang thương hiệu; nếu đó là Trang của chính bạn, skill cảnh báo, hỏi bạn xác nhận rồi mới học thành hồ sơ cá nhân (mục 4c). Quy tắc từ bộ quy chuẩn nằm riêng ở mục `Quy tắc thương hiệu`; chỗ bài đăng làm khác quy tắc vào `Điểm chưa quyết` để bạn chốt. Hồ sơ không ghi tên người viết, nhân viên hay khách hàng.
- **Chấm đoạn mẫu:** sau khi học, skill hỏi bạn muốn chấm bao nhiêu đoạn (0–10), rồi đưa từng đoạn với bốn mức Kém, Trung bình, Khá, Tốt. Đoạn bị chấm thấp có thể thành đề xuất sửa hồ sơ (có diff). Số lượt chấm chỉ vào mục `Lịch sử chấm` khi bạn lưu, ghi là đánh giá của bạn, không phải điểm chất lượng; skill không tự tính điểm giống giọng.
- **Phân tích và bảo vệ dữ liệu:** phân tích các chiều tiếng Việt quan sát được (xưng hô theo quan hệ, hư từ/tiểu từ, chêm tiếng Anh, dấu câu và số, nhịp điệu, mở/kết) kèm trích đoạn minh họa ngắn hoặc ước lượng số lần xuất hiện. Agent được chỉ dẫn bỏ tên riêng, số điện thoại, email, thông tin tài chính và dữ liệu nhạy cảm khỏi hồ sơ; v1 không có bộ lọc bằng mã, nên bước bảo vệ thực sự là bạn đọc toàn bộ dự thảo trước khi lưu.
- **Duyệt trước khi lưu:** luôn hiển thị trọn vẹn dự thảo hồ sơ cho người dùng xem và chỉnh sửa.
- **Lưu theo yêu cầu tại nơi người dùng chọn:** chỉ lưu khi người dùng yêu cầu rõ ràng. Skill phát hiện công cụ Orrery hoặc Obsidian từ danh sách công cụ sẵn có của agent để gợi ý, trừ kho mà quy tắc của host hay chỉ dẫn của bạn đã cho ngừng dùng; nếu không có thì hỏi đường dẫn file Markdown và đề xuất `~/.agents/vietnamizer/profiles`. Tuyệt đối không tự tạo thư mục trước khi xác nhận. Người dùng có thể lưu nhiều hồ sơ với các tên khác nhau cho từng kênh viết.
- **Tái sử dụng:** khi biên tập hoặc viết mới, gọi lại hồ sơ đã lưu bằng `/vietnamizer:vietnamizer <tên>` (Claude Code cài qua plugin; cài skill riêng thì `/vietnamizer <tên>`), `$vietnamizer <tên>` (Codex) hoặc câu “theo hồ sơ <tên>”; cùng lệnh ấy với `cá nhân` hay câu “theo giọng của tôi” dùng hồ sơ cá nhân mặc định. Lưu xong, nếu bạn đồng ý, skill ghi một dòng (tên, loại, kho, vị trí; không có nội dung hồ sơ) vào sổ hồ sơ `~/.agents/vietnamizer/registry.md` và in đúng câu cần gõ lần sau. Lời gọi của bạn được tính là đồng ý cho skill đọc sổ và đúng một hồ sơ khớp tên; skill không dò kho, không đọc hồ sơ khác và nói rõ đã dùng hồ sơ nào. Trên Chat không có file (claude.ai bản web, Desktop, Mobile và Cowork chạy trên cloud), hồ sơ lưu được dưới dạng bản gọn khoảng 1.200 ký tự trong bộ nhớ của Chat, có câu chặn để chỉ dùng khi bạn gọi tên, sau khi bạn xem đúng văn bản và đồng ý; skill báo trước rằng bộ nhớ ấy được nạp vào mọi cuộc trò chuyện và gợi ý lưu trong một Project. Tạo hồ sơ không bắt buộc. Chưa có hồ sơ thì skill vẫn sửa bài ngay và chỉ nhắc một dòng mỗi phiên sau khi đã trả bài, tắt được hẳn (trên Chat cũng vậy). Hồ sơ dán thẳng trong yêu cầu đi tuyến “Theo mẫu”. Yêu cầu trong lượt hiện tại luôn được ưu tiên hơn hồ sơ đã lưu; năm quy tắc chốt chặn trong `SKILL.md` luôn giữ nguyên giá trị.

### `calibration/LOG.md`

Đây là nhật ký bằng chứng dùng để bảo trì quy tắc chung của skill, không phải hồ sơ cá nhân. Chỉ ghi vào log khi phản hồi cho thấy:

- một pattern sửa nhầm câu vốn đúng;
- mục **Không flag** còn thiếu trường hợp loại trừ;
- skill bỏ sót một lỗi có thể gọi tên;
- người bản ngữ nêu một quy tắc tiếng Việt có thể kiểm tra độc lập.

Khác biệt chỉ thuộc sở thích cá nhân không được đưa vào log. Nhờ ranh giới này, skill không âm thầm học giọng của một người rồi áp lên mọi người dùng khác.

Quy trình đầy đủ nằm trong `AGENTS.md`.


Trong cấu trúc source 0.13.3, card chọn trực tiếp từ core khi việc đã rõ. Không bắt đọc resolver
hoặc profile rules trước mỗi card; chỉ tra resolver khi ngữ cảnh mâu thuẫn/pha chức năng, rules khi
có nghi vấn thể loại. Năm chốt và quyền đổi giọng do core sở hữu, không lặp quy trình ở các guide.
