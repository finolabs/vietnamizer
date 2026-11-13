# Data model: spec 030

Additions to the spec 028 data model (and the PR #39 amendment). Everything is optional for old profiles.

## Voice profile

- `kind`: `personal` | `brand`; absent means `personal`.
- `brand_rules[]` (brand only): {statement, source label (guide name or "người dùng nêu"), scope}. Rules are quoted or paraphrased from the guide, redacted.
- `voice`, `surfaces[]`, `tone_shifts[]`, `dos[]`, `donts[]`, `open_points[]`: as in spec 028 and PR #39. In a brand profile, evidence comes from brand posts or documents; author identity is never recorded.
- `rating_history[]`: {date, paragraph_count, tot, kha, trung_binh, kem, unrated, label}. `label` is fixed: "đánh giá của người dùng, không phải điểm chất lượng".
- Validation: no personal data (spec 028 FR-007) in any field; one profile per use; a brand profile is applied only when named in the current request.

## Learning source (transient)

- `type`: paste | export | browser.
- `platform`: linkedin | facebook | other | none.
- `owner_statement`: yes | no | brand-authorized; `no` stops the flow.
- `kept`, `dropped`: approximate counts, reported to the user, not stored beyond the provenance line.
- `terms_warning_shown`: required `true` before a LinkedIn browser read.

## Rating session (transient until saved)

- `requested_count` (0–10), `answers[]` of Tốt | Khá | Trung bình | Kém | none, `reasons[]` (≤ 2, redacted), `proposed_diff`.
- Becomes one `rating_history` entry only when the user saves or confirms an update.

## State transitions

`no profile` → (consent, source) → `draft` → (optional rating session) → `draft + proposed diff` → (explicit save) → `saved` → (named reuse) → applied → (update with confirmed diff) → `saved`.
