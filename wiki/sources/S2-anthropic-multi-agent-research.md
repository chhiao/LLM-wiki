---
title: S2 How we built our multi-agent research system（Anthropic）
type: source
sources: [S2]
updated: 2026-11-21
---
# S2 — How we built our multi-agent research system（Anthropic, 2025-06）

## 先討論紀錄（Ingest #2）
**LLM 提出的 key takeaways**
1. 這是一個「真的上線」的多代理系統，採 orchestrator-worker（lead agent + subagents）。
2. 效果：內部評測比單一 agent 高 90.2%；但成本約是聊天的 15 倍 token。
3. 適合「可以平行、資訊量超過一個 context window」的任務；不適合寫程式這種高度依賴的任務。
4. 很多工程經驗：委派指令要寫清楚、依難度調整投入、看結果而非步驟來評估。

**討論問題**：90.2% 這種數字放進教學簡報會不會讓人以為 MAS 一定比較好？
**決定**：數字要和「15 倍 token」「只適合高價值任務」放在同一頁，避免單面呈現。
**要強調**：好處 + 代價並列；「token 用量解釋 80% 表現差異」說明 MAS 本質上是用更多運算換表現。
**與現有 Wiki 關係**：補充 S1 的 orchestrator-workers，給出實際案例與數據。

## 摘要
- 架構：lead agent 分析問題、規劃策略，平行派出多個 subagent 各自搜尋，再把濃縮結果交回給 lead 整合；最後由 CitationAgent 補上引用 [S2]。
- 為什麼有效：研究問題的步驟無法事先固定；每個 subagent 有獨立的 context window，可同時探索不同方向並壓縮結果 [S2]。
- 成效：多代理系統（Claude Opus 4 當 lead、Claude Sonnet 4 當 subagent）在內部評測比單一 Opus 4 agent 高 90.2% [S2]。
- 在 BrowseComp 上，三個因素解釋 95% 的表現差異，其中 token 用量單獨解釋 80% [S2]。
- 代價：agent 約用聊天互動 4 倍的 token，多代理系統約 15 倍，所以只對高價值任務划算 [S2]。
- 不適合：需要所有 agent 共享同一份 context、或 agent 間依賴很多的任務；多數寫程式任務屬於這類 [S2]。
- 早期失敗：簡單問題派出幾十個 subagent、一直找不存在的資料、subagent 互相干擾 [S2]。
- 經驗：委派時要給目標、輸出格式、工具指引與任務邊界；依問題難度調整 subagent 數量；平行化讓複雜查詢的研究時間最多減少 90% [S2]。
- 評估：看最終結果是否正確而非步驟是否照劇本；一開始約 20 個真實問題就足夠；用單一 LLM-as-judge 依 rubric 評分；人工測試仍不可少 [S2]。

## 影響的頁面
[[mas-architectures]]、[[when-to-use-mas]]、[[cost-and-tradeoffs]]、[[verification-and-evaluation]]、[[multi-agent-system]]
