from neo4j import GraphDatabase
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class GraphRetriever:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def cypher_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        with self.driver.session() as session:
            result = session.run(query, params or {})
            return [record.data() for record in result]

    def get_context(self, node_id: str, entity_name: str = None) -> Dict[str, Any]:
        if node_id is not None:
            try:
                node_id_int = int(node_id)
            except (TypeError, ValueError):
                return {"graph_context": [], "error": "Invalid node_id"}
            query = """
            MATCH (n)-[r]->(m)
            WHERE id(n) = $node_id
            RETURN n, r, m
            """
            results = self.cypher_query(query, {"node_id": node_id_int})
            return {"graph_context": results}
        elif entity_name:
            # 以名稱查詢節點與一跳關係
            query = """
            MATCH (n {name: $name})-[r]->(m)
            RETURN n, r, m
            """
            results = self.cypher_query(query, {"name": entity_name})
            return {"graph_context": results}
        else:
            # 兩者都沒有，回傳空 context
            return {"graph_context": [], "error": "未提供 node_id 或 entity_name"}

if __name__ == "__main__":
    # 互動測試：查詢所有 Camera 節點
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "test1234")
    retriever = GraphRetriever(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    cameras = retriever.cypher_query("MATCH (c:Camera) RETURN c")
    print("Camera nodes:", cameras)
    retriever.close()