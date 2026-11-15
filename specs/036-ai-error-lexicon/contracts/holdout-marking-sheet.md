# Contract: Fio's holdout marking sheet (O2)

One sheet per article, filled before any 0.16.2 or 0.17.0 run over that article. Stored with the article outside Git; the committed manifest holds only ids and SHA-256 of article and sheet. The sheet is the label; nothing else counts as ground truth.

## Header

```text
Bài: H01            Thể loại: blog cá nhân        Model sinh bài: <family / id>
Ngày đánh dấu: dd/mm/yyyy   Người đánh dấu: Fio   SHA-256 bài: <hex>
```

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

- A marked error is **fixed** when the output no longer contains the marked span as written and contains one accepted fix in the same paragraph, or Fio accepts the output's fix when the cell was empty.
- A guard is **broken** when its span is not byte-identical in the output.
- Edits outside both tables are listed for Fio, blind to which version made them, as `đúng`, `không cần` or `sai`; `sai` counts as an over-correction, `không cần` is reported separately.
- Time and tokens come from the run log, not from Fio.
