# Phase 03 - 驗證清單 (Validation Checklist)

## 邏輯架構 (Checkpoint 3)
- [ ] LangGraph 中是否明確包含 `Check_Safety` 節點？
- [ ] `Check_Safety` 節點是否連接到 `END` (若失敗) 與 `Execute` (若成功)？

## 功能測試
- [ ] **物理極限攔截**: 輸入「轉動 360 度」 -> 系統拒絕 (因為 Max_Pan=180)。
- [ ] **隱私區域攔截**: 輸入「看休息室」 -> 系統拒絕 (因為是 Privacy_Zone)。
- [ ] **合法路徑規劃**: 輸入「轉向大門」 -> 系統產出包含 `Unlock` -> `Rotate` -> `Zoom` 的步驟。
- [ ] **狀態機流轉**: 驗證從 Plan -> Check -> Execute 的狀態轉移日誌是否正確。

## 代碼品質
- [ ] `ConstraintEngine` 是否與具體的圖譜結構解耦 (通用性)？

