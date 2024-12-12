# modules/knowledge_graph.py

from neo4j import GraphDatabase
import logging
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

# Load environment variables
load_dotenv(dotenv_path='config/.env')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLAlchemy setup for PostgreSQL
Base = declarative_base()

class KenyaBill(Base):
    __tablename__ = 'bills'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    text_content = Column(Text, nullable=True)  # Assuming you have this column

class KnowledgeGraph:
    def __init__(self):
        # PostgreSQL connection setup
        self.pg_engine = create_engine(os.environ.get("DATABASE_URL"))
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.pg_engine)
        
        # Neo4j connection setup
        uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        user = os.environ.get("NEO4J_USER", "neo4j")
        password = os.environ.get("NEO4J_PASSWORD", "password")  # Replace with your Neo4j password
        self.neo4j_driver = GraphDatabase.driver(uri, auth=(user, password))
        
        # Initialize the Neo4j index
        self._ensure_fulltext_index()
        
        # Perform initial data sync
        self.sync_data()
        
    def _ensure_fulltext_index(self):
        """
        Ensures that the full-text index 'billIndex' exists for Bill nodes.
        If it doesn't exist, it creates the index.
        """
        with self.neo4j_driver.session() as session:
            result = session.run("SHOW INDEXES")
            indexes = [record["name"] for record in result]
            if "billIndex" not in indexes:
                logger.info("Creating full-text index 'billIndex'")
                session.run(
                    """
                    CREATE FULLTEXT INDEX billIndex 
                    FOR (b:Bill) 
                    ON EACH [b.title, b.description]
                    """
                )
                logger.info("Full-text index 'billIndex' created successfully.")
            else:
                logger.info("Full-text index 'billIndex' already exists.")
    
    def sync_data(self):
        """
        Synchronizes data from PostgreSQL to Neo4j.
        Fetches all bills from PostgreSQL and ensures they exist in Neo4j.
        """
        logger.info("Starting data synchronization from PostgreSQL to Neo4j.")
        session = self.SessionLocal()
        try:
            bills = session.query(KenyaBill).all()
            logger.info(f"Fetched {len(bills)} bills from PostgreSQL.")
            
            with self.neo4j_driver.session() as neo_session:
                for bill in bills:
                    # Clean and prepare data
                    bill_id = bill.id
                    title = bill.title.strip()
                    url = bill.url.strip()
                    file_path = bill.file_path.strip()
                    description = bill.text_content.strip() if bill.text_content else ""
                    
                    # MERGE ensures that the node is created if it doesn't exist
                    # and updated if it does
                    neo_session.run(
                        """
                        MERGE (b:Bill {id: $id})
                        SET b.title = $title,
                            b.url = $url,
                            b.file_path = $file_path,
                            b.description = $description
                        """,
                        id=bill_id,
                        title=title,
                        url=url,
                        file_path=file_path,
                        description=description
                    )
                    logger.debug(f"Synchronized Bill ID {bill_id}: {title}")
            
            logger.info("Data synchronization completed successfully.")
        except Exception as e:
            logger.error(f"Error during data synchronization: {e}")
        finally:
            session.close()
    
    def query_knowledge_graph(self, prompt):
        """
        Queries the knowledge graph using the provided prompt.
        Utilizes the full-text index 'billIndex' to find relevant Bill nodes.

        Args:
            prompt (str): The search term or query.

        Returns:
            str or None: The description of the matching Bill, or None if no match is found.
        """
        try:
            with self.neo4j_driver.session() as session:
                result = session.run(
                    """
                    CALL db.index.fulltext.queryNodes('billIndex', $prompt) YIELD node, score
                    RETURN node.description AS description
                    ORDER BY score DESC
                    LIMIT 1
                    """,
                    prompt=prompt
                )
                record = result.single()
                if record and record["description"]:
                    logger.info("Found matching bill in knowledge graph.")
                    return record["description"]
                else:
                    logger.info("No matching bills found in knowledge graph.")
                    return None
        except Exception as e:
            logger.error(f"Error querying knowledge graph: {e}")
            return None
    
    def close(self):
        """
        Closes the Neo4j driver connection.
        """
        self.neo4j_driver.close()
