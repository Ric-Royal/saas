from typing import Optional, Dict
from app.models.models import IntentEnum, LanguageEnum
from app.core.config import settings
from transformers import pipeline
import spacy
import logging
from langdetect import detect

logger = logging.getLogger(__name__)

class NLPService:
    def __init__(self):
        # Initialize models
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.intent_classifier = pipeline("text-classification", model=settings.INTENT_MODEL_PATH)
        self.nlp = spacy.load("en_core_web_sm")
        self.translation_model = pipeline("translation", model=settings.TRANSLATION_MODEL_PATH)

    async def detect_language(self, text: str) -> LanguageEnum:
        try:
            lang_code = detect(text)
            return LanguageEnum(lang_code.upper())
        except Exception as e:
            logger.error(f"Error detecting language: {str(e)}")
            return LanguageEnum.ENGLISH

    async def detect_intent(self, text: str) -> Optional[IntentEnum]:
        try:
            # Preprocess text
            doc = self.nlp(text.lower())
            processed_text = " ".join([token.lemma_ for token in doc if not token.is_stop])

            # Classify intent
            result = self.intent_classifier(processed_text)[0]
            intent_name = result["label"]
            confidence = result["score"]

            # Only return intent if confidence is above threshold
            if confidence >= settings.INTENT_CONFIDENCE_THRESHOLD:
                return IntentEnum[intent_name.upper()]
            return None

        except Exception as e:
            logger.error(f"Error detecting intent: {str(e)}")
            return None

    async def analyze_sentiment(self, text: str) -> int:
        try:
            result = self.sentiment_analyzer(text)[0]
            # Convert sentiment to score between -100 and 100
            if result["label"] == "POSITIVE":
                return int(result["score"] * 100)
            else:
                return int(-result["score"] * 100)
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return 0

    async def translate_text(self, text: str, target_lang: LanguageEnum) -> str:
        try:
            if target_lang == LanguageEnum.ENGLISH:
                return text

            result = self.translation_model(text, target_language=target_lang.value.lower())[0]
            return result["translation_text"]

        except Exception as e:
            logger.error(f"Error translating text: {str(e)}")
            return text

    async def process_message(
        self,
        text: str,
        context: Optional[Dict] = None
    ) -> str:
        try:
            # Detect intent
            intent = await self.detect_intent(text)
            
            # Get response based on intent
            if intent == IntentEnum.GREETING:
                response = "Hello! How can I assist you today with civil services?"
            elif intent == IntentEnum.FAREWELL:
                response = "Goodbye! Feel free to reach out if you need assistance in the future."
            elif intent == IntentEnum.HELP:
                response = "I can help you with various civil services including:\n- Filing complaints\n- Checking application status\n- Finding nearby offices\n- Scheduling appointments"
            else:
                response = "I understand you're asking about civil services. Could you please provide more specific details about what you need help with?"

            return response

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return "I apologize, but I'm having trouble understanding your request. Could you please rephrase it?"

nlp_service = NLPService() 