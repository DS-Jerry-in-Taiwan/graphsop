# Phase 01 - 開發流程：知識建模

**階段**: Day 1
**目標**: 完成設備手冊的圖譜化 (Graph Extraction)

## 📅 執行步驟流程

### Step 1: 數據準備 (@INFRA)
1. **生成虛擬手冊**: 撰寫 `camera_manual_v1.md`，包含：
   - **硬體參數**: `Max_Pan_Angle: 180`, `Zoom_Limit: 10x`。
   - **SOP 流程**: `Adjust_Angle` 需先 `Check_Obstruction`。
   - **安全規範**: 定義 `Privacy_Zone` (如: 休息室)。
2. **環境配置**: 準備 Python 環境與 Graph Database (Neo4j/NetworkX) 連接器。

### Step 2: Schema 設計 (@ARCH)
1. **定義 Ontology**: 設計節點類型 (`Device`, `Action`, `Constraint`, `SOP_Step`) 與關係類型 (`HAS_LIMIT`, `REQUIRES`, `RESTRICTS`)。
2. **【Checkpoint 1】架構審查**: 人工確認 Schema 是否足以描述物理限制。

### Step 3: 圖譜提取與構建 (@CODER)
1. **Pipeline 開發**: 使用 LlamaIndex `PropertyGraphIndex` 建立提取腳本。
2. **實體提取**: 執行腳本，將 `camera_manual_v1.md` 轉化為圖譜節點。
3. **實體消解**: 確保 "Lens" 與 "Camera_Lens" 合併為同一節點。

### Step 4: 初步驗證 (@ANALYST)
1. **連通性檢查**: 確認所有 `Action` 都有對應的 `Constraint` 或 `Next_Step`。
2. **孤島偵測**: 確保沒有未連接的孤立節點。

