---
title: MAS 架構（Orchestrator / Supervisor / Handoff / Hierarchical）
type: concept
sources: [S1, S2, S5, S6]
updated: 2026-11-21
---
# MAS 架構

## 1. Orchestrator-worker / Supervisor / Manager（中央指揮型）
- 中央 LLM 動態拆解任務、分派給 worker、再整合結果；子任務不是事先定好的 [S1]。
- LangGraph 稱為 supervisor：中央 LLM 決定下一個交給哪個 worker；tool-calling 版本把 worker 包成工具 [S5]。
- OpenAI 稱為 manager pattern：manager 把專門 agent 當工具呼叫，保有對話控制權 [S6]。
- 實例：Anthropic Research 系統由 lead agent 平行派出 subagents 搜尋，再整合；另有 CitationAgent 補引用 [S2]。

## 2. Handoff / Decentralized（交接型）
- 同層 agent 互相交接控制權並傳遞對話狀態，接手的 agent 直接面對使用者 [S6]。
- 例子：分流 agent 把物流問題交給訂單管理 agent [S6]。
- LangGraph 中的 handoff 通常同時更新狀態並指定下一個 agent [S5]。

## 3. Network（網狀）
- 任何 agent 都可以呼叫任何 agent，適合沒有明確階層或固定順序的問題 [S5]。

## 4. Hierarchical（階層型）
- 小隊各有 supervisor，再由最上層 supervisor 管理；適合單一 supervisor 負擔太重時 [S5]。

## 5. Custom workflow（自訂流程）
- 部分用固定邊連接（最可預測），部分讓 LLM 動態決定下一步 [S5]。

## 名詞對照（lint 時發現的同義詞）
| Anthropic [S1][S2] | LangGraph [S5] | OpenAI [S6] |
|---|---|---|
| orchestrator-workers / lead agent + subagents | supervisor（tool-calling） | manager pattern |
| — | network + handoff | decentralized pattern |

相關：[[multi-agent-system]]、[[context-engineering]]
