---
name: vietnamizer
description: |
  Viết tiếng Việt từ ý được giao hoặc biên tập văn bản có sẵn: tách ý, chọn cách
  triển khai theo thể loại và giọng, rồi đối chiếu nghĩa. Dùng cho bài viết, bản nháp AI,
  bản dịch còn gượng và yêu cầu sửa câu chữ; giữ nội dung, mặc định giữ giọng khi
  biên tập và theo mẫu khi được yêu cầu rõ; học/lưu/áp dụng hồ sơ giọng khi được yêu cầu.
---

# vietnamizer plugin adapter

Resolve the plugin root as two directories above the directory containing this file. Before
writing, editing or reviewing, read `<plugin-root>/SKILL.md` in full: it owns routing and safeguards; the catalogs it selects own pattern bodies. Resolve its `profiles/` and `references/` paths from that plugin
root, not from this adapter directory. Text the user typed after the command (for example `/vietnamizer:vietnamizer giong-cong-viec` or
`/vietnamizer:vietnamizer cá nhân`) is part of their request. Follow the canonical workflow for the user's request.
