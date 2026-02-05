# Phase 04 - 驗證清單 (Validation Checklist)

## 硬體模擬
- [ ] Mock Camera 能正確更新狀態 (Pan 從 0 變 30)。
- [ ] `get_status()` 能回傳正確的 JSON 格式遙測數據。

## UI 功能 (Checkpoint 4)
- [ ] Streamlit App 能成功啟動並載入 LangGraph。
- [ ] 聊天視窗能正常發送指令並接收回應。
- [ ] 側邊欄能即時顯示設備狀態變化。

## 閉環邏輯
- [ ] **成功案例**: 發送指令 -> 設備轉動 -> UI 顯示「執行成功」。
- [ ] **失敗案例**: 發送違規指令 -> 邏輯攔截 -> UI 顯示「拒絕執行」。
- [ ] **故障案例**: 模擬 Mock 故障 -> Verifier 報錯 -> UI 顯示「驗證失敗」。

