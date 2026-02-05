import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool, AgentType
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

def parse_sop_steps(sop_steps):
    """
    將自然語言 SOP 步驟列表轉為結構化序列
    Input: ["TwinLex S-2026 執行 Adjust_Angle 前需完成 Check_Obstruction"]
    Output: [{"camera_name": "TwinLex S-2026", "action": "Adjust_Angle", "sop_step": "Check_Obstruction"}]
    """
    import re
    parsed = []
    for step in sop_steps:
        m = re.match(r"(.*?) 執行 (.*?) 前需完成 (.*)", step)
        if m:
            parsed.append({
                "camera_name": m.group(1).strip(),
                "action": m.group(2).strip(),
                "sop_step": m.group(3).strip()
            })
    return parsed

# 工具2：查詢攝影機 SOP 步驟
def validate_agent_response(response):
    # schema 驗證已停用，僅保留型別檢查
    return True

from src.schema.agent_response_model import AgentResponse, SOPStep, MultiStepResult

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
        response = AgentResponse(
            output="查無攝影機 SOP 步驟",
            can_auto_sop=False,
            error="NO_SOP",
            sop_steps=[],
            sop_structured=[]
        )
        validate_agent_response(response.dict())
        return response.dict()
    steps = [f"{s['c']['name']} 執行 {s['a']['name']} 前需完成 {s['s']['name']}" for s in sops]
    parsed_steps = [SOPStep(camera_name=s['c']['name'], action=s['a']['name'], sop_step=s['s']['name']) for s in sops]
    response = AgentResponse(
        output="偵測到需先完成前置步驟：{}。是否要自動為您執行所有 SOP？".format("; ".join(steps)),
        can_auto_sop=bool(parsed_steps),
        error=None,
        sop_steps=steps,
        sop_structured=parsed_steps
    )
    validate_agent_response(response.dict())
    return response.dict()

# 工具3：根據 SOP 執行控制（僅回傳對應參數範例）
def control_camera_by_sop_tool(input):
    """
    支援單步驟 Dict 或多步驟 List[Dict] input，統一 structured output，並 schema 驗證
    """
    import json
    print("DEBUG control_camera_by_sop_tool input:", input)
    try:
        params = json.loads(input)
        print("DEBUG control_camera_by_sop_tool parsed params:", params)
        results = []
        # 判斷是否為多步驟
        if isinstance(params, list):
            results = []
            for step in params:
                print("DEBUG control_camera_by_sop_tool step:", step)
                camera = step.get("camera_name", "未知攝影機")
                action = step.get("action", "未知動作")
                sop = step.get("sop_step", "未知步驟")
                results.append(MultiStepResult(
                    output=f"控制指令：請對 {camera} 執行 {action}，並依照 SOP 步驟「{sop}」操作。",
                    camera_name=camera,
                    action=action,
                    sop_step=sop,
                    error=None
                ))
            response = AgentResponse(
                output="所有 SOP 步驟已自動完成。",
                can_auto_sop=False,
                error=None,
                sop_steps=[],
                sop_structured=[SOPStep(**step) if not isinstance(step, SOPStep) else step for step in params],
                multi_step_result=results
            )
            validate_agent_response(response.dict())
            return response.dict()
        else:
            print("DEBUG control_camera_by_sop_tool single step:", params)
            camera = params.get("camera_name", "未知攝影機")
            action = params.get("action", "未知動作")
            sop = params.get("sop_step", "未知步驟")
            response = AgentResponse(
                output=f"控制指令：請對 {camera} 執行 {action}，並依照 SOP 步驟「{sop}」操作。",
                can_auto_sop=False,
                error=None,
                sop_steps=[],
                sop_structured=[SOPStep(camera_name=camera, action=action, sop_step=sop)],
                multi_step_result=[MultiStepResult(
                    output=f"控制指令：請對 {camera} 執行 {action}，並依照 SOP 步驟「{sop}」操作。",
                    camera_name=camera,
                    action=action,
                    sop_step=sop,
                    error=None
                )]
            )
            validate_agent_response(response.dict())
            return response.dict()
    except Exception as e:
        print("DEBUG control_camera_by_sop_tool error:", e)
        response = AgentResponse(
            output="請提供正確的 JSON 格式參數：{\"camera_name\": \"...\", \"action\": \"...\", \"sop_step\": \"...\"}",
            error=str(e)
        )
        validate_agent_response(response.dict())
        return response.dict()

tools = [
    Tool(
        name="list_cameras",
        func=list_cameras_tool,
        description="列出所有可用攝影機"
    ),
    Tool(
        name="query_camera_sop",
        func=query_camera_sop_tool,
        description="查詢指定攝影機的可執行動作及其 SOP 步驟。若未指定 camera_name，請先要求使用者明確指定攝影機名稱後再查詢。"
    ),
    Tool(
        name="control_camera_by_sop",
        func=control_camera_by_sop_tool,
        description="根據 SOP 步驟與參數控制攝影機，需提供 camera_name, action, sop_step"
    )
]

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini")
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
        '{"camera_name": "TwinLex S-2026", "action": "Adjust_Angle", "sop_step": "Check_Obstruction"}'
    ]
    for q in queries:
        print(f"User Query: {q}")
        result = agent_executor.invoke({"input": q})
        print(f"Agent 回答：{result['output']}\n{'-'*40}")