# Cài đặt Vietnamizer

[← README](../README.md)

## Cài nhanh

Mỗi agent có một đường cài riêng. Bạn chỉ cần tìm đúng mục cho công cụ mình đang dùng ở bên dưới.
Cài xong là biên tập được ngay, không cần thiết lập gì thêm. Bản hiện tại là **0.16.0**.

### Codex và các agent dùng Skills CLI

```bash
npx --yes skills@1.5.20 add finolabs/vietnamizer --global
```

Cài cho mọi agent mà Skills CLI hỗ trợ:

```bash
npx --yes skills@1.5.20 add finolabs/vietnamizer \
  --skill vietnamizer \
  --agent '*' \
  --global \
  --yes
```

Bỏ `--global` nếu muốn cài trong phạm vi dự án. Muốn xem trước skill mà CLI tìm được thì chạy:

```bash
npx --yes skills@1.5.20 add finolabs/vietnamizer --list
```

Skills CLI nhận repository, URL hoặc đường dẫn cục bộ làm nguồn. Cờ `--agent '*'` chọn mọi agent
được hỗ trợ, còn cờ `--copy` buộc CLI sao chép file thay vì tạo liên kết tượng trưng.

### Claude Code plugin

Cài từ catalog chung của Finolabs:

```bash
claude plugin marketplace add finolabs/plugins
claude plugin install vietnamizer@finolabs
```

Cập nhật catalog bằng `claude plugin marketplace update finolabs`. Cài xong, gọi skill bằng
`/vietnamizer:vietnamizer` kèm đoạn cần biên tập. Gõ `/vietnamizer:help` nếu muốn xem hướng dẫn
một màn hình; thiết lập giọng riêng chỉ là phần tùy chọn. Chưa thấy skill thì mở phiên mới.
Selector cũ `vietnamizer@vietnamizer` không còn nguồn cập nhật.

### Claude web và Claude Desktop: thêm marketplace

1. Mở **Customize → Plugins → Add → Add marketplace**.
2. Chọn **Add from a repository**, nhập `finolabs/plugins` hoặc
   `https://github.com/finolabs/plugins`.
3. Trong **Discover**, chọn **Vietnamizer → Add**, rồi kiểm plugin đã bật.
4. Trong cuộc trò chuyện, gõ `/` hoặc bấm `+`, chọn skill **Vietnamizer** và gửi đoạn cần sửa.

Theo [hướng dẫn của Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude),
plugin trên web/Desktop dành cho các gói Pro, Max, Team và Enterprise. Không thấy tùy chọn này thì
bạn kiểm tra lại gói và chính sách của tổ chức; cài riêng không bỏ qua được các giới hạn đó.

Bạn cũng có thể tải `vietnamizer-plugin.zip` từ
[Releases](https://github.com/finolabs/vietnamizer/releases/latest) để upload plugin thay vì thêm
catalog. Đừng dùng `vietnamizer.skill` hay `vietnamizer-claude-org.zip` ở bước upload plugin, vì
hai file đó là gói skill riêng.

### Marketplace plugin cho tổ chức Claude

Owner của tổ chức Team/Enterprise tải `vietnamizer-plugin.zip` từ Releases, mở
**Organization settings → Plugins & skills → Add → Upload a plugin**, chọn marketplace mới
hoặc có sẵn rồi upload. Thành viên cài plugin từ **Discover** theo quyền được cấp.

Đừng nhầm với **Sync from GitHub** của marketplace tổ chức. Đường sync này yêu cầu repo GitHub
private/internal, nên không nhận trực tiếp repo public `finolabs/vietnamizer`; trường hợp đó dùng
upload ZIP. Quyền, cách bật Cowork/Skills và chính sách phân phối nằm trong
[hướng dẫn quản trị plugin](https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization).

### Codex plugin

Cài từ catalog chung của Finolabs:

```bash
codex plugin marketplace add finolabs/plugins
codex plugin add vietnamizer@finolabs
```

Cập nhật catalog bằng `codex plugin marketplace upgrade finolabs`.

Máy còn catalog cũ thì gỡ trước khi thêm `finolabs/plugins`. Catalog cũ là `Finolabs` (đăng ký
từ `agybird`, selector dạng `vietnamizer@Finolabs`) hoặc `vietnamizer@vietnamizer`. Trên macOS,
Codex có thể dùng chung một thư mục cache cho hai tên chỉ khác chữ hoa–thường, khiến cùng một
plugin cài từ cả hai nơi ghi đè lẫn nhau. Catalog cũ cũng có thể còn phục vụ plugin khác
(`agybird`, `markmap-skills`), nên chạy `codex plugin list` để xem trước khi gỡ. Sao lưu cấu
hình, rồi chạy:

```bash
codex plugin remove vietnamizer@Finolabs      # hoặc vietnamizer@vietnamizer
codex plugin marketplace remove Finolabs      # hoặc vietnamizer
codex plugin marketplace add finolabs/plugins
codex plugin add vietnamizer@finolabs
```

### Antigravity plugin

Antigravity 1.4 chỉ phân giải `plugin@marketplace` với marketplace chính thức của nó, nên bạn cài
trực tiếp từ repository:

```bash
agy plugin install https://github.com/finolabs/vietnamizer
agy plugin list
```

### Claude web và Claude Desktop: chỉ cài skill

[Tải gói skill từ trang Releases](https://github.com/finolabs/vietnamizer/releases/latest),
mở **Customize → Skills → + Create skill → Upload a skill**, chọn file vừa tải rồi bật skill.
Claude cần bật **Code execution and file creation** để dùng custom skill. Xem thêm
[hướng dẫn chính thức của Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

### Claude Org: chỉ cài skill

[Tải gói Claude Org từ trang Releases](https://github.com/finolabs/vietnamizer/releases/latest),
mở **Organization settings → Plugins & skills → Add → Upload a skill**, rồi chọn file ZIP. Gói này
đặt `SKILL.md` và `LICENSE` ở thư mục gốc, cùng các file cần khi skill chạy.

### Cài thủ công

Chép `LICENSE`, `SKILL.md` cùng `profiles/`, `references/`, `agents/` và `assets/` vào
thư mục skill của agent:

```bash
git clone https://github.com/finolabs/vietnamizer.git /duong/dan/toi/skills/vietnamizer
```

Dữ liệu và điều kiện dùng nằm ở [quyền riêng tư](../PRIVACY.md) và [điều kiện sử dụng](../TERMS.md).
Người bảo trì muốn đóng gói từ source thì xem [hướng dẫn đóng góp](../CONTRIBUTING.md).
