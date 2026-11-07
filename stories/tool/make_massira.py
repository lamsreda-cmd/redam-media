"""Green March anniversary story -> stories/out/massira_51.jpg (run from repo root)."""
import base64, pathlib
from playwright.sync_api import sync_playwright
REPO = pathlib.Path(__file__).resolve().parents[2]; TOOL = REPO / 'stories/tool'
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONTS = ''.join(f"@font-face{{font-family:Cairo;font-weight:{w};src:url(data:font/woff2;base64,{b64(TOOL/f'fonts/cairo-{s}-{w}-normal.woff2')}) format('woff2');{r}}}" for w in (700, 900) for s, r in (('arabic', ''), ('latin', 'unicode-range:U+0000-00FF;')))
PEN = b64(TOOL / 'pennant.png')
STAR = '<svg viewBox="-50 -50 100 100" width="330" height="330"><polygon points="0,-46 27,37 -44,-14 44,-14 -27,37" fill="none" stroke="#0B7A3B" stroke-width="7" stroke-linejoin="miter"/></svg>'
html = f"""<html><head><style>{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}html{{overflow:hidden}}
body{{width:1080px;height:1920px;font-family:Cairo;direction:rtl;position:relative;overflow:hidden;
background:radial-gradient(circle at 50% 38%,#D9262E 0%,#B5161E 55%,#7E0A10 100%)}}
.wave{{position:absolute;left:0;right:0;height:420px;border-radius:50%;background:rgba(255,255,255,.05)}}
</style></head><body>
<div class="wave" style="top:1500px"></div><div class="wave" style="top:1620px;background:rgba(0,0,0,.08)"></div>
<div style="position:absolute;top:360px;left:0;right:0;display:flex;flex-direction:column;align-items:center;text-align:center;gap:10px">
 <div style="background:#fff;border-radius:50%;width:400px;height:400px;display:flex;align-items:center;justify-content:center;box-shadow:0 20px 60px rgba(0,0,0,.35)">{STAR}</div>
 <div style="margin-top:40px;font-weight:900;font-size:64px;color:#FFE9A8">ذكرى</div>
 <div style="font-weight:900;font-size:112px;line-height:1.1;color:#fff;text-shadow:0 8px 0 #7E0A10">المسيرة الخضراء</div>
 <div style="font-weight:900;font-size:64px;color:#fff">المظفرة 🇲🇦</div>
 <div style="margin-top:26px;font-weight:900;font-size:50px;color:#7E0A10;background:#fff;border-radius:999px;padding:4px 44px 14px">6 نونبر 1975</div>
 <div style="margin-top:40px;font-weight:700;font-size:48px;line-height:1.5;color:#fff">كل عام والمغرب موحد من طنجة للكويرة<br>وعيد سعيد لكل المغاربة</div>
</div>
<div style="position:absolute;bottom:150px;left:0;right:0;text-align:center;font-weight:700;font-size:38px;color:#fff;opacity:.9;direction:ltr">Redam Travel Agency</div>
<img src="data:image/png;base64,{PEN}" style="position:absolute;inset:0;width:1080px;height:1920px">
</body></html>"""
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1920})
    pg.set_content(html); pg.wait_for_timeout(300)
    pg.screenshot(path=str(REPO / 'stories/out/massira_51.jpg'), type='jpeg', quality=92); br.close()
print('ok')
