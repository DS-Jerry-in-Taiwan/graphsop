# Phase 01 - Agent 角色職責

## 🏗️ @ARCH (架構師)
* **職責**: 定義「數位孿生」的邏輯骨架 (Ontology)。
* **輸入**: 需求文檔、設備功能描述。
* **輸出**: `schema_definition.json` (定義節點與邊的規範)。
* **關鍵任務**: 確保 Schema 能表達「物理極限」與「邏輯順序」。

## 💻 @CODER (開發者)
* **職責**: 實作圖譜提取 Pipeline 與數據生成。
* **輸入**: `schema_definition.json`、虛擬手冊文本。
* **輸出**: `extract_graph.py`、`mock_manual.md`。
* **關鍵任務**: 使用 LlamaIndex 將非結構化文本精確轉化為結構化圖譜數據。

## 🧪 @ANALYST (測試員)
* **職責**: 驗證圖譜的邏輯正確性。
* **輸入**: 已構建的 Graph DB。
* **輸出**: `graph_validation_report.md`。
* **關鍵任務**: 檢查「禁止進入區域」是否正確關聯到「移動指令」上。

## 🔧 @INFRA (運維)
* **職責**: 準備 GraphRAG 運行環境。
* **輸入**: 環境需求。
* **輸出**: `docker-compose.yml` (Neo4j) 或本地環境配置腳本。

