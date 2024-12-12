# pdf_processor.py

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

import os
import logging
import pytesseract
from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
from sqlalchemy.exc import SQLAlchemyError
from .database_setup import SessionLocal, Bill, engine

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pdf_processor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

DOWNLOAD_DIR = "bills_pdfs"
PROCESSED_DIR = "processed_bills"

def is_scanned_pdf(pdf_path):
    try:
        text = extract_text(pdf_path, maxpages=1)
        return not bool(text.strip())
    except Exception as e:
        logger.warning(f"Could not determine if PDF is scanned: {e}")
        return True

def extract_text_with_ocr(pdf_path):
    try:
        pages = convert_from_path(pdf_path)
    except Exception as e:
        logger.error(f"Error converting PDF to images: {e}")
        return ""

    text = ""
    for page_number, page in enumerate(pages, start=1):
        logger.info(f"Performing OCR on page {page_number} of {pdf_path}")
        try:
            page_text = pytesseract.image_to_string(page, lang='eng')
            text += page_text + "\n"
        except Exception as e:
            logger.error(f"OCR error on page {page_number}: {e}")
    return text

def extract_text_from_pdf(pdf_path):
    if is_scanned_pdf(pdf_path):
        logger.info(f"{pdf_path} is a scanned PDF. Using OCR.")
        return extract_text_with_ocr(pdf_path)
    else:
        logger.info(f"{pdf_path} is a text-based PDF. Extracting text.")
        try:
            return extract_text(pdf_path)
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {e}")
            return ""

def process_pdfs():
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)
        logger.debug(f"Created processed bills directory at {PROCESSED_DIR}.")

    session = SessionLocal()
    # Fetch bills where text_content is empty or None
    bills = session.query(Bill).filter(
        (Bill.text_content == "") | (Bill.text_content == None)
    ).all()

    logger.info(f"Processing {len(bills)} bills with no extracted text.")

    for bill in bills:
        pdf_path = bill.file_path  # Updated from pdf_path to file_path
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file does not exist: {pdf_path}. Deleting bill from database.")
            try:
                session.delete(bill)
                session.commit()
                logger.info(f"Deleted bill '{bill.title}' due to missing PDF file.")
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Failed to delete bill '{bill.title}': {e}")
            continue

        text = extract_text_from_pdf(pdf_path)
        if text.strip():
            bill.text_content = text
            # Save the text to a file
            text_filename = os.path.join(
                PROCESSED_DIR,
                f"{os.path.splitext(os.path.basename(pdf_path))[0]}.txt"
            )
            try:
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                logger.info(f"Processed and saved text for '{bill.title}'.")
            except Exception as e:
                logger.error(f"Error writing text file {text_filename}: {e}")
                continue

            try:
                session.commit()
                logger.debug(f"Updated text_content for '{bill.title}' in the database.")
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Database error while updating '{bill.title}': {e}")
        else:
            logger.warning(f"No text extracted for '{bill.title}'. Deleting from database.")
            try:
                session.delete(bill)
                session.commit()
                logger.info(f"Deleted bill '{bill.title}' due to no extracted text.")
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Failed to delete bill '{bill.title}': {e}")

    session.close()
    logger.info("Completed PDF processing and OCR.")

if __name__ == "__main__":
    process_pdfs()
