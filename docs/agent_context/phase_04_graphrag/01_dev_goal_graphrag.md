# Phase 04 - 開發目標：GraphRAG 真實整合與執行

**專案名稱**: TwinLex (GraphSOP)
**階段**: Day 4 - GraphRAG Integration
**分支**: feature/phase04-graphrag-integration
**執行模式**: 混合模式 (Mixed Mode)

## 🎯 核心目的
將前端 UI 與虛擬硬體，與 **Phase 01-03 建立的 GraphRAG 大腦** 進行真實對接。
**嚴禁使用 Hard-coded (寫死) 的邏輯判斷**。
1.  **意圖解析**：必須經過 LLM (OpenAI/LlamaIndex) 處理。
2.  **安全檢查**：必須動態執行 Cypher 查詢 Neo4j，提取關聯的 `Constraint` 節點。
3.  **決策制定**：Agent 必須根據檢索到的「圖譜上下文 (Graph Context)」來決定是否放行操作。

## 🚩 開發目標
1.  **Graph Retriever 實作**: 開發能根據 User Entity (如 "大門") 動態檢索 Neo4j 子圖的模組。
2.  **LangGraph Agent 迴路**: 構建 `Reasoning Loop` (Retrieve -> Think -> Act)，取代簡單的線性腳本。
3.  **Tool 封裝**: 將 `MockCamera` 封裝為標準 LangChain/LlamaIndex Tool，供 LLM 自主調用。
4.  **可解釋性 UI**: Streamlit 介面必須顯示「檢索到的知識」與「AI 的思考鏈 (Chain of Thought)」。

## 📦 預期產出物
* **Retriever**: `src/rag/graph_retriever.py` (負責 Cypher 查詢)。
* **Agent Core**: `src/agent/graph_agent.py` (LangGraph 狀態機)。
* **Streamlit App**: `src/ui/app_rag.py` (支援串流輸出的前端)。
* **Requirements**: 更新後的 `requirements.txt` (包含 neo4j, llama-index 等)。

## ✅ 驗收標準 (Definition of Done)
* **真實查詢**: Log 中必須看見真實的 Cypher 語句被發送至 Neo4j。
* **上下文注入**: 在 LLM 的 Prompt Log 中，必須看見來自圖譜的 `Constraint` 描述（如：「禁止拍攝休息室」）。
* **動態攔截**: 若在 Neo4j 中手動修改某區域為 `Privacy_Zone`，Agent 需在不改代碼的情況下立即攔截相關指令。

