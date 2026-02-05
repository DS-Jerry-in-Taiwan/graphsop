# Phase 04 - 開發流程：GraphRAG 整合

## 📅 執行步驟流程

### Step 1: 環境與工具準備 (@INFRA / @CODER)
1.  **依賴安裝**: 安裝 `llama-index-graph-stores-neo4j`, `langchain-openai`, `neo4j`。
2.  **DB 連線**: 設定 `.env` 中的 `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`。
3.  **Tool 封裝**: 將 Phase 04 (Mock) 的 `MockCamera` 類別加上 `@tool` 裝飾器或包裝為 `FunctionTool`，並撰寫詳細的 Docstring 供 LLM 理解工具用途。

### Step 2: 圖譜檢索器開發 (@CODER)
1.  **實作 Retriever**: 撰寫 Cypher 查詢邏輯。
    -   輸入: 實體名稱 (e.g., "休息室")
    -   查詢: 找尋該節點及其一跳 (1-hop) 內的 `Constraint` 或 `Property`。
    -   輸出: 結構化文本 (String) 作為 Context。

### Step 3: LangGraph Agent 組裝 (@ARCH / @CODER)
1.  **State 定義**: 在 `AgentState` 中增加 `context` (存檢索結果) 與 `messages` (存對話歷史)。
2.  **節點邏輯**:
    -   `Node: Retrieve`: 呼叫 Retriever 更新 State。
    -   `Node: Reason`: 將 `User Query + Context` 送入 LLM，決定下一步 (Call Tool 或 回絕)。
    -   `Node: Act`: 執行 Tool。
3.  **Prompt 設計**: 編寫 System Prompt，強制模型「依據 Context 判斷安全性」。

### Step 4: UI 串接與測試 (@CODER / @ANALYST)
1.  **Streamlit 整合**: 使用 `st.write_stream` 串接 LangGraph 的事件流。
2.  **【Checkpoint 4】RAG 驗證**:
    -   測試案例 A (未知指令): 輸入「啟動自毀模式」，確認系統去查圖譜並回覆「無此功能/未定義」。
    -   測試案例 B (違規指令): 輸入「轉向隱私區」，確認系統引用圖譜條款拒絕。

