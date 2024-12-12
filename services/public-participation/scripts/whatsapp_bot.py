# whatsapp_bot.py

import os
import logging
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from modules.ai_model import OllamaResponder
from modules.knowledge_graph import KnowledgeGraph
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables from .env file
load_dotenv(dotenv_path='config/.env')  # Ensure the path is correct

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more detailed logs if needed
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/whatsapp_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize AI Responder and Knowledge Graph
responder = None
knowledge_graph = None
try:
    responder = OllamaResponder()
    logger.info("OllamaResponder initialized successfully.")
except Exception as e:
    logger.critical(f"Cannot initialize OllamaResponder: {e}")

try:
    knowledge_graph = KnowledgeGraph()
    logger.info("KnowledgeGraph initialized successfully.")
except Exception as e:
    logger.critical(f"Cannot initialize KnowledgeGraph: {e}")

def search_bills(prompt):
    """
    Retrieve relevant bills from the knowledge graph based on the user's prompt.
    Returns a list of bill descriptions.
    """
    if not knowledge_graph:
        logger.error("KnowledgeGraph is not initialized.")
        return []
    
    descriptions = knowledge_graph.query_knowledge_graph(prompt)
    if descriptions:
        logger.info(f"Found {len(descriptions)} relevant bill(s) for the prompt.")
        return descriptions
    else:
        logger.info("No relevant bills found in the Knowledge Graph.")
        return []

def construct_prompt(user_query, aggregated_context):
    """
    Construct the prompt for the AI model using the user's query and the aggregated context.
    """
    return (
        f"You are an assistant knowledgeable about Kenyan bills.\n"
        f"Here is some relevant information:\n{aggregated_context}\n\n"
        f"User's question: {user_query}\n\n"
        f"Provide a comprehensive and accurate response based on the above information."
    )

def construct_general_prompt(user_query):
    """
    Construct a general prompt for the AI model without additional context.
    """
    return (
        f"You are an assistant knowledgeable about Kenyan bills.\n\n"
        f"User's question: {user_query}\n\n"
        f"Provide a comprehensive and accurate response based on your knowledge."
    )

@app.route('/', methods=['GET'])
def home():
    return "WhatsApp Bot is running."

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    logger.info("Received request at /whatsapp endpoint.")
    try:
        incoming_msg = request.form.get('Body', '').strip()
        from_number = request.form.get('From', 'unknown')
        logger.info(f"Received message from {from_number}: {incoming_msg}")

        resp = MessagingResponse()
        msg = resp.message()

        if incoming_msg:
            # Input sanitization
            incoming_msg = incoming_msg.strip()
            if len(incoming_msg) > 500:
                incoming_msg = incoming_msg[:500]
                logger.warning("Incoming message truncated to 500 characters.")

            # Retrieve relevant bills from Knowledge Graph
            bills_descriptions = search_bills(incoming_msg)

            if bills_descriptions:
                aggregated_context = "\n\n".join(bills_descriptions)
                prompt = construct_prompt(incoming_msg, aggregated_context)
                logger.debug(f"Constructed Knowledge-based Prompt: {prompt[:200]}{'...' if len(prompt) > 200 else ''}")

                if responder:
                    ai_response = responder.generate_response(prompt)
                    # Truncate ai_response if too long
                    if len(ai_response) > 1600:
                        ai_response = ai_response[:1597] + '...'
                        logger.warning("AI response truncated to 1600 characters.")
                    msg.body(ai_response)
                    logger.info("Sent Knowledge-based AI response.")
                else:
                    logger.error("Responder is not initialized.")
                    msg.body("Sorry, I'm unable to process your request at the moment.")
            else:
                if responder:
                    # If no bills found, generate a response using AI without additional context
                    prompt = construct_general_prompt(incoming_msg)
                    logger.debug(f"Constructed General Prompt: {prompt[:200]}{'...' if len(prompt) > 200 else ''}")
                    ai_response = responder.generate_response(prompt)
                    # Truncate ai_response if too long
                    if len(ai_response) > 1600:
                        ai_response = ai_response[:1597] + '...'
                        logger.warning("AI response truncated to 1600 characters.")
                    msg.body(ai_response)
                    logger.info("Sent General AI response.")
                else:
                    logger.error("Responder is not initialized.")
                    msg.body("Sorry, I'm unable to process your request at the moment.")
        else:
            # Handle empty message
            msg.body("Hello! How can I assist you with Kenyan bills today?")
            logger.info("Sent greeting message for empty prompt.")

        return str(resp)
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        # Return a generic error message to the user
        resp = MessagingResponse()
        resp.message("Sorry, an error occurred while processing your request.")
        return str(resp)

@app.route("/health", methods=['GET'])
def health_check():
    """
    Health check endpoint to verify that the bot is running.
    """
    status = "OK"
    if not responder:
        status = "Responder Unavailable"
    if not knowledge_graph:
        status = "KnowledgeGraph Unavailable" if status == "OK" else f"{status}, KnowledgeGraph Unavailable"
    logger.info(f"Health Check: {status}")
    return status, 200

@app.errorhandler(404)
def page_not_found(e):
    logger.warning(f"404 error: {e}")
    return "This endpoint does not exist.", 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"500 error: {e}")
    return "An internal server error occurred.", 500

if __name__ == "__main__":
    # Get host and port from environment variables with defaults
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_PORT", 5001))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"

    # Run the Flask app with threaded=True to handle multiple requests
    app.run(host=host, port=port, debug=debug, threaded=True)


# # simple_whatsapp_bot.py

# from flask import Flask, request
# from twilio.twiml.messaging_response import MessagingResponse
# import logging

# app = Flask(__name__)

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# @app.route('/whatsapp', methods=['POST'])
# def whatsapp_reply():
#     incoming_msg = request.form.get('Body', '')
#     from_number = request.form.get('From', 'unknown')
#     logging.info(f"Received message from {from_number}: {incoming_msg}")

#     # Create a Twilio MessagingResponse
#     resp = MessagingResponse()
#     msg = resp.message()

#     # For this simple example, echo back the received message
#     response_text = f"You said: {incoming_msg}"
#     msg.body(response_text)

#     return str(resp)

# if __name__ == "__main__":
#     app.run(debug=True, port=5001)
