from pydantic import BaseModel, Field
from typing import Optional

class TwilioWebhookRequest(BaseModel):
    MessageSid: str = Field(..., description="The unique identifier of the message")
    From: str = Field(..., description="The phone number that sent the message")
    To: str = Field(..., description="The phone number that received the message")
    Body: str = Field(..., description="The text body of the message")
    NumMedia: Optional[int] = Field(0, description="Number of media attachments")
    WaId: Optional[str] = Field(None, description="The WhatsApp ID of the sender")
    ProfileName: Optional[str] = Field(None, description="The sender's WhatsApp profile name")
    Timestamp: Optional[str] = Field(None, description="The time the message was sent")

class TwilioStatusCallback(BaseModel):
    MessageSid: str = Field(..., description="The unique identifier of the message")
    MessageStatus: str = Field(..., description="The status of the message")
    From: str = Field(..., description="The phone number that sent the message")
    To: str = Field(..., description="The phone number that received the message")
    ErrorCode: Optional[str] = Field(None, description="Error code if message failed")
    ErrorMessage: Optional[str] = Field(None, description="Error message if message failed") 