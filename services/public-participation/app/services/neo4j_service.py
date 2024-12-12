from typing import Dict, List
from neo4j import GraphDatabase
from app.core.config import settings
from app.models.models import Bill, Comment

class Neo4jService:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def add_bill(self, bill: Bill):
        with self.driver.session() as session:
            session.write_transaction(self._create_bill_node, bill)

    def add_comment(self, comment: Comment):
        with self.driver.session() as session:
            session.write_transaction(self._create_comment_node, comment)

    @staticmethod
    def _create_bill_node(tx, bill: Bill):
        query = (
            "MERGE (b:Bill {id: $id}) "
            "SET b.title = $title, "
            "b.description = $description, "
            "b.status = $status, "
            "b.created_at = $created_at"
        )
        tx.run(query, id=bill.id, title=bill.title,
               description=bill.description, status=bill.status,
               created_at=str(bill.created_at))

    @staticmethod
    def _create_comment_node(tx, comment: Comment):
        query = (
            "MATCH (b:Bill {id: $bill_id}) "
            "MERGE (c:Comment {id: $id}) "
            "SET c.text = $text, "
            "c.created_at = $created_at "
            "MERGE (c)-[:COMMENTS_ON]->(b)"
        )
        tx.run(query, id=comment.id, text=comment.text,
               bill_id=comment.bill_id,
               created_at=str(comment.created_at))

    def get_bill_graph(self, bill_id: int) -> Dict:
        with self.driver.session() as session:
            return session.read_transaction(self._get_bill_subgraph, bill_id)

    @staticmethod
    def _get_bill_subgraph(tx, bill_id: int) -> Dict:
        query = (
            "MATCH (b:Bill {id: $bill_id})-[r]-(n) "
            "RETURN b, r, n"
        )
        result = tx.run(query, bill_id=bill_id)
        nodes = []
        relationships = []
        for record in result:
            nodes.extend([record["b"], record["n"]])
            relationships.append(record["r"])
        return {
            "nodes": [dict(node) for node in nodes],
            "relationships": [dict(rel) for rel in relationships]
        }

neo4j_service = Neo4jService()

def add_bill_to_graph(bill: Bill):
    neo4j_service.add_bill(bill)

def add_comment_to_graph(comment: Comment):
    neo4j_service.add_comment(comment)

def get_bill_knowledge_graph(bill_id: int) -> Dict:
    return neo4j_service.get_bill_graph(bill_id) 