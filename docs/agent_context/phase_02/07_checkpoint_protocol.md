# Checkpoint Protocol - Phase 02

## 🛑 Checkpoint 2: Intent Schema & Router 確認

**觸發時機**: @ARCH 完成 Intent Definition 後，@CODER 開始寫核心邏輯前。
**決策者**: 人類架構師 (您)

### 審查重點
1. **與圖譜的相容性**:
   - 定義的 Intent 是否能映射到 Phase 01 圖譜中的 `SOP`？
   - (例如：圖譜中有 `Adjust_Angle`，Intent 中是否有對應的 `ROTATE`？)

2. **參數完整性**:
   - 是否遺漏了關鍵參數（如：變焦倍率）？

### 決策選項
- **✅ 通過**: Schema 設計合理，允許 @CODER 開始實作 Router 與 Extractor。
- **🔄 修改**: 缺少動作定義，退回 @ARCH 補全。

### 執行指令
審查通過後，請在終端機輸入：
`@CODER 啟動 Phase 2.3 - NLU 邏輯實作`

