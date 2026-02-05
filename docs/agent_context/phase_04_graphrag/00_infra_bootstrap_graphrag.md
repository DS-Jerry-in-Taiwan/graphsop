# Phase 04 基礎建設引導：環境與數據初始化 (Infra Bootstrap)

**檔案路徑**: `docs/agent_context/phase_04_graphrag/00_infra_bootstrap_graphrag.md`
**專案名稱**: TwinLex (GraphSOP)
**當前分支**: feature/phase04-infra-setup
**執行模式**: 基礎建設模式 (Infra Mode)
**負責角色**: @INFRA (配置), @CODER (數據腳本)

## 🎯 任務目標
在進入 RAG 邏輯開發前，建立一個**立即可用**的 Neo4j 運行環境與測試數據集。
目標是讓開發者只需執行 `docker-compose up` 與 `python scripts/seed_graph.py`，即可完成所有準備。

## 📋 待辦事項清單 (To-Do List)

### 1. 容器化環境 (Docker Setup)
- [ ] **產出檔案**: `docker-compose.yml` (置於專案根目錄)
- **配置規格**:
  - Service: `neo4j`
  - Image: `neo4j:5.15-community`
  - Ports: `7474:7474` (HTTP), `7687:7687` (Bolt)
  - Env: `NEO4J_AUTH=${NEO4J_USER}/${NEO4J_PASSWORD}`
  - Volumes: `./neo4j_data:/data` (確保資料持久化)

### 2. 環境變數管理
- [ ] **產出檔案**: `.env.example`
- **必要變數**:
  ```ini
  # OpenAI
  OPENAI_API_KEY=sk-proj-xxxx
  
  # Neo4j
  NEO4J_URI=bolt://localhost:7687
  NEO4J_USER=neo4j
  NEO4J_PASSWORD=password

```

* [ ] **產出檔案**: `.gitignore` (務必排除 `.env` 與 `neo4j_data/`)

### 3. Python 依賴清單

* [ ] **產出檔案**: `requirements_graphrag.txt`
* **核心套件**:
* `python-dotenv`
* `neo4j`
* `langchain`
* `langchain-openai`
* `langchain-community`
* `llama-index`
* `llama-index-graph-stores-neo4j`



### 4. 數據注入腳本 (Data Seeding)

* [ ] **產出檔案**: `scripts/seed_graph.py`
* **邏輯要求**:
1. 連接 Neo4j。
2. **清除舊資料**: `MATCH (n) DETACH DELETE n` (確保每次執行都是乾淨的)。
3. **寫入測試圖譜 (TwinLex Demo Data)**:
* **Device**: `TwinLex-S2026` (屬性: max_pan: 180, max_tilt: 90)
* **Location**: `大門` (Public), `員工休息室` (Private)
* **Zone**: `Privacy_Zone_B`
* **Constraint**: `禁止拍攝員工隱私區域` (Level: High)


4. **建立關係**:
* `(員工休息室)-[:RESTRICTED_BY]->(Privacy_Zone_B)`
* `(Privacy_Zone_B)-[:HAS_CONSTRAINT]->(Constraint)`
* `(Device)-[:LOCATED_AT]->(大門)`





### 5. 環境驗證腳本

* [ ] **產出檔案**: `scripts/verify_setup.py`
* **檢查項目**:
1. `.env` 檔案存在性。
2. Neo4j 連線測試 (查詢節點數)。
3. OpenAI API Key 格式檢查。



## ✅ 驗收標準 (Definition of Done)

1. `docker-compose up -d` 成功啟動容器。
2. `pip install -r requirements_graphrag.txt` 無衝突。
3. `python scripts/seed_graph.py` 成功寫入至少 5 個節點。
4. `python scripts/verify_setup.py` 顯示 **"✅ System Ready"**。

