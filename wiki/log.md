---
title: Log
type: log
sources: []
updated: 2026-11-21
---
# Log（append-only）

## [2026-11-21] init | 建立 schema（CLAUDE.md）、目錄結構、來源 ID 對照表
## [2026-11-21] ingest | S1 Building Effective Agents → 討論 3 個 takeaways；新增 agent, workflow-vs-agent；更新 glossary, index
## [2026-11-21] ingest | S2 Multi-agent research system → 決定「90.2% 與 15× token 並列」；新增 multi-agent-system, mas-architectures, cost-and-tradeoffs, verification-and-evaluation
## [2026-11-21] ingest | S3 Don't Build Multi-Agents → 討論 S2/S3 是否矛盾，結論為任務類型不同；新增 context-engineering, single-vs-multi-agent
## [2026-11-21] ingest | S4 MAST → 決定簡報只放 3 大類，14 種留 Wiki；新增 failure-modes-mast
## [2026-11-21] ingest | S5 LangGraph docs → 擴充 mas-architectures 為 5 種架構
## [2026-11-21] ingest | S6 OpenAI guide → 發現 manager≈supervisor、decentralized≈handoff，加入名詞對照表；新增 when-to-use-mas
## [2026-11-21] lint | 手動 lint：補上 mas-architectures 名詞對照、確認所有數字與 raw 來源卡一致
## [2026-11-21] lint | pipeline L0：發現 4 條事實句缺逐句來源（context-engineering, failure-modes-mast）→ 補標後 PASS
## [2026-11-21] query | 簡報產生 N1：8 個學習目標各取 top-3 Wiki 頁（結果存 build/query_result.json）
## [2026-11-21] build | graph v1 執行：G2 失敗 3 項（數字不在指定頁、測驗題自編數字、術語先用後定義）→ 回 N2/N3 修正後通過
## [2026-11-21] build | 截圖檢查發現版面問題 → G3 加入 headless 瀏覽器版面檢查（v2），22 項失敗 → 修正 CSS 後通過
## [2026-11-21] build | graph v2：術語順序與數字追溯移到 G1；以原始大綱回歸測試，v2 G1 抓到 3/3、v1 G1 抓到 0/3；v2 全流程一次通過
