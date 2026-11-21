---
title: S1 Building Effective Agents（Anthropic）
type: source
sources: [S1]
updated: 2026-11-21
---
# S1 — Building Effective Agents（Anthropic, 2024-12）

## 先討論紀錄（Ingest #1）
**LLM 提出的 key takeaways**
1. 「workflow」和「agent」是不同東西：前者路徑寫死，後者讓 LLM 自己決定。
2. 五種常見模式，其中 orchestrator-workers 就是多代理的雛形。
3. 核心態度是「先簡單、再加複雜度」。

**討論問題**：這篇幾乎沒講「多代理」，要放進 MAS Wiki 嗎？
**決定**：要。它提供新手需要的地基（agent 是什麼、模式有哪些），而且「先簡單」原則會和 S2/S3 形成對照。
**要強調**：workflow vs agent 的分界、orchestrator-workers、停止條件。
**與現有 Wiki 關係**：第一篇，建立基礎概念頁。

## 摘要
- Anthropic 把 workflow 和 agent 合稱 agentic systems：workflow 用預先定義的程式路徑串起 LLM 與工具，agent 則由 LLM 動態決定自己的流程與工具使用 [S1]。
- 建議先找最簡單的解法，常常一次 LLM 呼叫加上檢索就夠；agentic 系統是用延遲和成本換表現 [S1]。
- 基本積木是 augmented LLM：加上檢索、工具、記憶的 LLM [S1]。
- 五種 workflow 模式：prompt chaining、routing、parallelization（sectioning / voting）、orchestrator-workers、evaluator-optimizer [S1]。
- orchestrator-workers：中央 LLM 動態拆解任務、分派給 worker、再整合結果；和 parallelization 不同，子任務不是事先定好的 [S1]。
- agent 適合步驟數無法預測的開放問題，但成本較高、錯誤會累積，需要沙盒與 guardrail，並設停止條件（例如迭代上限）[S1]。
- 三個核心原則：設計保持簡單、規劃步驟透明可見、仔細設計 agent 與工具的介面 [S1]。

## 影響的頁面
[[agent]]、[[workflow-vs-agent]]、[[mas-architectures]]、[[when-to-use-mas]]、[[glossary]]
