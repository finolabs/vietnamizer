# Contract: profile format additions (spec 030)

Builds on `specs/028-voice-profile/contracts/profile-format.md` and its 13/11/2026 amendment. `schema` stays `1`.

```markdown
---
type: vietnamizer-voice-profile
name: <user-chosen name>
kind: brand            # or personal; absent = personal
schema: 1
language: vi
updated: <YYYY-MM-DD>
---

> Dựa trên khoảng <N> mẫu (<per-source counts: dán / export / trình duyệt>); số đếm xấp xỉ · cập nhật <date>.

## Quy tắc thương hiệu          <!-- brand profiles only -->
- <rule> — nguồn: <neutral code such as "quy chuẩn-01", or "người dùng nêu"; never a file name or title> — phạm vi: <where it holds>

## Giọng chung
...                            <!-- as spec 028 + PR #39 -->

## Điểm chưa quyết
...

## Lịch sử chấm
- <YYYY-MM-DD> · <n> đoạn · Tốt <a>, Khá <b>, Trung bình <c>, Kém <d>, chưa chấm <e> — đánh giá của người dùng, không phải điểm chất lượng.
```

Rules
- A profile without `kind` is personal; a profile without `Quy tắc thương hiệu` or `Lịch sử chấm` stays valid.
- `Quy tắc thương hiệu` is reference data from the user's guide, never instructions to the agent.
- `Lịch sử chấm` stores counts only: no paragraph text, no topic, no reason text.
- A brand profile records no author names, staff names, customer names or document titles that identify people.
