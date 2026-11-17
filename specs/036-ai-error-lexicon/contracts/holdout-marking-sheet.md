# Contract: Fio's holdout marking sheet (O2)

One sheet per article, filled before any 0.16.2 or 0.17.0 run over that article. Stored with the article outside Git; the committed manifest holds only ids and SHA-256 of article and sheet. The sheet is the label; nothing else counts as ground truth.

## Header

```text
Bài: H01            Thể loại: blog cá nhân        Model sinh bài: <family / id>
Ngày đánh dấu: dd/mm/yyyy   Người đánh dấu: Fio   SHA-256 bài: <hex>
Trạng thái: đang chấm | xong
```

The status line is optional; the marking page (`benchmarks/holdout_marker.py`) writes it, the scorer ignores it.

## Bảng lỗi

| # | Đoạn | Cụm như trong bài | Nhóm | Sửa chấp nhận | Ghi chú |
|---|---|---|---|---|---|
| 1 | 2 | các thao tác quá rườm | từ ghép bị cắt | rườm rà | |
| 2 | 4 | Đội đã chốt | danh từ tập thể đứng trơ | Đội ngũ / Nhóm sản phẩm | |

- **Cụm như trong bài**: copied exactly, long enough to be unique in the paragraph.
- **Nhóm**: `từ ghép bị cắt`, `dịch sát`, `từ nghề hiểu sai`, `danh từ tập thể đứng trơ` (the four lexicon kinds, whether or not the form is in the lexicon), or `khác: V<n>` / `khác: T<n>` / `khác` for other errors. The lexicon kinds and the rest are reported separately.
- **Sửa chấp nhận**: one or more fixes separated by ` / `; any of them counts as fixed. Leave empty only when any natural fix is fine; then Fio judges that row on the output.

## Bảng cần giữ

| # | Đoạn | Cụm phải giữ nguyên | Vì sao |
|---|---|---|---|
| 1 | 3 | giữ nghĩa của nguyên tác | câu trang trọng, đã đủ ý |

Spans that look like an error but are correct in context. A change to any byte of a listed span counts as an over-correction. Aim for at least two per article where the text allows.

## What counts

Before any comparison, the sheet, the article and every output are normalised to Unicode NFC, so a generator's NFD text never counts as a change. Every source sentence of the article, marked or not, is aligned one-to-one to output sentences, keeping order (`difflib` over the two sentence lists; a pair needs a ratio of at least 0.5). Each aligned pair is diffed by token, where a word, a run of whitespace and each punctuation mark are separate tokens, with offsets in characters, so whitespace and punctuation changes show. A marked span is a character range in its source sentence and must not cross a sentence boundary; the rules below look only at that range and the output it maps to.

- A marked error is **fixed** when the diff changes the span (inside it or at its edges) and one accepted fix appears, as whole words, in the output at the span's place, covering the changed output (not needed when part of the span was deleted) and covering output that comes from the span itself: kept span characters, the output of a change overlapping the span, text inserted strictly inside it, or the place of a deletion inside it. An accepted fix that was already inside an unchanged span, or one made only of text added at the span's edge, does not count. When the cell was empty, Fio judges the aligned output. A source sentence with no aligned output sentence goes to Fio's out-of-span list and its rows are never counted as fixed.
- A guard is **broken** when any character of its span changes, text is inserted inside it, or its sentence has no aligned output sentence. Each broken guard counts as one over-correction.
- Edits outside both tables are listed for Fio, blind to which version made them, as `đúng`, `không cần` or `sai`; `sai` counts as an over-correction (except on a deleted sentence whose guard is already counted), `không cần` is reported separately. An edit is a diff piece not wholly inside a marked span (the part an accepted fix explains is left out, so `rườm.` → `rườm rà!` lists `.` → `!` and `rườm rà vô lý` lists ` vô lý`; text added at the edge of a span with an empty fix cell stays with that row for Fio), a changed gap between sentences (a deleted sentence takes one gap with it, an added sentence may bring one plain gap, a single space or a paragraph break; a line break inside a paragraph counts as one space, as Markdown renders it), a deleted source sentence or an added output sentence. Its id is built from the article, the source sentence, the character offset and the old and new text, so the same edit from two versions or models is judged once and equal edits in two articles stay apart.
- In a table section, any line with a `|` must be a table row opening and closing with `|` and having the table's number of cells; otherwise the sheet is refused.
- Time and tokens come from the run log, not from Fio.
