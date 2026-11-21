---
title: S4 Why Do Multi-Agent LLM Systems Fail?（Cemri et al.）
type: source
sources: [S4]
updated: 2026-11-21
---
# S4 — Why Do Multi-Agent LLM Systems Fail?（Cemri et al., arXiv 2503.13657 / NeurIPS 2025）

## 先討論紀錄（Ingest #4）
**LLM 提出的 key takeaways**
1. 這是唯一一篇有系統性實證資料的來源：7 個框架、1600+ 條執行軌跡。
2. MAST：14 種失敗模式分成 3 大類。
3. 最大類是「系統設計問題」——代表很多失敗可以靠設計修正，不完全是模型不夠強。
4. 驗證常只做表面檢查。

**討論問題**：14 種模式全放進簡報會不會太多？
**決定**：簡報只放 3 大類 + 各類最常見的 1–2 種；完整 14 種留在 Wiki 的 [[failure-modes-mast]]。
**要強調**：「失敗率 41%–86.7%」與「驗證要檢查高層目標」，這也會反過來影響我們自己的簡報產生流程設計（加入多層檢查）。
**與現有 Wiki 關係**：補上 S2 的「早期失敗」案例的系統性版本；新增 [[failure-modes-mast]]。

## 摘要
- 雖然大家對多代理系統很熱衷，但它在常見 benchmark 上相對單一 agent 的進步常常很小 [S4]。
- 作者把 agent 定義為具備三部分的實體：prompt 規格（初始狀態）、對話軌跡（狀態）、與環境互動的能力如工具（行動）；MAS 是透過協調互動的一群 agent [S4]。
- 分析 7 個框架：MetaGPT、ChatDev、HyperAgent、AppWorld、AG2、Magentic-One、OpenManus；人工標註一致性 κ = 0.88 [S4]。
- 失敗率約 41% 到 86.7% [S4]。
- MAST 三大類：系統設計問題（約 44%）、agent 間不對齊（約 32%）、任務驗證（約 24%）[S4]。
- 最常見模式：步驟重複 15.7%、推理與行動不一致 13.2%、不知道終止條件 12.4%、違反任務規格 11.8% [S4]。
- 介入實驗：ChatDev 改善角色規格，成功率提升約 9.4%；加入高層目標驗證最多 +15.6% [S4]。
- 結論：許多失敗反映的是系統設計，同一個模型配上更好的設計就能改善；驗證常只做「能不能編譯」這類表面檢查，應做多層、檢查高層目標的驗證 [S4]。

## 影響的頁面
[[failure-modes-mast]]、[[verification-and-evaluation]]、[[multi-agent-system]]、[[glossary]]
