import sys
from html import escape
SANS="'Space Grotesk', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
THEMES={
 "light":dict(paper="#FFFFFF",box="#FFFFFF",ink="#0B0B17",muted="#5B5B79",rule="#BCBCD0",accent="#9750C4",tint="#F5EDFA"),
 "dark":dict(paper="#1A0A2E",box="#241238",ink="#F4F1FA",muted="#BCBCD0",rule="#5B5B79",accent="#7FE2CE",tint="#163A3A"),
}
W,H=960,488
def build(name):
    c=THEMES[name]; slug="voice-setup"+("" if name=="light" else "-dark")
    o=[]
    a=o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="{slug}-title {slug}-desc">')
    a(f'<title id="{slug}-title">Luồng thiết lập giọng của Vietnamizer</title>')
    a(f'<desc id="{slug}-desc">Năm bước chọn loại giọng, đưa nguồn mẫu, đồng ý đọc, xem hồ sơ nháp và chấm thử dẫn tới câu hỏi bạn có muốn lưu không; có thì hồ sơ được lưu và lần sau gọi bằng tên, không thì hồ sơ chỉ nằm trong cuộc trò chuyện. Dừng ở bước nào cũng không có gì được lưu.</desc>')
    a('<defs>')
    for mid,col in (("a",c["muted"]),("b",c["accent"])):
        a(f'<marker id="{slug}-{mid}" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{col}"/></marker>')
    a('</defs>')
    a(f'<rect width="100%" height="100%" fill="{c["paper"]}"/>')
    def arrow(d,accent=False):
        col=c["accent"] if accent else c["muted"]; m="b" if accent else "a"
        a(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.2" marker-end="url(#{slug}-{m})"/>')
    def label(x,y,text,anchor="middle",w=48):
        rx = x-w/2 if anchor=="middle" else x-4
        a(f'<rect x="{rx}" y="{y-12}" width="{w}" height="16" rx="2" fill="{c["paper"]}"/>')
        a(f'<text x="{x}" y="{y}" fill="{c["muted"]}" font-size="12" font-family="{MONO}" text-anchor="{anchor}" letter-spacing="0.06em">{escape(text)}</text>')
    # connectors first
    xs=[24,212,400,588,776]
    for x in xs[:-1]:
        arrow(f"M {x+160} 92 L {x+188-2} 92")
    arrow("M 856 144 L 856 230",True)
    arrow("M 776 268 L 722 268",True); label(748,252,"CÓ",w=32)
    arrow("M 520 268 L 466 268")
    arrow("M 856 304 L 856 372 Q 856 380 848 380 L 722 380"); label(868,344,"KHÔNG",anchor="start",w=56)
    def box(x,y,w,h,eyebrow,title,subs,focal=False):
        fill=c["tint"] if focal else c["box"]; st=c["accent"] if focal else c["ink"]
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c["paper"]}"/>')
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{st}" stroke-width="1"/>')
        cx=x+w/2; ty=y+20
        if eyebrow:
            a(f'<text x="{cx}" y="{ty}" fill="{c["muted"]}" font-size="12" font-family="{MONO}" text-anchor="middle" letter-spacing="0.12em">{escape(eyebrow)}</text>'); ty+=28
        else: ty+=16
        a(f'<text x="{cx}" y="{ty}" fill="{c["ink"]}" font-size="16" font-weight="600" font-family="{SANS}" text-anchor="middle">{escape(title)}</text>')
        for i,s in enumerate(subs):
            a(f'<text x="{cx}" y="{ty+24+i*16}" fill="{c["muted"]}" font-size="12" font-family="{SANS}" text-anchor="middle">{escape(s)}</text>')
    steps=[("Chọn loại giọng",["Cá nhân hoặc","Thương hiệu"]),("Đưa nguồn mẫu",["bài dán, file export,","trang qua trình duyệt"]),
           ("Đồng ý đọc",["mỗi nguồn, mỗi URL","một câu đồng ý"]),("Xem hồ sơ nháp",["sửa tới khi ưng"]),("Chấm thử",["0–10 đoạn,","từ Kém đến Tốt"])]
    for i,(x,(t,s)) in enumerate(zip(xs,steps)):
        box(x,40,160,104,f"BƯỚC {i+1}",t,s)
    box(776,232,160,72,"","Bạn muốn lưu?",[],focal=True)
    box(520,232,200,72,"","Lưu hồ sơ",["nơi bạn chọn, kèm sổ hồ sơ"])
    box(264,232,200,72,"","Lần sau gọi bằng tên",["mỗi lần áp một hồ sơ"])
    box(520,344,200,72,"","Không lưu",["chỉ nằm trong cuộc trò chuyện"])
    # note strip
    a(f'<line x1="24" y1="444" x2="{W-24}" y2="444" stroke="{c["rule"]}" stroke-width="0.8" stroke-dasharray="4,4"/>')
    a(f'<text x="24" y="472" fill="{c["muted"]}" font-size="12" font-family="{MONO}" letter-spacing="0.12em">BƯỚC 1–5</text>')
    a(f'<text x="112" y="472" fill="{c["ink"]}" font-size="16" font-family="{SANS}">Dừng ở bước nào cũng được; dừng thì không có gì được lưu.</text>')
    a('</svg>')
    return "\n".join(o)+"\n"
out=sys.argv[1]
open(f"{out}/voice-setup.svg","w",encoding="utf-8").write(build("light"))
open(f"{out}/voice-setup-dark.svg","w",encoding="utf-8").write(build("dark"))
