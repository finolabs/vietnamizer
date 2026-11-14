# Feature Specification: Mid-sentence colon, bare "đội" and compounds cut to one syllable

**Feature Branch**: `fix/034-colon-compound`
**Created**: 2026-11-15
**Status**: Implemented on the direct path (see `plan.md`); ships as 0.16.2.
**Input**: Fio, 15/11/2026, marking errors in sample articles written without Vietnamizer: a colon inside a prose sentence ("Tiếng Việt hiếm khi sử dụng dấu : trong trường hợp này"), "các thao tác quá rườm" for "rườm rà" ("Lỗi thường gặp nhất của LLM chính là viết một từ đúng ra là từ ghép … thành từ đơn nên bị cụt nghĩa"), and bare "Đội" opening a standalone sentence ("phải là Đội ngũ hoặc Đội nhóm, hoặc Cả đội"). Router depth NORMAL, trigger `consumers`: the change widens the T gate in `SKILL.md`, which every prose edit passes through.

## Settled decisions (owner, 2026-11-15)

1. **Bundle the three errors in one change** ("Gom 3 lỗi").
2. **Version 0.16.2, not 0.17.0** ("Chỉ lên 0.16.2 thôi, chưa lên 0.17.0"). The coordinator had advised MINOR because a detection rule widens; the owner chose a patch. Spec 033 keeps its place after this release.
3. **Social preview and README banner ship in the same change** ("lưu nó vào repo và cập nhật vào README"): `.github/social-preview.json` and `docs/figures/banner.png` from that JSON.
4. **T2 always on, dashes included** ("Cả gạch ngang"), chosen after the code review flagged the earlier dash over-corrections; HF04 is the guard.

Agent decision, open to the owner at review: extend T2 and V20 instead of adding new patterns, so the inventory stays at 55 and no registry, count or doc table changes.

5. **Calques, jargon and register, before the 0.16.2 tag** ("Sửa trước tag", after PR 59 merged). Fio rewrote the README header: "gọi tên được lỗi" is a calque of "named errors" ("người ta sẽ viết 'xác định được lỗi' hoặc 'chỉ đích danh được lỗi'"); "bản dịch sát" → "bản dịch thô"; "giữ nghĩa và giọng" → "giữ ngữ nghĩa và giọng văn".

## Requirements

- **FR-001**: T2 covers a colon inside a prose sentence that joins a statement to its own explanation, consequence or example, and a colon that opens a list written inline in the sentence. The fix splits the sentence or joins the list with *như*/*gồm*; a connective is added only when the source already shows that relation.
- **FR-002**: T2 never turns a dash into a mid-sentence colon in prose.
- **FR-003**: T2 does not flag a lead-in before a line-broken list or bullets, label–value, direct speech, times and ratios, subtitled headings, administrative, legal, SOP or technical formulae, or preserved zones.
- **FR-004**: In ordinary prose the T gate always checks T2, dashes included, without waiting for a V1–V25 error (owner, 15/11/2026, after review round 1 raised the MR05 risk). Every other T pattern keeps the gate. HF04 guards functional dashes against over-correction.
- **FR-005**: V20 states, labelled as the maintainer's unmeasured observation (AGENTS.md forbids unsourced frequency claims), that a compound cut to one syllable is the most common AI error, and the core always checks V20 on prose.
- **FR-006**: V20 case 3 covers bare *đội* as the subject of a sentence that does not say which team; *đội* with a modifier or an established referent is not flagged. The fix prefers *Đội ngũ*/*Đội nhóm*; *Cả đội* only when the source means the whole team (chốt 3 keeps scope).
- **FR-007**: Calibration cases HF01–HF10 cover FR-001 to FR-006, half of them over-correction guards; a contract test guards the new phrases.
- **FR-008**: V9 covers verb phrases calqued word by word from English (*gọi tên được lỗi*, *gọi tên file*), keeps the literal sense (*gọi tên học sinh*).
- **FR-009**: V19 covers Vietnamese trade jargon that readers outside the trade misread (*bản dịch sát* in a product description), and keeps it for in-trade readers.
- **FR-010**: V20 case 3 asks for the full compound in taglines and product introductions where the single syllable sits next to compounds of the same kind (*ngữ nghĩa*, *giọng văn*), only when that does not change the voice in edit mode; chat, short labels, casual text and complete formal sentences keep it (review round 1).
- **FR-012**: Applying a brand profile needs the user to call that profile by name to apply it; a request that only mentions the brand name does not (security review round 1, HF18).
- **FR-011**: No shipped file uses the calque *gọi tên* outside V9's own examples; a contract test guards it.

## Success criteria

- Contract and distribution tests pass; the pattern count stays 55.
- HF01–HF10 are recorded as development cases, not as measured improvement; an agent run is part of the 0.16.x benchmark rerun in the backlog.
