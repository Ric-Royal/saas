from twilio.rest import Client
from app.core.config import settings
from app.services.nlp_service import nlp_service
from app.crud.crud_conversation import crud_conversation
from app.crud.crud_user import crud_user
from app.schemas.conversation import MessageCreate
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.from_number = settings.TWILIO_PHONE_NUMBER

    async def handle_incoming_message(
        self,
        db: Session,
        from_number: str,
        message_body: str
    ):
        try:
            # Get or create user
            user = crud_user.get_by_phone(db, phone_number=from_number)
            if not user:
                user = crud_user.create(db, obj_in={
                    "phone_number": from_number,
                    "is_active": True
                })

            # Get active conversation or create new one
            conversation = crud_conversation.get_active_by_user(db, user_id=user.id)
            if not conversation:
                conversation = crud_conversation.create(db, obj_in={
                    "user_id": user.id,
                    "is_active": True
                })

            # Detect language if not set
            if not user.language_preference:
                detected_lang = await nlp_service.detect_language(message_body)
                crud_user.update(db, db_obj=user, obj_in={
                    "language_preference": detected_lang
                })

            # Process message with NLP
            intent = await nlp_service.detect_intent(message_body)
            response = await nlp_service.process_message(
                message_body,
                conversation.context
            )

            # Save user message
            crud_conversation.add_message(db, conversation_id=conversation.id, message_in=MessageCreate(
                content=message_body,
                is_bot=False,
                intent=intent
            ))

            # Save bot response
            crud_conversation.add_message(db, conversation_id=conversation.id, message_in=MessageCreate(
                content=response,
                is_bot=True
            ))

            # Send response via WhatsApp
            await self.send_message(from_number, response)

        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            # Send error message to user
            await self.send_message(
                from_number,
                "I apologize, but I'm having trouble processing your message right now. Please try again later."
            )
            raise

    async def send_message(self, to_number: str, message: str):
        try:
            self.client.messages.create(
                from_=f"whatsapp:{self.from_number}",
                body=message,
                to=f"whatsapp:{to_number}"
            )
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {str(e)}")
            raise

whatsapp_service = WhatsAppService() 