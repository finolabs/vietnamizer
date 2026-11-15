# Data model: AI-error lexicon, phrase inventory and optional scanner

## Lexicon entry (one row of `references/ai-error-lexicon.md`)

| Field (column) | Type | Rule |
|---|---|---|
| `ID` | `L` + two digits | Unique, continuous from `L01` in table order |
| `Dạng` | one or more forms separated by ` / ` | Each form is 1–4 syllables, written in NFC, lower case unless the case column says otherwise |
| `Loại` | one of `từ ghép bị cắt`, `dịch sát`, `từ nghề hiểu sai`, `danh từ tập thể đứng trơ` | The four kinds of spec scope 1 |
| `Pattern` | `V9`, `V19`, `V20` or another existing V/T id | Must exist in the catalog files (validator) |
| `Sửa` | one or more fixes separated by ` / ` | Non-empty; the agent picks the one that fits the sentence |
| `Sau không là` | syllables separated by `, `, or `—` | A match followed by one of these is not a candidate (completing neighbours: *rà* after *rườm*) |
| `Trước không là` | syllables separated by `, `, or `—` | A match preceded by one of these is not a candidate |
| `Chữ hoa` | `mọi` or `đầu câu` | `đầu câu` matches only a capitalised form at a sentence start: the first syllable of a paragraph, or the first after `.`, `!`, `?` or `…` followed by optional closing quotes and spaces (bare *Đội* opening a sentence) |
| `Không flag` | prose | Registers and contexts where the form is correct; the agent's check. Non-empty |
| `Ca` | case ids separated by `, ` | At least one positive HF/LX case and, for every entry, at least one guard case id |

`—` is the only allowed "empty" value, and only in the two neighbour columns. Every other column must be filled (FR-005, FR-001). The table is the single source for both paths (spec decision 2).

## Seed entries (from merged HF01–HF18)

Drafted here so the review can check coverage; the implementation writes the final Vietnamese wording.

| ID | Dạng | Loại | Pattern | Sửa | Sau không là | Trước không là | Chữ hoa | Không flag (gist) | Ca |
|---|---|---|---|---|---|---|---|---|---|
| L01 | rườm | từ ghép bị cắt | V20 | rườm rà | rà | — | mọi | Văn nói, chat | HF02, HF10, HF09 |
| L02 | bỡ | từ ghép bị cắt | V20 | bỡ ngỡ | ngỡ | — | mọi | Văn nói, chat | HF10, HF09 |
| L03 | giữ nghĩa | từ ghép bị cắt | V20 | giữ ngữ nghĩa / giữ nguyên nghĩa | — | — | mọi | Câu trang trọng đã đủ ý (*giữ nghĩa của nguyên tác*); chat | HF11, HF17 |
| L04 | giữ giọng / nghĩa và giọng | từ ghép bị cắt | V20 | giữ giọng văn / ngữ nghĩa và giọng văn | văn, nói, điệu | — | mọi | Chat, nhãn giao diện ngắn | HF11, HF12, HF16 |
| L05 | gọi tên | dịch sát | V9 | xác định / chỉ đích danh / nêu tên | — | — | mọi | Nghĩa đen, gọi tên người hay vật | HF11, HF14, HF13 |
| L06 | dịch sát | từ nghề hiểu sai | V19 | dịch thô | — | — | mọi | Người đọc là người trong nghề | HF11, HF15 |
| L07 | đội | danh từ tập thể đứng trơ | V20 | đội ngũ / cả đội (khi ngữ cảnh nói toàn đội) / tên đội cụ thể | ngũ, trưởng, viên, hình, quân, tuyển, bóng, mũ, nón, ơn, lốt, sổ | — | đầu câu | *đội* đã có quy chiếu hoặc định ngữ; *đội* là động từ | HF07, HF08 |

Coverage against FR-003 (as amended): error forms of HF02, HF07, HF10, HF11, HF14 are in L01–L07; word-level guards HF08, HF09, HF12, HF13, HF15, HF16, HF17 each appear in a `Ca` cell. HF01 and HF03–HF06 are T2 (punctuation, not lexicon). HF18 is profile routing (no lexicon form).

Notes on L07: lower-case *đội* inside a sentence is left to the reading path and the inventory, because it is a verb or has a referent far more often than not; the lexicon targets the observed failure (sentence-initial *Đội*, HF07 and the Sonnet run on 0.16.2). Whether to widen it is a future FR-004 change with its own evidence.

## Candidate (scanner output, reading-path row source)

| Field | Type | Rule |
|---|---|---|
| `entry` | `L..` id | Existing entry |
| `text` | string | The matched text exactly as written in the input (original code points, original case) |
| `line`, `column` | int, 1-based | Position of the first character in the original input; column counts Unicode code points |
| `paragraph` | int, 1-based | Paragraphs are separated by one or more blank lines |
| `zone` | `null` or `frontmatter`, `code`, `link-url`, `quote`, `blockquote` | research.md R5 |

A candidate is not an error. It becomes an edit only through an inventory row.

## Inventory row (internal, agent-side)

| Field | Rule |
|---|---|
| Paragraph | Every paragraph in scope appears at least once; a paragraph with no suspect appears as visited |
| Phrase | As written |
| Suspect | Pattern id or lexicon entry id |
| Evidence | Context that supports the suspicion (register, referent, neighbour words) |
| Fix | Proposed replacement at the smallest unit (chốt 4) |
| Không flag result | `sửa` or `giữ: <reason>`; `giữ` leaves the phrase byte-identical (SC-006) |
| Source | `lexicon` (scanner or reading) or `catalog` |

State transitions: candidate → row (always) → `sửa` (edit kept, then rescanned) or `giữ` (no edit). A voice adjustment that recreates a lexicon form outside its **Không flag** sends the row back to `sửa` and the adjustment is reverted (FR-016).

## Fixture

Stored in `tests/fixtures/lexicon/fixtures.json` (scanner, deterministic) and mirrored as block LX in `calibration/test-cases.md` (agent judgment, by hand).

| Field | Rule |
|---|---|
| `id` | `LXF` + two digits |
| `text` | Short Vietnamese text, NFC unless the fixture tests normalisation |
| `expected` | List of candidates (`entry`, `text`, `line`, `column`, `zone`); empty for a lexical guard |
| `agent` | `sửa` with the expected output, or `giữ` (register guard: candidate expected, no edit) |
| `cases` | HF or LX ids it comes from |

Each entry has at least one positive fixture and one guard fixture (FR-017). Two kinds of guard: **lexical** (the scanner must return nothing: *rườm rà*, *bỡ ngỡ*, *đội ngũ*, *ý nghĩa*) and **register** (the scanner returns the candidate, the agent keeps the text: HF12, HF13, HF15, HF16, HF17, HF08). Normalisation fixtures: NFD input, a soft hyphen inside *rườm­rà*, a line break between *giữ* and *nghĩa*, sentence-initial *Đội* vs inner *đội*.
