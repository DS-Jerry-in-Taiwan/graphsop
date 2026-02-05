# Phase 01 - Agent Prompts

## 1. 生成虛擬手冊 Prompt (@INFRA/@CODER)
```text
你是一位資深的工業設備技術寫手。請生成一份名為《TwinLex 智慧攝影機 S-2026 操作與安全手冊》的 Markdown 文件，長度約 3 頁。
內容必須包含：
1. **物理規格**：最大旋轉角度 (Pan/Tilt)、變焦倍率、工作溫度。
2. **操作 SOP**：詳細列出「遠端視角調整」、「隱私遮蔽設定」的步驟 (Step-by-Step)。
3. **安全與合規限制**：明確指出「禁止拍攝員工休息室 (Zone-B)」、「夜間模式強制開啟紅外線」等約束 (Constraints)。
請使用專業但結構清晰的語氣，便於後續 AI 進行實體提取。

```

## 2. 圖譜 Schema 設計 Prompt (@ARCH)

```text
請根據《智慧攝影機操作手冊》設計一個 GraphRAG 的 Ontology (Schema)。
目標是建立一個「數位孿生控制核心」。
請定義以下節點與關係的 JSON 結構：
- Nodes: Device, Action, Parameter, Constraint, Location, SOP_Step, Validation_Metric
- Edges: PERFORMED_ON, HAS_CONSTRAINT, NEXT_STEP, LOCATED_AT, REQUIRES_VALIDATION
請特別注重要能夠表達「動作 A 在條件 B 下被禁止」的邏輯。

```

## 3. 實體關係提取 Prompt (@CODER)

```text
你是一個邏輯嚴密的知識圖譜工程師。請從以下文本中提取實體與關係，並嚴格遵循定義好的 Schema。
重點提取規則：
1. **約束提取**：看到「禁止」、「必須」、「限制」等詞，必須建立 [Action] --(RESTRICTED_BY)--> [Constraint] 關係。
2. **流程提取**：看到步驟 1、2、3，必須建立 [Step 1] --(NEXT_STEP)--> [Step 2] 關係。
3. **參數提取**：將具體的數值 (如 180度) 提取為節點的屬性 (Property)。
請忽略修辭性的文字，只保留邏輯骨幹。

```
