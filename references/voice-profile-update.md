# Hồ sơ giọng: cập nhật, chấm đoạn mẫu và kiểm A/B

## 6. Cập nhật từ phản hồi (FR-009, FR-010, FR-014, FR-015)

Chỉ cập nhật hồ sơ khi đã có một hồ sơ trong phạm vi tác vụ (đã chỉ định ở mục 5 hoặc vừa tạo ở mục 3)
và người dùng yêu cầu ghi vào hồ sơ; phản hồi chỉ về một bản viết thì sửa bản viết. Đọc lại đích
ngay trước khi ghi; nếu nội dung đã đổi so với bản đã trình thì dừng và trình lại diff. Dùng
đúng hồ sơ được chỉ định và phiên bản người dùng đã sửa, theo cổng đọc ở mục 2. Xếp phản
hồi vào mục liên quan, không mở rộng một nhận xét cục bộ thành thói quen ở mọi kênh:

| Phản hồi nói về | Mục cần đề xuất sửa |
|---|---|
| Nét ổn định xuyên kênh có bằng chứng | Giọng chung |
| Cách viết riêng cho chat, email, bài đăng hoặc tài liệu | Theo kênh |
| Cách thay đổi theo quan hệ/người đọc | Tông theo người đọc |
| Từ/cách viết muốn tránh hoặc muốn giữ rõ ràng | Nên và không nên |
| Mức hoặc vị trí mà quá đó thì một nét thành áp quá tay | `ranh giới` của nét đó |
| Câu trả lời cho một điểm trong `Điểm chưa quyết` | Mục mà câu trả lời thuộc về; bỏ điểm khỏi `Điểm chưa quyết` |

Sau bản nháp, hỏi tối đa hai câu bổ sung để làm rõ phạm vi hoặc ý sửa; không hỏi thêm để
lấp đủ mục. Nếu vẫn chưa rõ, giữ điểm đó là chưa quyết định, không tự điền. Yêu cầu hiện
tại đủ để sửa bản viết nhưng không đủ rõ cho quy tắc lâu dài thì chỉ sửa bản viết. Chỉ khi người dùng
yêu cầu ghi điểm chưa rõ ấy vào hồ sơ mới đề xuất một mục `Điểm chưa quyết` theo
`references/voice-analysis.md`.

Trình diff chính xác so với hồ sơ hiện hành, gồm từng dòng bỏ/thêm, kể cả ngày cập nhật nếu
đổi. Trình toàn bộ bản sau sửa trước khi lưu; không chỉ tóm tắt là “đã chỉnh giọng”. Không
thêm dữ liệu cá nhân, bí mật hoặc lời người khác vào diff hay hồ sơ. Với lệnh cấm trực tiếp
như “đừng dùng từ này”, ghi đúng phạm vi người dùng nêu, không giả làm kết luận từ mẫu.

Chỉ ghi bản cập nhật sau khi người dùng xác nhận lưu **diff đã thấy**, tại đúng đích đã
chọn; áp lại mục 4 nếu đổi đích hoặc cần tạo thư mục. Chưa xác nhận thì giữ bản đề xuất
trong hội thoại, không sửa bản lưu. Không đưa phản hồi này vào nhật ký hiệu chuẩn chung.

## 7. Chấm đoạn mẫu và kiểm A/B (FR-015, FR-016; spec 030 FR-010–FR-013)

### Chấm đoạn mẫu

Mời chấm ngay sau khi trình bản nháp hồ sơ ở mục 3, hoặc khi người dùng yêu cầu với một hồ sơ đã nêu
tên (sau câu đồng ý đọc ở mục 2). Trước hết hỏi số đoạn muốn chấm (0–10): “Bạn muốn xem và chấm bao
nhiêu đoạn mẫu (0–10)?”. Trả lời 0 hoặc từ chối thì bỏ bước chấm; số lớn hơn 10 thì lấy 10 và nói rõ.

Với mỗi đoạn i trên n:

- Viết một đoạn khoảng 60–120 chữ về chủ đề nằm ngoài các mẫu đã đọc, ở một kênh hồ sơ có căn cứ, theo
  đúng loại hồ sơ. Lấy tình huống giả định được nói rõ là giả định; không tạo trải nghiệm hay dữ kiện
  riêng cho người dùng hoặc thương hiệu. Đoạn giữ năm chốt, không vượt `ranh giới` của nét và không áp
  đề xuất nào trong `Điểm chưa quyết`.
- Trình đoạn trong tin nhắn, ghi nhãn “Đoạn i/n”, rồi mới hỏi.
- Hỏi đúng một câu: “Đoạn này giống cách bạn viết đến mức nào?” (hồ sơ thương hiệu: “giống giọng
  thương hiệu”). Có công cụ câu hỏi của host thì dùng nó, tiêu đề “Đoạn i/n”, bốn lựa chọn theo đúng
  thứ tự Kém, Trung bình, Khá, Tốt, và không đánh dấu lựa chọn nào là đề xuất. Không có công cụ thì nhờ
  người dùng trả lời bằng một trong bốn từ đó.
