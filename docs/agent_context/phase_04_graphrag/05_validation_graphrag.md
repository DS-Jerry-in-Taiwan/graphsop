# Phase 04 - 驗證清單 (GraphRAG 版)

## 基礎建設驗證
- [ ] `requirements.txt` 包含 `neo4j`, `langgraph`, `llama-index`。
- [ ] `.env` 檔案設定正確，且能成功連線 Neo4j。

## RAG 功能驗證 (Checkpoint 4 重點)
- [ ] **檢索測試**: 呼叫 `retrieve_constraints("休息室")`，能回傳包含 "Privacy_Zone" 的文字描述。
- [ ] **Prompt 注入測試**: 檢查 Log，確認 System Prompt 中的 `{graph_context}` 確實被替換為檢索內容。
- [ ] **工具調用測試**: 當 LLM 決定執行時，Mock Camera 的數值確實改變。

## 端到端場景驗證
- [ ] **場景 A (合規)**: 輸入「轉向大門」 -> 檢索大門資訊 -> 無約束 -> 執行 Tool -> 回覆成功。
- [ ] **場景 B (違規)**: 輸入「轉向休息室」 -> 檢索休息室資訊 -> 發現 Privacy 約束 -> **LLM 決定不呼叫 Tool** -> 回覆拒絕原因。
- [ ] **場景 C (幻覺防護)**: 輸入圖譜中不存在的地點 -> 檢索回傳空 -> LLM 回覆「找不到該地點」。

