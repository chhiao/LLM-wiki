"""N4 render：slides.json + outline.json + wiki → 單一自含 HTML 簡報（內嵌 Wiki 對照面板）。"""
import json, re, html
import markdown
from wikilib import ROOT, load_pages

SRC_NAMES = {
    "S1": "Anthropic — Building Effective Agents (2024)",
    "S2": "Anthropic — Multi-agent research system (2025)",
    "S3": "Cognition — Don't Build Multi-Agents (2025)",
    "S4": "Cemri et al. — Why Do Multi-Agent LLM Systems Fail? (2025)",
    "S5": "LangGraph Docs — Multi-agent systems",
    "S6": "OpenAI — A practical guide to building agents (2025)",
}
SRC_PAGE = {"S1": "S1-building-effective-agents", "S2": "S2-anthropic-multi-agent-research",
            "S3": "S3-cognition-dont-build-multi-agents", "S4": "S4-mast-why-mas-fail",
            "S5": "S5-langgraph-multi-agent-docs", "S6": "S6-openai-practical-guide"}


def wiki_html(pages):
    out = {}
    for name, p in pages.items():
        body = re.sub(r"\[\[([^\]]+)\]\]", lambda m: f'<a class="wl" data-page="{m.group(1)}">{m.group(1)}</a>', p["body"])
        out[name] = {"title": p["title"], "path": p["path"],
                     "html": markdown.markdown(body, extensions=["tables", "fenced_code"])}
    return out


def esc(s): return html.escape(s, quote=False)


