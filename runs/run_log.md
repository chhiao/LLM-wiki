# Pipeline 執行紀錄（自動產生自 runs/run_log.jsonl）

| # | 時間 | graph | 回合 | 節點 | 結果 | 問題數 |
|---|---|---|---|---|---|---|
| 1 | 19:39:59 | v1 | 1 | L0-lint | ❌ FAIL | 4 |
| 2 | 19:39:59 | v1 | 1 | N1-query | ✅ PASS | 0 |
| 3 | 19:40:06 | v1 | 2 | L0-lint | ✅ PASS | 0 |
| 4 | 19:40:18 | v1 | 1 | G1-outline-gate | ✅ PASS | 0 |
| 5 | 19:41:02 | v1 | 1 | G2-content-gate | ❌ FAIL | 3 |
| 6 | 19:41:13 | v1 | 2 | G1-outline-gate | ✅ PASS | 0 |
| 7 | 19:41:13 | v1 | 2 | G2-content-gate | ✅ PASS | 0 |
| 8 | 19:42:08 | v1 | 1 | N4-render | ✅ PASS | 0 |
| 9 | 19:42:08 | v1 | 1 | G3-render-gate | ✅ PASS | 0 |
| 10 | 19:43:04 | v2 | 1 | G3-render-gate | ❌ FAIL | 22 |
| 11 | 19:43:18 | v2 | 3 | G2-content-gate | ✅ PASS | 0 |
| 12 | 19:43:18 | v2 | 2 | N4-render | ✅ PASS | 0 |
| 13 | 19:43:26 | v2 | 2 | G3-render-gate | ✅ PASS | 0 |
| 14 | 19:43:56 | v1 | 0 | G1-outline-gate | ✅ PASS | 0 |
| 15 | 19:43:56 | v2 | 0 | G1-outline-gate | ❌ FAIL | 3 |
| 16 | 19:44:02 | v2 | 1 | L0-lint | ✅ PASS | 0 |
| 17 | 19:44:02 | v2 | 1 | N1-query | ✅ PASS | 0 |
| 18 | 19:44:02 | v2 | 1 | G1-outline-gate | ✅ PASS | 0 |
| 19 | 19:44:02 | v2 | 1 | G2-content-gate | ✅ PASS | 0 |
| 20 | 19:44:02 | v2 | 1 | N4-render | ✅ PASS | 0 |
| 21 | 19:44:09 | v2 | 1 | G3-render-gate | ✅ PASS | 0 |
| 22 | 19:44:30 | v2 | 2 | N4-render | ✅ PASS | 0 |
| 23 | 19:44:38 | v2 | 2 | G3-render-gate | ✅ PASS | 0 |

## 失敗明細

### #1 L0-lint（graph v1, 回合 1）
- context-engineering: 事實句缺來源 → - 任務拆成「背景＋水管」與「小鳥」給兩個 subagent…
- context-engineering: 事實句缺來源 → - 一個做成瑪利歐風背景，另一個做出不像 Flappy Bi…
- failure-modes-mast: 事實句缺來源 → - 很多失敗來自系統設計；同一模型配更好的設計就能進步。…
- failure-modes-mast: 事實句缺來源 → - ChatDev 改善角色規格 → 成功率約 +9.4%；…

### #5 G2-content-gate（graph v1, 回合 1）
- s13: 數字 15.6% 在指定 Wiki 頁找不到（可能幻覺或寫錯）
- s15: 數字 50 在指定 Wiki 頁找不到（可能幻覺或寫錯）
- [內容] s04: 術語「Multi-Agent System」在定義前就被使用

### #10 G3-render-gate（graph v2, 回合 1）
- s01: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s02: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s02: 版面失衡，內容只占上方 39%
- s03: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s04: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s05: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s06: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s06: 版面失衡，內容只占上方 50%
- s07: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s08: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s09: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s10: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s11: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s11: 版面失衡，內容只占上方 39%
- s12: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s13: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s13: 版面失衡，內容只占上方 39%
- s14: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s15: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s15: 版面失衡，內容只占上方 58%
- s16: 導覽按鈕遮住頁尾（頁碼/Wiki 對照）
- s16: 版面失衡，內容只占上方 50%

### #15 G1-outline-gate（graph v2, 回合 0）
- [大綱] s04: 術語「Multi-Agent System」在定義前就被使用
- [大綱] s13: 預計使用的數字 15.6% 在指定 Wiki 頁找不到
- [大綱] s15: 預計使用的數字 50 在指定 Wiki 頁找不到