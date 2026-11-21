---
title: 單一 Agent vs 多代理——正反觀點比較
type: comparison
sources: [S2, S3, S4, S6]
updated: 2026-11-21
---
# 單一 Agent vs 多代理：正反觀點

| 面向 | 支持多代理（S2 Anthropic） | 反對多代理（S3 Cognition） |
|---|---|---|
| 主要任務類型 | 開放式研究、廣度優先查詢 [S2] | 長時間、高度依賴的任務（如寫程式）[S3] |
| 核心理由 | 各 subagent 獨立 context，可平行探索 [S2] | 平行 agent 的隱含假設會衝突 [S3] |
| 證據 | 內部評測 +90.2% [S2] | Flappy Bird 思想實驗、edit-apply 模型經驗 [S3] |
| 建議架構 | orchestrator-worker [S2] | 單執行緒線性 agent + 壓縮模型 [S3] |

## 看似矛盾，其實在講不同任務 [推論]
- S2 自己也承認：需要共享 context、依賴多的任務（多數寫程式）不適合 MAS [S2]。
- S3 也承認：Claude Code 有用 subagent，但只拿來回答窄問題 [S3]。
- 兩者共識：**context 怎麼分配**決定成敗 → 見 [[context-engineering]]。

## 第三方證據
- 學術研究顯示 MAS 相對單一 agent 的進步常常很小，失敗率約 41% 到 86.7% [S4]。
- OpenAI 建議先把單一 agent 用到極致 [S6]。

## 結論 [推論]
預設用單一 agent；只有任務「可平行、價值高、context 放不下」時才組隊。

相關：[[when-to-use-mas]]、[[multi-agent-system]]
