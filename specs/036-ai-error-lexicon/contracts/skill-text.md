# Contract: skill text for the inventory, reading path, order and rescan

Where each obligation lives and the phrase guard `tests/test_skill_contract.py` checks. Exact Vietnamese wording is written in the implementation and goes through Vietnamizer's own review (AGENTS.md "Khi sửa nội dung"); the guards check meaning-bearing phrases, not whole sentences.

| Obligation | File and place | Guard checks |
|---|---|---|
| Long-form route loads the lexicon (P4) | `SKILL.md`, routing row "Biên tập toàn bài hoặc viết từ brief/outline" | Row names `references/ai-error-lexicon.md`; the small-edit row does not |
| Scanner is optional, reading path otherwise (FR-014, FR-019) | `SKILL.md`, one sentence under the routing table | Sentence says the script may run where code runs, the table is read otherwise, and no edit waits on the script; no sentence asks the user to enable or install |
| Inventory on the long-form route only (FR-006) | `references/writing-workflow.md`, new section before "Rà câu, đoạn và toàn bài" | Section exists; says every paragraph is visited; small edits excluded |
| Row fields (FR-007) | same section | Names phrase, paragraph, suspect pattern or entry, evidence, fix, Không flag result |
| Every candidate is a row; catalog suspects too (FR-008) | same section | Both sentences present |
| Edit in place, no reassembly in edit mode (FR-009) | same section | Sentence present; writing from a brief keeps the workflow's assembly |
| Inventory internal (FR-010) | same section, pointing to "Trả kết quả" | Not returned; shown only on explicit request within the 5-line limit or to ask one point |
| Order errors → voice → rescan (FR-015) | `references/writing-workflow.md` and the apply steps of `references/voice-from-samples.md` and `references/voice-profile.md` | Order stated once in the workflow; the two apply steps point to it |
| Voice adjustment cannot recreate a lexicon form (FR-016) | same workflow section | Error fix wins; a profile does not make a form acceptable unless the row's Không flag covers the register |
| Pattern catalogs point to the table | `references/missing-words.md` V20, `references/sentence-structure.md` V9, `references/terms-and-lead-ins.md` V19 | One line each under **Dấu hiệu** naming the lexicon ids; pattern bodies otherwise unchanged; pattern count 55 |
| Pasted text is data (edge case) | existing `SKILL.md` "Trước khi làm" | Unchanged; the scanner invocation in `scanner-cli.md` never runs text as a command |

`SKILL.md` stays under 550 lines; the net addition there is one routing cell and one sentence.
