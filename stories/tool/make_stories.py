"""Render REDAM story images (1080x1920) from stories/tool/stories.json.

Usage: python3 stories/tool/make_stories.py   (run from the repo root)
Each entry: {"id": "...", "kind": "poster", "poster": "posts/xx.png", "hook": "...", "sub": "..."}
         or {"id": "...", "kind": "text", "title": "...", "lines": ["..."], "cta": "..."}
Output: stories/out/<id>.jpg
"""
import base64, json, pathlib
from playwright.sync_api import sync_playwright

REPO = pathlib.Path(__file__).resolve().parents[2]
TOOL = REPO / 'stories/tool'
def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONTS = ''.join(
    f"@font-face{{font-family:Cairo;font-weight:{w};src:url(data:font/woff2;base64,{b64(TOOL/f'fonts/cairo-{s}-{w}-normal.woff2')}) format('woff2');{r}}}"
    for w in (700, 900) for s, r in (('arabic', ''), ('latin', 'unicode-range:U+0000-00FF;')))
PENNANT = b64(TOOL / 'pennant.png')
WA = """<svg viewBox="0 0 32 32" width="62" height="62"><path fill="#fff" d="M16 3C8.8 3 3 8.7 3 15.8c0 2.5.7 4.9 2 7L3 29l6.4-2c2 1.1 4.3 1.7 6.6 1.7 7.2 0 13-5.7 13-12.8S23.2 3 16 3zm6.1 15.2c-.3-.2-2-1-2.3-1.1-.3-.1-.5-.2-.8.2-.2.3-.9 1.1-1.1 1.3-.2.2-.4.3-.7.1-.3-.2-1.4-.5-2.7-1.7-1-.9-1.7-2-1.9-2.3-.2-.3 0-.5.1-.7l.5-.6c.2-.2.2-.3.3-.6.1-.2 0-.4 0-.6l-1-2.5c-.3-.7-.6-.6-.8-.6h-.7c-.2 0-.6.1-.9.4-.3.3-1.2 1.2-1.2 2.9s1.2 3.4 1.4 3.6c.2.2 2.4 3.7 5.9 5.2 2.9 1.1 3.5.9 4.1.8.6-.1 2-.8 2.3-1.6.3-.8.3-1.5.2-1.6-.1-.2-.3-.3-.6-.4z"/></svg>"""
CSS = f"""{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;font-family:Cairo;direction:rtl;position:relative;overflow:hidden;background:#0B2A6B}}
.pen{{position:absolute;top:0;left:0;width:1080px;height:1920px;pointer-events:none}}
.hook{{font-weight:900;font-size:72px;line-height:1.25;color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;text-shadow:0 6px 18px rgba(0,0,0,.6)}}
.hook b{{background:#E53935;color:#fff;-webkit-text-stroke:0;padding:0 14px 6px;border-radius:12px}}
.sub{{display:inline-block;margin-top:14px;font-weight:900;font-size:40px;color:#111;background:#FFD54A;padding:2px 28px 10px;border-radius:999px}}
.cta{{position:absolute;left:0;right:0;top:1440px;display:flex;flex-direction:column;align-items:center;gap:14px}}
.cta .t{{font-weight:900;font-size:46px;color:#fff;text-shadow:0 3px 12px rgba(0,0,0,.8)}}
.wa{{display:flex;align-items:center;gap:18px;background:#1FAF55;border:6px solid #fff;border-radius:999px;padding:6px 44px 14px;font-weight:900;font-size:70px;color:#fff;direction:ltr;box-shadow:0 12px 30px rgba(0,0,0,.45)}}
"""

def hl(s):  # **word** -> highlighted
    parts = s.split('**')
    return ''.join(f'<b>{p}</b>' if i % 2 else p for i, p in enumerate(parts))

def poster(e):
    img = b64(REPO / e['poster']); ext = 'jpeg' if e['poster'].endswith('jpg') else 'png'
    sub = f'<div class="sub">{e["sub"]}</div>' if e.get('sub') else ''
    return f"""<div style="position:absolute;inset:-60px;background:url(data:image/{ext};base64,{img}) center/cover;filter:blur(38px) brightness(.55) saturate(1.2)"></div>
<div style="position:absolute;top:262px;left:40px;right:40px;text-align:center"><div class="hook">{hl(e['hook'])}</div>{sub}</div>
<img src="data:image/{ext};base64,{img}" style="position:absolute;top:{e.get('top', 520)}px;left:50%;transform:translateX(-50%);width:{e.get('w', 900)}px;border-radius:28px;box-shadow:0 20px 60px rgba(0,0,0,.6);border:6px solid #fff">
<div class="cta" style="top:{e.get('cta_top', 1470)}px"><div class="t">{e.get('cta', 'صيفط لينا فالواتساب 👇').replace('👇', '')}</div>
<div class="wa">{WA}<span>060 905 06 21</span></div></div>"""

def text(e):
    lines = ''.join(f'<div style="background:#fff;color:#0B2A6B;border-radius:22px;padding:10px 30px 18px;font-weight:900;font-size:52px;box-shadow:0 8px 20px rgba(0,0,0,.3)">{l}</div>' for l in e['lines'])
    return f"""<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 30%,#1D4FA8 0%,#0B2A6B 55%,#061636 100%)"></div>
<div style="position:absolute;top:340px;left:60px;right:60px;display:flex;flex-direction:column;align-items:center;gap:30px;text-align:center">
<div class="hook" style="font-size:88px">{hl(e['title'])}</div>
<div style="display:flex;flex-direction:column;gap:22px;width:100%;margin-top:20px">{lines}</div></div>
<div class="cta"><div class="t" style="color:#FFD54A">{e.get('cta', 'جاوبنا فالميساج')}</div><div class="wa">{WA}<span>060 905 06 21</span></div></div>"""

def main():
    items = json.loads((TOOL / 'stories.json').read_text(encoding='utf8'))
    out = REPO / 'stories/out'; out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        for e in items:
            if e['kind'] not in ('poster', 'text'):
                continue
            body = poster(e) if e['kind'] == 'poster' else text(e)
            pg.set_content(f"<html><head><style>{CSS}</style></head><body>{body}<img class='pen' src='data:image/png;base64,{PENNANT}'></body></html>")
            pg.wait_for_timeout(250)
            pg.screenshot(path=str(out / f"{e['id']}.jpg"), type='jpeg', quality=90)
            print('rendered', e['id'])
        b.close()

if __name__ == '__main__':
    main()
