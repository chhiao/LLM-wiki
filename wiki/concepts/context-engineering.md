---
title: Context Engineering
type: concept
sources: [S2, S3, S5]
updated: 2026-11-21
---
# Context Engineering

## 定義
- 刻意管理「系統的每個部分能看到哪些資訊」；Cognition 認為這是打造可靠 agent 的核心工作 [S3]。
- context window：模型一次能讀進的內容量；Anthropic 的 lead agent 會把計畫存到外部記憶，因為超過約 200,000 tokens 的內容會被截斷 [S2]。

## 兩個原則 [S3]
1. **共享 context**：subagent 需要的不只是任務描述，還有前面的對話、工具呼叫與推理。
2. **行動隱含決策**：每個行動都帶著假設，平行 agent 的假設衝突時，結果會不一致。

## 經典例子：Flappy Bird [S3]
- 任務拆成「背景＋水管」與「小鳥」給兩個 subagent [S3]。
- 一個做成瑪利歐風背景，另一個做出不像 Flappy Bird 的鳥 → 最後拼不起來 [S3]。
- 教訓：只把「任務描述」交出去，不夠 [S3]。

## 設計取捨
| 做法 | 優點 | 缺點 |
|---|---|---|
| 共享完整 scratchpad | 推理較好 [S5] | 成長很快 [S5] |
| 只分享最終結果 | 精簡，適合 agent 多時 [S5] | 可能遺失決策脈絡 [推論] |
| 壓縮模型摘要歷史 | 延長可執行長度 [S3] | 難做，只是把上限往後推 [S3] |
| subagent 只回答窄問題 | 調查過程不塞滿主 agent [S3] | 不能平行寫程式 [S3] |
| 把結果存檔、只回傳參照 | 減少資訊遺失與 token [S2] | 需要檔案系統 [推論] |

相關：[[single-vs-multi-agent]]、[[mas-architectures]]
