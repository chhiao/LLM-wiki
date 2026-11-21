"""
Wiki → 教學 HTML 簡報 的 graph pipeline。

節點（node）：
  L0  lint     Wiki 健康檢查（斷連結、孤兒頁、無來源事實句、來源 ID 不存在）
  N1  query    依學習目標查詢 Wiki（先讀 index，再以關鍵字打分）→ build/query_result.json
  N2  outline  [LLM] 產生大綱 → build/outline.json
  G1  gate1    大綱關卡
  N3  draft    [LLM] 產生投影片內容 → build/slides.json
  G2  gate2    內容關卡（引用、數字可追溯、術語先定義後使用、字數）
  N4  render   產生 HTML → dist/slides.html
  G3  gate3    呈現關卡（HTML 結構、每頁有 Wiki 對照、導覽可用）

[LLM] 節點由 LLM 撰寫 JSON；關卡失敗時回到對應節點重新生成（最多 3 次）。
用法：python pipeline.py <node> [--graph v1|v2] [--iter N]
"""
import json, re, sys, pathlib, datetime, argparse
from wikilib import ROOT, load_pages, load_glossary, CITE_RE, NUM_RE, SRC_IDS, norm_num

BUILD = ROOT / "build"; BUILD.mkdir(exist_ok=True)
DIST = ROOT / "dist"; DIST.mkdir(exist_ok=True)
RUNS = ROOT / "runs"; RUNS.mkdir(exist_ok=True)
MAX_BULLETS, MAX_CHARS = 5, 70


