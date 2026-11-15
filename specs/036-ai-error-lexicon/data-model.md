# Data model: AI-error lexicon, phrase inventory and optional scanner

## Lexicon entry (one row of `references/ai-error-lexicon.md`)

| Field (column) | Type | Rule |
|---|---|---|
| `ID` | `L` + two digits | Unique, continuous from `L01` in table order |
| `Dạng` | one form | 1–4 syllables, written in NFC, lower case. One form per row, so each row has fixes that fit that form only |
| `Loại` | one of `từ ghép bị cắt`, `dịch sát`, `từ nghề hiểu sai`, `danh từ tập thể đứng trơ` | The four kinds of spec scope 1 |
| `Pattern` | `V9`, `V19`, `V20` or another existing V/T id | Must exist in the catalog files (validator) |
| `Sửa` | one or more fixes separated by ` / ` | Non-empty; every fix replaces the whole form; the agent picks the one that fits the sentence |
| `Ngữ vực lỗi` | prose | Registers or genres where the form is an error (FR-001), for example "văn bản giới thiệu, hướng dẫn, bài chuyên môn". Always inside the table's global scope: prose outside the T1–T6-only genres |
| `Sau không là` | syllables separated by `, `, or `—` | A match followed by one of these is not a candidate (completing neighbours: *rà* after *rườm*) |
| `Trước không là` | syllables separated by `, `, or `—` | A match preceded by one of these is not a candidate |
| `Chữ hoa` | `mọi` or `đầu câu` | `đầu câu`: see "Sentence start" below |
| `Không flag` | prose | Registers and contexts where the form is correct; the agent's check. Non-empty |
| `Ca` | case ids separated by `, ` | At least one positive HF/LX case and at least one guard case id |

`—` is the only allowed "empty" value, and only in the two neighbour columns. Every other column must be filled (FR-005, FR-001). The table is the single source for both paths (spec decision 2).

### Sentence start (`Chữ hoa: đầu câu`)

A capitalised form is at a sentence start when the text before it on its line, after removing one leading Markdown marker (`-`, `*`, `+`, `1.`/`1)`, `>`, or `#` to `######`) and spaces, is empty; or when it follows `.`, `!`, `?`, `…`, `:`, `;` or `—`, with optional closing quotes and spaces between. Colon and dash are included because AI text often opens a clause there with a capital (HF02 shape), even though T2 may later remove the colon.

## Seed entries (from merged HF01–HF18)

Drafted so the review can check coverage; the implementation writes the final Vietnamese wording.

| ID | Dạng | Loại | Pattern | Sửa | Ngữ vực lỗi | Sau không là | Trước không là | Chữ hoa | Không flag (gist) | Ca |
|---|---|---|---|---|---|---|---|---|---|---|
| L01 | rườm | từ ghép bị cắt | V20 | rườm rà | Văn viết | rà | — | mọi | Văn nói, chat | HF02, HF10, HF09 |
| L02 | bỡ | từ ghép bị cắt | V20 | bỡ ngỡ | Văn viết | ngỡ | — | mọi | Văn nói, chat | HF10, HF09 |
| L03 | giữ nghĩa | từ ghép bị cắt | V20 | giữ ngữ nghĩa / giữ nguyên nghĩa | Giới thiệu sản phẩm, hướng dẫn, bài chuyên môn | vụ, tình, cử, khí | — | mọi | Câu trang trọng đã đủ ý (*giữ nghĩa của nguyên tác*); chat | HF11, HF17 |
| L04 | giữ giọng | từ ghép bị cắt | V20 | giữ giọng văn | Giới thiệu sản phẩm, hướng dẫn, bài chuyên môn | văn, nói, điệu | — | mọi | Chat, nhãn giao diện ngắn | HF11, HF12, HF16 |
| L05 | nghĩa và giọng | từ ghép bị cắt | V20 | ngữ nghĩa và giọng văn | Giới thiệu sản phẩm, hướng dẫn, bài chuyên môn | văn, nói, điệu | ngữ, ý | mọi | Chat | HF11, HF12 |
| L06 | gọi tên | dịch sát | V9 | xác định / chỉ đích danh / nêu tên | Văn viết | — | — | mọi | Nghĩa đen, gọi tên người hay vật | HF11, HF14, HF13 |
| L07 | dịch sát | từ nghề hiểu sai | V19 | dịch thô | Văn bản cho người ngoài nghề | nghĩa | — | mọi | Người đọc là người trong nghề | HF11, HF15 |
| L08 | đội | danh từ tập thể đứng trơ | V20 | đội ngũ / cả đội (khi ngữ cảnh nói toàn đội) / tên đội cụ thể | Bài đăng công việc, giới thiệu, báo cáo | ngũ, trưởng, viên, hình, quân, tuyển, bóng, nhóm, tàu, xe, bay, lân, mũ, nón, ơn, lốt, sổ, vốn, giá | — | đầu câu | *đội* đã có quy chiếu hoặc định ngữ; *đội* là động từ | HF07, HF08 |

