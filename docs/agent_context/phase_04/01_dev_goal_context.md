# Phase 04 - 開發目標：虛擬執行與驗證回饋 (Execution & UI Layer)

**專案名稱**: TwinLex (GraphSOP)
**階段**: Day 4 - 執行與驗證
**執行模式**: 混合模式 (Mixed Mode)

## 🎯 核心目的
建立系統的「虛擬硬體層 (Mock Hardware)」與「互動介面 (UI)」。透過 **Streamlit** 可視化展示 LangGraph 的決策過程，並利用 **Mock Device** 模擬物理執行結果，最終透過 **Verifier** 模組比對「預期結果 (SOP)」與「實際遙測 (Telemetry)」，達成閉環控制。

## 🚩 開發目標
1. **虛擬設備 (Mock Device)**: 實作具備狀態記憶 (Stateful) 的攝影機模擬器，能回應 API 呼叫並更新自身屬性 (Pan, Tilt, Zoom)。
2. **驗證引擎 (Verification Engine)**: 開發比對邏輯，確認執行後的設備狀態是否符合 SOP 中的 `Standard` (驗證標準)。
3. **可視化儀表板 (UI)**: 使用 Streamlit 開發操作介面，即時顯示對話窗、圖譜路徑、以及設備當前狀態。
4. **整合測試 (Integration)**: 串接 NLU -> Logic -> Mock Device -> UI 的完整流程。

## 📦 預期產出物
* **Mock API**: `src/hardware/mock_camera.py` (模擬硬體行為)。
* **Verifier Module**: `src/logic/verifier.py` (執行後驗證)。
* **Frontend App**: `src/ui/app.py` (Streamlit 主程式)。
* **整合測試報告**: 驗證端到端 (End-to-End) 流程的成功率。

## ✅ 驗收標準 (Definition of Done)
* **狀態同步**: 當 UI 發送 "Rotate 30 deg"，Mock Device 的內部狀態必須更新為 30。
* **閉環驗證**: 若模擬硬體故障 (如：馬達卡住)，UI 必須顯示「驗證失敗」警告。
* **可視化完整**: 使用者能看見 AI 規劃的 SOP 步驟清單。