- Trả lời ngoài bốn mức, kể cả “không biết”, ghi là chưa chấm cho đoạn đó.

Sau đoạn cuối, báo số đoạn theo từng mức. Có đoạn Kém hoặc Trung bình thì hỏi tối đa hai câu hỏi lý do
cho cả lượt (“Đoạn i chưa giống ở chỗ nào?”), rồi chuyển lý do thành diff đề xuất theo mục 6 (phạm vi,
`ranh giới`, `Điểm chưa quyết`). Không có lý do rõ thì không đề xuất sửa. Hai câu hỏi lý do này chính là
hai câu bổ sung của mục 6 cho diff đó, dùng chung một trần, không cộng thêm.

Diff từ lý do chấm đi theo một trong hai đường. Hồ sơ còn là bản nháp chưa lưu (mục 3): người dùng đồng ý
diff thì gộp vào bản nháp và trình lại toàn bộ bản sẽ lưu trước câu hỏi lưu; chưa đồng ý thì không gộp.
Hồ sơ đã lưu: diff cần người dùng xác nhận riêng theo mục 6; dòng chấm nằm trong cùng diff đó, còn khi không
có diff từ lý do hoặc người dùng bác diff đó thì dòng chấm là một diff riêng, trình ra và xác nhận theo mục 6.

Lượt chấm chỉ được ghi vào hồ sơ khi người dùng lưu hồ sơ (mục 4) hoặc xác nhận diff (mục 6). Dòng chấm
nằm sẵn trong bản toàn văn hoặc diff trình cho người dùng trước câu hỏi lưu; không thêm dòng nào người dùng
chưa thấy. Dòng đó là đúng một dòng trong `## Lịch sử chấm` theo mẫu ở `references/voice-analysis.md`, gồm ngày, số đoạn, số đoạn
theo từng mức, số chưa chấm, và nhãn cố định “đánh giá của người dùng, không phải điểm chất lượng”.
Dòng này không lưu nội dung đoạn, chủ đề hay lý do. Chưa lưu hoặc chưa xác nhận thì không ghi gì; lượt
chấm chỉ còn trong hội thoại.

Số lượt chấm là đánh giá của người dùng về hồ sơ của họ; không đưa vào `calibration/LOG.md` hay dùng làm
bằng chứng chất lượng của skill. Skill không tự tính điểm giống giọng. Không nêu phần trăm, điểm trung
bình hay mức khớp do skill tự tính, kể cả khi tóm tắt lượt chấm.

### Kiểm A/B ẩn chế độ (tùy chọn)

Khi người dùng yêu cầu kiểm giọng, dùng một chủ đề ngoài các mẫu đã được đồng ý đọc;
không tìm thêm mẫu. Lấy dữ kiện từ brief hiện tại hoặc chọn tình huống giả định được nói
rõ, không tạo trải nghiệm cá nhân cho người dùng. Giữ cùng brief, dữ kiện, thể loại và
các chốt cho cả hai bản, gồm một bản theo brief không áp hồ sơ và một bản áp hồ sơ được chỉ định.

Trình hai bản bằng ký hiệu trung tính A/B, không ghi “bản thường”, “bản theo hồ sơ” hay
tiết lộ ánh xạ trước khi người dùng chọn. Giữ ánh xạ trong ngữ cảnh làm việc; không luôn
đặt bản áp hồ sơ ở cùng một vị trí. Hỏi bản nào giống cách họ viết hơn và vì sao; cho phép
trả lời không phân biệt được hoặc không bản nào. Chỉ tiết lộ chế độ sau lựa chọn.

Nếu bản không áp hồ sơ thắng, kiểm lý do thay vì tăng mức bắt chước:

- **Áp sai nét:** nét đúng nhưng sai kênh, người đọc hoặc chức năng; đề xuất thu hẹp phạm vi.
- **Chưa phân biệt được:** hai bản không khác rõ hoặc bằng chứng còn yếu; ghi giới hạn,
  không kết luận hồ sơ đã đúng hoặc đã sai.
- **Áp quá tay:** lặp tiểu từ, khẩu ngữ hay nhịp quá dày; đề xuất bỏ cách áp máy móc hoặc
  giới hạn nét ở vị trí có căn cứ bằng cách đề xuất `ranh giới` cho nét đó (ở Giọng chung, Theo kênh
  hoặc mục `Nên:`), không đặt quota mới.

Đưa từng lý do vào Giọng chung, Theo kênh, Tông theo người đọc, Nên và không nên hoặc `ranh giới`
của nét theo mục 6. Giữ trần hai câu hỏi bổ sung, trình diff rồi xin xác nhận lưu; lựa chọn A/B không
tự cấp quyền cập nhật hồ sơ. Lượt chọn A/B không ghi vào `Lịch sử chấm` và không thành bằng chứng chất
lượng tổng quát; skill cũng không tự tính điểm giống giọng từ đó.