Coverage against FR-003 (as amended): error forms of HF02, HF07, HF10, HF11, HF14 are in L01–L08; word-level guards HF08, HF09, HF12, HF13, HF15, HF16, HF17 each appear in a `Ca` cell. HF01 and HF03–HF06 are T2 (punctuation, not lexicon). HF18 is profile routing (no lexicon form).

Notes:

- L03 and L05 overlap on HF11 (*giữ nghĩa và giọng*). Both are reported; the inventory merges overlapping candidates into one row (below), so one in-place fix *giữ ngữ nghĩa và giọng văn* resolves both.
- L08: lower-case *đội* inside a sentence is left to the reading path and the inventory, because it is a verb or has a referent far more often than not; the lexicon targets the observed failure (sentence-initial *Đội*, HF07 and the Sonnet run on 0.16.2). Widening it is a future FR-004 change with its own evidence.
- The neighbour lists only remove candidates. A compound missing from a list yields a candidate the agent keeps under **Không flag**; it never yields an edit by itself.

## Candidate (scanner output, reading-path row source)

| Field | Type | Rule |
|---|---|---|
| `entry` | `L..` id | Existing entry |
| `text` | string | The matched text exactly as written in the input (original code points, original case) |
| `line`, `column` | int, 1-based | Position of the first character in the original input; column counts Unicode code points |
| `paragraph` | int, 1-based | Paragraphs are separated by one or more blank lines |
| `zone` | `null` or `frontmatter`, `code`, `link-url`, `quote`, `blockquote` | research.md R5 |

A candidate is not an error. It becomes an edit only through an inventory row.

### Zone semantics for the agent

- `frontmatter`, `code`, `link-url`: frozen. The row is recorded as `giữ: vùng bảo toàn`; never edited.
- `quote`: frozen when it is a verbatim quotation (SKILL.md "Trước khi làm"); a term put in quotes for emphasis is judged like any other row.
- `blockquote`: structure only (callouts, notes, summaries). Judged like any other row unless the blockquote is itself a verbatim quotation.

## Inventory row (internal, agent-side)

| Field | Rule |
|---|---|
| Paragraph | Every paragraph in scope appears at least once; a paragraph with no suspect appears as visited |
| Phrase | As written; when candidates overlap, the union of their spans |
| Suspect | Pattern id or lexicon entry ids (all overlapping entries) |
| Evidence | Context that supports the suspicion (register, referent, neighbour words) |
| Fix | Proposed replacement at the smallest unit (chốt 4), applied once for the merged span |
| Không flag result | `sửa` or `giữ: <reason>`; `giữ` leaves the phrase byte-identical (SC-006) |
| Source | `lexicon` (scanner or reading) or `catalog` |

State transitions: candidate → row (always; overlapping candidates share one row) → `sửa` (edit kept, then rescanned) or `giữ` (no edit). A voice adjustment that recreates a lexicon form outside its **Không flag** sends the row back to `sửa` and the adjustment is reverted (FR-016).

## Fixture

Stored in `tests/fixtures/lexicon/fixtures.json` (scanner, deterministic) and mirrored as block LX in `calibration/test-cases.md` (agent judgment, by hand).

| Field | Rule |
|---|---|
| `id` | `LXF` + two digits |
| `text` | Short Vietnamese text, NFC unless the fixture tests normalisation |
| `expected` | List of candidates (`entry`, `text`, `line`, `column`, `zone`); empty for a lexical guard |
| `agent` | `sửa` with the expected output, or `giữ` (register guard: candidate expected, no edit) |
| `cases` | HF or LX ids it comes from |

Each entry has at least one positive fixture and one guard fixture (FR-017). Two kinds of guard: **lexical** (the scanner must return nothing: *rườm rà*, *bỡ ngỡ*, *Đội ngũ*, *giữ nghĩa vụ*, *dịch sát nghĩa*) and **register** (the scanner returns the candidate, the agent keeps the text: HF12, HF13, HF15, HF16, HF17, HF08). Normalisation and position fixtures: NFD input, a soft hyphen inside *rườm­rà*, a line break between *giữ* and *nghĩa*, sentence-initial *Đội* in a paragraph, after `- `, after `1. `, after `> ` and after `: `, inner *đội*, and the L03/L05 overlap of HF11.
