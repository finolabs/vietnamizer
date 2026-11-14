# Feature Specification: Mid-sentence colon, bare "đội" and compounds cut to one syllable

**Feature Branch**: `fix/034-colon-compound`
**Created**: 2026-11-15
**Status**: Implemented on the direct path (see `plan.md`); ships as 0.16.2.
**Input**: Fio, 15/11/2026, marking errors in sample articles written without Vietnamizer: a colon inside a prose sentence ("Tiếng Việt hiếm khi sử dụng dấu : trong trường hợp này"), "các thao tác quá rườm" for "rườm rà" ("Lỗi thường gặp nhất của LLM chính là viết một từ đúng ra là từ ghép … thành từ đơn nên bị cụt nghĩa"), and bare "Đội" opening a standalone sentence ("phải là Đội ngũ hoặc Đội nhóm, hoặc Cả đội"). Router depth NORMAL, trigger `consumers`: the change widens the T gate in `SKILL.md`, which every prose edit passes through.

## Settled decisions (owner, 2026-11-15)

1. **Bundle the three errors in one change** ("Gom 3 lỗi").
2. **Version 0.16.2, not 0.17.0** ("Chỉ lên 0.16.2 thôi, chưa lên 0.17.0"). The coordinator had advised MINOR because a detection rule widens; the owner chose a patch. Spec 033 keeps its place after this release.
3. **Social preview and README banner ship in the same change** ("lưu nó vào repo và cập nhật vào README"): `.github/social-preview.json` and `docs/figures/banner.png` from that JSON.

Agent decision, open to the owner at review: extend T2 and V20 instead of adding new patterns, so the inventory stays at 55 and no registry, count or doc table changes.

## Requirements

- **FR-001**: T2 covers a colon inside a prose sentence that joins a statement to its own explanation, consequence or example, and a colon that opens a list written inline in the sentence. The fix splits the sentence or joins the list with *như*/*gồm*; a connective is added only when the source already shows that relation.
- **FR-002**: T2 never turns a dash into a mid-sentence colon in prose.
- **FR-003**: T2 does not flag a lead-in before a line-broken list or bullets, label–value, direct speech, times and ratios, subtitled headings, administrative, legal, SOP or technical formulae, or preserved zones.
- **FR-004**: In ordinary prose the T gate always checks the mid-sentence colon part of T2, without waiting for a V1–V25 error. Dashes under T2 and every other T pattern keep the gate (review round 1: keeps the MR05 guard; owner may widen it to dashes).
- **FR-005**: V20 states, labelled as the maintainer's unmeasured observation (AGENTS.md forbids unsourced frequency claims), that a compound cut to one syllable is the most common AI error, and the core always checks V20 on prose.
- **FR-006**: V20 case 3 covers bare *đội* as the subject of a sentence that does not say which team; *đội* with a modifier or an established referent is not flagged. The fix prefers *Đội ngũ*/*Đội nhóm*; *Cả đội* only when the source means the whole team (chốt 3 keeps scope).
- **FR-007**: Calibration cases HF01–HF10 cover FR-001 to FR-006, half of them over-correction guards; a contract test guards the new phrases.

## Success criteria

- Contract and distribution tests pass; the pattern count stays 55.
- HF01–HF10 are recorded as development cases, not as measured improvement; an agent run is part of the 0.16.x benchmark rerun in the backlog.
