# scripts/main_phase1.py
import logging
from .scraper import get_bill_links, download_bills
from .pdf_processor import process_pdfs
from .database_setup import init_db
from sqlalchemy.exc import SQLAlchemyError
from modules.ai_model import OllamaResponder

from dotenv import load_dotenv
load_dotenv(dotenv_path='config/.env')  # Load environment variables from .env

import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG for detailed logs
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize the database
        logger.info("Initializing the database...")
        init_db()
        logger.info("Database initialized successfully.")

        # Scrape bill links
        logger.info("Scraping bill links...")
        links = get_bill_links()
        logger.info(f"Found {len(links)} bill links.")

        if not links:
            logger.warning("No bill links found. Exiting the script.")
            return

        # Download bills
        logger.info("Downloading bills...")
        download_success = download_bills(links)
        if download_success:
            logger.info("All bills downloaded successfully.")
        else:
            logger.warning("Some bills failed to download.")

        # Process PDFs and perform OCR if necessary
        logger.info("Processing PDFs and extracting text...")
        process_success = process_pdfs()
        if process_success:
            logger.info("All PDFs processed and text extracted successfully.")
        else:
            logger.warning("Some PDFs failed to process.")

    except SQLAlchemyError as db_err:
        logger.error(f"Database error occurred: {db_err}")
    except FileNotFoundError as fnf_err:
        logger.error(f"File not found error: {fnf_err}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
