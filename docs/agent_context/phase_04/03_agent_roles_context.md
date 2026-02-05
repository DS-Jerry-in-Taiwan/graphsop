# Phase 04 - Agent 角色職責

## 🏗️ @ARCH (架構師)
* **職責**: 定義前後端介面與硬體抽象層 (HAL)。
* **輸入**: Phase 03 的 Workflow 輸出格式。
* **輸出**: `hardware_interface.py`。
* **關鍵任務**: 確保 UI 與邏輯層解耦，硬體實作可隨時替換 (Mock vs Real)。

## 💻 @CODER (開發者)
* **職責**: 實作 Mock Hardware、Verifier 與 Streamlit UI。
* **輸入**: 硬體介面定義、LangGraph 實例。
* **輸出**: `mock_camera.py`, `app.py`。
* **關鍵任務**: 處理 LangGraph 的串流輸出 (Streaming Output)，讓 UI 像打字機一樣顯示思考過程。

## 🧪 @ANALYST (測試員)
* **職責**: 進行端到端 (E2E) 測試。
* **輸入**: 完整的 Streamlit App。
* **輸出**: 整合測試報告。
* **關鍵任務**: 模擬「硬體執行成功但驗證失敗」的邊界情況 (例如：指令成功發送，但鏡頭沒轉到位)。

## 🔧 @INFRA (運維)
* **職責**: 準備 UI 運行環境。
* **任務**: 安裝 `streamlit`, `watchdog` 等依賴。

