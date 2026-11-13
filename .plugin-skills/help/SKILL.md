---
name: help
description: Hướng dẫn dùng Vietnamizer trong một màn hình (biên tập, viết, giọng cá nhân, giọng thương hiệu, học và chấm giọng), không đọc file của người dùng và không lưu gì; khi người dùng muốn bắt đầu, chạy bước thiết lập giọng theo cổng đồng ý đọc và lưu của skill.
---

# vietnamizer help adapter

Resolve the plugin root as two directories above the directory containing this file. Read
`<plugin-root>/references/help.md` when it exists (source checkout); otherwise read
`<plugin-root>/skills/vietnamizer/references/help.md` (packaged plugin). Follow that file. When the user
starts the voice setup it describes, also read `SKILL.md` and the references it names from the
directory that contains that `references/` folder. Do not read any other file of the user's to answer help.
