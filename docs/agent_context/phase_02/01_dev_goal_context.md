# Phase 02 - 開發目標：意圖解析與實體映射 (NLU Layer)

**專案名稱**: TwinLex (GraphSOP)
**階段**: Day 2 - 意圖解析
**執行模式**: 混合模式 (Mixed Mode)

## 🎯 核心目的
建立系統的「語義翻譯層」，將使用者模糊的自然語言指令（如：「看大門」），轉化為精確對應圖譜節點的結構化意圖（如：`Action: ROTATE`, `Target: NODE_ID_001`）。

## 🚩 開發目標
1. **意圖定義 (Intent Definition)**: 設計標準化的操作意圖 Schema (Pydantic Models)。
2. **語義路由 (Semantic Router)**: 實作能區分「操作指令」、「狀態查詢」、「維修對話」的分類器。
3. **實體對齊 (Entity Resolution)**: 開發模糊比對邏輯，將口語名詞（如 "Lounge"）映射至 Graph DB 中的唯一節點 ID。
4. **參數提取 (Slot Filling)**: 從對話中提取角度、倍率等具體參數。

## 📦 預期產出物
* **Intent Schema**: `src/schema/intents.py`
* **NLU Pipeline**: `src/nlu/router.py`, `src/nlu/extractor.py`
* **Entity Resolver**: `src/nlu/resolver.py` (連接 Neo4j 進行查詢)
* **測試報告**: 針對模糊指令的解析準確率報告。

## ✅ 驗收標準 (Definition of Done)
* **路由準確率**: 能 100% 區分「查詢手冊」與「操作設備」的意圖。
* **實體映射率**: 當輸入「轉向休息室」時，系統能解析出 `Target: Privacy_Zone_B` (對應 Phase 01 的圖譜數據)。
* **結構合規性**: 輸出的 JSON 必須完全符合 `ontology.json` 定義的操作類型。

