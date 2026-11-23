# Benchmark: phương pháp, kết quả và giới hạn

[← README](../README.md)

> **Ghi chú (13/11/2026):** Jev đã bị gỡ khỏi Vietnamizer (spec `specs/029-remove-jev/`). Các mục dưới đây
> nhắc nhánh "Vietnamizer + Jev", runner và test của nó là bằng chứng lịch sử đã ngừng dùng; script
> benchmark Jev/công khai và `eval/guard/` đã bị xóa khỏi repo, các file raw nằm trong lịch sử Git.

## Vietnamizer tự biên tập chính nó (0.16.2)

Ngày 15/11/2026, ba model dùng Vietnamizer 0.16.2 (commit `823ce7a`) biên tập lại văn bản của chính gói
skill. Sonnet 5.5, Gemini 3.8 Flash và Opus 5.5 làm riêng, mỗi model trên một nhánh, theo hồ sơ giọng của
tác giả. Fable 5.2 sau đó so từng file với bản gốc và chọn bản tốt nhất, hoặc giữ bản gốc khi không bản nào
tốt hơn. Fable xét nghĩa và phạm vi của từng quy tắc trước, rồi mới tới lỗi được sửa và độ hợp giọng.

| | Bản gốc | Sonnet 5.5 | Gemini 3.8 Flash | Opus 5.5 | Bản phát hành |
|---|---|---|---|---|---|
| File được sửa | | 23 | 28 | 23 | 27 |
| Dấu hai chấm giữa câu | 109 | 78 | 84 | 62 | 60 |
| *rà*, *soát* đứng một mình | 46 | 46 | 45 | 29 | 29 |
| File giám khảo chọn | 16 | 6 | 2 | 18 | |

Phạm vi là 42 file Markdown phát hành cùng gói, gồm `SKILL.md`, `references/`, `profiles/`,
`.plugin-skills/`, README, các file chính sách và `docs/`. Riêng `docs/changelog.md` chỉ tính mục 0.16.2.
Bản phát hành gồm các bản Fable chọn, hai chỗ khôi phục từ bản gốc và mười chỗ sửa lấy từ các bản không
được chọn.

Script `benchmarks/self_edit_count.py` đếm bằng biểu thức chính quy, không dùng model. Có hai dấu hiệu.

- Dấu hai chấm giữa câu được tính khi chữ ngay sau nó viết thường và phía trước nó, trong cùng câu, có
  hơn ba từ.
- Từ ghép bị cắt được tính khi `rà` không có `soát` hoặc `lại` theo sau, hoặc `soát` không có `rà` đứng
  trước.

Script bỏ qua code, dòng bảng, heading, HTML, frontmatter, dòng có URL và nhãn in đậm đầu dòng. Các ví
dụ sai cố ý trong catalog pattern vẫn nằm trong số đếm, nên bản phát hành không về 0. Đây là dấu hiệu cơ
học, không đo chất lượng văn bản, vì có những dấu hai chấm đúng chức năng mà script vẫn tính.

Chạy lại từ thư mục gốc của repo. Ba nhánh biên tập viên chỉ có trên máy tác giả, nên người khác chỉ
chạy lại được cột bản gốc và bản phát hành.

```bash
python3 benchmarks/self_edit_count.py Gốc=823ce7a Sonnet=edit/0162-sonnet Gemini=edit/0162-gemini Opus=edit/0162-opus "Bản phát hành=HEAD"
```

## Holdout 036: 0.17.0 chưa tốt hơn 0.16.2 (17/11/2026)

Spec 036 thêm vào 0.17.0 một bảng từ vựng lỗi hay gặp trong văn bản AI và một script quét các dạng đó. Để
kiểm tra có hiệu quả thật không, hai model sinh 14 bài mới (H01–H07 bằng `claude-opus-5-5`, H08–H14 bằng
`gpt-6`). Tác giả đánh dấu 48 lỗi và 38 cụm đúng phải giữ nguyên; trong 48 lỗi có 33 lỗi thuộc bốn nhóm
của bảng từ vựng. Không agent nào tham gia sửa bảng từ vựng được đọc các bài này. Bài và bảng đánh dấu nằm
ngoài Git; repo chỉ giữ mã băm trong `benchmarks/holdout-036-manifest.json`.

Mỗi bài được chạy với cả hai phiên bản trên Sonnet 5.5 và Opus 5.5 (mức Medium) trong Claude Cowork, tổng
cộng 56 lượt. Yêu cầu gửi kèm bài là "Dùng skill Vietnamizer biên tập bài sau, giữ nội dung và giọng của tác giả.
Chỉ trả bài đã sửa, không giải thích." Argon, Flash và GPT chưa được chạy thử. `benchmarks/holdout_036.py`
chấm theo `specs/036-ai-error-lexicon/contracts/holdout-marking-sheet.md`.

