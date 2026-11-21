"""把 wiki/ 轉成單一 HTML 瀏覽頁（含 log 與 pipeline 執行紀錄），並把 run_log.jsonl 轉成 run_log.md。"""
import json, html
from wikilib import ROOT, load_pages
from render import wiki_html

pages = load_pages()
W = wiki_html(pages)

# run_log.md
rows = [json.loads(l) for l in (ROOT / "runs/run_log.jsonl").read_text(encoding="utf-8").splitlines()]
md = ["# Pipeline 執行紀錄（自動產生自 runs/run_log.jsonl）", "",
      "| # | 時間 | graph | 回合 | 節點 | 結果 | 問題數 |", "|---|---|---|---|---|---|---|"]
for i, r in enumerate(rows, 1):
    md.append(f"| {i} | {r['time'][11:]} | {r['graph']} | {r['iter']} | {r['node']} | {'✅ PASS' if r['pass'] else '❌ FAIL'} | {r['n_issues']} |")
md += ["", "## 失敗明細"]
for i, r in enumerate(rows, 1):
    if r["issues"]:
        md.append(f"\n### #{i} {r['node']}（graph {r['graph']}, 回合 {r['iter']}）")
        md += [f"- {x}" for x in r["issues"]]
(ROOT / "runs/run_log.md").write_text("\n".join(md), encoding="utf-8")
import markdown
W["_runlog"] = {"title": "Pipeline 執行紀錄", "path": "runs/run_log.md",
                "html": markdown.markdown("\n".join(md), extensions=["tables"])}

groups = [("Overview", ["overview", "glossary"]),
          ("Concepts", [n for n, p in pages.items() if p["type"] == "concept"]),
          ("Comparisons", [n for n, p in pages.items() if p["type"] == "comparison"]),
          ("Sources", [n for n, p in pages.items() if p["type"] == "source"]),
          ("Meta", ["index", "log", "_runlog"])]
nav = ""
for g, names in groups:
    nav += f"<h4>{g}</h4>" + "".join(f'<a class="wl" data-page="{n}">{html.escape(W[n]["title"])}</a>' for n in names)

page = r"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LLM Wiki：Multi-Agent 系統</title><style>
:root{--bg:#f4f1ea;--ink:#1d1b18;--mute:#6b665d;--acc:#d9480f;--acc2:#1864ab;--line:#e2dccf}
*{box-sizing:border-box}body{margin:0;font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;background:var(--bg);color:var(--ink);display:flex;min-height:100vh}
nav{width:290px;flex:none;background:#1d1b18;color:#eee;padding:22px 16px;position:sticky;top:0;height:100vh;overflow:auto}
nav .brand{font-weight:900;font-size:19px;margin-bottom:4px}nav .sub{font-size:12px;color:#aaa;margin-bottom:10px}
nav h4{font-size:11px;letter-spacing:.14em;color:#ffa94d;margin:18px 0 6px;text-transform:uppercase}
nav a{display:block;color:#ddd;padding:5px 8px;border-radius:4px;font-size:14px;cursor:pointer}nav a:hover,nav a.on{background:#ffffff1a;color:#fff}
main{flex:1;max-width:900px;padding:34px 48px 80px;line-height:1.75}
.path{font-family:ui-monospace,monospace;font-size:12px;color:var(--mute)}
main h1{font-size:34px;line-height:1.25;margin:.3em 0}main h2{border-bottom:2px solid var(--ink);padding-bottom:4px;margin-top:1.6em}
table{border-collapse:collapse;width:100%;background:#fffdf8;font-size:15px;margin:10px 0}th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}th{background:var(--ink);color:#fff}
main a.wl{color:var(--acc2);text-decoration:underline;cursor:pointer}code,pre{background:#fffdf8;border:1px solid var(--line);border-radius:4px;padding:1px 4px}pre{padding:12px;overflow:auto}
blockquote{border-left:4px solid var(--acc);margin:0;padding:4px 14px;background:#fff4e6}
@media(max-width:760px){body{display:block}nav{width:auto;height:auto;position:static}main{padding:20px}}
</style></head><body>
<nav><div class="brand">📚 LLM Wiki</div><div class="sub">主題：Multi-Agent 系統（6 篇來源 · Karpathy LLM Wiki pattern）</div>__NAV__</nav>
<main id="m"></main>
<script id="wiki-data" type="application/json">__W__</script>
<script>
const W=JSON.parse(document.getElementById('wiki-data').textContent);
function show(p){if(!W[p])return;const w=W[p];document.getElementById('m').innerHTML='<div class="path">'+w.path+'</div>'+w.html;
document.querySelectorAll('nav a').forEach(a=>a.classList.toggle('on',a.dataset.page===p));history.replaceState(null,'','#'+p);scrollTo(0,0)}
document.addEventListener('click',e=>{const t=e.target.closest('[data-page]');if(t)show(t.dataset.page)});
show(location.hash.slice(1)||'index');
</script></body></html>"""
out = page.replace("__NAV__", nav).replace("__W__", json.dumps(W, ensure_ascii=False).replace("</", "<\\/"))
(ROOT / "dist/wiki.html").write_text(out, encoding="utf-8")
print("wiki.html", len(out), "bytes;", len(rows), "log rows")