def build_html():
    pages = load_pages()
    outline = json.loads((ROOT / "build/outline.json").read_text(encoding="utf-8"))
    sl = json.loads((ROOT / "build/slides.json").read_text(encoding="utf-8"))
    refs = {s["id"]: s.get("wiki_refs", []) for s in outline["slides"]}
    secs = []
    n = len(sl["slides"])
    for i, s in enumerate(sl["slides"], 1):
        k = s["kind"]
        inner = ""
        if k == "title":
            inner = f"""<div class="title-wrap"><div class="kicker">LLM Wiki 教學簡報 · 6 篇來源</div>
<h1>{esc(s['title'])}</h1><p class="sub">{esc(s.get('subtitle',''))}</p>
<div class="hint">按 → 或空白鍵翻頁 · 每頁下方「📖」可打開對應的 Wiki 頁</div></div>"""
        else:
            bl = ""
            for b in s.get("bullets", []):
                tag = ""
                if b.get("src"):
                    tag = "".join(f'<a class="src wiki-cite" data-page="{SRC_PAGE[c]}" title="{esc(SRC_NAMES[c])}">{c}</a>' for c in b["src"])
                elif b.get("inference"):
                    tag = '<span class="src inf" title="由 Wiki 內容歸納，非單一來源">歸納</span>'
                bl += f"<li><span>{esc(b['text'])}</span>{tag}</li>"
            quiz = ""
            for qi, q in enumerate(s.get("quiz", [])):
                opts = "".join(f'<button class="opt" data-correct="{1 if j == q["answer"] else 0}">{esc(o)}</button>'
                               for j, o in enumerate(q["options"]))
                quiz += f'<div class="quiz-item"><p class="q">Q{qi+1}. {esc(q["q"])}</p><div class="opts">{opts}</div><p class="why">💡 {esc(q["why"])}</p></div>'
            defs = "".join(f'<span class="def">新名詞：{esc(d)}</span>' for d in s.get("defines", []))
            has_vis = bool(s.get("visual"))
            body = f'<ul class="bul">{bl}</ul>' if bl else ""
            if quiz: body += f'<div class="quiz">{quiz}</div>'
            vis = f'<div class="vis">{s["visual"]}</div>' if has_vis else ""
            inner = f"""<header><div class="num">{i:02d}</div><h2>{esc(s['title'])}</h2><div class="defs">{defs}</div></header>
<div class="content {'split' if has_vis else ''}"><div class="text">{body}</div>{vis}</div>"""
        foot_refs = "".join(f'<button class="wiki-ref" data-page="{r}">📖 {r}</button>' for r in refs.get(s["id"], []))
        secs.append(f"""<section class="slide" id="{s['id']}" data-kind="{k}">{inner}
<footer><div class="refs">Wiki 對照：{foot_refs}</div><div class="pg">{i} / {n}</div></footer></section>""")

    wiki = json.dumps(wiki_html(pages), ensure_ascii=False).replace("</", "<\\/")
    return TEMPLATE.replace("{{TITLE}}", esc(sl["title"])).replace("{{SLIDES}}", "\n".join(secs)).replace("{{WIKI}}", wiki)


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{TITLE}}</title>
<style>
:root{--bg:#f4f1ea;--ink:#1d1b18;--mute:#6b665d;--card:#fffdf8;--acc:#d9480f;--acc2:#1864ab;--line:#e2dccf;--ok:#2b8a3e;--bad:#c92a2a}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#2a2723;font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;color:var(--ink)}
#stage{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
#deck{width:1280px;height:720px;position:relative;transform-origin:center}
.slide{position:absolute;inset:0;background:var(--bg);border-radius:6px;padding:52px 64px 70px;display:none;flex-direction:column;overflow:hidden}
.slide.on{display:flex;animation:in .35s ease}
@keyframes in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.slide[data-kind=title]{background:radial-gradient(circle at 85% 20%,#ffd8a8 0,transparent 40%),var(--bg)}
.title-wrap{margin:auto 0;max-width:900px}.kicker{font-size:18px;letter-spacing:.12em;color:var(--acc);font-weight:700}
h1{font-size:72px;line-height:1.1;margin:18px 0 14px;font-weight:900}.sub{font-size:28px;color:var(--mute);margin:0}
.hint{margin-top:48px;font-size:16px;color:var(--mute);border-left:4px solid var(--acc);padding-left:12px}
header{display:flex;align-items:baseline;gap:18px;flex-wrap:wrap;border-bottom:2px solid var(--ink);padding-bottom:14px;margin-bottom:26px}
.num{font-family:ui-monospace,Menlo,monospace;font-size:20px;color:var(--acc);font-weight:700}
h2{font-size:42px;margin:0;font-weight:900}.defs{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
.def{font-size:14px;background:#fff3bf;border:1px solid #f0d36b;padding:4px 10px;border-radius:99px}
.content{flex:1;display:flex;gap:44px;min-height:0;padding-bottom:18px}.content.split .text{flex:1.1}.vis{flex:1;display:flex;align-items:center;justify-content:center}
.text{flex:1;display:flex;flex-direction:column;justify-content:center}.bul{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:22px}
.bul li{font-size:27px;line-height:1.45;padding-left:26px;position:relative}
.bul li:before{content:"";position:absolute;left:0;top:.55em;width:11px;height:11px;background:var(--acc);border-radius:2px}
.src{display:inline-block;font-size:13px;font-weight:700;margin-left:8px;padding:1px 7px;border-radius:4px;background:#e7f0fa;color:var(--acc2);cursor:pointer;vertical-align:3px;font-family:ui-monospace,monospace}
.src.inf{background:#eee;color:var(--mute);cursor:help}
footer{position:absolute;left:64px;right:64px;bottom:20px;display:flex;justify-content:space-between;align-items:center;font-size:14px;color:var(--mute)}
.wiki-ref{font:inherit;font-size:13px;margin-left:6px;background:var(--card);border:1px solid var(--line);border-radius:4px;padding:3px 8px;cursor:pointer;color:var(--ink)}
.wiki-ref:hover,.src:hover{outline:2px solid var(--acc2)}
.pg{font-family:ui-monospace,monospace}
/* visuals */
.trio{display:grid;gap:14px;width:100%}.trio div{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:16px 20px}
.trio b{display:block;font-size:24px}.trio span{color:var(--mute);font-size:18px}
.loop{display:flex;flex-wrap:wrap;gap:10px;align-items:center;font-size:20px;color:var(--mute)}
.loop span{background:var(--card);border:2px solid var(--ink);border-radius:8px;padding:10px 14px;color:var(--ink);font-weight:700}
.loop .end{border-color:var(--ok);color:var(--ok)}
table{border-collapse:collapse;width:100%;font-size:19px;background:var(--card)}th,td{border:1px solid var(--line);padding:12px;text-align:left}th{background:var(--ink);color:#fff}
.tree{text-align:center;width:100%}.boss{display:inline-block;background:var(--ink);color:#fff;padding:14px 24px;border-radius:8px;font-size:22px;font-weight:700}
.kids{display:flex;gap:12px;justify-content:center;margin-top:34px;position:relative}.kids:before{content:"";position:absolute;top:-22px;left:16%;right:16%;border-top:2px solid var(--ink)}
.kids div{background:var(--card);border:2px solid var(--ink);border-radius:8px;padding:12px;font-size:17px}.note{margin-top:18px;color:var(--mute);font-size:17px}
.stats{display:grid;gap:14px;width:100%}.stats div{background:var(--card);border-left:6px solid var(--acc);padding:14px 20px;border-radius:4px}
.stats b{font-size:38px;display:block;font-weight:900}.stats span{color:var(--mute);font-size:18px}
.bars{width:100%;display:flex;flex-direction:column;gap:16px}.bars div{position:relative;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:16px;font-size:20px;display:flex;justify-content:space-between;overflow:hidden}
.bars div:before{content:"";position:absolute;inset:0 auto 0 0;width:calc(var(--w)*2);background:#ffe3d3;z-index:0}.bars span,.bars b{position:relative}
.layers{display:flex;flex-direction:column;gap:8px;width:100%}.layers div{background:var(--card);border:2px solid var(--ink);border-radius:8px;padding:12px 16px;font-size:19px}.layers div b{color:var(--acc)}.layers .top{background:var(--ink);color:#fff}.layers .top b{color:#ffd8a8}
.steps{display:flex;flex-direction:column;gap:10px;width:100%}.steps div{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 16px;font-size:20px;font-weight:700}
.steps i{display:block;font-style:normal;font-weight:400;color:var(--mute);font-size:16px}
.quiz{display:flex;flex-direction:column;gap:30px}.q{font-size:25px;font-weight:700;margin:0 0 8px}
.opts{display:flex;gap:10px;flex-wrap:wrap}.opt{font:inherit;font-size:20px;padding:10px 18px;border:2px solid var(--ink);background:var(--card);border-radius:6px;cursor:pointer}
.opt.right{background:var(--ok);color:#fff;border-color:var(--ok)}.opt.wrong{background:var(--bad);color:#fff;border-color:var(--bad)}
.why{display:none;margin:8px 0 0;color:var(--mute);font-size:17px}.quiz-item.done .why{display:block}
/* chrome */
#bar{position:fixed;left:0;top:0;height:4px;background:var(--acc);transition:width .3s}
#nav{position:fixed;top:10px;right:14px;z-index:5;display:flex;gap:8px}#nav button{background:#ffffff22;color:#fff;border:0;border-radius:6px;padding:8px 12px;font-size:16px;cursor:pointer}
#drawer{position:fixed;top:0;right:0;height:100%;width:min(560px,92vw);background:#fffdf8;box-shadow:-10px 0 30px #0006;transform:translateX(105%);transition:transform .3s;display:flex;flex-direction:column;z-index:10}
#drawer.open{transform:none}#drawer .hd{padding:14px 20px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;gap:10px}
#drawer .hd small{color:var(--mute);font-family:ui-monospace,monospace}#drawer .bd{padding:6px 24px 30px;overflow:auto;font-size:15px;line-height:1.65}
#drawer h1{font-size:26px;margin:16px 0 8px}#drawer h2{font-size:20px;margin:18px 0 6px}#drawer h3{font-size:17px}#drawer table{font-size:14px}#drawer th,#drawer td{padding:6px}.wl{color:var(--acc2);cursor:pointer;text-decoration:underline}
#drawer button{border:0;background:var(--ink);color:#fff;border-radius:4px;padding:6px 10px;cursor:pointer}
</style></head><body>
<div id="bar"></div>
<div id="stage"><div id="deck">
{{SLIDES}}
</div></div>
<div id="nav"><button id="prev" aria-label="上一頁">←</button><button id="idx" aria-label="Wiki 首頁">📚 Wiki</button><button id="next" aria-label="下一頁">→</button></div>
<aside id="drawer" aria-label="Wiki 對照"><div class="hd"><div><b id="dt"></b><br><small id="dp"></small></div><button id="dc">關閉 ✕</button></div><div class="bd" id="db"></div></aside>
<script id="wiki-data" type="application/json">{{WIKI}}</script>
<script>
const W=JSON.parse(document.getElementById('wiki-data').textContent);
const S=[...document.querySelectorAll('.slide')];let cur=0;
function fit(){const s=Math.min(innerWidth/1300,innerHeight/740);document.getElementById('deck').style.transform='scale('+s+')'}
function go(i){cur=Math.max(0,Math.min(S.length-1,i));S.forEach((s,j)=>s.classList.toggle('on',j===cur));
document.getElementById('bar').style.width=((cur+1)/S.length*100)+'%';history.replaceState(null,'','#'+S[cur].id)}
function openWiki(p){const w=W[p];if(!w)return;document.getElementById('dt').textContent=w.title;document.getElementById('dp').textContent=w.path;
const b=document.getElementById('db');b.innerHTML=w.html;b.scrollTop=0;document.getElementById('drawer').classList.add('open')}
document.addEventListener('click',e=>{const t=e.target.closest('[data-page]');if(t){openWiki(t.dataset.page);return}
const o=e.target.closest('.opt');if(o){const it=o.closest('.quiz-item');if(it.classList.contains('done'))return;it.classList.add('done');
o.classList.add(o.dataset.correct==='1'?'right':'wrong');it.querySelector('[data-correct="1"]').classList.add('right')}});
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){e.preventDefault();go(cur+1)}
else if(e.key==='ArrowLeft'||e.key==='PageUp'){go(cur-1)}else if(e.key==='Escape'){document.getElementById('drawer').classList.remove('open')}});
document.getElementById('prev').onclick=()=>go(cur-1);document.getElementById('next').onclick=()=>go(cur+1);
document.getElementById('idx').onclick=()=>openWiki('index');document.getElementById('dc').onclick=()=>document.getElementById('drawer').classList.remove('open');
let tx=null;addEventListener('touchstart',e=>tx=e.touches[0].clientX);addEventListener('touchend',e=>{if(tx===null)return;const d=e.changedTouches[0].clientX-tx;if(Math.abs(d)>50)go(cur+(d<0?1:-1));tx=null});
addEventListener('resize',fit);fit();const h=location.hash.slice(1);go(Math.max(0,S.findIndex(s=>s.id===h)));
</script></body></html>"""
