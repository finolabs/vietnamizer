# Hướng dẫn dùng và thiết lập giọng

Đọc khi người dùng hỏi Vietnamizer làm được gì, cách dùng, gõ `/vietnamizer:help`, hoặc nói “bắt đầu”,
“thiết lập giọng”. Phần hướng dẫn không đọc file của người dùng, không tìm hồ sơ và không lưu gì. Trả
lời bằng tiếng Việt, gọn trong một màn hình.

## 1. Hướng dẫn một màn hình

Trình bốn ý, mỗi ý kèm một câu yêu cầu mẫu, rồi mời bắt đầu:

1. **Biên tập và viết.** Sửa bản nháp, bản dịch hay bài AI còn gượng; giữ nghĩa và giọng hiện có. Viết
   mới từ ý hoặc dàn ý. Ví dụ: “Sửa giúp email này cho tự nhiên hơn.”
2. **Chọn giọng.** Mặc định giữ giọng của chính người viết. Có thể gọi tên một hồ sơ giọng cá nhân
   hoặc một hồ sơ giọng thương hiệu; mỗi lần chỉ dùng một hồ sơ. Ví dụ: “Viết lại bài này theo hồ sơ
   `giong-cong-viec`.”
3. **Học giọng.** Dán 10–20 bài tự viết, đưa file export LinkedIn hoặc Facebook, hoặc đọc trang của
   chính mình qua trình duyệt nếu host có công cụ đó (có cảnh báo điều khoản của LinkedIn và Facebook).
   Giọng thương hiệu học từ bộ quy chuẩn, bài đã đăng và tài liệu nội bộ người dùng đưa. Ví dụ: “Học
   giọng viết LinkedIn của tôi.”
4. **Kiểm giọng.** Chấm vài đoạn mẫu theo bốn mức Kém, Trung bình, Khá, Tốt để sửa hồ sơ; đó là đánh giá
   của người dùng, skill không tự tính điểm giống giọng. Ví dụ: “Cho tôi chấm 3 đoạn mẫu của hồ sơ này.”

Kết bằng: “Muốn bắt đầu thiết lập giọng không?”. Người dùng không muốn thì dừng ở đây.

## 2. Thiết lập giọng từng bước

Chạy khi người dùng đồng ý lời mời trên, hoặc nói “bắt đầu”, “thiết lập giọng”. Mỗi lựa chọn hỏi qua
công cụ câu hỏi của host khi có, lựa chọn đề xuất đứng đầu; không có thì hỏi bằng chữ. Người dùng có thể dừng
ở bất kỳ bước nào: không lưu gì nếu người dùng dừng, và không đọc gì ngoài phần họ đã đồng ý.

1. **Loại giọng:** Cá nhân (đề xuất) hoặc Thương hiệu.
2. **Nguồn mẫu:** Dán bài (đề xuất), File export, hoặc Đọc trang qua trình duyệt. Chỉ đưa lựa chọn trình
   duyệt khi agent thấy có công cụ trình duyệt và loại giọng là Cá nhân. File export thì nêu các bước của
   nền tảng theo `references/voice-sources.md` mục 3; trình duyệt thì nêu cảnh báo điều khoản ở mục 4 của
   file đó.
3. **Đồng ý đọc:** đúng một câu theo `references/voice-profile.md` mục 2, gọi tên nguồn, hỏi luôn tài khoản
   có phải của chính người dùng (hoặc người dùng có được nói thay thương hiệu không, theo
   `references/brand-voice.md`).
4. **Học:** soạn và trình toàn bộ hồ sơ theo `references/voice-profile.md` mục 3.
5. **Chấm:** mời chấm đoạn mẫu theo mục 7 của file đó; trả lời 0 là bỏ qua.
6. **Lưu:** hỏi có lưu không, rồi theo mục 4 của file đó (nơi lưu, tên, đường dẫn). Không lưu thì hồ sơ
   chỉ ở lại trong hội thoại.

Ngân sách câu hỏi: tối đa 6 câu hỏi trước bước chấm, gồm loại giọng, nguồn, nền tảng khi cần, câu đồng ý
đọc và tối đa một câu hỏi làm rõ. Không hỏi thêm để lấp đủ hồ sơ; thiếu thì ghi thiếu như hướng dẫn
phân tích.

Thiết lập chỉ chạy khi người dùng yêu cầu; skill không tự phát hiện lần dùng đầu và không tạo file đánh
dấu.