Model được dùng là `claude-sonnet-5-5` và `claude-opus-5-5`. Mã băm của bộ bài là `832539ad281833df23b7c817f9461901b39d14ae727ec9dfd0f5cfb91521a69a`,
của bảng từ vựng là `b846635e5b30c04f876a2935da95d55e10ae2318e02e2748f1e06cb0f5807a4e`. Cowork không cho
xem số token của từng lượt nên bảng không có cột token, chỉ có thời gian đo từ lúc gửi đến khi trả xong.

| Model | Phiên bản | Lỗi nhóm từ vựng đã sửa | Lỗi khác đã sửa | Cụm đúng bị đổi | Thời gian trung bình mỗi bài |
|---|---|---|---|---|---|
| Opus 5.5 | 0.16.2 | 3/33 | 2/15 | 0/38 | 57 giây |
| Opus 5.5 | 0.17.0 | 2/33 | 2/15 | 1/38 | 76 giây |
| Sonnet 5.5 | 0.16.2 | 0/33 | 1/15 | 0/38 | 43 giây |
| Sonnet 5.5 | 0.17.0 | 0/33 | 1/15 | 0/38 | 39 giây |

0.17.0 không sửa được nhiều lỗi hơn 0.16.2 trên model nào, nên chưa đạt tiêu chí SC-005 và chưa được phát
hành. Các chỗ sửa nằm ngoài vùng đánh dấu (95–97 chỗ mỗi bộ lượt Opus, 31–37 chỗ mỗi bộ lượt Sonnet) chưa
được tác giả chấm, nên bảng chưa tính chúng vào số chỗ sửa thừa.

Số liệu cho thấy khâu phát hiện lỗi là chỗ hỏng chắc chắn. Việc model ngại sửa có thể góp phần, nhưng phép đo này chưa tách được hai nguyên nhân.

- Cả 56 lượt đều nạp skill. Với 0.17.0, model đọc bảng từ vựng trong 24/28 lượt và chạy script quét trong
  6 lượt, cả 6 lần đều không ra ứng viên nào.
- Chạy script quét trên máy với 14 bài thì không trúng lỗi nào trong 33 lỗi nhóm từ vựng (23 lỗi dịch sát,
  9 từ ghép bị cắt, 1 danh từ tập thể đứng trơ). 11 ứng viên script đưa ra đều không trùng chỗ tác giả
  đánh dấu.
- Model sửa rất ít. Opus đổi khoảng 50–60 ký tự mỗi bài, Sonnet khoảng 9 ký tự.
- Khi đổi yêu cầu thành "Dùng skill Vietnamizer sửa lỗi tiếng Việt trong bài sau, không viết lại. Chỉ trả
  bài đã sửa." trên bốn bài có 18 lỗi nhóm từ vựng, Opus vẫn để nguyên 16 đến 17 lỗi và sửa còn ít hơn.

Trên 14 bài này, bảng từ vựng cố định 8 dòng không bao quát được lỗi. Spec 037 sẽ làm lại khâu phát hiện và đo
lại trên đúng 14 bài này.

## Spec 037: ca phát triển và cổng chặn (21/11/2026)

Đây là kết quả phát triển, không phải holdout. Ngày 21/11/2026, Fio quyết định không chạy cổng trên Cowork như
plan P8. Cổng chạy trên Claude Code (`claude -p`, plugin cài từ file ZIP qua `--plugin-dir`, giống các vòng
chỉnh T020), với `claude-opus-5-5` và `claude-sonnet-5-5`. Bản ứng viên là commit `1c3e9b7` trên main. File
`~/.claude/CLAUDE.md` của người chạy vẫn được nạp trong mọi lượt, nên kết quả có thêm biến nhiễu này.

**Cổng chặn T022.** Bốn bài chặn D04, D05, D09 và D10 có 4 lỗi nhóm từ vựng, 7 lỗi khác và 12 cụm cần giữ. Mỗi
bài chạy một lượt cho mỗi model và mỗi phiên bản, tổng cộng 16 lượt, chấm bằng `benchmarks/holdout_036.py`.

| Model | Phiên bản | Lỗi nhóm từ vựng đã sửa | Lỗi khác đã sửa | Cụm cần giữ bị đổi |
|---|---|---|---|---|
| Opus 5.5 | 0.16.2 | 0/4 | 0/7 | 1/12 |
| Opus 5.5 | ứng viên | 1/4 | 1/7 | 1/12 |
| Sonnet 5.5 | 0.16.2 | 0/4 | 0/7 | 1/12 |
| Sonnet 5.5 | ứng viên | 0/4 | 0/7 | 0/12 |

Mức P3 đòi Opus sửa ít nhất một nửa và Sonnet ít nhất một phần ba số lỗi nhóm từ vựng, tức 2/4 cho mỗi model.
Cả hai model đều không đạt, nên cổng trượt. Bản ứng viên không làm vỡ thêm cụm cần giữ nào so với 0.16.2. Trên
sáu bài chỉnh, các bản ở lượt chỉnh c9 và c10 (spec 037, mục O2) sửa được 6–7 trên 11 lỗi nhóm từ vựng, nên
các phép thử V9 và V20 hiện mới khớp với bài chỉnh, chưa áp dụng được cho bài mới.

