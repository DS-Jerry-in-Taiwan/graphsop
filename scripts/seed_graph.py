import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "test1234")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def seed():
    with driver.session() as session:
        # 清空資料庫
        session.run("MATCH (n) DETACH DELETE n")
        # 建立 TwinLex 測試圖譜
        session.run("""
        CREATE (c:Camera {id: "C1", name: "TwinLex S-2026", max_pan: 180, zoom_limit: 10})
        CREATE (z:Zone {id: "Zone-B", name: "休息室", type: "Privacy_Zone"})
        CREATE (a:Action {id: "A1", name: "Adjust_Angle"})
        CREATE (s:SOP_Step {id: "S1", name: "Check_Obstruction"})
        CREATE (c)-[:HAS_LIMIT]->(a)
        CREATE (a)-[:RESTRICTS]->(z)
        CREATE (a)-[:REQUIRES]->(s)
        """)
        print("TwinLex 測試圖譜已建立。")

if __name__ == "__main__":
    seed()
    driver.close()