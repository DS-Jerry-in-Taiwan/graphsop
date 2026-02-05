import os
import json
import sys
from openai import OpenAI
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.agent.retriever import GraphRetriever
from dotenv import load_dotenv

load_dotenv()

class GraphRAGAgent:
    def __init__(self, neo4j_uri, neo4j_user, neo4j_password, openai_api_key):
        self.retriever = GraphRetriever(neo4j_uri, neo4j_user, neo4j_password)
        self.llm = OpenAI(api_key=openai_api_key)
    
    def llm_extract_entity(self, user_query: str) -> str:
        prompt = f"從以下問題中提取相關的實體名稱：{user_query}\n只回傳實體名稱，不要其他文字。"
        response = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "你是實體名稱提取助理。"}, {"role": "user", "content": prompt}]
        )
        entity = response.choices[0].message.content.strip()
        return entity if entity else None

    def query(self, user_query: str, node_id: str) -> str:
        # 決定查詢方式
        if node_id is not None:
            context = self.retriever.get_context(node_id=node_id)
        else:
            entity_name = self.llm_extract_entity(user_query)
            if entity_name:
                context = self.retriever.get_context(node_id=None, entity_name=entity_name)
            else:
                return {
                    "llm_reply": "請提供明確的目標名稱或節點編號。",
                    "can_execute": False,
                    "graph_context": [],
                    "error": "缺少 node_id 與 entity_name"
                }
                
        graph_context = context.get("graph_context", [])
        prompt = (
            "你是一個知識圖譜助理。"
            "根據以下圖譜知識回答問題：\n"
            f"{graph_context}\n\n"
            f"問題：{user_query}\n\n"
            "如果你無法回答，請明確指出缺少哪些關鍵資訊，"
            "並用 JSON 格式回覆：{\"can_execute\": true/false, \"llm_reply\": \"...\"}"
        )
        error = context.get("error")
        response = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "你是知識圖譜助理。"}, {"role": "user", "content": prompt}]
        )
        deny_keywords = [
            "無法回答", "不知道", "不清楚", "缺少資訊", "請補充", "資訊不足", "無法執行", "請提供"
        ]
        llm_content = response.choices[0].message.content
        try:
            result = json.loads(llm_content)
            can_execute = error is None and result.get("can_execute", False)
            llm_reply = result.get("llm_reply", "")
        except Exception:
            # fallback: deny_keywords
            llm_reply = llm_content
            can_execute = error is None and not any(kw in llm_reply for kw in deny_keywords)
        return {
            "llm_reply": llm_reply,
            "can_execute": can_execute,
            "graph_context": graph_context,
            "error": error
        }

    def close(self):
        self.retriever.close()

if __name__ == "__main__":
    # 範例：查詢 Camera 節點並調用 LLM 回答
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "test1234")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-xxxxxxx")
    agent = GraphRAGAgent(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, OPENAI_API_KEY)
    # 取得第一個 Camera 節點 id
    cameras = agent.retriever.cypher_query("MATCH (c:Camera) RETURN id(c) AS node_id LIMIT 1")
    if cameras:
        node_id = cameras[0]["node_id"]
        user_queries = [
            "調整攝影機角度",
            "攝影機調低一點",
            "攝影機調高一點"
        ]
        for user_query in user_queries:
            answer = agent.query(user_query, node_id)
            print(f"User Query: {user_query}\nLLM 回答：{answer}\n{'-'*40}")
    else:
        print("查無 Camera 節點")
    agent.close()
