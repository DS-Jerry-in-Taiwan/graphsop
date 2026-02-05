# Phase 04 - Agent Prompts (GraphRAG 實作指引)

## 1. Graph Retriever 實作指引 (@CODER)
```python
# 請參考此邏輯實作 src/rag/graph_retriever.py
def retrieve_constraints(entity_name: str) -> str:
    """
    連接 Neo4j，查詢目標實體是否有相關約束。
    Cypher Template:
    MATCH (t:Location {name: $name})
    OPTIONAL MATCH (t)-[r:HAS_CONSTRAINT]->(c:Constraint)
    OPTIONAL MATCH (t)-[r2:RESTRICTED_BY]->(z:Zone)
    RETURN t, c, z
    """
    # TODO: 使用 neo4j-driver 執行查詢
    # TODO: 將結果格式化為自然語言字串，例如 "目標 [休息室] 被標記為 [隱私禁區]，限制等級 [高]。"
    pass

```

## 2. Agent System Prompt 設計 (@ARCH)

```text
你是一個負責控制工業設備的 AI 助理。
你擁有一個「數位孿生」知識庫。在執行任何指令前，你必須先檢查 Context 中的約束條件。

**當前上下文 (From Graph)**:
{graph_context}

**使用者指令**:
{user_query}

**決策規則**:
1. 如果 Context 顯示目標是「禁區 (Privacy_Zone)」或有「物理限制」，你必須**拒絕執行**，並引用 Context 中的具體原因。
2. 如果 Context 安全，請呼叫對應的工具 (Camera Tool) 執行操作。
3. 如果 Context 為空或找不到實體，請詢問使用者更多細節，不要盲目執行。

請一步步思考 (Chain of Thought)，並解釋你的判斷依據。

```

## 3. LangGraph 構建指引 (@CODER)

```python
# 請參考此結構實作 src/agent/graph_agent.py
workflow = StateGraph(AgentState)

# 定義節點
workflow.add_node("retrieve", retrieve_node) # 查圖譜
workflow.add_node("agent", agent_node)       # LLM 思考
workflow.add_node("action", tool_node)       # 執行工具

# 定義邊 (Edge)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue, # 判斷 LLM 是要回覆文字(拒絕) 還是 呼叫工具
    {
        "end": END,
        "continue": "action"
    }
)
workflow.add_edge("action", "agent") # 工具執行後回傳結果給 LLM 總結

```

