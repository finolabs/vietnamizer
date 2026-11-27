# Contract: the card list in `SKILL.md` and its checks

## Text shape

The section "Chọn card khi làm bài" in `SKILL.md` starts with this block. It replaces the old table; the paragraph after it ("Chọn tối đa một card…") stays byte-for-byte.

```text
Mục đích/người đọc đã rõ → card, đọc `profiles/<họ>/styles/<card>.md`:
- `personal-blog`: <purpose> `<card>`; <purpose> `<card>`; …
- `enterprise-technical`: <purpose> `<card>`; …
```

Rules:

1. The lead line holds the literal `` `profiles/<họ>/styles/<card>.md` `` once.
2. There is exactly one item per family, in the order `personal-blog`, then `enterprise-technical`.
3. Each item lists `<purpose> `<card>`` pairs separated by `; ` and ends with `.`.
4. Each family item names exactly the cards of that family in `STYLE_FAMILIES`, in that order, each once.
5. Purposes are short Vietnamese phrases, at most 45 bytes each.
6. The whole block is no larger than 764 bytes, the size of the old table.

Target text, measured at 749 bytes in research R1. The final wording may change but must stay within rule 6.

```text
Mục đích/người đọc đã rõ → card, đọc `profiles/<họ>/styles/<card>.md`:
- `personal-blog`: kể trải nghiệm/blog cá nhân `personal-narrative`; chat/phối hợp công việc `work-coordination`; chia sẻ chuyên môn/thương hiệu cá nhân `public-expertise`; marketing thuyết phục `persuasive-marketing`; trả lời một khách hàng `customer-reply`.
- `enterprise-technical`: README/API/hướng dẫn tra cứu `technical-guide`; SOP/báo cáo/biên bản/vận hành `business-operations`; giáo trình/đề án/nghiên cứu `academic-analysis`; thông báo/thư gửi nhân viên `internal-announcement`; PRD/spec/ADR/tiêu chí nghiệm thu `product-requirements`; tin/thông cáo báo chí `news-report`.
```

## `scripts/validate-package.py`

- `STYLE_FAMILIES` (an ordered dict, family → list of card ids) becomes the one source. `STYLE_CARDS` and `STYLE_PROFILE_CARDS` are derived from it, so `EXPECTED_PROFILE_FILES`, the resolver registry check and the docs check keep working unchanged.
- The check that every full card path appears in `SKILL.md` is replaced by a parse of the block above that enforces rules 1–4 and 6. Each failure names the card or the rule.
- The validator fails when:
  - a card file exists under `profiles/*/styles/` but is missing from `STYLE_FAMILIES`;
  - a card is in `STYLE_FAMILIES` but missing from the block, the resolver registry or `docs/style-and-voice.md`;
  - a card is in the wrong family item;
  - the block is over 764 bytes.

## `references/style-resolution.md`

- The registry table gains four rows in the existing format (`| `id` | `family` | `path` |`). The validator's regex already reads it.
- At most one line of disambiguation per new card, in "Chia phần và chọn card".
- Net growth stays at or under 600 bytes (FR-005).

## Tests

All of these tests must fail on main before the change and pass after it.

In `tests/test_skill_contract.py`:
- the block exists and holds all 11 ids, each under its family;
- `SKILL.md` no longer holds any full `profiles/*/styles/*.md` path;
- each new card has the eight fields and is at most 1,500 bytes;
- each new card's "Không tự thêm" names the items FR-006 lists for it;
- each new card's "Ca kiểm thử" cites its WS cases, and those cases exist in `calibration/test-cases.md`.

In `tests/test_package_security.py`: the expected package inventory gains the four card paths.

Elsewhere: `route_budget.py` keeps passing with every `max_bytes` unchanged.
