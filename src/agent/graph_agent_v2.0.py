import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType, Tool
from langchain_openai import ChatOpenAI
from src.agent.retriever import GraphRetriever

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "test1234")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-xxxxxxx")

# 工具1：查詢攝影機清單
def list_cameras_tool(input):
    retriever = GraphRetriever(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    cameras = retriever.cypher_query("MATCH (c:Camera) RETURN c")
    retriever.close()
    if not cameras:
        return "查無攝影機"
    return "攝影機清單：" + ", ".join([c["c"]["name"] for c in cameras])

# 工具2：查詢攝影機 SOP 步驟
def query_camera_sop_tool(input):
    retriever = GraphRetriever(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    sops = retriever.cypher_query(
        """
        MATCH (c:Camera)-[:HAS_LIMIT]->(a:Action)-[:REQUIRES]->(s:SOP_Step)
        RETURN c, a, s
        """
    )
    retriever.close()
    if not sops:
        return "查無攝影機 SOP 步驟"
    return "SOP 步驟：" + "; ".join([
        f"{s['c']['name']} 執行 {s['a']['name']} 前需完成 {s['s']['name']}" for s in sops
    ])

# 工具3：根據 SOP 執行控制（僅回傳對應參數範例）
def control_camera_by_sop_tool(input):
    # input 預期格式：{"camera_name": "...", "action": "...", "sop_step": "..."}
    try:
        import json
        params = json.loads(input)
        camera = params.get("camera_name", "未知攝影機")
        action = params.get("action", "未知動作")
        sop = params.get("sop_step", "未知步驟")
        return f"控制指令：請對 {camera} 執行 {action}，並依照 SOP 步驟「{sop}」操作。"
    except Exception:
        return "請提供正確的 JSON 格式參數：{\"camera_name\": \"...\", \"action\": \"...\", \"sop_step\": \"...\"}"

tools = [
    Tool(
        name="list_cameras",
        func=list_cameras_tool,
        description="列出所有可用攝影機"
    ),
    Tool(
        name="query_camera_sop",
        func=query_camera_sop_tool,
        description="查詢攝影機可執行動作及其 SOP 步驟"
    ),
    Tool(
        name="control_camera_by_sop",
        func=control_camera_by_sop_tool,
        description="根據 SOP 步驟與參數控制攝影機，需提供 camera_name, action, sop_step"
    )
]

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
agent_executor = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    handle_parsing_errors=True
)

if __name__ == "__main__":
    queries = [
        "有哪些攝影機可以選擇？",
        "TwinLex S-2026 執行調整角度前要做什麼？",
    ]
    for q in queries:
        print(f"User Query: {q}")
        result = agent_executor.invoke({"input": q})
        print(f"Agent 回答：{result['output']}\n{'-'*40}")