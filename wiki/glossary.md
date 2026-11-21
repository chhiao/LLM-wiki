---
title: 術語表
type: glossary
sources: [S1, S2, S3, S4, S5, S6]
updated: 2026-11-21
---
# 術語表

> 格式：`- **術語** | aliases: 別名1, 別名2 | 定義 [來源]`
> 簡報產生器會用 aliases 掃描投影片文字，檢查每個術語是否「先定義、再使用」。

- **Agent** | aliases: Agent, 代理 | 由 LLM 主導流程、使用工具、高度獨立完成多步驟任務的系統 [S6]
- **Workflow** | aliases: Workflow, 工作流程 | 用事先寫好的程式路徑串起 LLM 與工具的系統 [S1]
- **Tool** | aliases: 工具, Tools | agent 用來對外行動的功能，例如搜尋、呼叫 API [S6]
- **Run loop** | aliases: run loop, 迴圈 | agent 重複「思考→用工具→看結果」直到結束條件 [S6]
- **Multi-Agent System** | aliases: Multi-Agent, 多代理, MAS | 一群透過協調互動、合作完成任務的 agent [S4]
- **Subagent** | aliases: subagent, 子代理 | 被主 agent 派出去執行子任務的 agent [S2]
- **Orchestrator-worker** | aliases: Orchestrator, orchestrator-worker, Supervisor, Manager, lead agent | 由中央 agent 拆任務、分派、整合結果的架構 [S1][S5][S6]
- **Handoff** | aliases: Handoff, 交接 | 一個 agent 把控制權交給另一個 agent [S5][S6]
- **Context window** | aliases: context window, 上下文視窗 | 模型一次能讀進的內容量 [S2]
- **Context engineering** | aliases: context engineering, Context Engineering | 刻意管理系統每個部分能看到哪些資訊 [S3]
- **Token** | aliases: token, Token | 模型處理文字的基本計量單位，也是計費單位 [推論]
- **Guardrail** | aliases: guardrail, Guardrails, 護欄 | 限制 agent 行為的檢查與防護 [S6]
- **LLM-as-judge** | aliases: LLM-as-judge | 用 LLM 依評分標準評估輸出 [S2]
- **MAST** | aliases: MAST | 多代理系統失敗分類法：14 種模式、3 大類 [S4]
