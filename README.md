# LLM Wiki：Multi-Agent 系統

以 Karpathy 的 LLM Wiki pattern 建立的主題知識庫，主題是 **Multi-Agent 系統（多代理系統，MAS）**；再用一條有檢查關卡的 pipeline，把 Wiki 自動轉成給初學者的教學簡報。

## 線上瀏覽

| 成品 | 連結 |
|---|---|
| 📚 Wiki 瀏覽頁 | https://chhiao.github.io/LLM-wiki/dist/wiki.html |
| 🎞️ 教學簡報（16 頁） | https://chhiao.github.io/LLM-wiki/dist/slides.html |

- 簡報用 ← → 或空白鍵翻頁；每頁下方的「📖」按鈕會打開對應的 Wiki 頁面，可以直接查證內容出處。
- 兩個檔案都是單一自含的 HTML，不需網路也能直接開啟。

## 專案概念

- **讀者**：資管系大學生，懂一點 LLM，但沒做過 agent 系統。
- **三層結構**：`raw/`（來源卡，只增不改）→ `wiki/`（LLM 整理的知識頁）→ `CLAUDE.md`（規則層 schema）。
- **可追溯**：每個事實句都標來源 ID（如 `[S2]`），沒有來源的句子標 `[推論]`；數字必須與來源完全一致。
- **先討論、後生成**：每篇來源 ingest 時，先列出 key takeaways 並與使用者討論要強調什麼，紀錄在來源頁的「先討論紀錄」，再寫入 Wiki。

### 來源

| ID | 來源 |
|----|------|
| S1 | Anthropic — Building Effective Agents (2024-12) |
| S2 | Anthropic — How we built our multi-agent research system (2025-06) |
| S3 | Cognition (Walden Yan) — Don't Build Multi-Agents (2025-06-12) |
| S4 | Cemri et al. — Why Do Multi-Agent LLM Systems Fail? (arXiv 2503.13657, NeurIPS 2025) |
| S5 | LangChain / LangGraph Docs — Multi-agent systems |
| S6 | OpenAI — A practical guide to building agents (2025) |

## 目錄結構

```
CLAUDE.md          Wiki 的規則層（頁面規則、ingest / query / lint 流程、來源對照）
raw/               來源卡（URL、日期、擷取筆記）
wiki/
  index.md         全部頁面目錄
  overview.md      給新手的第一頁
  glossary.md      術語表（簡報檢查「先定義、再使用」時會用到）
  log.md           append-only 操作紀錄
  concepts/        9 個概念頁
  comparisons/     比較頁（單一 agent vs 多代理）
  sources/         6 個來源摘要頁
pipeline/
  pipeline.py      簡報產生 pipeline（各節點與檢查關卡）
  objectives.json  簡報的 8 個學習目標
  render.py        產生 HTML 簡報
  build_wiki_site.py  產生 Wiki 瀏覽頁
  wikilib.py       讀取 Wiki 的共用工具
build/             pipeline 的中間產物（查詢結果、大綱、投影片內容 JSON）
dist/              最終成品（wiki.html、slides.html）
runs/              每次執行 pipeline 的紀錄
```

## 簡報產生 Pipeline

```
L0 lint → N1 query → N2 outline → G1 大綱關卡 → N3 draft → G2 內容關卡 → N4 render → G3 呈現關卡
```

| 節點 | 做什麼 |
|---|---|
| L0 lint | Wiki 健康檢查：斷掉的連結、孤兒頁、缺來源的事實句、不存在的來源 ID |
| N1 query | 依 8 個學習目標先讀 index，再找出相關 Wiki 頁 → `build/query_result.json` |
| N2 outline | 由 LLM 撰寫大綱 → `build/outline.json` |
| G1 大綱關卡 | 檢查大綱是否涵蓋學習目標；v2 起也檢查術語順序與數字可追溯 |
| N3 draft | 由 LLM 撰寫投影片內容 → `build/slides.json` |
| G2 內容關卡 | 每句有引用、數字能在 Wiki 找到、術語先定義後使用、字數限制 |
| N4 render | 產生 `dist/slides.html` |
| G3 呈現關卡 | HTML 結構、每頁都有 Wiki 對照、鍵盤導覽；v2 加上 headless 瀏覽器版面檢查 |

關卡失敗時會回到對應節點重新生成。N2、N3 由 LLM 撰寫 JSON，其餘節點都是程式。設計理由參考 S4（MAST）的建議：驗證要多層，而且要檢查高層目標，不能只看表面。

### 迭代紀錄

完整紀錄見 [`runs/run_log.md`](runs/run_log.md)，重點如下：

- **v1**：G2 抓到 3 個問題（數字在 Wiki 找不到、測驗題自編數字、術語先用後定義），修正後通過。
- **v2**：截圖發現版面問題，在 G3 加入瀏覽器版面檢查（第一次跑抓到 22 項），修正 CSS 後通過；並把術語順序與數字追溯提前到 G1。用原始大綱做回歸測試，v2 的 G1 抓到 3/3 個問題，v1 抓到 0/3。

## 在本機執行

需要 Python 3。

```bash
pip install markdown beautifulsoup4

cd pipeline
python pipeline.py lint      # L0
python pipeline.py query     # N1
python pipeline.py gate1     # G1（檢查 build/outline.json）
python pipeline.py gate2     # G2（檢查 build/slides.json）
python pipeline.py render    # N4 → dist/slides.html
python pipeline.py gate3     # G3
python build_wiki_site.py    # → dist/wiki.html、runs/run_log.md
```

- 參數 `--graph v1|v2` 選擇 pipeline 版本、`--iter N` 標記回合數，結果會寫入 `runs/run_log.jsonl`。
- `--graph v2` 的 G3 版面檢查需要 `pip install playwright`；程式中的 Chrome 路徑是 `/usr/bin/google-chrome`，在其他系統上需修改 `pipeline.py` 的 `visual_check()`。
