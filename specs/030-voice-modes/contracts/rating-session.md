# Contract: rating session (spec 030)

1. Offer after a draft profile, or on request for a named profile (after consent to read it).
2. Ask the count: "Bạn muốn xem và chấm bao nhiêu đoạn mẫu (0–10)?" Zero ends the session; above 10 is capped at 10 with a note.
3. For each paragraph i of n:
   - Write one paragraph (60–120 words) on a topic not drawn from the samples, in the profile's kind and a surface the profile covers; it follows the five chốt and the profile's `ranh giới`; it applies no `Điểm chưa quyết` proposal.
   - Show the paragraph in the message, labelled "Đoạn i/n".
   - Ask one question through the host form when available: header "Đoạn i/n", question "Đoạn này giống cách bạn viết đến mức nào?", options in this order, none marked recommended: **Kém**, **Trung bình**, **Khá**, **Tốt**. Without a form, ask for one of the four words.
   - Any other answer, including "không biết", records no rating.
4. After the last paragraph: report the counts. If any Kém or Trung bình, ask at most two reason questions in total ("Đoạn i chưa giống ở chỗ nào?"), then propose a diff through spec 028 mục 6.
5. Nothing is written until the user saves the profile or confirms the diff; then append one `Lịch sử chấm` line (profile-format contract).
6. The skill never states a percentage, average or similarity score of its own.
