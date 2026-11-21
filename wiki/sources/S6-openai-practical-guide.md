---
title: S6 A practical guide to building agents（OpenAI）
type: source
sources: [S6]
updated: 2026-11-21
---
# S6 — A practical guide to building agents（OpenAI, 2025）

## 先討論紀錄（Ingest #6）
**LLM 提出的 key takeaways**
1. 給新手最清楚的 agent 定義：model + tools + instructions，在 loop 裡跑到結束條件。
2. 「先把單一 agent 用到極致」——和 S1 的「先簡單」、S3 的「不要做多代理」方向一致。
3. 什麼時候拆：prompt 條件分支太多、工具相似到選錯；工具相似度比數量重要。
4. manager vs decentralized（handoff）兩種多代理模式。

**討論問題**：S6 的 manager / decentralized 和 S5 的 supervisor / network 是不是同一件事？
**決定**：概念對應——manager ≈ supervisor（tool-calling），decentralized ≈ 以 handoff 串接的 network。在 [[mas-architectures]] 加對照表，避免新手以為是不同東西。
**要強調**：agent 三元件、run loop 結束條件（連到 MAST 的「不知道終止條件」）、拆分時機。
**與現有 Wiki 關係**：補強 [[agent]] 定義；提供 [[when-to-use-mas]] 的判斷準則。

## 摘要
- agent 是高度獨立、代替使用者完成多步驟任務的系統；由 LLM 主導流程並使用工具，且在 guardrail 範圍內運作；單輪 LLM 呼叫或簡單聊天機器人不算 agent [S6]。
- 何時考慮 agent：需要細緻判斷或處理例外、規則多到難以維護、大量非結構化資料；不符合時，確定性的程式可能就夠了 [S6]。
- 三個核心元件：負責推理的 model、對外行動的 tools、設定行為與界線的 instructions [S6]。
- 單一 vs 多代理：先把單一 agent 的能力發揮到極致；當 prompt 有太多糾結的條件分支，或工具相似到改名稱與描述都無法避免選錯時，才拆成多個 agent；工具的相似度比數量重要 [S6]。
- run loop：agent 在迴圈中執行，直到結束條件，例如呼叫 final-output 工具、模型不再呼叫工具、發生錯誤、達到最大回合數 [S6]。
- Manager pattern：中央 manager 把專門 agent 當成工具呼叫，保有對話控制權並整合結果；例如一個 agent 協調多語翻譯 [S6]。
- Decentralized pattern：同層 agent 互相 handoff 控制權並傳遞對話狀態；例如分流 agent 把物流問題交給訂單管理 agent [S6]。
- Guardrails 要多層；超過重試上限、或要做敏感／不可逆／高成本動作前，交給人類 [S6]。

## 影響的頁面
[[agent]]、[[mas-architectures]]、[[when-to-use-mas]]、[[verification-and-evaluation]]、[[glossary]]
