# Phase 03 - 開發目標：邏輯編排與安全攔截 (Logic Layer)

**專案名稱**: TwinLex (GraphSOP)
**階段**: Day 3 - 邏輯編排
**執行模式**: 混合模式 (Mixed Mode)

## 🎯 核心目的
構建數位孿生的「決策中樞」，利用 **LangGraph** 建立狀態機，將使用者意圖 (Intent) 轉化為合規的操作序列 (SOP)。並透過 **Constraint Engine** 在虛擬圖譜中預演路徑，攔截任何違反物理極限或安全規範的指令。

## 🚩 開發目標
1. **狀態機設計 (State Machine)**: 使用 LangGraph 定義 `Plan` -> `Check` -> `Execute` -> `Verify` 的控制流。
2. **約束檢查引擎 (Constraint Engine)**: 實作邏輯判斷模組，查詢 Graph DB 中的 `Constraint` 節點，驗證意圖的合法性。
3. **路徑規劃 (SOP Path Finding)**: 根據意圖在圖譜中尋找從「當前狀態」到「目標狀態」的最短合規路徑。
4. **安全攔截 (Guardrails)**: 確保當使用者指令涉及禁區（如 Privacy_Zone）時，系統能主動拒絕並說明原因。

## 📦 預期產出物
* **LangGraph Workflow**: `src/logic/workflow.py` (包含 StateGraph 定義)。
* **Constraint Checker**: `src/logic/guardrails.py`。
* **SOP Planner**: `src/logic/planner.py`。
* **安全性測試報告**: 驗證攔截成功率的測試結果。

## ✅ 驗收標準 (Definition of Done)
* **攔截率 100%**: 所有指向 `Privacy_Zone` 或超過 `Max_Pan_Angle` 的指令，必須被拒絕。
* **流程閉環**: 合法指令必須能產出完整的 SOP 步驟序列。
* **死鎖預防**: 狀態機在遇到錯誤時必須能優雅地轉移到 `Error` 狀態並回饋訊息。

