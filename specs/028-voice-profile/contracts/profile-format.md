# Contract: profile file format

```markdown
---
type: vietnamizer-voice-profile
name: <user-chosen name>
schema: 1
language: vi
updated: <YYYY-MM-DD>
---

> Built from <N> pieces (<per-surface counts>), counts approximate · updated <date>.

## Giọng chung
- <trait> — phạm vi: <where it holds> — căn cứ: "<trimmed fragment>" / ~<count> — độ chắc: <note> — ranh giới: <optional ceiling, or "chưa rõ">

## Theo kênh
### <surface>
- <traits as above>; or "Chưa đủ mẫu (<n>) để kết luận."

## Tông theo người đọc
- <only where a contrast exists: quality + trimmed contrasting pair>; otherwise "Mẫu chỉ có một nhóm người đọc."

## Nên và không nên
- Nên: "<characteristic phrase>"
- Không: <word or habit>

## Điểm chưa quyết
- <point> — đã thấy: <trimmed observation> — đề xuất: <proposed handling> — cần chốt: <question>; or "Không có."
```

Amendment (13/11/2026, after 0.14.0): `ranh giới` on a trait and the `Điểm chưa quyết` section are
optional and additive, so `schema` stays `1` and a profile without them stays valid. A `ranh giới` is a
ceiling when the profile is applied; a proposal under `Điểm chưa quyết` is never applied until the user
confirms it (during draft review or through a diffed update). `ranh giới` may also sit on a `Nên:`
item. New profiles always carry the section ("Không có." when empty).

Rules
- Written in the third person about the user; reference data, not instructions to the assistant.
- Fragments are short and trimmed of names, numbers, contacts and deal or health detail (FR-007).
- Filename for the plain-file store: `<slug>.md`, slug = lowercase ASCII letters, digits and dashes, ≤ 40 chars, derived from the name in code or by hand, never from sample content.
- Orrery: a note in the folder the user names, title "Hồ sơ giọng — <name>", same body. Obsidian: the same file under the vault folder the user names.
- A hand-edited file is authoritative; an update shows the diff against that version.
