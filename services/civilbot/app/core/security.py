from fastapi import Request, HTTPException, Depends
from twilio.request_validator import RequestValidator
from app.core.config import settings
import hmac
import hashlib
import base64
from typing import Optional

def verify_twilio_request(request: Request) -> bool:
    """
    Verify that incoming requests are from Twilio
    """
    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)

    # Get the URL and POST data
    url = str(request.url)
    post_data = request.form()
    
    # Get the X-Twilio-Signature header
    signature = request.headers.get("X-Twilio-Signature")

    return validator.validate(url, post_data, signature)

def verify_admin_token(request: Request) -> bool:
    """
    Verify admin access token
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization header")

    token = auth_header.split(" ")[1]
    
    # Verify token
    try:
        # Implement your token verification logic here
        # This is just a placeholder
        is_valid = hmac.compare_digest(
            token,
            settings.ADMIN_API_KEY
        )
        if not is_valid:
            raise HTTPException(status_code=403, detail="Invalid admin token")
        return True
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid admin token")

def get_message_signature(message: str, secret: str) -> str:
    """
    Create HMAC signature for message
    """
    return base64.b64encode(
        hmac.new(
            secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
    ).decode('utf-8') 