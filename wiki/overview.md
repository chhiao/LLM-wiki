---
title: 總覽：Multi-Agent 系統入門
type: overview
sources: [S1, S2, S3, S4, S5, S6]
updated: 2026-11-21
---
# 總覽：Multi-Agent 系統入門

**一句話**：多代理系統（MAS）是讓多個 LLM agent 分工合作的設計；它能處理單一 agent 放不下、需要平行的任務，但成本高、容易失敗，所以應該「先單一、後多個」。

## 學習路線
1. 先懂單一 agent：[[agent]] → [[workflow-vs-agent]]
2. 為什麼要組隊：[[multi-agent-system]]
3. 怎麼組隊：[[mas-architectures]]
4. 組隊最難的地方：[[context-engineering]]
5. 正反觀點：[[single-vs-multi-agent]]
6. 代價：[[cost-and-tradeoffs]]
7. 會怎麼失敗、怎麼檢查：[[failure-modes-mast]] → [[verification-and-evaluation]]
8. 實務決策：[[when-to-use-mas]]

## 五個最重要的事實
1. agent = model + tools + instructions，在 loop 裡跑到結束條件 [S6]。
2. Anthropic 的多代理研究系統在內部評測比單一 agent 高 90.2%，但約用 15 倍 token [S2]。
3. Cognition 主張不要做多代理，因為平行 agent 的隱含假設會衝突（Flappy Bird 例子）[S3]。
4. 學術研究找出 14 種 MAS 失敗模式，最大類是系統設計問題（約 44%）[S4]。
5. 常見架構：supervisor / manager（中央指揮）與 handoff / decentralized（交接）[S5][S6]。

## 來源
見 [[index]] 的 Sources 區。
