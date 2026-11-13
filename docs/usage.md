# Sử dụng, phạm vi và dữ liệu

[← README](../README.md)

## Dùng ngay

```text
/vietnamizer

[văn bản cần biên tập]
```

Khi cần sửa file, nêu rõ phạm vi:

```text
Dùng vietnamizer để sửa phần văn xuôi trong docs/bai-viet.md.
Giữ nguyên code, bảng tham số và các trích dẫn.
```

### Viết từ ý hoặc biên tập bản có sẵn

Cả hai đi qua tách ý → chọn giọng → khai triển → rà nghĩa và cách viết. Biên tập lấy ý từ
bản gốc đầy đủ; viết mới lấy từ brief/dữ kiện được giao. Outline không thay nguồn đối chiếu.
Không cần đưa qua một nháp AI trung gian. Nêu rõ người đọc, mục đích và phạm vi khi chúng
ảnh hưởng cách viết; thiếu mẫu không có nghĩa được tự tìm hồ sơ hay bịa trải nghiệm.

```text
Dùng Vietnamizer viết một thông báo cho nhóm phát triển từ các ý sau:
- Bản thử mở thứ Hai, tối đa 20 người.
- Chưa chốt ngày kết thúc.
Giọng ngắn gọn cho công việc. Không tự thêm giờ, hạn chót hoặc lời hứa.
Chỉ trả thông báo cuối.
```

Khi chỉ sửa một cụm/câu, quy trình áp dụng trong đúng phạm vi đó; đọc đoạn xung quanh để hiểu,
không tự viết lại cả bài. Khi giao biên tập toàn bài, tách các ý và sắc thái trước khi chọn
cách diễn đạt; không mặc định phải thay mọi câu. Bản tách ý không phải đầu ra bắt buộc.
Source 0.13.3 đóng gói quy trình mới; chưa có pilot xác nhận nó tốt hơn
payload 0.13.2 đã phát hành trước cập nhật này.

### Tuyến hồ sơ giọng cá nhân (opt-in)

Khi muốn tạo hồ sơ phong cách viết để tái sử dụng, người dùng yêu cầu rõ và cung cấp mẫu văn do chính mình viết:

```text
Dùng Vietnamizer phân tích các mẫu văn tôi tự viết dưới đây để tạo hồ sơ giọng cá nhân:
- Kênh: bài chia sẻ chuyên môn trên LinkedIn.
- Người đọc: đồng nghiệp và kỹ sư trong ngành.
Sau khi phân tích xong, hãy hiển thị hồ sơ để tôi duyệt trước khi lưu.

<writing_samples>
[Dán các đoạn văn bạn tự viết vào đây]
</writing_samples>
```

Skill sẽ hỏi xác nhận phạm vi đọc và nội dung dự kiến tạo trước khi phân tích mẫu, hiển thị trọn vẹn dự thảo hồ sơ và chỉ lưu khi người dùng yêu cầu rõ tại nơi họ chọn (Orrery, Obsidian hoặc file Markdown tại `~/.agents/vietnamizer/profiles`). Để sử dụng hồ sơ đã lưu khi biên tập hoặc viết mới, chỉ cần nêu tên hồ sơ hoặc dán hồ sơ vào yêu cầu; skill chỉ đọc đúng hồ sơ đó và yêu cầu hiện tại luôn được ưu tiên.

### Đọc ít theo đúng việc

Chỉ review vẫn đọc năm chốt trước nhận xét; nếu review cả bài/giọng theo mẫu thì đọc đúng workflow/card/guide như tuyến tương ứng. Kết luận nghĩa và cách viết riêng, không tự sửa.

