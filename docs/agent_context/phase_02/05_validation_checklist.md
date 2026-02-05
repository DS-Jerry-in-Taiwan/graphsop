# Phase 02 - 驗證清單 (Validation Checklist)

## Schema 邏輯 (Checkpoint 2)
- [ ] `Intent` 模型中的 Action Enum 是否包含 `ROTATE`, `ZOOM`？
- [ ] 是否包含 `target_id` 欄位用於儲存圖譜節點 ID？

## 功能測試
- [ ] **路由測試**: 輸入「這台攝影機多重？」應分類為 `QUERY`。
- [ ] **路由測試**: 輸入「轉向大門」應分類為 `CONTROL`。
- [ ] **提取測試**: 輸入「向左轉 30 度」應提取出 `{"direction": "LEFT", "angle": 30}`。
- [ ] **實體對齊測試**: 輸入「轉向休息室」應成功關聯到 `Privacy_Zone` 的節點 ID。

## 異常處理
- [ ] 輸入未知地點（如「轉向月球」），Resolver 應回傳 None 或提示錯誤。

