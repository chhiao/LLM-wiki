"""Wiki 讀取工具：解析 frontmatter、[[連結]]、來源標記與術語表。"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
SRC_IDS = {f"S{i}" for i in range(1, 7)}

LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
CITE_RE = re.compile(r"\[(S\d)\]")
NUM_RE = re.compile(r"\d[\d,]*(?:\.\d+)?%?")


def load_pages():
    pages = {}
    for p in sorted(WIKI.rglob("*.md")):
        text = p.read_text(encoding="utf-8")
        fm, body = {}, text
        if text.startswith("---"):
            _, fm_txt, body = text.split("---", 2)
            for line in fm_txt.strip().splitlines():
                k, _, v = line.partition(":")
                fm[k.strip()] = v.strip()
        srcs = re.findall(r"S\d", fm.get("sources", ""))
        pages[p.stem] = {
            "path": str(p.relative_to(ROOT)),
            "title": fm.get("title", p.stem),
            "type": fm.get("type", ""),
            "sources": srcs,
            "body": body,
            "links": LINK_RE.findall(body),
        }
    return pages


def load_glossary(pages):
    terms = []
    for line in pages["glossary"]["body"].splitlines():
        m = re.match(r"- \*\*(.+?)\*\* \| aliases: (.+?) \| (.+)", line)
        if m:
            aliases = [a.strip() for a in m.group(2).split(",")]
            terms.append({"term": m.group(1), "aliases": aliases, "definition": m.group(3)})
    return terms


def norm_num(s):
    return s.replace(",", "")
