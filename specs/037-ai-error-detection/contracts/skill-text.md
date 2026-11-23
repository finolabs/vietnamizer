# Contract: skill text for the recognition tests and the detection pass

Where each obligation lives and what `tests/test_skill_contract.py` checks. Exact Vietnamese wording is written in the implementation from development examples only and goes through Vietnamizer's own review (AGENTS.md "Khi sửa nội dung"); the guards check meaning-bearing phrases, not whole sentences.

| Obligation | File and place | Guard checks |
|---|---|---|
| Calque test (FR-001–FR-003) | `references/sentence-structure.md`, V9, a paragraph **Phép thử nhận diện** after **Dấu hiệu** | Paragraph exists; names the back-translation question and the "người Việt viết khác" question; at least three examples; **Không flag** names standard calques and in-trade terms |
| Clipped-compound test | `references/missing-words.md`, V20, **Phép thử nhận diện** | Paragraph exists; asks about a one-syllable content word whose role needs a two-syllable word in written prose; at least three examples; points to V20 **Không flag** |
| Bare-collective test | same paragraph of V20 | Names collective nouns beyond *đội*; asks for a determiner or earlier referent; at least three examples |
| Ambiguity questions (decision 8) | V20 clipped-word test question (3); `references/terms-and-lead-ins.md`, V19, **Phép thử nhận diện, từ nghề** | A bare form with two meanings in the same article is a candidate in any genre; a trade term a reader outside the trade can take in its everyday sense, or with a second meaning in the article, is a candidate; V19 **Không flag** keeps in-trade terms except in those two cases |
| Narrower keep rules (decision 8) | V20 **Không flag** and "Phân biệt câu ngắn có chủ ý với câu thiếu từ"; V15 **Không flag** | Trade shorthand and terse style are kept only in labels, table cells and bullets; V15 does not protect a causal *Với việc X, Y* |
| Examples by rule (decision 8, FR-002) | V9, V20, V19 tests | No example quoted from a scored development article; each test pairs fixes with keep examples |
| No new pattern (FR-003) | catalogs | Pattern count 55; V9 and V20 headings unchanged |
| Long-form route loads both catalogs (P4) | `SKILL.md`, routing row "Biên tập toàn bài hoặc viết từ brief/outline" | Row names `references/missing-words.md` and `references/sentence-structure.md`; the small-edit row does not add them |
| Detection pass before fixing (FR-005) | `references/writing-workflow.md`, head of "Kê cụm khi biên tập toàn bài" | Says every sentence in scope is visited, the four tests (V9, two in V20, V19) apply to each, each kind of phrase is walked and sentences with figures, comparisons or negation are named, hits become inventory rows, a sentence with no hit is recorded as visited, and fixing starts after the walk |
| Small edits exempt (FR-006) | same section | Existing "sửa nhỏ không lập bảng kê" kept |
| Lexicon is examples, not the detector (FR-008) | `references/ai-error-lexicon.md`, intro | Says a row hit is a known example and an article with no hit is not clean; points to the tests |
| Scanner gone from the skill text (FR-008) | `SKILL.md`, `references/writing-workflow.md` | Neither names `scripts/scan-lexicon.py`; no instruction runs a shell command for detection |
| Inventory internal (FR-007) | unchanged spec 036 text | Existing guards stay green |

`SKILL.md` stays under 550 lines; the net change there is one routing cell and one sentence removed.
