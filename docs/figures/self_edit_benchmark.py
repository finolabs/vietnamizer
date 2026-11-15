"""Draw the 0.16.2 self-edit benchmark charts (light and dark SVG).

Numbers come from `benchmarks/self_edit_count.py` (error counts) and the
Fable 5.2 selection table (files chosen). Run: python3 docs/figures/self_edit_benchmark.py
"""
import sys
from html import escape
from pathlib import Path

SANS = "'Space Grotesk', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
THEMES = {
    "light": dict(paper="#FFFFFF", ink="#0B0B17", muted="#5B5B79", rule="#E4E4EE", bar="#8E8EA8", accent="#9750C4"),
    "dark": dict(paper="#1A0A2E", ink="#F4F1FA", muted="#BCBCD0", rule="#3A2A52", bar="#8A86A6", accent="#7FE2CE"),
}
MODELS = ["Sonnet 5.5 + Vietnamizer", "Gemini 3.8 Flash + Vietnamizer", "Opus 5.5 + Vietnamizer", "Fable 5.2 + Vietnamizer"]
PANELS = [
    dict(title="Lỗi dấu hai chấm giữa câu mà Vietnamizer giúp từng model phát hiện và sửa",
         sub="Bản gốc có 109 chỗ dùng dấu hai chấm nối hai ý trong một câu, kiểu “Khách ít kiên nhẫn: họ sẽ hỏi nơi khác”.",
         base=109, fixed=[31, 25, 47, 49], scale=50, unit="%"),
    dict(title="Từ ghép bị cắt còn một tiếng mà Vietnamizer giúp từng model phát hiện và sửa",
         sub="Bản gốc có 46 chỗ viết “rà” hoặc “soát” trong khi đúng ra phải là “rà soát”.",
         base=46, fixed=[0, 1, 17, 17], scale=50, unit="%"),
    dict(title="Giám khảo chọn bản biên tập của model nào nhiều nhất",
         sub="Fable 5.2 so 42 file và chọn bản tốt nhất cho từng file. “Giữ bản gốc” là khi không bản sửa nào hơn bản gốc.",
         rows=["Opus 5.5 + Vietnamizer", "Giữ bản gốc", "Sonnet 5.5 + Vietnamizer", "Gemini 3.8 Flash + Vietnamizer"],
         values=[18, 16, 6, 2], scale=20, unit="file"),
]
W = 960
LABEL_X, BAR_X, BAR_W = 32, 272, 500
ROW_H, BAR_H = 34, 16
PANEL_HEAD, PANEL_GAP = 64, 28


def bar_path(x, y, w, h, r=4):
    if w <= 0:
        return None
    r = min(r, w, h / 2)
    return (f"M{x} {y}H{x + w - r}Q{x + w} {y} {x + w} {y + r}V{y + h - r}"
            f"Q{x + w} {y + h} {x + w - r} {y + h}H{x}Z")


def build(name):
    c = THEMES[name]
    slug = "self-edit-benchmark" + ("" if name == "light" else "-dark")
    height = 74 + sum(PANEL_HEAD + 4 * ROW_H for _ in PANELS) + PANEL_GAP * (len(PANELS) - 1) + 16
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" height="{height}" '
      f'role="img" aria-labelledby="{slug}-title {slug}-desc">')
    a(f'<title id="{slug}-title">Kết quả Vietnamizer tự biên tập chính nó, bản 0.16.2</title>')
    a(f'<desc id="{slug}-desc">Ba model biên tập bằng Vietnamizer 0.16.2. Lỗi dấu hai chấm giữa câu, bản gốc có 109 chỗ. Sonnet sửa 31 (28%), Gemini 25 (23%), Opus 47 (43%), '
      f'Fable 5.2 chọn và ghép lại 49 (45%). Từ ghép bị cắt còn một tiếng như rà, soát, bản gốc có 46 chỗ. Sonnet sửa 0, Gemini 1 (2%), '
      f'Opus 17 (37%), Fable 5.2 chọn và ghép lại 17 (37%). Giám khảo Fable 5.2 chọn trên 42 file, Opus 18, giữ bản gốc 16, Sonnet 6, Gemini 2.</desc>')
    a(f'<rect width="100%" height="100%" fill="{c["paper"]}"/>')
    a(f'<text x="{LABEL_X}" y="34" fill="{c["muted"]}" font-size="13" font-family="{SANS}">Ba model biên tập bằng Vietnamizer 0.16.2. Thanh tô màu là Fable 5.2 dùng Vietnamizer chọn bản tốt nhất</text>')
    a(f'<text x="{LABEL_X}" y="52" fill="{c["muted"]}" font-size="13" font-family="{SANS}">cho từng file rồi ghép lại, chính là bản phát hành 0.16.2. Fable không tự viết câu nào.</text>')
    y = 74
    for p in PANELS:
        a(f'<text x="{LABEL_X}" y="{y + 18}" fill="{c["ink"]}" font-size="17" font-weight="600" font-family="{SANS}">{escape(p["title"])}</text>')
        a(f'<text x="{LABEL_X}" y="{y + 40}" fill="{c["muted"]}" font-size="13" font-family="{SANS}">{escape(p["sub"])}</text>')
        top = y + PANEL_HEAD
        a(f'<line x1="{BAR_X}" y1="{top - 6}" x2="{BAR_X}" y2="{top + 4 * ROW_H - 6}" stroke="{c["muted"]}" stroke-width="1"/>')
        for tick in range(0, p["scale"] + 1, 10 if p["unit"] == "%" else 5):
            tx = BAR_X + BAR_W * tick / p["scale"]
            if tick:
                a(f'<line x1="{tx:.1f}" y1="{top - 6}" x2="{tx:.1f}" y2="{top + 4 * ROW_H - 6}" stroke="{c["rule"]}" stroke-width="1"/>')
        rows = p.get("rows", MODELS)
        for i, label in enumerate(rows):
            ry = top + i * ROW_H
            if p["unit"] == "%":
                n = p["fixed"][i]
                pct = round(100 * n / p["base"])
                value, text = pct, f'sửa {n}/{p["base"]} chỗ ({pct}%)'
                emph = label.startswith("Fable")
            else:
                value = p["values"][i]
                text, emph = f"{value}/42 file", False
            fill = c["accent"] if emph else c["bar"]
            weight = "600" if emph else "400"
            a(f'<text x="{BAR_X - 14}" y="{ry + 12.5}" fill="{c["ink"]}" font-size="14" font-weight="{weight}" '
              f'font-family="{SANS}" text-anchor="end">{escape(label)}</text>')
            w = BAR_W * value / p["scale"]
            d = bar_path(BAR_X + 1, ry, w, BAR_H)
            if d:
                a(f'<path d="{d}" fill="{fill}"/>')
            a(f'<text x="{BAR_X + 1 + w + 10:.1f}" y="{ry + 12.5}" fill="{c["ink"]}" font-size="13" font-weight="{weight}" '
              f'font-family="{SANS}">{escape(text)}</text>')
        y = top + 4 * ROW_H + PANEL_GAP
    a("</svg>")
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    for theme, suffix in (("light", ""), ("dark", "-dark")):
        (out / f"self-edit-benchmark{suffix}.svg").write_text(build(theme), encoding="utf-8")
