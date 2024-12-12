from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.api import deps
from app.services.whatsapp_service import whatsapp_service
from app.schemas.webhook import TwilioWebhookRequest
from app.core.security import verify_twilio_request
from typing import Dict, Any

router = APIRouter()

@router.post("/twilio")
async def twilio_webhook(
    request: TwilioWebhookRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    verified: bool = Depends(verify_twilio_request)
):
    """
    Handle incoming WhatsApp messages via Twilio webhook
    """
    if not verified:
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")

    # Process message in background
    background_tasks.add_task(
        whatsapp_service.handle_incoming_message,
        db=db,
        from_number=request.From,
        message_body=request.Body
    )

    return {"status": "processing"}

@router.post("/status")
async def status_webhook(
    data: Dict[str, Any],
    db: Session = Depends(deps.get_db),
    verified: bool = Depends(verify_twilio_request)
):
    """
    Handle message status updates from Twilio
    """
    if not verified:
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")

    # Update message status in database
    message_sid = data.get("MessageSid")
    status = data.get("MessageStatus")
    
    if message_sid and status:
        # Update message status in database
        pass

    return {"status": "updated"} 