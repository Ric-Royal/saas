# modules/rag_system.py

from .knowledge_graph import KnowledgeGraph
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='config/.env')

import logging
logger = logging.getLogger(__name__)

class RAGSystem:
    def __init__(self):
        self.kg = KnowledgeGraph()
    
    def retrieve_information(self, prompt):
        """
        Retrieves relevant information from the knowledge graph based on the prompt using full-text search.
        """
        description = self.kg.query_knowledge_graph(prompt)
        return description
    
    def retrieve_information(self, prompt):
        logger.debug(f"Retrieving information for prompt: {prompt}")

    def retrieve_information(self, prompt):
        description = self.kg.query_knowledge_graph(prompt)
        if description:
            return description
        else:
            return None
    
    def close(self):
        self.kg.close()

# Example usage
if __name__ == "__main__":
    rag = RAGSystem()
    user_prompt = "Agriculture Bill"
    info = rag.retrieve_information(user_prompt)
    if info:
        print(f"Retrieved Information: {info}")
    else:
        print("Information not available in the knowledge bank.")
    rag.close()
