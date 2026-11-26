# Data model

- **Project registry** `.vietnamizer/registry.md`: the same front matter and table as the home registry (spec 032). `Kho` is `project`, and `Vị trí` is a path relative to the project folder.
- **Project profile** `.vietnamizer/profiles/<slug>.md`: the same format as the home Markdown profile.
- **Drive profile**: a Markdown file `<slug>.md` in the user's Drive folder `Vietnamizer` (they may choose another), with the full profile. The compact memory copy gains one line: `Bản đầy đủ: Google Drive, <folder>/<slug>.md`.
- **Precedence on call**:
  1. The project registry, when a writable project folder is attached and the registry exists.
  2. Otherwise the home registry.
  3. On Chat, the compact copy, and the Drive file it names.
