---
title: S5 LangGraph Multi-agent systems（官方文件）
type: source
sources: [S5]
updated: 2026-11-21
---
# S5 — LangGraph Multi-agent systems（LangChain 官方文件）

## 先討論紀錄（Ingest #5）
**LLM 提出的 key takeaways**
1. 從「實作者」角度列出拆成多 agent 的三個理由。
2. 五種架構：network、supervisor、supervisor（tool-calling）、hierarchical、custom workflow。
3. handoff 是 agent 之間交接控制權的基本動作。
4. 溝通設計的取捨：共享完整 scratchpad vs 只分享結果。

**討論問題**：這篇是框架文件，會不會太偏實作？
**決定**：架構分類很適合畫成圖給新手看，保留；但不寫 API 細節（符合 schema 的範圍外規定）。
**要強調**：架構圖、「共享全部 vs 只傳結果」這個取捨正好連到 S3 的 context engineering。
**與現有 Wiki 關係**：讓 [[mas-architectures]] 從 S1 的一種模式擴充到完整分類。

## 摘要
- 當單一 agent 工具太多而選錯、context 大到難以管理、或系統需要不同專長時，可以拆成多個較小的 agent [S5]。
- 好處：模組化（好開發、測試、維護）、專業化、可明確控制 agent 之間如何溝通 [S5]。
- Network：任何 agent 都可以呼叫任何 agent，適合沒有明確階層或固定順序的問題 [S5]。
- Supervisor：中央 LLM 決定下一個交給哪個 worker；tool-calling 版本是把 worker 包成工具給 supervisor 呼叫 [S5]。
- Hierarchical：每個小隊有自己的 supervisor，再由最上層 supervisor 管理各小隊；適合單一 supervisor 負擔太重時 [S5]。
- Custom workflow：部分流程用固定的邊連接（最可預測），部分讓 LLM 動態決定下一步 [S5]。
- Handoff：一個 agent 把控制權交給另一個 agent，通常同時更新狀態並指定下一個 agent [S5]。
- 溝通取捨：共享完整 scratchpad 推理較好但成長很快；只分享最終結果較精簡，適合 agent 多或很複雜時 [S5]。

## 影響的頁面
[[mas-architectures]]、[[context-engineering]]、[[when-to-use-mas]]、[[glossary]]
