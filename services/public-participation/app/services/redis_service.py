from typing import Optional
import json
from redis import Redis
from app.core.config import settings
from app.models.models import Bill
from app.schemas.bill import Bill as BillSchema

class RedisService:
    def __init__(self):
        self.redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.bill_prefix = "bill:"
        self.ttl = 3600  # 1 hour cache

    def cache_bill(self, bill: Bill):
        """Cache bill data in Redis"""
        bill_data = {
            "id": bill.id,
            "title": bill.title,
            "description": bill.description,
            "status": bill.status,
            "pdf_url": bill.pdf_url,
            "created_at": str(bill.created_at),
            "updated_at": str(bill.updated_at) if bill.updated_at else None,
        }
        self.redis.setex(
            f"{self.bill_prefix}{bill.id}",
            self.ttl,
            json.dumps(bill_data)
        )

    def get_bill(self, bill_id: int) -> Optional[dict]:
        """Get bill data from Redis cache"""
        data = self.redis.get(f"{self.bill_prefix}{bill_id}")
        if data:
            return json.loads(data)
        return None

    def invalidate_bill(self, bill_id: int):
        """Remove bill from cache"""
        self.redis.delete(f"{self.bill_prefix}{bill_id}")

    def cache_bill_list(self, bills: list[Bill], key: str):
        """Cache list of bills"""
        bills_data = [
            {
                "id": bill.id,
                "title": bill.title,
                "description": bill.description,
                "status": bill.status,
                "pdf_url": bill.pdf_url,
                "created_at": str(bill.created_at),
                "updated_at": str(bill.updated_at) if bill.updated_at else None,
            }
            for bill in bills
        ]
        self.redis.setex(key, self.ttl, json.dumps(bills_data))

    def get_bill_list(self, key: str) -> Optional[list]:
        """Get list of bills from cache"""
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return None

redis_service = RedisService()

def cache_bill(bill: Bill):
    redis_service.cache_bill(bill)

def get_cached_bill(bill_id: int) -> Optional[dict]:
    return redis_service.get_bill(bill_id)

def invalidate_cached_bill(bill_id: int):
    redis_service.invalidate_bill(bill_id)

def cache_bill_list(bills: list[Bill], key: str):
    redis_service.cache_bill_list(bills, key)

def get_cached_bill_list(key: str) -> Optional[list]:
    return redis_service.get_bill_list(key) 