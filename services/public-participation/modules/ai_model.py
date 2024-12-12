# modules/ai_model.py

import requests
import json
import logging
from dotenv import load_dotenv
import os
from neo4j import GraphDatabase, basic_auth
import time
from thefuzz import fuzz
from thefuzz import process

# Load environment variables from .env file
load_dotenv(dotenv_path='config/.env')

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/ai_model.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OllamaResponder:
    def __init__(
        self,
        model_name: str = "llama3.2:latest",
        base_url: str = "http://127.0.0.1:11434",
        max_retries: int = 3,
        retry_delay: float = 2.0
    ):
        self.model_name = model_name
        self.base_url = base_url.rstrip('/')  # Ensure no trailing slash
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        logger.info(f"Initialized OllamaResponder with model: {self.model_name} at {self.base_url}")

        # Initialize Neo4j connection
        try:
            neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
            neo4j_user = os.getenv("NEO4J_USER", "neo4j")
            neo4j_password = os.getenv("NEO4J_PASSWORD", "password")

            self.driver = GraphDatabase.driver(
                neo4j_uri,
                auth=basic_auth(neo4j_user, neo4j_password)
            )
            logger.info("Connected to Neo4j Knowledge Graph successfully.")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j Knowledge Graph: {e}")
            self.driver = None

    def close_neo4j(self):
        if self.driver:
            self.driver.close()
            logger.info("Closed Neo4j driver connection.")

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize the text by removing underscores, dashes, and file extensions.
        Ensures that words are capitalized appropriately.
        """
        # Remove the file extension if present
        text = os.path.splitext(text)[0]
        # Replace underscores and dashes with spaces
        normalized = text.replace('_', ' ').replace('-', ' ').strip()
        # Capitalize each word
        normalized = ' '.join([word.capitalize() for word in normalized.split()])
        return normalized

    def is_list_bills_request(self, prompt: str) -> bool:
        """
        Determines if the user's prompt is requesting a list of bills.
        """
        prompt_lower = prompt.lower()
        list_bills_keywords = [
            "list of bills",
            "bills in kenya",
            "all bills",
            "list bills",
            "what bills",
            "which bills",
            "bills passed",
            "bills available",
            "bills proposed",
            "bills introduced",
            "bills currently",
            "bills in parliament",
            "give me a list of bills",
            "provide list of bills",
            "what are the bills",
        ]
        for keyword in list_bills_keywords:
            if keyword in prompt_lower:
                return True
        return False

    def extract_year_from_title(self, title: str) -> str:
        """
        Extracts the year from the title if present.
        Assumes the year is a four-digit number in the title.
        """
        import re
        match = re.search(r'20\d{2}', title)
        if match:
            return match.group(0)
        else:
            return "Unknown"

    def get_best_fuzzy_match(self, records, prompt: str):
        """
        Uses fuzzy matching to compare the normalized prompt with titles from the Knowledge Graph.
        Returns the best match based on the highest similarity score.
        """
        titles = [record[0] for record in records]
        normalized_titles = [self.normalize_text(title) for title in titles]
        # Normalize the prompt
        normalized_prompt = self.normalize_text(prompt)
        # Perform fuzzy matching between the prompt and the normalized titles
        best_title, score = process.extractOne(normalized_prompt, normalized_titles, scorer=fuzz.partial_ratio)
        logger.debug(f"Best fuzzy match: {best_title} with score {score}")
        # Set a threshold to ensure the match is relevant (e.g., at least 70% similarity)
        if score >= 70:
            # Find the corresponding record with the best match
            for record in records:
                if self.normalize_text(record[0]) == best_title:
                    return {'title': record[0], 'description': record[1]}
        return None

    def query_knowledge_graph(self, prompt: str) -> (str, str):
        """
        Queries the Neo4j Knowledge Graph based on the prompt and returns relevant information.
        If the user requests a list of bills, return all bill titles grouped by year.
        Otherwise, use fuzzy matching to find the most relevant bill.

        Returns:
            knowledge (str): The knowledge to include in the prompt.
            response_type (str): 'list', 'detail', or 'general' indicating the type of response.
        """
        if not self.driver:
            logger.warning("Neo4j driver not initialized. Skipping knowledge graph query.")
            return "", "general"

        # Check if the prompt is requesting a list of bills
        if self.is_list_bills_request(prompt):
            # Fetch all unique bill titles
            query = """
            MATCH (n)
            RETURN DISTINCT n.title AS title
            """
            try:
                with self.driver.session() as session:
                    result = session.run(query)
                    records = result.values()
                    if records:
                        # Process records to group titles by year
                        bills_by_year = {}
                        titles_seen = set()
                        for record in records:
                            title = record[0]
                            # Normalize the title
                            normalized_title = self.normalize_text(title)
                            # Ensure uniqueness
                            if normalized_title in titles_seen:
                                continue
                            titles_seen.add(normalized_title)
                            # Extract year from title (assuming year is in title)
                            year = self.extract_year_from_title(title)
                            if year:
                                if year not in bills_by_year:
                                    bills_by_year[year] = []
                                bills_by_year[year].append(normalized_title)
                        # Format the knowledge string
                        knowledge = "List of Bills in Kenya grouped by year:\n"
                        for year in sorted(bills_by_year.keys(), reverse=True):
                            knowledge += f"\nYear {year}:\n"
                            for bill_title in sorted(bills_by_year[year]):
                                knowledge += f"- {bill_title}\n"
                        return knowledge, "list"
                    else:
                        logger.info("No records found in Knowledge Graph.")
                        return "", "general"
            except Exception as e:
                logger.error(f"Error querying Knowledge Graph: {e}", exc_info=True)
                return "", "general"
        else:
            # Proceed with previous code using fuzzy matching
            # Fetch all nodes with their titles and descriptions
            query = """
            MATCH (n)
            RETURN n.title AS title, n.description AS description
            """
            try:
                with self.driver.session() as session:
                    result = session.run(query)
                    records = result.values()
                    if records:
                        # Apply fuzzy matching to rank the best matches
                        best_match = self.get_best_fuzzy_match(records, prompt)
                        if best_match:
                            title = best_match['title']
                            description = best_match['description']
                            logger.debug(f"Knowledge Graph Query Result: Title - {title}, Description Length - {len(description)}")
                            # Limit description length
                            if description and len(description) > 16000:
                                description = description[:15970] + '...'
                            # Format the knowledge into a readable string
                            knowledge = f"**Knowledge Graph Data:**\n**Title:** {self.normalize_text(title)}\n**Description:**\n{description}\n"
                            return knowledge, "detail"
                        else:
                            logger.info("No relevant data found in Knowledge Graph for the given prompt.")
                            return "", "general"
                    else:
                        logger.info("No records found in Knowledge Graph.")
                        return "", "general"
            except Exception as e:
                logger.error(f"Error querying Knowledge Graph: {e}", exc_info=True)
                return "", "general"



    def generate_response(
        self,
        prompt: str,
        max_tokens: int = 150,
        temperature: float = 0.7,
    ) -> str:
        if not prompt.strip():
            logger.warning("Empty prompt received.")
            return "Please provide a valid query."

        # Query the Knowledge Graph for additional context
        knowledge, response_type = self.query_knowledge_graph(prompt)

        # Determine how to respond based on the response_type
        if response_type == "list" and knowledge:
            # For list of bills, return the knowledge directly
            logger.debug("Returning list of bills directly without invoking AI model.")
            return knowledge.strip()
        elif response_type == "detail" and knowledge:
            # For a specific bill, include user's question and knowledge
            augmented_prompt = (
                f"You are an assistant knowledgeable about Kenyan bills.\n\n"
                f"Here is some relevant information from the knowledge graph:\n{knowledge}\n\n"
                f"User's question: {prompt}\n\n"
                f"Based on the above information, provide a comprehensive and accurate response."
            )
            use_knowledge = True
        else:
            # General case
            augmented_prompt = (
                f"You are an assistant knowledgeable about Kenyan bills.\n\n"
                f"User's question: {prompt}\n\n"
                f"Provide a comprehensive and accurate response based on your knowledge."
            )
            use_knowledge = False

        logger.debug(f"Augmented Prompt:\n{augmented_prompt}")
        
        payload = {
            "model": self.model_name,
            "prompt": augmented_prompt,
            "options": {
                "max_tokens": max_tokens,
                "temperature": temperature
            }
        }

        url = f"{self.base_url}/api/generate"  # Adjust endpoint if necessary
        headers = {
            "Content-Type": "application/json",
            # "Authorization": f"Bearer {os.environ.get('OLLAMA_API_KEY')}"  # Uncomment if authentication is required
        }

        logger.debug(f"Sending request to Ollama API at {url} with payload: {json.dumps(payload)}")

        # Implementing retry mechanism
        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=300, stream=True)
                response.raise_for_status()
                logger.debug(f"Received response status: {response.status_code}")
                break  # Exit the retry loop if successful
            except requests.exceptions.HTTPError as http_err:
                logger.error(f"HTTP error occurred: {http_err} (Attempt {attempt}/{self.max_retries})")
            except requests.exceptions.RequestException as req_err:
                logger.error(f"Request exception occurred: {req_err} (Attempt {attempt}/{self.max_retries})")
            if attempt < self.max_retries:
                logger.info(f"Retrying after {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
            else:
                logger.error("Max retries exceeded. Unable to generate response.")
                return "Sorry, I couldn't process your request at this time."

        # Process the streaming response
        full_response = ""
        try:
            for line in response.iter_lines():
                if line:
                    line_decoded = line.decode('utf-8').strip()
                    logger.debug(f"Received line: {line_decoded}")
                    try:
                        data = json.loads(line_decoded)
                        chunk = data.get("response", "")
                        full_response += chunk
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError as json_err:
                        logger.error(f"JSON decode error: {json_err} - Line: {line_decoded}")
                        continue
        except Exception as e:
            logger.error(f"Error processing streaming response: {e}")
            return "Sorry, an error occurred while processing the AI model's response."

        if full_response.strip():
            response_type_desc = "Knowledge-based" if use_knowledge else "General"
            logger.info(f"Generated {response_type_desc} response successfully.")
            return full_response.strip()
        else:
            logger.warning("AI returned an empty content.")
            return "Sorry, I couldn't generate a response."


    def close(self):
        logger.info("OllamaResponder is shutting down.")
        self.close_neo4j()
