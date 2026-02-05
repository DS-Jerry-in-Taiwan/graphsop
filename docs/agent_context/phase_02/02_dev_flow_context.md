# Phase 02 - 開發流程：意圖解析

## 📅 執行步驟流程

### Step 1: 意圖 Schema 設計 (@ARCH)
1. **分析圖譜**: 讀取 Phase 01 產出的 `ontology.json`。
2. **定義模型**: 設計 `CameraIntent`, `QueryIntent` 等 Pydantic 類別。
3. **【Checkpoint 2】Schema 審查**: 確保 Intent 定義涵蓋所有圖譜支援的操作（如 Pan, Tilt, Zoom）。

### Step 2: 語義路由實作 (@CODER)
1. **Router 開發**: 使用 LLM 或向量相似度判斷使用者意圖類型。
2. **提取器開發**: 撰寫 Prompt 讓 LLM 輸出符合 Pydantic 格式的 JSON。

### Step 3: 圖譜實體對齊 (@CODER)
1. **檢索邏輯**: 實作 `EntityResolver`，當 LLM 提取出 "大門" 時，去 Graph DB 搜尋 `label=Location` 且 `name~="大門"` 的節點。
2. **消歧義**: 若找到多個節點（如：前門、後門），設計「回頭詢問」的邏輯。

### Step 4: 整合測試 (@ANALYST)
1. **測試案例**: 準備 10 句測試語料（包含別名、錯別字）。
2. **驗證**: 執行 Pipeline，檢查輸出是否正確對應到圖譜節點 ID。

