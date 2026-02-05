# Phase 01 - 驗證清單 (Validation Checklist)

## 數據品質驗證
- [ ] `mock_manual.md` 是否包含至少 3 個具體的物理限制？
- [ ] `mock_manual.md` 是否包含至少 2 條完整的 SOP 流程？

## Schema 邏輯驗證 (Checkpoint 1 重點)
- [ ] 是否有 `Constraint` (約束) 類型的節點定義？
- [ ] 是否有 `Validation_Metric` (驗證指標) 類型的節點定義？
- [ ] 關係定義是否包含方向性 (如: `Action` -> `Constraint`)？

## 圖譜構建驗證
- [ ] 提取腳本執行後，Neo4j/Graph Store 中是否有數據？
- [ ] 檢查「攝影機」節點，是否有 `Max_Pan` 屬性？
- [ ] 檢查「休息室」節點，是否被標記為 `Privacy_Zone`？
- [ ] 是否無孤立節點 (Orphan Nodes)？

