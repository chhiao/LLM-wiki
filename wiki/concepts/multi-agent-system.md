---
title: Multi-Agent System（多代理系統, MAS）
type: concept
sources: [S2, S4, S5]
updated: 2026-11-21
---
# Multi-Agent System（多代理系統, MAS）

## 定義
- MAS 是一群透過協調（orchestration）互動、合作完成任務的 agent [S4]。
- 實作上常把每個 agent 當成圖（graph）上的一個節點，節點之間可以交接控制權（handoff）[S5]。
- 生活類比：一個專案小組，有組長分工、組員各自負責一塊，最後由組長整合 [推論]。

## 為什麼要多個 agent？
單一 agent 遇到以下狀況時，可以考慮拆分 [S5]：
1. 工具太多，常常選錯工具。
2. context 大到難以管理。
3. 需要不同的專長（例如規劃、搜尋、寫作）。

多代理的額外好處：每個 subagent 有獨立的 context window，可以同時探索不同方向，再把結果濃縮交回 [S2]。

## 但是：多代理不一定比較好
- MAS 在常見 benchmark 上相對單一 agent 的進步常常很小 [S4]。
- 七個框架的失敗率約 41% 到 86.7% [S4]。
- 正反觀點整理見 [[single-vs-multi-agent]]，失敗原因見 [[failure-modes-mast]]。

相關：[[agent]]、[[mas-architectures]]、[[context-engineering]]
