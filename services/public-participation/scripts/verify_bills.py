# verify_bills.py

import os
import logging
from sqlalchemy import inspect
from .database_setup import SessionLocal, Bill, engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='config/.env')

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("verify_bills.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def verify_bills():
    # Retrieve and log the DATABASE_URL
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        logger.error("DATABASE_URL environment variable is not set.")
        print("DATABASE_URL environment variable is not set.")
        return
    logger.info(f"Using DATABASE_URL: {database_url}")
    print(f"Using DATABASE_URL: {database_url}")

    # Inspect the database to check available tables
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Available tables in the database: {tables}")
        print(f"Available tables in the database: {tables}")

        if 'bills' not in tables:
            logger.error("Table 'bills' does not exist in the database.")
            print("Table 'bills' does not exist in the database.")
            return
    except Exception as e:
        logger.error(f"Failed to inspect the database: {e}")
        print(f"Failed to inspect the database: {e}")
        return

    # Fetch and display bills
    session = SessionLocal()
    try:
        bills = session.query(Bill).all()
        if not bills:
            logger.info("No bills found in the database.")
            print("No bills found in the database.")
            return
        for bill in bills:
            print(f"ID: {bill.id}")
            print(f"Title: {bill.title}")
            print(f"PDF Path: {bill.file_path}")
            text_content = bill.text_content or "No text content available."
            print(f"Text Content: {text_content[:100]}...")  # Display first 100 characters
            print("-" * 40)
    except Exception as e:
        logger.error(f"Error querying the database: {e}")
        print(f"Error querying the database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    verify_bills()
