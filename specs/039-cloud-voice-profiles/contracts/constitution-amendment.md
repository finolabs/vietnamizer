# Contract: constitution amendment 2.10.0 → 2.11.0 (needs Fio's approval of the exact text)

This changes the constraint "Tuyến hồ sơ giọng" in the section "Ràng buộc về gói và dữ liệu". The Vietnamese text below is what Fio approves word for word.

## Change 1: the project registry

The current sentence:

> Khi đó skill được đọc sổ hồ sơ `~/.agents/vietnamizer/registry.md`.

becomes:

> Khi đó skill được đọc sổ hồ sơ của project đang mở, tức file `.vietnamizer/registry.md` trong thư mục
> project người dùng đã gắn vào phiên và agent ghi được; không có sổ ấy thì đọc sổ
> `~/.agents/vietnamizer/registry.md`. Hồ sơ lưu theo project nằm trong `.vietnamizer/profiles/` của
> chính thư mục đó, chỉ khi người dùng chọn lưu vào project.

The rules after it stay unchanged and apply to both registries:
- The registry holds names, kinds, stores and locations only.
- The user's call is the consent to read the registry and exactly one profile.
- No registry inside a Git work tree, an instruction file or folder, or agent memory.

## Change 2: the full copy in Google Drive

After the sentence ending "Skill chỉ áp bản gọn ấy khi người dùng gọi tên nó.", add:

> Khi host có connector Google Drive, người dùng có thể chọn lưu thêm bản đầy đủ của hồ sơ thành
> một file Markdown trong Drive của chính họ. Bản gọn có thể ghi tên file đó để lần gọi sau đọc
> đúng file ấy. Skill chỉ ghi khi người dùng đồng ý và host duyệt thao tác; lần gọi chỉ đọc đúng
> file đã ghi tên, không đọc hay tìm file nào khác trong Drive.

## Sync Impact Report lines

- MINOR bump: the voice-profile constraint gains two stores (the project registry and a Drive copy). No principle's obligation is removed.
- Principle V is unchanged: the skill writes through the host's own tools and connectors, with no network code in the package.
