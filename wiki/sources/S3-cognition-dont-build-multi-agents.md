---
title: S3 Don't Build Multi-Agents（Cognition）
type: source
sources: [S3]
updated: 2026-11-21
---
# S3 — Don't Build Multi-Agents（Walden Yan, Cognition, 2025-06-12）

## 先討論紀錄（Ingest #3）
**LLM 提出的 key takeaways**
1. 反方立場：多代理在正式環境很脆弱。
2. 核心概念是 context engineering：決定系統每個部分「看得到什麼資訊」。
3. 兩原則：共享 context、行動隱含決策。
4. Flappy Bird 例子非常適合教學。

**討論問題**：S2 說 MAS 好、S3 說不要做，這是矛盾嗎？
**決定**：不是真正矛盾，而是「任務類型不同」——S2 是可平行的研究任務，S3 關注高度依賴的寫程式任務；S2 自己也承認寫程式不適合 MAS。在 [[single-vs-multi-agent]] 比較頁明確寫出這個調和。
**要強調**：Flappy Bird 例子（新手一看就懂）、「共享 context」原則。
**與現有 Wiki 關係**：與 S2 形成正反對照；新增 [[context-engineering]] 概念頁。

## 摘要
- 作者認為多個 agent 分工協作的架構在正式環境很脆弱，並點名 OpenAI Swarm、Microsoft AutoGen 推廣的方向 [S3]。
- 可靠的長時間 agent 靠的是 context engineering，也就是刻意管理每個部分能看到的資訊 [S3]。
- 原則一「共享 context」：subagent 不只需要原始任務，還需要前面的對話、工具呼叫與推理；應分享完整軌跡 [S3]。
- 原則二「行動隱含決策」：每個行動背後都有假設；平行 agent 若假設衝突，合起來的結果就會不一致 [S3]。
- Flappy Bird 例子：把任務拆成「背景與水管」和「小鳥」兩個 subagent，一個做成瑪利歐風背景，一個做出不像 Flappy Bird 的鳥，最後的 agent 拿到兩塊拼不起來的成果 [S3]。
- 建議架構：單執行緒線性 agent；任務很長時加一個壓縮模型，把歷史濃縮成關鍵細節與決策 [S3]。
- 例子：Claude Code（2025 年 6 月時）的 subagent 只回答窄問題、不和主 agent 平行寫程式，好處是調查過程不會塞滿主 agent 的 context [S3]。

## 影響的頁面
[[context-engineering]]、[[single-vs-multi-agent]]、[[when-to-use-mas]]、[[glossary]]
