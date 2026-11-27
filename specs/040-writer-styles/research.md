# Research: Style cards for common Vietnamese writer types

Measured on main `de8a2ba` (0.16.3, spec 039 merged) on 2026-11-27.

## R1. The card list in `SKILL.md` fits only as a list, not a table

**Measured.** `SKILL.md` is 14,428 bytes. `benchmarks/route-budget.json` gives `short-edit` a `max_bytes` of 14,428, so the file has no spare byte. The table under "Chọn card khi làm bài" (header row included) is 764 bytes. The spec estimated 903; that figure was wrong.

| Form, 11 cards | Bytes | Change |
|---|---|---|
| Current table, 7 rows with full paths | 764 | 0 |
| Table, 11 id-only rows plus one path sentence | 897 | +133 |
| One lead line naming the path pattern `profiles/<họ>/styles/<card>.md`, then one list item per family with `purpose `card`` pairs | 749 | −15 |

**Decision.** Use the list form. FR-003 asks that each row carries the card id, that the path is written once as a pattern, and that the family stays visible. The list form keeps all three: one item per family, and inside it one *purpose → `card`* pair per card. It is not literally a table, so `route_budget.py` is unaffected (it reads only the route table) and the validator parses the list instead (R3). Fio's settled answer was "Rút gọn bảng card"; this is the smallest form that keeps `SKILL.md` within budget.

**Alternatives rejected.**
- Keeping the table and cutting 133 bytes from other `SKILL.md` text: it would touch the five chốt or the route table, which spec 038 tuned and measured.
- Raising `max_bytes`: SC-002 forbids it.
- Moving the card list to the resolver: FR-003 requires that the agent can open a card without reading the resolver.

**Risk.** A list may route worse than a table. The early model run (FR-010) measures this on MS01–MS14 against the base arm, so a drop shows before any docs work.

## R2. Card families follow FR-001

FR-001 fixes the families: `customer-reply` goes under `personal-blog`; `internal-announcement`, `product-requirements` and `news-report` go under `enterprise-technical`. Their leaks match that split. `customer-reply` leaks into B14 (dropped particles) and B15 (unclear address). The other three leak into K7 (anonymous authority), K2 (empty institutional phrases) and K5 (empty lead-ins).

Press releases still carry some B risks (B7 praise of the company, B8 inflated titles). The resolver's "read B/K rules only when in doubt" rule covers them, and the card's "Không tự thêm" names superlatives, so no family move is needed. A move would need Fio's yes.

The family lists on the path line are therefore:
- `personal-blog`: five cards (the four current ones and `customer-reply`)
- `enterprise-technical`: six cards

## R3. Validator and test changes

The current checks live in `scripts/validate-package.py`:
- `STYLE_CARDS[:4]` / `[4:]` slicing;
- the line ``f"`{card_path}`" not in skill``, which requires every full path to appear in `SKILL.md`.

**Decision.**
- Replace the slicing with an explicit `STYLE_FAMILIES = {"personal-blog": [...], "enterprise-technical": [...]}`. Derive `STYLE_CARDS` and `STYLE_PROFILE_CARDS` from it, so that every other check keeps its input.
- Replace the path check with a parse of the card list block:
  - the lead line must contain `` `profiles/<họ>/styles/<card>.md` ``;
  - each family item must start with `` `<family>`: `` and list exactly that family's cards as backticked ids, in registry order;
  - no card may appear twice and none may be missing.
- Keep every other check: canonical heading, the eight fields, the resolver registry row, `docs/style-and-voice.md`, and the profile rules pointing to the resolver.

The test change is in `tests/test_package_security.py:521-528`, which hard-codes the seven paths in the expected package inventory; it gains the four new paths. `tests/fixtures/review_contract/development.json` names `public-expertise` only, so it is unchanged. `tests/test_skill_contract.py` has no card-path assertions (checked with grep), so the new red tests go there.

## R4. How "the agent picks the card" is measured

The spec 038 runner (`.finolabs/harness-038/run_round.py`, outside Git) logs every `Read`/`Glob`/`Grep` target. A run *picks* card X when the only `profiles/*/styles/*.md` file it reads is X.

**Measured baseline risk.** In the 038 runs on D01–D34, many runs read no card at all:
- 26 of 120 in `t038early`;
- 11 of 24 in `t038floor`.

Most of those are whole-article edits, where the route table says to read one card. If routing cases show the same skip rate, no arm can reach 9 of 10.

**Decision.**
- The first paid step is a probe: 4 routing cases, 5 runs per model, on the base arm.
- If the base arm reads a card in fewer than 9 of 10 runs on cases whose purpose is clear, the bar in FR-010 cannot be met by card content. In that case the plan stops and asks Fio to choose. One option is to count a run that reads no card but whose output meets the "giữ" and "không được" columns as a pass. The other is to accept a lower bar.
- The probe costs about $3 (20 short runs), against about $95 for the full run (R6).

## R5. Sources for convention claims (FR-008)

These are candidates, to be checked and recorded in `docs/sources.md` with their reliability during implementation. A claim with no source found is labelled as an inference in the card.

| Claim | Candidate source | Note |
|---|---|---|
| *phải / nên / có thể* carry requirement, recommendation and permission | TCVN 1-2:2008 (trình bày tiêu chuẩn quốc gia), which follows ISO/IEC Directives Part 2 | Normative wording for standards; it applies to PRDs by analogy, so the card says so |
| Reporting verbs differ in strength (*cho biết* vs *khẳng định*) | A journalism textbook or style guide, or a public Vietnamese newsroom style guide | Found nowhere yet; fallback is an inference label |
| Customer-service address forms (*anh/chị–em*, *dạ*, *ạ*) and *quý khách* | The B14 sources already in `docs/sources.md` (tiểu từ tình thái, lịch sự) | Already recorded; reuse them |
| Internal announcements keep the signer, the decision and the date | No convention claim; the meaning invariants of principle II already cover it | No source needed |

## R6. Model run size and cost (FR-010)

The base arm is v0.16.3 (main `de8a2ba`, packaged with `scripts/package-plugin.py`). The candidate arm is the branch head once all four cards are in place. Both arms run in the same batch, through the heavy-job lock, with `WORKERS=3` and the load-average gate the runner already has.

| Part | Runs | Estimate |
|---|---|---|
| D11–D34, 2 reps, 2 models, 2 arms | 192 | about $48 (Opus $0.35, Sonnet $0.15 per run, from T035) |
| 12 new routing cases, 10 reps, 2 models, candidate arm | 240 | about $36 (short texts, roughly 60% of an article's cost) |
| MS01–MS14, 2 reps, 2 models, 2 arms | 112 | about $11 |
| Probe from R4 | 20 | about $3 |

The total is about $98 and 10–14 hours of wall time at three workers. Fio approved an early model run on 2026-11-26 ("Test + chạy model sớm"). The figures are estimates and are reported with the actual cost.

## R7. Teachers, public sector, legal

These need no research. The spec keeps them out of scope: teachers use the existing cards; public-sector and legal text stays behind the T1–T6 gate (FR-012).
