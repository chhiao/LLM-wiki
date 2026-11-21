# Raw 來源卡（immutable — 只新增不修改）

擷取日期：2026-11-21。以下為每篇來源的書目資訊與擷取筆記（重點以中文改寫，非原文複製）。

---
## S1 — Building Effective Agents
- 作者／單位：Anthropic（Erik Schluntz, Barry Zhang）
- 日期：2024-12
- URL：https://www.anthropic.com/engineering/building-effective-agents
- 類型：工程部落格（實務指南）
- 擷取筆記：workflow（預先寫好的程式路徑）vs agent（LLM 自己決定流程與工具）；兩者合稱 agentic systems。
  五種 workflow 模式：prompt chaining、routing、parallelization（sectioning / voting）、orchestrator-workers、evaluator-optimizer。
  建議先用最簡單的解法，只有在效果明顯提升時才增加複雜度；agent 要有停止條件（例如迭代上限）。
  核心原則：設計簡單、規劃步驟可見、仔細設計 agent 與工具之間的介面。

## S2 — How we built our multi-agent research system
- 作者／單位：Anthropic Engineering
- 日期：2025-06
- URL：https://www.anthropic.com/engineering/multi-agent-research-system
- 類型：工程部落格（實際系統案例）
- 擷取筆記：orchestrator-worker 架構，lead agent 規劃並平行派出 subagents；另有 CitationAgent 補引用。
  內部評測中多代理系統（Opus 4 lead + Sonnet 4 subagents）比單一 Opus 4 agent 高 90.2%。
  BrowseComp 上三個因素解釋 95% 表現差異，其中 token 用量單獨解釋 80%。
  agent 約用聊天的 4 倍 token，多代理約 15 倍；只適合高價值任務。
  不適合：需要共享 context、agent 間依賴多的任務（多數寫程式任務屬此類）。
  早期失敗：簡單問題派出幾十個 subagent、無止盡搜尋、互相干擾。
  評估：看結果不看步驟；約 20 個測試題就能起步；LLM-as-judge 用 rubric 評分；人工測試仍必要。
  平行化讓複雜查詢研究時間最多減少 90%。

## S3 — Don't Build Multi-Agents
- 作者／單位：Walden Yan, Cognition
- 日期：2025-06-12
- URL：https://cognition.com/blog/dont-build-multi-agents
- 類型：觀點文章（反方立場）
- 擷取筆記：主張多代理架構在正式環境很脆弱；關鍵是 context engineering。
  兩原則：(1) 共享 context，要分享完整軌跡而不是單一訊息；(2) 行動隱含決策，平行 agent 若假設衝突，結果就差。
  Flappy Bird 例子：兩個 subagent 分別做背景與小鳥，風格完全不搭。
  建議：單執行緒線性 agent；任務很長時加一個壓縮模型摘要歷史。
  Claude Code 的 subagent 只回答窄問題、不與主 agent 平行寫程式。

## S4 — Why Do Multi-Agent LLM Systems Fail?
- 作者：Mert Cemri, Melissa Z. Pan, Shuyi Yang 等 13 人（UC Berkeley 等）
- 日期：arXiv 2025-03-17 首版，v3 2025-10-26；NeurIPS 2025
- URL：https://arxiv.org/abs/2503.13657
- 類型：學術論文（實證研究）
- 擷取筆記：提出 MAST 失敗分類法：14 種失敗模式、3 大類——
  系統設計問題（約 44%）、agent 間不對齊（約 32%）、任務驗證（約 24%）。
  分析 7 個框架（MetaGPT、ChatDev、HyperAgent、AppWorld、AG2、Magentic-One、OpenManus）。
  人工標註一致性 κ = 0.88；失敗率約 41% 到 86.7%。
  常見模式：步驟重複 15.7%、推理與行動不一致 13.2%、不知道何時結束 12.4%、違反任務規格 11.8%。
  ChatDev 改善角色規格成功率提升約 9.4%；加入高層目標驗證最多 +15.6%。
  結論：很多失敗來自系統設計而非模型能力；驗證常只做表面檢查（例如能編譯）。

## S5 — LangGraph Multi-agent systems（官方文件）
- 單位：LangChain
- URL：https://docs.langchain.com/oss/python/multi-agent （舊版 https://langchain-ai.github.io/langgraph/concepts/multi_agent）
- 類型：框架官方文件
- 擷取筆記：拆成多 agent 的理由：單一 agent 工具太多選錯、context 太大、需要不同專長。
  架構：network、supervisor、supervisor（tool-calling）、hierarchical、custom workflow。
  handoff：一個 agent 把控制權交給另一個。
  溝通：共享完整 scratchpad（推理較好但成長快）vs 只分享最終結果（較精簡）。

## S6 — A practical guide to building agents
- 單位：OpenAI
- 日期：2025
- URL：https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- 類型：企業實務指南（PDF）
- 擷取筆記：agent = 代替使用者高度獨立完成多步驟任務的系統；三元件：model、tools、instructions。
  何時用 agent：需要細緻判斷、規則難維護、大量非結構化資料。
  先把單一 agent 用到極致；prompt 條件分支太多、或工具相似到選錯時才拆分。工具「相似度」比「數量」重要。
  run loop 結束條件：呼叫 final-output 工具、模型不再呼叫工具、錯誤、達最大回合數。
  manager pattern（agent 當工具）vs decentralized pattern（agent 間 handoff）。
  guardrails 要多層；高風險、不可逆動作前交給人類。
