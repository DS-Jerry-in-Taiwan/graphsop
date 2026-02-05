# Phase 03 - Agent 角色職責

## 🏗️ @ARCH (架構師)
* **職責**: 設計決策邏輯流 (Control Flow)。
* **輸入**: 業務邏輯需求、Phase 02 的 Intent Schema。
* **輸出**: `workflow_design.md` 或 `workflow.py` 的骨架代碼。
* **關鍵任務**: 確保「安全檢查」是執行的必要前置條件 (Pre-condition)。

## 💻 @CODER (開發者)
* **職責**: 實作約束檢查器與狀態機節點。
* **輸入**: LangGraph 架構、Graph DB 連接器。
* **輸出**: 完整的 `ConstraintEngine` 類別與 `StateGraph` 實作。
* **關鍵任務**: 撰寫 Cypher 查詢語句，精準抓取與目標實體關聯的所有 `RESTRICTS` 關係。

## 🧪 @ANALYST (測試員)
* **職責**: 驗證邏輯邊界的強韌性。
* **輸入**: 攻擊測試案例集 (Attack Vectors)。
* **輸出**: 安全攔截測試報告。
* **關鍵任務**: 驗證系統在「多重約束」下的表現（例如：既超過角度又是隱私區）。

## 🔧 @INFRA (運維)
* **職責**: 支援 LangGraph 運行環境。
* **任務**: 確保 Python 環境包含 `langgraph` 與 `langchain` 依賴。

