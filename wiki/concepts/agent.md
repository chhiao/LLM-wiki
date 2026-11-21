---
title: Agent（代理）
type: concept
sources: [S1, S4, S6]
updated: 2026-11-21
---
# Agent（代理）

## 定義
- agent 是高度獨立、代替使用者完成多步驟任務的系統，由 LLM 主導流程並使用工具 [S6]。
- Anthropic 的說法：agent 讓 LLM 自己決定流程與工具使用，與路徑寫死的 workflow 不同 [S1]。見 [[workflow-vs-agent]]。
- 學術定義（MAST 論文）：agent 有三部分——prompt 規格（初始狀態）、對話軌跡（狀態）、與環境互動的能力（行動）[S4]。

## 三個核心元件 [S6]
| 元件 | 做什麼 | 生活類比 [推論] |
|---|---|---|
| Model | 推理與做決定 | 大腦 |
| Tools | 對外行動（查資料、呼叫 API） | 手腳 |
| Instructions | 設定行為與界線 | 工作手冊 |

## Agent 怎麼運作：run loop
- agent 在迴圈中執行：思考 → 呼叫工具 → 看結果 → 再思考，直到結束條件 [S6]。
- 結束條件例如：呼叫 final-output 工具、模型不再呼叫工具、發生錯誤、達最大回合數 [S6]。
- 每一步都從環境取得「ground truth」（工具結果、程式執行結果）來判斷進度，並應設停止條件如迭代上限 [S1]。
- 沒設好結束條件是多代理系統常見失敗之一（不知道終止條件 12.4%）[S4]，見 [[failure-modes-mast]]。

## 什麼不算 agent
- 單輪 LLM 呼叫、簡單聊天機器人、情緒分類器不算 agent [S6]。

相關：[[multi-agent-system]]、[[glossary]]
