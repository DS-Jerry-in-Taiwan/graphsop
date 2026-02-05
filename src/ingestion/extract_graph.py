import os
from llama_index.core import SimpleDirectoryReader, PropertyGraphIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.graph_stores import Neo4jGraphStore
from llama_index.schema import NodeWithScore
import networkx as nx

# 路徑與參數
MANUAL_PATH = "../../docs/manuals/camera_manual_v1.md"
ONTOLOGY_PATH = "../schema/ontology.json"
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

def load_manual(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_ontology(path):
    import json
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_triples(text, ontology):
    # 使用 LlamaIndex PropertyGraphIndex 進行三元組提取
    llm = OpenAI(model="gpt-3.5-turbo")
    embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
    index = PropertyGraphIndex(
        llm=llm,
        embed_model=embed_model,
        ontology=ontology
    )
    triples = index.extract_triples(text)
    return triples

def save_to_neo4j(triples):
    store = Neo4jGraphStore(
        uri=NEO4J_URI,
        username=NEO4J_USER,
        password=NEO4J_PASSWORD
    )
    store.save_triples(triples)

def save_to_networkx(triples, out_path="graph.gml"):
    G = nx.MultiDiGraph()
    for s, p, o in triples:
        G.add_edge(s, o, label=p)
    nx.write_gml(G, out_path)

def main():
    manual = load_manual(MANUAL_PATH)
    ontology = load_ontology(ONTOLOGY_PATH)
    triples = extract_triples(manual, ontology)
    save_to_neo4j(triples)
    save_to_networkx(triples, out_path="camera_graph.gml")
    print("Graph extraction complete. Triples saved to Neo4j and camera_graph.gml.")

if __name__ == "__main__":
    main()