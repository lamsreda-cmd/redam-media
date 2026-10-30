"""Render Friday (جمعة مباركة) story images -> stories/out/j_*.jpg. Run from repo root."""
import base64, pathlib
from playwright.sync_api import sync_playwright

REPO = pathlib.Path(__file__).resolve().parents[2]
TOOL = REPO / 'stories/tool'
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONTS = ''.join(f"@font-face{{font-family:Cairo;font-weight:{w};src:url(data:font/woff2;base64,{b64(TOOL/f'fonts/cairo-{s}-{w}-normal.woff2')}) format('woff2');{r}}}" for w in (700, 900) for s, r in (('arabic', ''), ('latin', 'unicode-range:U+0000-00FF;')))
PEN = b64(TOOL / 'pennant.png')

ITEMS = {
 'j_1': ('اللهم صلّ وسلم وبارك<br>على نبينا محمد', 'أكثروا من الصلاة على النبي فهاد النهار المبارك'),
 'j_2': ('ما تنساوش قراءة<br>سورة الكهف', 'نور ما بين الجمعتين'),
 'j_3': ('اللهم اجعلها جمعة<br>خير وبركة على الجميع', 'ومتقبل منا ومنكم صالح الأعمال'),
 'j_4': ('اللهم ارزق كل مشتاق<br>زيارة بيتك الحرام', 'آمين يا رب العالمين'),
}

# eight-point star pattern as SVG tile
STAR = "<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120'><g fill='none' stroke='%23D4AF37' stroke-opacity='.16' stroke-width='2'><rect x='35' y='35' width='50' height='50'/><rect x='35' y='35' width='50' height='50' transform='rotate(45 60 60)'/><circle cx='60' cy='60' r='12'/></g></svg>"

def page(main, sub):
    return f"""<html><head><style>{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;font-family:Cairo;direction:rtl;position:relative;overflow:hidden;
background:url("data:image/svg+xml;utf8,{STAR}"),radial-gradient(circle at 50% 42%,#1A4C93 0%,#0B2A6B 48%,#04102A 100%)}}
.wrap{{position:absolute;top:470px;left:70px;right:70px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:40px}}
.moon{{width:200px;height:200px;border-radius:50%;box-shadow:-38px 18px 0 0 #E9C46A;transform:translateX(30px) rotate(-20deg);filter:drop-shadow(0 0 30px rgba(233,196,106,.55))}}
.t{{font-weight:900;font-size:150px;line-height:1.1;color:#F4D27A;text-shadow:0 6px 0 #8A6512,0 16px 40px rgba(0,0,0,.6)}}
.line{{width:520px;height:6px;border-radius:6px;background:linear-gradient(90deg,transparent,#E9C46A,transparent)}}
.m{{font-weight:900;font-size:72px;line-height:1.4;color:#fff;text-shadow:0 4px 18px rgba(0,0,0,.7)}}
.s{{font-weight:700;font-size:44px;color:#BFE9FA}}
.foot{{position:absolute;bottom:170px;left:0;right:0;text-align:center;font-weight:700;font-size:38px;color:#fff;opacity:.85;direction:ltr}}
</style></head><body>
<div class="wrap"><div class="moon"></div><div class="t">جمعة مباركة</div><div class="line"></div>
<div class="m">{main}</div><div class="s">{sub}</div></div>
<div class="foot">Redam Travel Agency</div>
<img src="data:image/png;base64,{PEN}" style="position:absolute;inset:0;width:1080px;height:1920px"></body></html>"""

with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1920})
    out = REPO / 'stories/out'
    for k, (m, s) in ITEMS.items():
        pg.set_content(page(m, s)); pg.wait_for_timeout(300)
        pg.screenshot(path=str(out / f'{k}.jpg'), type='jpeg', quality=90); print(k)
    br.close()
