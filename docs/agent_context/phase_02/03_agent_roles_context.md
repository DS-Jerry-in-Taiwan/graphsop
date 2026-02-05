# Phase 02 - Agent 角色職責

## 🏗️ @ARCH (架構師)
* **職責**: 定義 NLU 的輸入/輸出介面標準。
* **輸入**: Phase 01 的 Ontology。
* **輸出**: `intents.py` (Pydantic Models)。
* **關鍵任務**: 確保 NLU 解析出的 `Action` 名稱與圖譜中的 `Relation` 名稱一致。

## 💻 @CODER (開發者)
* **職責**: 實作自然語言處理邏輯。
* **輸入**: Intent Schema、OpenAI/LlamaIndex SDK。
* **輸出**: NLU Pipeline 模組。
* **關鍵任務**: 實作 "Fuzzy Matching" (模糊比對) 邏輯，連接 Graph DB 進行實體驗證。

## 🧪 @ANALYST (測試員)
* **職責**: 測試語義理解的邊界。
* **輸入**: 測試語料集。
* **輸出**: 解析準確率報告。
* **關鍵任務**: 測試「不在圖譜中的名詞」（如：轉向火星），確保系統能回報「未知實體」。

## 🔧 @INFRA (運維)
* **職責**: 環境支援。
* **任務**: 確保 OpenAI API Key 或 Local LLM 連線正常，供 NLU 模組使用。

