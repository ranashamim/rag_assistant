from app.graph.graph import Graph
from app.graph.graph_extractor import GraphExtractor


text = """
Microsoft acquired GitHub in 2018.
GitHub later created GitHub Copilot.
GitHub Copilot is an AI-powered coding assistant.
"""

extractor = GraphExtractor()
graph = Graph()

graph = extractor.build_graph(text, graph)


microsoft = graph.get_entity_by_name("Microsoft")

relationships = graph.get_related_relationships(
    microsoft.entity_id
)

for relationship in relationships:
    print(relationship)