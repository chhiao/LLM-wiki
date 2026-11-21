# CLAUDE.md — Multi-Agent 系統 LLM Wiki 的 Schema

> 本檔是 Wiki 的「規則層」（依 Karpathy LLM Wiki pattern 的三層結構：raw → wiki → schema）。
> LLM 每次 ingest / query / lint 前都要先讀本檔。

## 1. 主題與範圍
- 主題：**Multi-Agent 系統（多代理系統，MAS）**——由多個 LLM agent 分工合作完成任務的系統。
- 讀者：資管系大學生，懂一點 LLM，但沒做過 agent 系統。
- 範圍內：agent 定義、workflow vs agent、MAS 架構、context engineering、何時該/不該用 MAS、失敗模式、驗證。
- 範圍外：特定框架的 API 細節、模型訓練。

## 2. 目錄結構
```
raw/            來源卡（URL、日期、擷取筆記）。不可修改，只能新增。
wiki/
  index.md      全部頁面目錄 + 一句話摘要（query 時先讀這頁）
  log.md        append-only 時間序紀錄（ingest / query / lint / build）
  overview.md   主題總覽（給新手的第一頁）
  glossary.md   術語表（簡報產生器用它檢查「先定義、再使用」）
  sources/      每篇來源一頁：先討論紀錄 → 摘要 → 影響了哪些頁
  concepts/     概念頁
  comparisons/  比較頁
```

## 3. 頁面規則
1. 每一個事實句結尾都要標來源 ID，例如 `[S2]`。沒有來源的句子要標 `[推論]`。
2. 數字（百分比、倍數、日期）必須和來源頁完全一致，不可四捨五入改寫。
3. 頁面互連用 `[[page-name]]`。
4. 每頁開頭有 YAML frontmatter：`title`, `type`, `sources`, `updated`。
5. 用自己的話改寫，不大段複製原文；引用原句最多一句、15 字以內。

## 4. 操作流程
### Ingest（先討論、後生成）
1. 讀 raw 來源卡。
2. **先討論**：LLM 列出 3–5 個 key takeaways、這篇和現有 Wiki 是補充還是衝突、建議強調什麼；
   由使用者確認或修改要強調的重點，記錄在來源頁的「先討論紀錄」。
3. **後生成**：寫來源摘要頁 → 更新/新增相關概念頁 → 更新 glossary → 更新 index → append log。

### Query
先讀 index.md → 打開相關頁 → 回答並附 `[S#]` 與頁名 → 有價值的答案可回存成新頁。

### Lint
檢查：斷掉的 `[[連結]]`、沒有被連到的孤兒頁、沒有來源標記的事實句、來源 ID 不存在、頁面間矛盾。

## 5. 來源 ID 對照
| ID | 來源 |
|----|------|
| S1 | Anthropic — Building Effective Agents (2024-12) |
| S2 | Anthropic — How we built our multi-agent research system (2025-06) |
| S3 | Cognition (Walden Yan) — Don't Build Multi-Agents (2025-06-12) |
| S4 | Cemri et al. — Why Do Multi-Agent LLM Systems Fail? (arXiv 2503.13657, NeurIPS 2025) |
| S5 | LangChain / LangGraph Docs — Multi-agent systems |
| S6 | OpenAI — A practical guide to building agents (2025) |
