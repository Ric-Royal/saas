# scraper.py

import requests
from bs4 import BeautifulSoup
import os
import logging
from urllib.parse import urljoin, urlparse
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError
from .database_setup import SessionLocal, Bill
import requests

from dotenv import load_dotenv
load_dotenv(dotenv_path='config/.env')  # Load environment variables from .env

import os
import logging
from .database_setup import SessionLocal, Bill

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://kenyalaw.org/kl/index.php?id=12043"
DOWNLOAD_DIR = "bills_pdfs"

def get_bill_links():
    try:
        response = requests.get(BASE_URL, timeout=10)
        response.raise_for_status()
    except RequestException as e:
        logger.error(f"Failed to retrieve the page: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    bill_links = []

    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text().strip().lower()
        if 'pdf' in href.lower() or 'bill' in text:
            full_url = urljoin(BASE_URL, href)
            bill_links.append(full_url)

    return bill_links

def sanitize_filename(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    # Remove any query parameters
    filename = filename.split('?')[0]
    return filename

def download_bills(bill_links):
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    session = SessionLocal()

    for link in bill_links:
        filename = sanitize_filename(link)
        file_path = os.path.join(DOWNLOAD_DIR, filename)

        if not os.path.exists(file_path):
            logger.info(f"Downloading {link}")
            try:
                response = requests.get(link, timeout=10)
                response.raise_for_status()
            except RequestException as e:
                logger.error(f"Failed to download {link}: {e}")
                continue

            with open(file_path, 'wb') as f:
                f.write(response.content)

            # Add entry to the database
            bill = Bill(
                title=filename,
                url=link,
                file_path=file_path,
                text_content=""  # To be filled after processing
            )
            try:
                session.add(bill)
                session.commit()
                logger.info(f"Added {filename} to the database.")
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Database error for {filename}: {e}")
        else:
            logger.info(f"File {file_path} already exists. Skipping.")

    session.close()

if __name__ == "__main__":
    links = get_bill_links()
    logger.info(f"Found {len(links)} bills.")
    download_bills(links)
    logger.info("Downloaded bills and updated the database.")
