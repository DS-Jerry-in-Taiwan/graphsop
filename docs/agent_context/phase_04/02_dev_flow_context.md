# Phase 04 - 開發流程：執行與驗證

## 📅 執行步驟流程

### Step 1: 硬體介面定義 (@ARCH)
1. **介面設計**: 定義 `DeviceInterface` 抽象類別 (Abstract Base Class)，規範 `rotate()`, `zoom()`, `get_status()` 等方法。
2. **驗證標準定義**: 確定 Verifier 如何讀取 SOP 中的 `Verification_Metric` 節點。

### Step 2: 虛擬硬體實作 (@CODER)
1. **Mock 開發**: 實作 `MockCamera` 類別，包含隨機延遲與模擬誤差 (Simulated Error) 功能。
2. **API 封裝**: 將 Mock 類別封裝為 Tool，供 LangGraph 調用。

### Step 3: 驗證邏輯開發 (@CODER)
1. **Verifier 實作**: 撰寫邏輯：執行動作後 -> 讀取 Mock 狀態 -> 比對 SOP 預期值 -> 回傳 Pass/Fail。

### Step 4: UI 整合與測試 (@CODER / @ANALYST)
1. **Streamlit 開發**: 建立 Chat Interface，串接 LangGraph 的 `stream()` 輸出。
2. **【Checkpoint 4】整合審查**: 確認 UI 操作流暢度，以及「錯誤攔截」是否能正確顯示在前端。

### Step 5: 錄製 Demo (@ALL)
1. **案例演示**: 錄製「成功操作」、「安全攔截」、「硬體故障」三種情境。

