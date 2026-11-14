# Contract: help and onboarding (spec 030)

## Help (`/vietnamizer:help`, or "vietnamizer giúp gì", "hướng dẫn dùng vietnamizer")

One screen, Vietnamese, reads no user file, saves nothing:
1. What it does: edit Vietnamese drafts and translations, keep meaning and voice; write new text.
2. Voices: default keeps your own voice; a named personal profile; a named brand profile (one per use).
3. Learn a voice: paste posts, give a LinkedIn or Facebook export, or read your own page in the browser (LinkedIn and Facebook carry a terms warning).
4. Check a voice: rate sample paragraphs (Tốt, Khá, Trung bình, Kém).
5. How to start each, with one example request per line, and the offer: "Muốn bắt đầu thiết lập giọng không?"

## Onboarding ("bắt đầu", "thiết lập giọng", or yes to the offer)

Each choice through the host form where available, recommended option first; text otherwise. The user can stop at any step; nothing is saved unless asked at step 6.
1. Voice kind: Cá nhân (recommended) | Thương hiệu.
2. Source: Dán bài (recommended) | File export | Đọc trang qua trình duyệt (shown only for Cá nhân and only when the host has a browser tool; never for Thương hiệu, see `references/brand-voice.md`). Export shows the platform steps.
3. Consent: for the browser source, the LinkedIn and Facebook terms warning first; then the one consent question of spec 028 mục 2, naming the source. For an export or a page, that same question asks whether the account is the user's own; for a brand, whether the user may speak for the brand. Neither becomes a separate question.
4. Learn: draft the full profile (spec 028 mục 3, PR #39, spec 030 additions).
5. Rate: the rating session contract (count first; 0 skips).
6. Save: spec 028 mục 4 (store choice, name, path); a no ends with the profile left in the conversation.

Question budget before rating: at most 6 (kind, source, platform when needed, consent, plus one follow-up).
