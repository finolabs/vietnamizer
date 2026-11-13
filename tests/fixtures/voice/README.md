# Synthetic voice-source fixtures

Synthetic data for calibration cases VM05–VM10 (`calibration/test-cases.md`). No real person, account,
phone number or address. Column and field names follow the platform exports as described in
`specs/030-voice-modes/research.md` R4; real exports may differ.

- `linkedin-shares-sample.csv`: two own posts (keep), one reshare without own text (drop), one post
  with a fake phone and email (keep the writing habit, never the contact values).
- `linkedin-comments-sample.csv`: a comment on someone else's post (not a post sample).
- `facebook-posts-sample.json`: two own posts (keep), a post by someone else on the timeline (drop),
  a shared link without own text (drop).
