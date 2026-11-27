# Data model: Style cards for common Vietnamese writer types

## Style card

A file at `profiles/<family>/styles/<id>.md`. It opens with the heading `# `<id>`: <Vietnamese name>`, followed by eight bullet fields in this order:

1. Dùng khi
2. Thanh ngữ vực
3. Xưng hô
4. Nhịp
5. Thuật ngữ
6. Cách kết
7. Không tự thêm
8. Ca kiểm thử

Constraints:
- At most 1,500 bytes (FR-002).
- The card owns no pattern.
- The card names no person or company.
- A claim about Vietnamese convention cites `docs/sources.md` or is labelled *suy luận* (FR-008).

| id | family | Dùng khi (short) | Nearest existing card (leak pair) | Không tự thêm must name (FR-006) |
|---|---|---|---|---|
| `customer-reply` | `personal-blog` | Reply to one customer: complaint, quote follow-up, delivery delay | `persuasive-marketing`, `work-coordination` | compensation, discounts, deadlines, admissions of fault, promises |
| `internal-announcement` | `enterprise-technical` | Announcement or letter from a signer to all staff: policy, move, leadership letter | `business-operations`, `public-expertise` | approvals, benefits, dates, reasons, thanks |
| `product-requirements` | `enterprise-technical` | PRD, spec, feature proposal, ADR, acceptance criteria | `technical-guide`, `work-coordination` | obligation strength (*phải/nên/có thể*), actors, numbers, conditions, priorities |
| `news-report` | `enterprise-technical` | News item, event report, press release | `persuasive-marketing`, `public-expertise` | reporting-verb strength, attributions, titles, opinions, superlatives |

## Card list block

One block in `SKILL.md`, shaped as `contracts/card-list.md` says. Within each family, cards appear in the same order as in `STYLE_FAMILIES`:

- `personal-blog`: `personal-narrative`, `work-coordination`, `public-expertise`, `persuasive-marketing`, `customer-reply`
- `enterprise-technical`: `technical-guide`, `business-operations`, `academic-analysis`, `internal-announcement`, `product-requirements`, `news-report`

## Routing case (WS01–WS12)

The cases are rows in a new section of `calibration/test-cases.md`, "WS01–WS12 · card cho kiểu người viết (spec 040)". Each row has these columns:

- Ca
- Nguồn
- Context và đầu vào
- Card mong đợi
- Phải giữ
- Không được

Every row's Nguồn is "maintainer dựng", per the settled clarification. Each new card gets one positive case and two leak cases:

| Card | Positive | Leak pairs |
|---|---|---|
| `customer-reply` | WS01: complaint reply with *anh–em*, *dạ* | WS02: same facts as an offer page → `persuasive-marketing`; WS03: same facts as a chat with a colleague → `work-coordination` |
| `internal-announcement` | WS04: leadership letter with a reason and a date | WS05: same change as an SOP step → `business-operations`; WS06: same news as a public LinkedIn post → `public-expertise` |
| `product-requirements` | WS07: PRD line with *phải*, *có thể*, a number and an actor | WS08: same limit as README prose → `technical-guide`; WS09: same rule debated in an engineers' chat → `work-coordination` |
| `news-report` | WS10: news item with *cho biết* and a title | WS11: same launch as a product page with a price and a CTA → `persuasive-marketing`; WS12: same finding as an expert's own post → `public-expertise` |

The runner prompt for a routing case is: "Dùng skill Vietnamizer biên tập toàn bài sau, giữ nội dung và giọng. Chỉ trả bài đã sửa." followed by context and text. A run *picks* a card when the only `profiles/*/styles/*.md` file it reads is that card (research R4).

## Benchmark record

The record goes in `docs/benchmarks.md`. Each arm row holds:
- model id and host;
- date;
- pool manifest SHA-256;
- package commit and zip SHA-256;
- valid runs, mean cost per run, mean seconds;
- fixes and guard breaks as scored by the 038 scorer;
- for each routing case, the number of runs that picked the expected card.
