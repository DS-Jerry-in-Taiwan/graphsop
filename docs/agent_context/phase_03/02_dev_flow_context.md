# Phase 03 - 開發流程：邏輯編排

## 📅 執行步驟流程

### Step 1: 狀態機架構設計 (@ARCH)
1. **定義 State**: 設計 `AgentState` (包含 `input_intent`, `plan`, `safety_status`, `error`)。
2. **定義 Graph**: 繪製 LangGraph 流程圖，確定節點間的條件邊 (Conditional Edges)。
3. **【Checkpoint 3】邏輯審查**: 確認狀態機是否具備「檢查 (Check)」節點，且位於「執行 (Execute)」之前。

### Step 2: 約束引擎實作 (@CODER)
1. **規則檢索**: 開發從 Neo4j 查詢 `Constraint` 節點的函數。
2. **判斷邏輯**: 實作 `check_safety(intent, constraints)` 函數，比對參數是否越界。

### Step 3: SOP 路徑規劃實作 (@CODER)
1. **路徑搜尋**: 利用 Graph DB 的路徑演算法 (ShortestPath)，找出完成意圖所需的操作步驟。
2. **序列生成**: 將路徑轉化為可執行的 JSON 列表。

### Step 4: 安全性與壓力測試 (@ANALYST)
1. **紅隊演練 (Red Teaming)**: 故意輸入違規指令（如：轉向隱私區、轉動 400 度）。
2. **驗證攔截**: 確認系統是否回傳明確的拒絕訊息（如：「依據安全手冊第 3 條，禁止拍攝休息室」）。

