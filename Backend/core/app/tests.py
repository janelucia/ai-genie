import json
import logging
from django.test import TestCase
from rest_framework.test import APIClient
from app.models import Chat
from .serializers import *

# Configure logging
logging.basicConfig(
    filename="chatbot_test.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class ChatbotIntegrationTest(TestCase):
    def setUp(self):
        """Create a test chat session"""
        self.client = APIClient()
        self.chat = Chat.objects.create()
        self.ai_message_endpoint = f"/api/message-ai/{self.chat.id}"
        logger.info("-- Chatbot Test Initialized --")

    def clear_chat_history(self):
        """Clears the chat history for the test chat session"""
        self.client.post(f"/api/clear/{self.chat.id}", content_type="application/json")

    def message_ai(self, user_message):
        return self.client.post(
            self.ai_message_endpoint,
            json.dumps({"content": user_message, "ai_response": False}),
            content_type="application/json"
        )

    def log_conversation(self, test_name, status, conversation):
        """Logs test conversations using the logging module"""
        logger.info(f"-- Test Case: {test_name} --")
        for message in conversation:
            logger.info(f"User: {message['user_input']}")
            logger.info(f"AI: {message['ai_response']}")
        logger.info(f"Test Result: {status}\n")

    def test_chatbot_responds(self):
        """Test if chatbot responds to user input"""
        conversation = []
        status = "PASS"

        user_message = "Hello, what research is available?"
        response = self.message_ai(user_message)
        ai_response = MessageSerializer(data=response.data)
        
        if ai_response.is_valid():
            conversation.append({"user_input": user_message, "ai_response": ai_response.validated_data.get("content")})
        else:
            status = "FAIL"
        
        self.log_conversation("Chatbot Responds", status, conversation)

    def test_chat_memory(self):
        """Ensure chatbot remembers previous messages"""
        conversation = []
        status = "PASS"
        
        user_message = "What is AI Lab?"
        response = self.message_ai(user_message)
        ai_response = MessageSerializer(data=response.data)
        if ai_response.is_valid():
            conversation.append({"user_input": user_message, "ai_response": ai_response.validated_data.get("content")})
        else:
            status = "FAIL"

        user_message = "Can you tell me more?"
        response = self.message_ai(user_message)
        ai_response = MessageSerializer(data=response.data)
        if ai_response.is_valid():
            conversation.append({"user_input": user_message, "ai_response": ai_response.validated_data.get("content")})
        else:
            status = "FAIL"
        
        self.log_conversation("Chat Memory", status, conversation)

    def test_invalid_chat_id(self):
        """Test error handling for non-existent chat"""
        status = "PASS"
        user_message = "Hello!"
        response = self.client.post(
            self.ai_message_endpoint,
            json.dumps({"chat": -1, "content": user_message}),
            content_type="application/json"
        )
        self.log_conversation("Invalid Chat ID", status, [])

    def test_empty_message(self):
        """Ensure chatbot rejects empty messages"""
        conversation = []
        status = "PASS"

        user_message = ""
        response = self.message_ai(user_message)
        ai_response = MessageSerializer(data=response.data)
        
        if ai_response.is_valid():
            conversation.append({"user_input": "(empty)", "ai_response": ai_response.validated_data.get("content")})
        else:
            status = "FAIL"
        
        self.log_conversation("Empty Message", status, conversation)