def log_run(node, graph, it, ok, issues, extra=None):
    rec = {"time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "graph": graph,
           "iter": it, "node": node, "pass": ok, "n_issues": len(issues), "issues": issues}
    if extra: rec.update(extra)
    with open(RUNS / "run_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"[{node}] graph={graph} iter={it} -> {'PASS' if ok else 'FAIL'} ({len(issues)} issues)")
    for i in issues: print("   -", i)
    return ok


# ---------- L0 lint ----------
def lint(args):
    pages = load_pages(); issues = []
    linked = set()
    for name, p in pages.items():
        for l in p["links"]:
            linked.add(l)
            if l not in pages: issues.append(f"{name}: 斷掉的連結 [[{l}]]")
        for c in CITE_RE.findall(p["body"]):
            if c not in SRC_IDS: issues.append(f"{name}: 不存在的來源 {c}")
        if p["type"] in ("concept", "comparison", "source"):
            for line in p["body"].splitlines():
                s = line.strip()
                if s.startswith("- ") and len(s) > 25 and not CITE_RE.search(s) \
                        and "[推論]" not in s and "[[" not in s:
                    issues.append(f"{name}: 事實句缺來源 → {s[:30]}…")
    for name in pages:
        if name not in linked and name not in ("index", "log"):
            issues.append(f"{name}: 孤兒頁（沒有任何頁連到它）")
    return log_run("L0-lint", args.graph, args.iter, not issues, issues,
                   {"pages": len(pages)})


# ---------- N1 query ----------
def query(args):
    pages = load_pages()
    obj = json.loads((ROOT / "pipeline/objectives.json").read_text(encoding="utf-8"))
    index_links = pages["index"]["links"]  # 先讀 index，只在 index 列出的頁面中查
    result = []
    for o in obj["objectives"]:
        scored = []
        for name in index_links:
            p = pages[name]
            if p["type"] in ("index", "log", "glossary"): continue
            text = p["body"].lower()
            score = sum(text.count(k.lower()) for k in o["keywords"])
            if score: scored.append((score, name))
        scored.sort(reverse=True)
        top = [n for _, n in scored[:3]]
        facts = []
        for n in top:
            for line in pages[n]["body"].splitlines():
                if CITE_RE.search(line) and any(k.lower() in line.lower() for k in o["keywords"]):
                    facts.append({"page": n, "line": line.strip()[:160]})
        result.append({"objective": o["id"], "goal": o["goal"], "pages": top, "facts": facts[:6]})
    (BUILD / "query_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    issues = [f"{r['objective']}: Wiki 查無相關頁 → 需要回到 ingest 補資料" for r in result if not r["pages"]]
    return log_run("N1-query", args.graph, args.iter, not issues, issues,
                   {"hits": {r["objective"]: r["pages"] for r in result}})


# ---------- helpers ----------
def term_hits(text, glossary):
    hits = set()
    for t in glossary:
        for a in t["aliases"]:
            if re.search(r"[A-Za-z]", a):
                if re.search(r"(?<![A-Za-z\-])" + re.escape(a) + r"(?![A-Za-z])", text): hits.add(t["term"])
            elif a in text: hits.add(t["term"])
    return hits


def slide_text(s):
    parts = [s.get("title", "")]
    for b in s.get("bullets", []): parts.append(b["text"])
    if s.get("visual"): parts.append(re.sub(r"<[^>]+>", " ", s["visual"]))
    for q in s.get("quiz", []): parts += [q["q"]] + q["options"]
    return " ".join(parts)


def check_term_order(seq, glossary, where):
    """seq: list of (slide_id, defines, text, exempt)。回傳術語「先用後定義」的問題。"""
    issues, defined = [], set()
    for sid, defines, text, exempt in seq:
        defined |= set(defines)
        if exempt: continue
        for t in sorted(term_hits(text, glossary) - defined):
            issues.append(f"{where} {sid}: 術語「{t}」在定義前就被使用")
    return issues


def check_number(num, refs, pages):
    n = norm_num(num)
    return any(n in norm_num(pages[r]["body"]) for r in refs if r in pages)


# ---------- G1 outline gate ----------
def gate1(args):
    pages = load_pages(); glossary = load_glossary(pages)
    obj = json.loads((ROOT / "pipeline/objectives.json").read_text(encoding="utf-8"))
    out = json.loads(pathlib.Path(args.outline or BUILD / "outline.json").read_text(encoding="utf-8"))
    issues = []
    covered = {o for s in out["slides"] for o in s.get("objectives", [])}
    for o in obj["objectives"]:
        if o["id"] not in covered: issues.append(f"學習目標 {o['id']} 沒有任何投影片負責")
    for s in out["slides"]:
        if s.get("kind") not in ("title", "agenda") and not s.get("wiki_refs"):
            issues.append(f"{s['id']}: 沒有指定 Wiki 來源頁")
        for r in s.get("wiki_refs", []):
            if r not in pages: issues.append(f"{s['id']}: Wiki 頁 {r} 不存在")
    # 教學結構：開頭要有目標、結尾要有回顧與測驗
    kinds = [s.get("kind") for s in out["slides"]]
    if "agenda" not in kinds[:3]: issues.append("前 3 頁沒有學習目標/路線圖")
    if "quiz" not in kinds: issues.append("沒有測驗頁（無法確認學習成效）")
    if kinds[-1] != "summary": issues.append("最後一頁不是重點回顧")
    if args.graph == "v2":  # ★ v2：把術語順序與數字追溯往前移到大綱階段
        seq = [(s["id"], s.get("defines", []), " ".join(s.get("terms_used", [])) + " " + s["title"],
                s.get("kind") in ("title", "agenda")) for s in out["slides"]]
        issues += check_term_order(seq, glossary, "[大綱]")
        for s in out["slides"]:
            for f in s.get("key_facts", []):
                for num in NUM_RE.findall(f):
                    if not check_number(num, s.get("wiki_refs", []), pages):
                        issues.append(f"[大綱] {s['id']}: 預計使用的數字 {num} 在指定 Wiki 頁找不到")
    return log_run("G1-outline-gate", args.graph, args.iter, not issues, issues,
                   {"slides": len(out["slides"])})


# ---------- G2 content gate ----------
def gate2(args):
    pages = load_pages(); glossary = load_glossary(pages)
    out = json.loads((BUILD / "outline.json").read_text(encoding="utf-8"))
    sl = json.loads((BUILD / "slides.json").read_text(encoding="utf-8"))
    refs_of = {s["id"]: s.get("wiki_refs", []) for s in out["slides"]}
    issues = []
    if [s["id"] for s in sl["slides"]] != [s["id"] for s in out["slides"]]:
        issues.append("投影片順序/數量與大綱不一致")
    for s in sl["slides"]:
        refs = refs_of.get(s["id"], [])
        bl = s.get("bullets", [])
        if len(bl) > MAX_BULLETS: issues.append(f"{s['id']}: 重點 {len(bl)} 條，超過 {MAX_BULLETS}")
        allowed_src = {x for r in refs for x in pages.get(r, {}).get("sources", [])}
        for b in bl:
            t = b["text"]
            if len(t) > MAX_CHARS: issues.append(f"{s['id']}: 句子太長（{len(t)} 字）→ {t[:20]}…")
            if s.get("kind") not in ("title", "agenda", "quiz"):
                if not b.get("src") and not b.get("inference"):
                    issues.append(f"{s['id']}: 缺來源標記 → {t[:24]}…")
                for c in b.get("src", []):
                    if c not in allowed_src:
                        issues.append(f"{s['id']}: 引用 {c} 但指定 Wiki 頁 {refs} 沒有這個來源")
        for num in NUM_RE.findall(slide_text(s)):
            if len(norm_num(num).rstrip("%")) <= 1 and "%" not in num: continue  # 略過 1~9 的序號
            if not check_number(num, refs, pages):
                issues.append(f"{s['id']}: 數字 {num} 在指定 Wiki 頁找不到（可能幻覺或寫錯）")
    seq = [(s["id"], s.get("defines", []), slide_text(s), s.get("kind") in ("title", "agenda"))
           for s in sl["slides"]]
    issues += check_term_order(seq, glossary, "[內容]")
    return log_run("G2-content-gate", args.graph, args.iter, not issues, issues)


# ---------- N4 render ----------
def render(args):
    from render import build_html
    html = build_html()
    (DIST / "slides.html").write_text(html, encoding="utf-8")
    return log_run("N4-render", args.graph, args.iter, True, [], {"bytes": len(html.encode())})


# ---------- G3 render gate ----------
def gate3(args):
    from bs4 import BeautifulSoup
    html = (DIST / "slides.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    sl = json.loads((BUILD / "slides.json").read_text(encoding="utf-8"))
    pages = load_pages()
    issues = []
    secs = soup.select("section.slide")
    if len(secs) != len(sl["slides"]): issues.append(f"HTML 有 {len(secs)} 頁，slides.json 有 {len(sl['slides'])} 頁")
    for sec in secs:
        sid = sec.get("id")
        if not sec.get_text(strip=True): issues.append(f"{sid}: 空白頁")
        if sec.get("data-kind") not in ("title",) and not sec.select(".wiki-ref"):
            issues.append(f"{sid}: 沒有 Wiki 對照連結")
        for a in sec.select(".wiki-ref"):
            if a.get("data-page") not in pages: issues.append(f"{sid}: Wiki 連結指向不存在的頁 {a.get('data-page')}")
    if not soup.select("script#wiki-data"): issues.append("沒有內嵌 Wiki 資料，無法點開對照")
    js = " ".join(s.get_text() for s in soup.find_all("script"))
    for need in ("ArrowRight", "ArrowLeft"):
        if need not in js: issues.append(f"缺少鍵盤導覽 {need}")
    for q in soup.select(".quiz-item"):
        if not q.select("[data-correct='1']"): issues.append(f"測驗題沒有正確答案：{q.get_text()[:20]}")
    if args.graph == "v2":  # ★ v2：加入「真的打開瀏覽器看」的版面檢查
        issues += visual_check()
    return log_run("G3-render-gate", args.graph, args.iter, not issues, issues)


def visual_check():
    """用 headless Chrome 打開每一頁：內容溢出、導覽列遮住頁尾、內容只占上半部（版面失衡）。"""
    import asyncio
    from playwright.async_api import async_playwright
    js = """()=>{const s=document.querySelector('.slide.on'),r=s.getBoundingClientRect(),f=s.querySelector('footer').getBoundingClientRect();
      const n=document.getElementById('nav').getBoundingClientRect();const c=s.querySelector('.content');const out={};
      out.navOverlap=!(n.right<f.left||n.left>f.right||n.bottom<f.top||n.top>f.bottom);
      if(c){let top=1e9,bot=0;c.querySelectorAll('li,.vis>*,.quiz-item').forEach(e=>{const b=e.getBoundingClientRect();top=Math.min(top,b.top);bot=Math.max(bot,b.bottom)});
        const cr=c.getBoundingClientRect();out.overflow=bot>f.top-4;out.fill=(bot-cr.top)/(cr.height||1);out.topGap=(top-cr.top)/(cr.height||1)}
      return out}"""
    async def run():
        res = []
        async with async_playwright() as p:
            b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
            pg = await b.new_page(viewport={"width": 1300, "height": 740})
            await pg.goto((DIST / "slides.html").as_uri())
            ids = await pg.eval_on_selector_all("section.slide", "els=>els.map(e=>e.id)")
            for i, sid in enumerate(ids):
                await pg.evaluate(f"go({i})"); await pg.wait_for_timeout(380)
                o = await pg.evaluate(js)
                if o.get("navOverlap"): res.append(f"{sid}: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）")
                if o.get("overflow"): res.append(f"{sid}: 內容溢出到頁尾")
                if "fill" in o and o["fill"] < 0.6 and o["topGap"] < 0.08:
                    res.append(f"{sid}: 版面失衡，內容只占上方 {o['fill']:.0%}")
            await b.close()
        return res
    return asyncio.run(run())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("node"); ap.add_argument("--graph", default="v1"); ap.add_argument("--iter", type=int, default=1); ap.add_argument("--outline")
    a = ap.parse_args()
    ok = {"lint": lint, "query": query, "gate1": gate1, "gate2": gate2, "render": render, "gate3": gate3}[a.node](a)
    sys.exit(0 if ok else 1)
