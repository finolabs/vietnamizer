# Mẫu ghi chú ngữ vực (hiệu chuẩn, không bắt buộc)

Trạng thái: **mới có định dạng, chưa có số đo**. File này chưa chứa số liệu nào và không phải luật.

Dùng khi maintainer muốn ghi nhận tần suất một nhóm dấu hiệu (từ nối, từ tăng cường, từ giảm độ chắc
chắn) trong một thể loại tiếng Việt, làm mốc tham khảo cho người đọc ghi chú. Ghi chú không cho phép
agent thêm, bớt hoặc đổi từ trong bài người dùng, và không thay chốt 1–5 của `SKILL.md`.

## Định dạng một mục

- **Thể loại và phạm vi**: ví dụ “bài blog công nghệ, tiếng Việt, 2024–2026”.
- **Nguồn tập đo**: danh sách bài (đường dẫn hoặc định danh công khai), số bài, ngày thu thập, giấy phép.
- **Cách đo**: danh sách dấu hiệu đếm, cách chuẩn hóa văn bản, đơn vị (trên 1000 từ), công cụ.
- **Kết quả**: bảng số, kèm cỡ mẫu từng dòng; dòng dưới 20 bài ghi “mẫu nhỏ”.
- **Dev và holdout**: tập nào dùng để rút dấu hiệu, tập nào để kiểm; chưa có holdout thì ghi “chưa kiểm”.
- **Giới hạn**: thể loại hay giai đoạn nào không đại diện; không gọi là chuẩn.
- **Nhãn dùng**: “mốc tham khảo, không bắt buộc”.

Quy tắc IV của constitution: không đưa con số vào `references/` khi chưa có tập dev và holdout được ghi.
Ý tưởng định dạng học từ một kho công khai về viết học thuật; không sao chép số hay câu chữ từ đó.
