"""Daily engagement stories (history 'on this day' + fun POV/Story Time) from stories/tool/daily.json -> stories/out/<id>.jpg"""
import base64, json, pathlib
from playwright.sync_api import sync_playwright
REPO = pathlib.Path(__file__).resolve().parents[2]; TOOL = REPO / 'stories/tool'
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONTS = ''.join(f"@font-face{{font-family:Cairo;font-weight:{w};src:url(data:font/woff2;base64,{b64(TOOL/f'fonts/cairo-{s}-{w}-normal.woff2')}) format('woff2');{r}}}" for w in (700, 900) for s, r in (('arabic', ''), ('latin', 'unicode-range:U+0000-00FF;')))
PEN = b64(TOOL / 'pennant.png')
BASE = f"{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}html{{overflow:hidden}}body{{width:1080px;height:1920px;font-family:Cairo;direction:rtl;position:relative;overflow:hidden}}b{{color:#FFD54A}}"
FOOT = f'<div style="position:absolute;bottom:130px;left:0;right:0;text-align:center;font-weight:700;font-size:34px;color:#fff;opacity:.85;direction:ltr">Redam Travel Agency</div><img src="data:image/png;base64,{PEN}" style="position:absolute;inset:0;width:1080px;height:1920px">'

def history(e):
    lines = ''.join(f'<div style="font-weight:700;font-size:46px;line-height:1.5;color:#E8F4FF">{l}</div>' for l in e['lines'])
    return f"""<body style="background:radial-gradient(circle at 50% 30%,#1D4FA8 0%,#0B2A6B 50%,#061636 100%)">
<div style="position:absolute;top:330px;left:70px;right:70px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:22px">
 <div style="font-weight:900;font-size:42px;color:#0B2A6B;background:#FFD54A;border-radius:999px;padding:2px 36px 12px">📅 بحال اليوم فالتاريخ</div>
 <div style="display:flex;align-items:center;gap:22px;margin-top:10px">
  <div style="background:#fff;border-radius:28px;padding:6px 34px 18px;text-align:center;box-shadow:0 14px 40px rgba(0,0,0,.4)">
   <div style="font-weight:900;font-size:130px;line-height:1;color:#E53935">{e['day']}</div>
   <div style="font-weight:900;font-size:44px;color:#0B2A6B">{e['month']}</div></div>
  <div style="font-weight:900;font-size:96px;color:#fff;direction:ltr">{e['year']}</div></div>
 <div style="font-size:150px;line-height:1.2;margin-top:10px">{e['icon']}</div>
 <div style="font-weight:900;font-size:80px;line-height:1.3;color:#fff">{e['title']}</div>
 <div style="display:flex;flex-direction:column;gap:6px;margin-top:6px">{lines}</div>
 <div style="margin-top:34px;font-weight:900;font-size:50px;color:#fff;background:#E53935;border-radius:22px;padding:6px 38px 16px">{e['q']}</div>
</div>{FOOT}</body>"""

def fun(e):
    bub = ''.join(f'<div style="align-self:{"flex-start" if i % 2 == 0 else "flex-end"};max-width:880px;background:{"#fff" if i % 2 == 0 else "#DCF8C6"};color:#111;border-radius:34px;padding:16px 38px 26px;font-weight:900;font-size:56px;line-height:1.35;box-shadow:0 10px 26px rgba(0,0,0,.25)">{l}</div>' for i, l in enumerate(e['lines']))
    return f"""<body style="background:linear-gradient(160deg,#FF8A3D 0%,#FF5E62 55%,#C2185B 100%)">
<div style="position:absolute;top:320px;left:70px;right:70px;display:flex;flex-direction:column;gap:30px">
 <div style="align-self:center;font-weight:900;font-size:64px;color:#111;background:#FFD54A;border-radius:24px;padding:4px 44px 16px;direction:ltr;box-shadow:0 10px 30px rgba(0,0,0,.25)">😂 {e['tag']}</div>
 {bub}
 <div style="align-self:center;margin-top:30px;font-weight:900;font-size:50px;color:#fff;text-shadow:0 4px 14px rgba(0,0,0,.4)">{e['cta']}</div>
</div>{FOOT}</body>"""

items = json.loads((TOOL / 'daily.json').read_text(encoding='utf8'))
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1920})
    for e in items:
        body = history(e) if e['kind'] == 'history' else fun(e)
        pg.set_content(f"<html><head><style>{BASE}</style></head>{body}</html>"); pg.wait_for_timeout(250)
        pg.screenshot(path=str(REPO / f"stories/out/{e['id']}.jpg"), type='jpeg', quality=90); print(e['id'])
    br.close()
