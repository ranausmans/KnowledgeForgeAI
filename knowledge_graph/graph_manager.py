import os
from neo4j import GraphDatabase
from typing import List, Dict

class GraphManager:
    def __init__(self):
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USER")
        password = os.getenv("NEO4J_PASSWORD")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_entities(self, entities: List[Dict]):
        with self.driver.session() as session:
            for entity in entities:
                session.run(
                    "MERGE (e:Entity {name: $name, type: $type})",
                    name=entity['entity'],
                    type=entity['type']
                )

    def add_relationships(self, relationships: List[Dict]):
        with self.driver.session() as session:
            for rel in relationships:
                session.run(
                    """
                    MATCH (s:Entity {name: $subject})
                    MATCH (o:Entity {name: $object})
                    MERGE (s)-[r:RELATED {predicate: $predicate}]->(o)
                    """,
                    subject=rel['subject'],
                    predicate=rel['predicate'],
                    object=rel['object']
                )

    def get_subgraph(self, entity_name: str, depth: int = 2):
        with self.driver.session() as session:
            result = session.run(
                f"""
                MATCH (e:Entity {{name: $name}})
                CALL apoc.path.subgraphAll(e, {{maxLevel: $depth}})
                YIELD nodes, relationships
                RETURN nodes, relationships
                """,
                name=entity_name,
                depth=depth
            )
            return result.single()
