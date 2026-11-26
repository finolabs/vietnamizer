# Data model

- **Project registry** `.vietnamizer/registry.md`: the same front matter and table as the home registry (spec 032). `Kho` is `project`, and `Vị trí` is a path relative to the project folder.
- **Project profile** `.vietnamizer/profiles/<slug>.md`: the same format as the home Markdown profile.
- **Drive profile**: a Markdown file `<slug>.md` in the user's Drive folder `Vietnamizer` (they may choose another), with the full profile. The compact memory copy gains one line: `Bản đầy đủ: Google Drive, <folder>/<slug>.md (id: <file id>)`. The id is the one the connector returns, when it returns one; a call reads by id, else the exact file name in that folder.
- **Precedence on call**:
  1. The project registry, when a writable project folder is attached and the registry exists.
  2. The home registry, when the project registry is absent, empty or has no matching row. A match is used from one registry only; rows are never merged.
  3. On Chat, the compact copy, and the Drive file it names.
