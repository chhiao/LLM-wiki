---
title: Workflow vs Agent
type: concept
sources: [S1, S6]
updated: 2026-11-21
---
# Workflow vs Agent

| | Workflow | Agent |
|---|---|---|
| 誰決定下一步 | 工程師事先寫好的程式路徑 [S1] | LLM 動態決定 [S1] |
| 適合 | 定義清楚、重視可預測性的任務 [S1] | 步驟數無法預測的開放問題 [S1] |
| 代價 | 彈性低 [推論] | 成本較高、錯誤會累積 [S1] |

- 兩者合稱 agentic systems [S1]。
- 五種 workflow 模式 [S1]：
  1. **Prompt chaining**：把任務拆成連續步驟，每步處理上一步輸出，中間可加程式檢查。
  2. **Routing**：先分類輸入，再送到專門的後續處理。
  3. **Parallelization**：同時跑多個 LLM 呼叫再整合；分 sectioning（拆獨立子任務）與 voting（同任務跑多次）。
  4. **Orchestrator-workers**：中央 LLM 動態拆任務、分派、整合——多代理系統最常見的形狀，見 [[mas-architectures]]。
  5. **Evaluator-optimizer**：一個 LLM 生成、另一個評估並回饋，反覆改進。
- 建議：先用最簡單的方案，有明確效果才加複雜度 [S1]；若任務沒有細緻判斷、難維護規則或非結構化資料，確定性程式可能就夠 [S6]。

> 本作業的「簡報產生流程」本身就是 prompt chaining + evaluator-optimizer 的組合 [推論]。

相關：[[agent]]、[[when-to-use-mas]]
