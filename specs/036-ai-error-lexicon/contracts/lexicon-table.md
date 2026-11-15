# Contract: `references/ai-error-lexicon.md`

Consumers: the agent (reading path, inventory), `scripts/scan-lexicon.py`, `scripts/validate-package.py`, `tests/test_scan_lexicon.py`.

## Layout

1. YAML front matter with `type: vietnamizer-ai-error-lexicon` and `schema: 1`.
2. A short Vietnamese introduction (at most 12 lines): what the table is, that a hit is a candidate and never an edit by itself, that each row's **Không flag** and the owning pattern's **Không flag** both apply, that the table runs only on prose outside the T1–T6-only genres, and how to read the neighbour columns.
3. Exactly one Markdown table under the heading `## Bảng`, with this header row, in this order:

```text
| ID | Dạng | Loại | Pattern | Sửa | Sau không là | Trước không là | Chữ hoa | Không flag | Ca |
```

4. A section `## Thêm mục` restating FR-004 in one paragraph (LOG first, a calibration case and a guard, then the row; no personal preference).

Field rules are in [data-model.md](../data-model.md) "Lexicon entry". No other table may appear in the file, so the scanner finds the table by its header row without heuristics.

## Validation (`validate-package.py` and `tests/test_scan_lexicon.py`)

- Header row equals the one above, byte for byte.
- Every row has 10 cells; no cell is empty; `—` only in the neighbour columns.
- IDs unique and continuous from `L01`.
- `Loại` in the four allowed values; `Chữ hoa` in `mọi`, `đầu câu`.
- `Pattern` exists in the V/T catalogs.
- Every `Ca` id exists in `calibration/test-cases.md` (source checkout only; the payload has no calibration).
- Every form is NFC and 1–4 syllables.
- Every entry has at least one positive and one guard fixture in `tests/fixtures/lexicon/fixtures.json`.

A failure stops the package build, as the other validator checks do.

## Load route

Read on the whole-article and writing routes only (plan P4). The `SKILL.md` routing row for "Biên tập toàn bài hoặc viết từ brief/outline" adds the file; small edits do not load it. When the skill is given inline (Project knowledge, pasted text) and the file is absent, the agent says once that the lexicon is not available and keeps the catalog checks; it never invents rows.