| Khi cần | Bắt buộc đọc | Không nạp mặc định |
|---|---|---|
| Sửa một cụm/câu, rà cục bộ | Chỉ catalog đúng nghi vấn; đọc ngữ cảnh cần hiểu | Workflow bài, resolver, profile/card, guide mẫu |
| Biên tập toàn bài hoặc viết từ brief/outline | `references/quy-trinh-viet.md` và một card theo bảng mục đích | Các catalog chưa có nghi vấn, resolver nếu lựa chọn đã rõ |
| Theo mẫu được giao | Thêm `references/giu-giong-tu-mau.md` trên tuyến bài; với đoạn nhỏ chỉ guide và phạm vi ấy | Danh mục nguồn tham khảo khi mẫu đã đủ |
| Học, tạo, cập nhật, lưu hoặc áp dụng hồ sơ giọng cá nhân theo yêu cầu rõ | `references/ho-so-giong.md`; khi áp dụng, đọc thêm `references/giu-giong-tu-mau.md` | Không nạp tuyến này cho yêu cầu biên tập thông thường |
| Pha chức năng/mâu thuẫn | Mới đọc `references/bo-giai-phong-cach.md` | Giữ nguyên khi lựa chọn đã rõ |

- Sửa cụm/câu: core và catalog đúng nghi vấn; không cần workflow bài, resolver/profile/card hoặc guide mẫu.
- Biên tập bài/viết từ brief: thêm `references/quy-trinh-viet.md` và một card được core chọn trực tiếp.
- Theo mẫu: thêm `references/giu-giong-tu-mau.md`; không tự đọc danh mục nguồn khi mẫu đã đủ.
- Hồ sơ giọng (opt-in): thêm `references/ho-so-giong.md` khi người dùng yêu cầu rõ việc học, tạo, cập nhật, lưu hoặc áp dụng hồ sơ giọng cá nhân (khi áp dụng nạp thêm `references/giu-giong-tu-mau.md`); không nạp cho yêu cầu biên tập thông thường.
- Pha chức năng/mâu thuẫn: mới đọc `references/bo-giai-phong-cach.md`.

Các catalog giữ đủ 55 pattern để tra; giảm phần bắt buộc đọc không phải bỏ ngoại lệ hay bảo toàn nghĩa.

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

### Cách hoạt động, dữ liệu và hỗ trợ

Plugin nạp hướng dẫn Markdown, profile và bảng tra đi kèm; không có MCP server, hook, bước
cài dependency hoặc chương trình chạy nền. Chỉ phần văn bản người dùng giao để biên tập được
xử lý; không tự tìm mẫu giọng trong memory hoặc lịch sử hội thoại. Agent có thể đọc hay sửa
file được người dùng giao trong phạm vi cụ thể, theo quyền và cơ chế xác nhận của host.
Đó không phải quyền quét các file khác để thu thập dữ liệu.

Maintainer không có máy chủ nhận văn bản hay telemetry của plugin. Claude vẫn xử lý và có thể
lưu hội thoại theo chính sách của nền tảng; plugin không biến việc biên tập thành xử lý hoàn
toàn trên máy. Không gửi credential, định danh chính phủ, dữ liệu thẻ thanh toán hoặc PHI.
Xem [quyền riêng tư](../PRIVACY.md) và [điều kiện sử dụng](../TERMS.md).

Trước khi sửa, skill xác định thể loại/phạm vi; chỉ tra profile khi có nghi vấn phụ thuộc thể loại.
Làm bài chọn một card; có mẫu/hồ sơ chủ động cung cấp mới đọc guide mẫu. Skill không tự truy xuất memory hay lịch sử hội thoại để tìm mẫu.

Skill không dùng kết quả rà soát để xác định tác giả. Người viết song ngữ cũng có thể giữ cấu trúc tiếng Anh trong câu tiếng Việt; LLM cũng có thể tạo ra câu hoàn toàn tự nhiên.

### Đã gỡ Jev

Từ 0.14.0 Vietnamizer không còn runner đánh giá ngoài, không đọc `TYPESAFE_API_KEY` và không có
bước gọi API. Ai đã đặt key cho skill có thể xóa nó; key không còn tác dụng. Agent không cần chạy
`python3 -B -m jev`. Quy trình Markdown, năm chốt chặn và 55 pattern giữ nguyên. Các nghiên cứu cũ
chỉ còn là lịch sử, không phải runtime hay bằng chứng hiệu quả.
