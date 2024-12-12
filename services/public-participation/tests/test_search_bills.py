# test_search_bills.py

from scripts.database_setup import SessionLocal, Bill

def test_search_bills():
    session = SessionLocal()
    try:
        query = "TheTechnopolisBill_2024.pdf"  # Example query
        bills = session.query(Bill).filter(Bill.title.ilike(f"%{query}%")).all()
        if not bills:
            print("No matching bills found.")
            return
        for bill in bills:
            print(f"Title: {bill.title}")
            print(f"Text Content: {bill.text_content[:100]}...")  # Display first 100 chars
            print("-" * 40)
    finally:
        session.close()

if __name__ == "__main__":
    test_search_bills()
