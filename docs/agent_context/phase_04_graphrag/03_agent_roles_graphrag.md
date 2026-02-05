# Phase 04 - Agent 角色職責 (GraphRAG 版)

## 🏗️ @ARCH (架構師)
* **職責**: 設計 RAG Agent 的決策流程與 System Prompt。
* **輸入**: Phase 03 的邏輯規則、Phase 02 的 Intent Schema。
* **輸出**: `agent_architecture.md` (定義 StateGraph 結構), System Prompt 模板。
* **關鍵任務**: 確保 Prompt 能有效利用檢索到的 Context，避免 LLM 產生幻覺或忽略約束。

## 💻 @CODER (開發者)
* **職責**: 實作 Retriever、Tool Wrapper 與 LangGraph 代碼。
* **輸入**: 架構設計、Neo4j 連線資訊。
* **輸出**: `graph_retriever.py`, `graph_agent.py`, `app_rag.py`。
* **關鍵任務**:
    1. 撰寫高效的 Cypher 查詢 (避免全圖掃描)。
    2. 處理 Streamlit 的異步/串流顯示，確保 UI 不會卡住。

## 🧪 @ANALYST (測試員)
* **職責**: 驗證 RAG 的準確性與安全性。
* **輸入**: 運行中的 Streamlit App。
* **輸出**: RAG 整合測試報告。
* **關鍵任務**: 檢查 Log，確認每一條指令背後都有「檢索 -> 思考 -> 執行」的完整軌跡，而非瞎矇。

## 🔧 @INFRA (運維)
* **職責**: 管理 Graph DB 與 LLM 連線。
* **任務**: 
    1. 確保 Neo4j 服務正常且 Phase 01 的數據存在。
    2. 管理 OpenAI API Key 的 Quota。