**Chẩn đoán T030** (spec 037, quyết định 8; ngày 23/11/2026). Bản ứng viên `1c3e9b7` chạy trên cả mười bài D01–D10,
mỗi bài một lượt cho mỗi model, trên Claude Code `-p`. Opus được yêu cầu trả kèm bảng kê cụm của skill. Sonnet bị
bộ lọc an toàn của API chặn ở 9 trên 10 lượt có yêu cầu này, nên Sonnet chỉ chạy biên tập bài, không kèm bảng kê.
Số liệu chấm theo phiếu đã thêm hai cách sửa ngày 23/11/2026 (spec 037, mục O2).

| Model | Lỗi nhóm từ vựng đã sửa | Lỗi khác đã sửa | Cụm cần giữ bị đổi |
|---|---|---|---|
| Opus 5.5 | 10/15 | 1/21, 3 dòng chưa chấm | 2/32 (chín bài, không tính D10) |
| Sonnet 5.5 | 6/15 | 1/21, 3 dòng chưa chấm | 0/36 |

Ngoài các cụm đã đánh dấu, Opus còn sửa 25 chỗ trên chín bài và Sonnet sửa 6 chỗ trên mười bài; chưa ai chấm những chỗ này.

Với Opus, bảng kê cho biết lỗi bị sót ở bước nào. Trong 5 lỗi nhóm từ vựng chưa sửa, 4 lỗi không có dòng nào
trong bảng kê (D01#3, D02#4, D03#2 và D05#1, lỗi từ nghề hiểu sai *xếp hàng*), còn 1 lỗi có trong bảng kê nhưng
được giữ (D09#3, *tồn*). Như vậy chỗ hỏng chính là bước dò, chưa phải luật giữ. Ở D10, bộ lọc an toàn chặn câu
trả lời của Opus, nên file đầu ra chỉ có lời báo bị chặn, không có chữ nào của bài. Vì vậy bảng không tính bốn cụm
cần giữ của D10 cho Opus. D10 không có dòng lỗi nào, nên hai cột lỗi không đổi. Hai cụm cần giữ Opus đã đổi là
D04#g1 và D09#g1. Sonnet
sửa được ba lỗi của D01, một lỗi của D02, D03 và D07, và không sửa lỗi nào trong bốn bài chặn cũ.

**Vòng phát triển T034 (23–24/11/2026).** Mọi lượt dùng cùng một lời nhờ biên tập thường, không đòi bảng kê, mỗi
model chạy một lượt cho mỗi bài D01–D10 trên Claude Code `-p`. T034a và T034b chạy bản `c114d3f` (phép thử viết
lại ở T031). T034c chạy bản `0da20a7`: đưa `references/terms-and-lead-ins.md` (phép thử V19) vào bước đọc của
tuyến bài, vì ở T034a/b không model nào mở file này, và thêm vào `SKILL.md` danh sách dạng hay lọt khi bài đọc
trôi, viết theo luật chứ không chép từ bài nào. T034d chạy bản `29ec914`, sau review: danh sách bỏ dạng câu chấm
phẩy vì nó bám sát một lỗi đã đánh dấu (D01#3), bỏ các dạng catalog V9 không có ca giữ để quyết, và giữ nhãn
*Lưu ý:*, *Ghi chú:* ở dạng dấu hai chấm. Dòng bản cũ là `1c3e9b7`, chạy cùng lời nhờ.

| Lượt | Bản | Opus, nhóm từ vựng | Opus, cụm giữ bị vỡ | Sonnet, nhóm từ vựng | Sonnet, cụm giữ bị vỡ |
|---|---|---|---|---|---|
| T030o / T030s | `1c3e9b7` (bản cũ) | 9/15 | 1/36 | 6/15 | 0/36 |
| T034a | `c114d3f` | 6/15 | 3/36 | 2/15 | 0/36 |
| T034b | `c114d3f` | 5/15 | 0/36 | 2/15 | 0/36 |
| T034c | `0da20a7` | 9/15 | 0/36 | 3/15 | 0/36 |
| T034d | `29ec914` | 8/15 | 2/36 | 5/15 | 0/36 |

Opus đã sửa D02#1 (*hàng chậm*) ở cả T034a và T034b. Lỗi từ nghề còn lại, D05#1 (*xếp hàng*), chỉ được sửa ở
T034c và không được sửa lại ở T034d, nên một lượt chưa đủ để nói việc đưa V19 vào bước đọc đã giải quyết lỗi này.
Hai cụm giữ Opus làm vỡ ở T034d (D04#g1, D10#g3) cũng đã vỡ ở T034a. Sonnet sửa được 5/15 ở T034d (D01#4, D01#6,
D02#4, D05#4, D09#3), đúng bằng mức khoảng một phần ba của cổng chặn, nhưng chỉ trong một lượt trên chính các bài
dùng để chỉnh; ba lượt còn lại của Sonnet trên bản mới được 2 đến 3/15, và cổng chặn chấm trên D11–D22. Ở hầu hết
câu có lỗi, bài Sonnet trả về giữ nguyên từng chữ, dù nó đã mở các catalog chứa phép thử.

Bảng trên chấm theo phiếu sau các phán quyết của Fio ngày 24/11/2026. Ở D02#4, phiếu và ca DT06 nhận thêm *chưa
được cập nhật*, cùng cách sửa mà ví dụ V9 dùng sau PR 90 (*không được* dễ đọc thành lệnh cấm); trước đó cách sửa
này của Opus ở T034c/d và của Sonnet ở T034d bị tính là trượt. Ở D01#4, phiếu nhận thêm *"Tôi chỉ gửi một tin mỗi
ngày"*, cách Sonnet viết ở T034a và T034c, và *"Tôi gửi tối đa một tin mỗi ngày"*, cách Sonnet viết ở T034d; ca
DT01 bỏ câu không nhận *chỉ gửi*. Các phán quyết chỉ đổi
các ô của T034; số của T030 không đổi. Ngoài các cụm đã đánh dấu,
ở T034d Opus sửa 45 chỗ và Sonnet sửa 7 chỗ, chưa ai chấm. Mỗi bản chỉ có một đến hai lượt cho mỗi model, nên
chênh lệch một hai lỗi giữa các lượt chưa đủ để kết luận.

**Ca chạy tay T019.** Mỗi ca chạy một lượt cho mỗi model trên bản ứng viên, kèm thể loại ghi trong cột Đầu vào.
Ca DT dùng nguyên đoạn văn trong bài chỉnh chứa câu của ca. Ca LX dùng đúng văn bản của fixture và được so khớp
từng ký tự với cột Mong đợi. Ca HF và DT do agent chạy so với cột Mong đợi, chưa có người chấm lại.

| Khối | Opus 5.5 | Sonnet 5.5 |
|---|---|---|
| HF01–HF17 | 15 đạt, 1 đạt một phần (HF02), 1 trượt (HF11) | 7 đạt, 3 đạt một phần (HF02, HF07, HF10), 3 trượt (HF01, HF04, HF11), 4 hiểu nhầm đầu vào |
| DT01–DT08, ca cần sửa | 5/8 (sót DT04, DT05, DT06) | 5/8 (sót DT04, DT06, DT08) |
| DT09–DT14, ca cần giữ | giữ đủ 8 đoạn | giữ đủ 8 đoạn |
| LX01–LX29 | 14 khớp, 4 hiểu nhầm đầu vào, 11 lệch | 15 khớp, 6 hiểu nhầm đầu vào, 8 lệch |

HF18 chưa chạy, vì ca này cần một hồ sơ thương hiệu đã lưu. Hiểu nhầm đầu vào nghĩa là model coi một đoạn rất
ngắn (lời nhắn chat, nhãn nút, ghi chú) là lời nhờ của người dùng và hỏi lại bài cần sửa. Nhiều khả năng đây là
lỗi của cách dựng ca hơn là của pattern, nhưng chưa có lượt chạy nào kiểm chứng điều này. Trong các ca LX lệch, cả hai
model đều chưa sửa hoặc sửa chưa đủ LX04, LX07, LX11, LX16 và LX23
(*giữ nghĩa*, *bản dịch sát*, *Đội* đầu dòng danh sách), đều làm vỡ LX06 (*giữ nghĩa vụ*) và đều đổi dấu gạch
nối mềm của LX26. Riêng Opus còn sửa *đội* viết thường giữa câu (LX24) và sửa trong lời trích (LX28).

## Trước/sau: sửa chỗ cần sửa, giữ chỗ đã đúng

Ba ví dụ dưới đây là **đầu ra thật trong lượt hồi quy trên cùng Codex** ngày
27/10/2026. Cả hai phiên bản nhận cùng nguồn, ngữ cảnh và yêu cầu; các ô có dấu
`…` chỉ trích phần liên quan, không phải toàn bộ văn bản.

| Ca và mục tiêu | Bản gốc | Sau biên tập với 0.12.0 | Sau biên tập với 0.12.1 |
|---|---|---|---|
| MR04 · sửa thiếu bổ ngữ kết quả | Đã tìm khắp nhà nhưng vẫn không tìm chìa khóa. | Đã tìm khắp nhà nhưng vẫn không tìm **thấy** chìa khóa. | Đã tìm khắp nhà nhưng vẫn không tìm **thấy** chìa khóa. |
| MR05 · giữ điểm ngắt | Tất cả – chỉ khác là… | Tất cả, chỉ khác là… | Tất cả – chỉ khác là… |
| MR12 · giữ câu rút gọn đã rõ nghĩa | Tôi đang soạn hướng dẫn bàn giao. Soạn xong rồi dừng. | Tôi đang soạn hướng dẫn bàn giao. Soạn xong **bản hướng dẫn** rồi dừng. | Tôi đang soạn hướng dẫn bàn giao. Soạn xong rồi dừng. |

MR04 có ngữ cảnh đã tìm mà chưa thấy, không phải từ chối tìm. MR05 không có
quy chuẩn buộc đổi dấu; MR12 đã rõ đối tượng từ câu trước. Giữ nguyên ở hai ca
sau là hành vi mong đợi, không phải bằng chứng skill bỏ qua mọi câu ngắn.
[Báo cáo từng ca](../specs/018-mr-version-comparison/results.md) ghi tiêu chí, raw
đã lưu, các trường hợp không tái hiện lỗi và giới hạn của phép so sánh.

## Bằng chứng và kiểm thử

**Có dữ liệu thực thi, ví dụ đối chiếu và kết quả hồi quy; chưa có chấm người độc lập.**
Các phép so sánh thực hiện trên cùng agent/model, không dùng để xếp hạng Codex với Gemini.

| Đợt đánh giá | Số liệu cụ thể | Kết luận được hỗ trợ |
|---|---|---|
| [Hồi quy 0.12.0 → 0.12.1](../specs/018-mr-version-comparison/results.md) | 12 ca, 14 tình huống × 2 phiên bản = **28 đầu ra**; đạt **10/12 → 12/12 ca** | MR05 và MR12 chuyển từ chưa đạt sang đạt theo tiêu chí khóa trước; mỗi điều kiện chỉ sinh một lần, nhãn do agent đối chiếu và reviewer kiểm tra |
| [Pilot giữ giọng Mindfio, 0.12.0](../specs/016-sample-voice-preservation/mindfio-results.md) | **4 bài × 3 chế độ = 12 đầu ra**, cùng Codex | Workflow có hồ sơ đã chạy được; lợi ích giữ giọng chưa đồng đều và chưa tách riêng được tác động của hồ sơ với hướng dẫn đọc mẫu |
| [Nguồn AI công khai, 0.11.0](../specs/014-editorial-benchmark/execution-report.md) | **20 nguồn × 4 chế độ = 80 đầu ra** trong mỗi bộ Codex/Gemini; tổng **160 đầu ra** | Đo được thay đổi văn bản, thời gian và token; chưa suy thành điểm chất lượng hoặc tỷ lệ thắng |

MR01–MR12 là tập phát triển đã dùng để cải tiến skill, không phải tập đánh giá
độc lập. **12/12 không có nghĩa 100% văn bản sẽ được sửa đúng**; nhãn chỉ xét
tiêu chí của từng ca. Ở nhánh nhận xét MR11, 0.12.1 vẫn tự dùng “mày” khi ngữ
cảnh không xác lập quan hệ xưng hô; vấn đề này được ghi riêng trong báo cáo.

Số liệu thực thi và điểm chất lượng được tách riêng. Có thay đổi trong bản sửa chưa chứng
minh thay đổi đó tốt hơn; các ca giữ nguyên cũng được giữ trong bộ đánh giá.

| Bằng chứng hiện có | Có thể kiểm tra điều gì? | Giới hạn |
|---|---|---|
| [Test tự động](../tests/) | Đóng gói, inventory, pilot giọng và hợp đồng review | Test không đo chất lượng bản biên tập cuối |
| [Ca kiểm thử chạy tay](../calibration/test-cases.md) | Kết quả mong đợi của từng tình huống, gồm cả ca không được sửa | Có ca kiểm thử chưa đồng nghĩa đã chạy và đạt |
| [Nhật ký hiệu chuẩn](../calibration/LOG.md) | Bằng chứng và quyết định đằng sau các lần sửa quy tắc | Ca đã dùng để chỉnh quy tắc không phải tập đánh giá độc lập |

Kiểm đóng gói không cần gọi API:

```bash
python3 -B -m unittest tests.test_distribution tests.test_package_security
```

<details>
<summary>Chi tiết bộ 160 đầu ra công khai và biểu đồ trước/sau — quy tắc 0.11.0</summary>

### Trước và sau khi dùng Vietnamizer trên cùng agent — cập nhật 26/10/2026

Bộ số liệu dưới đây dùng quy tắc **0.11.0**. Từ lúc dùng các ca này để hiệu chuẩn bản 0.11.1, cả 20 nguồn trở thành **tập phát triển/hồi quy** cho những phiên bản sửa theo chúng; không dùng lại như holdout độc lập để chứng minh chất lượng bản mới. Xem [hồ sơ hiệu chuẩn](../specs/015-benchmark-calibration/results.md).

20 câu trả lời nguyên văn từ [TTP01/Vietverse-SFT-Preview](https://huggingface.co/datasets/TTP01/Vietverse-SFT-Preview/tree/6b4e4a86e3b399318ac4fe91b2bbe64501037f40), có nhãn `synthetic_llm` và dấu vết xử lý do bên phát hành công bố, giấy phép Apache 2.0. Đã lưu nguyên bản 100 dòng, câu hỏi gốc, metadata, revision và SHA-256; chốt 20 mẫu trước khi biên tập. Chưa có raw API hoặc tên model tạo nguồn được đối soát.

Câu hỏi chính: **cùng một văn bản, sau khi dùng Vietnamizer có tự nhiên, rõ ràng hơn mà vẫn giữ đúng ý, số liệu và giọng không?** “Trước” là bản AI gốc đã đóng băng; “sau” là bản agent biên tập từ chính bản đó. Nhánh yêu cầu cơ bản cũng là bản sau biên tập, không thay thế bản gốc.

Báo kết quả trước/sau riêng cho từng chế độ trên cùng agent. Các nhánh yêu cầu cơ bản và prompt thường giúp kiểm tra thêm phần đóng góp của Vietnamizer; nhánh có Jev giúp kiểm tra phần đóng góp của tư vấn. Codex và Gemini là hai lần thực hiện riêng của cùng thiết kế, không dùng để xếp hạng agent và không gộp nhãn thành một mẫu.

Cả bốn nhánh yêu cầu cùng cấu hình Codex `gpt-6.1-sol`, effort `medium`, **mỗi nhánh một lượt tạo bản cuối từ cùng bản gốc**. Backend thực chưa có attestation; 80 lượt đều hoàn tất, không ghi nhận tool.

| Chế độ | Bản hoàn tất | Trùng hoàn toàn bản gốc |
|---|---:|---:|
| Yêu cầu biên tập cơ bản | 20/20 | 0 |
| Prompt biên tập thông thường | 20/20 | 0 |
| Vietnamizer | 20/20 | 1 |
| Vietnamizer + Jev | 20/20 | 2 |

“Trùng hoàn toàn” tính cả khoảng trắng và định dạng, **không phải điểm chất lượng**. Jev hoàn tất phạm vi theo hợp đồng ở 1/20 nguồn; 19 nguồn có tư vấn thiếu do giới hạn, ngữ cảnh/phân đoạn hoặc lỗi phản hồi. Các ca này vẫn nằm trong bộ chấm. Chi phí Jev theo usage cộng dự phòng là **0,4564 USD / trần 2 USD**, gồm 0,2003 USD của đợt trước; chưa đối soát hóa đơn.

**[Báo cáo benchmark thực thi đầy đủ](../specs/014-editorial-benchmark/execution-report.md)** có 7 hình phân tích, bảng từng nguồn, trung vị và Q1–Q3, cùng phương pháp tái lập từ raw. Hình mô tả thay đổi và tài nguyên; không phải điểm chất lượng hoặc bằng chứng Vietnamizer thắng đối chứng.

#### Trong bộ Codex

Mức thay đổi ký tự trung vị so với bản gốc là **2,42%** với Vietnamizer và **1,75%** với Vietnamizer + Jev. Đây là `1 − SequenceMatcher.ratio`, có tính khoảng trắng/Markdown; không phải tỷ lệ lỗi hay tỷ lệ nội dung được cải thiện.

![Codex: phân bố thay đổi trước/sau trên cùng agent](../specs/014-editorial-benchmark/figures/execution/codex-text-distributions.svg)

#### Trong bộ Gemini

Đã đối soát **80/80 bản**, cùng bốn chế độ và 20 nguồn; raw CLI ghi nhận `gemini-3.8-flash-medium`. Mỗi chế độ lần lượt có **15, 12, 12, 15 bản giữ nguyên hoàn toàn** (yêu cầu cơ bản, prompt thường, Vietnamizer, Vietnamizer + Jev). Các trường hợp giữ nguyên vẫn được giữ trong phân tích; chưa đánh giá chúng đúng hay bỏ sót lỗi.

![Gemini: phân bố thay đổi trước/sau trên cùng agent](../specs/014-editorial-benchmark/figures/execution/gemini-text-distributions.svg)

Báo cáo tách riêng hai runtime và không dùng các số này để xếp hạng agent. Tổng cộng có 160 đầu ra nhưng chỉ 20 nguồn; mỗi nguồn/chế độ/runtime có một lượt tạo bản cuối. Nguồn từ một tập SFT đã tuyển chọn, chưa phải holdout đại diện cho mọi văn bản AI. Token/thời gian lấy từ CLI; chi phí thuê bao chưa quy thành USD.

Hai Forms và [công cụ chấm người](../specs/014-editorial-benchmark/human-analysis-runbook.md) giữ nguyên để dùng lại khi cần, không phải bước phải chờ để hoàn thành báo cáo mô tả. Không gọi thêm model/Jev, không dùng nhãn khảo sát hoặc điểm model từ pilot cũ cho báo cáo hiện tại. Xem [trạng thái](../specs/014-editorial-benchmark/CURRENT.md), [nguồn và thực thi](../specs/014-editorial-benchmark/public-ai-results.md), [phương pháp trước/sau](../specs/014-editorial-benchmark/within-agent-amendment.md).

</details>

<details>
<summary>Pilot trước trên văn bản giả lập — thiết kế và dữ liệu riêng</summary>

[Đặc tả benchmark](../specs/014-editorial-benchmark/spec.md) xác định phép so sánh cùng một
model ở bốn chế độ: không dùng skill, dùng prompt biên tập thông thường, dùng Vietnamizer
và dùng Vietnamizer kết hợp Jev. [Chế độ có Jev](../specs/014-editorial-benchmark/jev-extension.md)
đã được triển khai và chạy pilot trên Codex; tình trạng nhận tư vấn và fallback được báo riêng.
Benchmark cần đo sửa đúng, sửa quá tay, giữ nghĩa và giữ giọng, kèm thời gian và chi phí.
Điểm model thăm dò được báo riêng bên dưới; chưa có kết luận thắng đối chứng đã được người đọc xác nhận.

**Pilot ngày 25/10/2026:** đã thu 60 bản biên tập từ Codex và 10 bản từ Gemini 3.8 Flash trên
văn bản giả lập; một trial Gemini bị cách ly vì gọi tool ngoài yêu cầu. Việc chạy tiếp bị chặn
khi chưa xác minh được cách ly dữ liệu. Pilot chưa đạt mục tiêu 120 đầu ra và chưa được chấm
chất lượng độc lập. Xem [kết quả, phạm vi kiểm chứng và phần còn thiếu](../specs/014-editorial-benchmark/pilot-results.md).

**Codex + Jev, cập nhật ngày 25/10/2026:** đã nhận đủ phản hồi Jev cho **20/20 văn bản**
và tạo **20 bản Codex + Jev mới**. Bộ chấm hiện tại có 80 bản cuối cho bốn chế độ, dùng lại
các bản đối chứng từ đợt trước. Các câu trả lời “chưa đủ ngữ cảnh” vẫn được giữ nguyên;
nhận đủ phản hồi không đồng nghĩa biên tập đã đúng. Tổng chi phí Jev từ usage cộng dự phòng
khoảng **0.2003 USD / 2 USD**, chưa phải hóa đơn đối soát. Raw request/response, lỗi,
nguồn từng câu trả lời và bảng phân tích được lưu local. Chưa có chấm chất lượng độc lập
hoặc bằng chứng hiệu quả Jev. Xem [báo cáo phục hồi và giới hạn](../specs/014-editorial-benchmark/recovery-results.md),
[lưu trữ dữ liệu](../specs/014-editorial-benchmark/data-archive.md) và
[báo cáo đợt partial/fallback trước](../specs/014-editorial-benchmark/codex-jev-results.md).


**Chấm bằng model, ngày 25/10/2026 — MODEL-ASSESSED / EXPLORATORY:** hai cấu hình giám khảo
Codex (yêu cầu GPT-6.1 Sol và GPT-6 Astra; backend chưa được attestation) chấm 80 bản cuối.
Có **156/160 nhận xét hợp lệ**; bốn nhận xét thiếu do một nhóm lỗi enum, không gọi lại.
Vietnamizer + Jev so với Vietnamizer tự rà: **2 phiếu thắng, 37 hòa, 0 thua, 1 thiếu**.
CI 95% của preference còn chạm mức trung tính; chưa có bằng chứng rõ về lợi ích tăng thêm
của Jev. Hai baseline cũ ít lượt sửa hơn nên các so sánh với chúng có giới hạn thiết kế.

![Pilot model: phiếu lựa chọn, gồm phần thiếu](../specs/014-editorial-benchmark/figures/model-preferences.svg)

Đơn vị thống kê là 20 nguồn giả lập; CI ghép cặp dùng 19 nguồn đủ cả hai giám khảo, không
coi các nhận xét là mẫu độc lập. Hai model cùng nhà cung cấp; điểm model không phải nhãn
chuẩn. Xem [kết quả, CI, an toàn và dữ liệu](../specs/014-editorial-benchmark/quality-results.md),
[protocol](../specs/014-editorial-benchmark/quality-protocol.md) và
[bộ giao hai người chấm](../specs/014-editorial-benchmark/human-handoff.md).
Bộ người đọc dùng [cách chấm trực tiếp](../specs/014-editorial-benchmark/human-simple-protocol.md),
tức là xem bản gốc cạnh bản sửa, trả lời ba câu cho mỗi đoạn; vẫn ẩn tên bốn chế độ.
Nhãn giữ đúng và độ dễ đọc được báo riêng, không suy thành precision/recall của từng lần sửa.

</details>

[Pilot tách mẫu và skill trên cùng Codex, nguồn 0.12.1](../specs/019-voice-factorial-benchmark/results.md)
có 32 đầu ra và 15/16 phiếu model hợp lệ. Trên bốn nháp AI trung tính, cả hai giám khảo đều chọn
prompt+mẫu hơn Vietnamizer+cùng mẫu. Đây là dữ liệu phát triển dẫn tới hai chế độ của 0.13.0,
không phải bằng chứng bản mới đã tốt hơn. Giám khảo có thiên lệch về hình thức; chưa có chấm
người hoặc tác giả xác nhận.

[Pilot so 0.13.0 với 0.12.1](../specs/021-voice-version-pilot/results.md) đã có **32 đầu ra** trên cùng
Codex. So 0.13.0 với prompt+cùng mẫu, Codex chọn thắng/hòa/thua **1/1/6**, Gemini **2/0/6** trên
tám bản. V1 còn thêm chú giải số nhiều ngoài nguồn. Đây là dữ liệu phát triển, chưa chứng minh
skill vượt prompt+mẫu. Bản 0.13.1 sửa chỉ dẫn và ví dụ từ các lỗi đó.

[Pilot 023 cho 0.13.1](../specs/023-voice-patch-pilot/results.md) có 32 đầu ra trên cùng Codex. So với
prompt+cùng mẫu, Codex chọn thắng/hòa/thua 4/2/2, Gemini 5/0/3; hai giám khảo chỉ đồng ý lựa chọn
ở 3/8 bản. Riêng N2 cả hai thích 0.13.0 hơn, dù đều ghi nghĩa được giữ. Đây là tập phát triển đã dùng
sửa skill, không chứng minh vượt trội. Bản 0.13.2 làm rõ chọn nét giọng theo chức năng từ ca này;
kiểm offline/package không xác nhận hiệu quả biên tập.

[Pilot 025 cho 0.13.2](../specs/025-section-voice-pilot/results.md) có 32 đầu ra và 15/16 phiếu chấm hợp lệ;
V2–Gemini thiếu do quote sai, không hỏi lại. N2: Codex cho 0.13.1/0.13.2 hòa 4→4, Gemini nâng 4→5;
cả hai ghi nghĩa được giữ và chọn 0.13.2 hơn prompt+cùng mẫu. Toàn bộ so phiên bản, Codex 0/6/2
thắng/hòa/thua trên 8 bản, Gemini 4/0/3 trên 7 bản có phiếu. N2 có tín hiệu tích cực, chưa chứng minh
nâng cấp đồng đều. Đây vẫn là tập phát triển và model chấm, không phải xác nhận từ tác giả/người đọc.

[Pilot Mindfio ngày 27/10/2026](../specs/016-sample-voice-preservation/mindfio-results.md)
đã có **12/12 bản cuối** trên cùng Codex, gồm bốn bài, ba chế độ, hồ sơ được chủ nhân
duyệt và nguồn 0.12.0 đóng băng trước khi chạy. Có raw CLI, đối chiếu trước/sau và
hai hình phân tích thay đổi/tài nguyên. Nhận xét chất lượng là thăm dò của agent;
chưa chứng minh thêm hồ sơ giúp giữ giọng tốt hơn trên mọi bài. Bộ này giữ riêng,
không thay kết quả benchmark 0.11.0 hoặc hai Forms cũ.

Ví dụ ở M05: nhánh core thêm `với sự trống rỗng ấy` vào câu `Mà chạy để tránh
đối diện.`, còn nhánh kèm hồ sơ giữ câu ngắn. Tuy nhiên prompt thường kèm hồ sơ
cũng giữ câu này. Đây là ví dụ hữu ích để đọc và chọn bản sửa, **chưa chứng minh
lợi ích riêng của Vietnamizer hoặc tỷ lệ khớp giọng**. Cả bốn bài đã qua biên tập
AI theo xác nhận của chủ nhân; không có bản nháp trước AI để đối chiếu.

[Hiệu chỉnh 0.12.1 từ Mindfio](../specs/017-preserve-meaning-rhythm/results.md) ưu tiên
giữ ý muốn/khả năng/phạm vi, câu rút gọn có chức năng và quan hệ ý khi đổi dấu.
Đã [chạy đối chiếu MR01–MR12 trên cùng Codex](../specs/018-mr-version-comparison/results.md),
trong đó 0.12.0 đạt 10/12 ca và 0.12.1 đạt 12/12 theo tiêu chí đã khóa, với MR05/MR12 chuyển
từ chưa đạt sang đạt. Mỗi tình huống chỉ sinh một bản cho mỗi phiên bản; nhãn do
agent đối chiếu và reviewer kiểm tra, không phải chấm người độc lập. Những bài đã dùng để hiệu chỉnh là dữ liệu phát triển/hồi quy,
không còn là holdout độc lập để chứng minh bản mới tốt hơn.
