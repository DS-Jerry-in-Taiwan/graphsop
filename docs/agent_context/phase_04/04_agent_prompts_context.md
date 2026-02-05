# Phase 04 - Agent Prompts

## 1. Mock Hardware 生成 Prompt (@CODER)
```text
請依據 `DeviceInterface` 實作一個 `MockCamera` 類別。
功能需求：
1. **Stateful**: 內部需維護 `pan`, `tilt`, `zoom`, `power` 等變數。
2. **Methods**: 實作 `rotate(pan, tilt)`, `zoom(level)`。
3. **Simulation**: 加入 5% 的機率模擬「執行失敗」(return success=False)。
4. **Telemetry**: `get_status()` 需回傳當前所有狀態。

```

## 2. Streamlit UI 生成 Prompt (@CODER)

```text
請撰寫一個 Streamlit App (`app.py`) 作為 TwinLex 的控制台。
介面佈局：
- **左側邊欄**: 顯示 Mock Camera 的即時遙測數據 (Pan/Tilt/Zoom 值)，需每秒自動更新。
- **主畫面**: 聊天視窗 (Chat Interface)。
- **邏輯展示**: 在對話泡泡下方，使用 `st.expander` 顯示 LangGraph 的思考過程 (Plan -> Check -> Execute)。

串接邏輯：
- 使用 `workflow.stream(user_input)` 獲取回應。
- 實時渲染 Agent 的中間步驟。

```

## 3. Verifier 邏輯 Prompt (@CODER)

```text
請實作 `verify_execution(expected_state, actual_state)` 函數。
邏輯：
1. 比對 `expected_state` (來自 SOP) 與 `actual_state` (來自 Mock Device)。
2. 允許 5% 的數值容差 (Tolerance)。
3. 若超出容差，拋出 `VerificationError`。

```

