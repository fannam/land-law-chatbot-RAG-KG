from langchain.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_community.graphs.neo4j_graph import Neo4jGraph
from fuzzysearch import find_near_matches
import os
os.environ["NEO4J_URI"] = ""
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = ""
graph = Neo4jGraph()

def response_by_graph_search(user_message, llm):
    chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True)
    response = chain.invoke({"query": user_message})
    print(f"graph: {response['result']}")
    return response["result"]


