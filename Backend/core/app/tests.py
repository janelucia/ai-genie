import json
import logging
from django.test import TestCase
from django.core.management import call_command
from rest_framework.test import APIClient
from app.models import Chat
from .serializers import *
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename=datetime.now().strftime("chatbot_test_%Y-%m-%d_%H:%M:%S.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class ChatbotIntegrationTest(TestCase):
    @classmethod
    def setUpTestData(self):
        """Create a db for testing"""
        call_command('loaddata', 'mock_db.json') 

    def setUp(self):
        """Create a test chat session"""
        self.client = APIClient()
        self.chat = Chat.objects.create()
        self.ai_message_endpoint = f"/api/message-ai/{self.chat.id}/"
        test_name = self._testMethodName
        logger.info(f"--TEST {test_name.upper()} STARTED--")

    def tearDown(self):
        logger.info("--TEST ENDEND--\n")

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
        logger.info(f"_________ conversation for: {test_name} _________")
        for message in conversation:
            logger.info(f"User: {message['user_input']}")
            logger.info(f"AI: {message['ai_response']}")
        logger.info(f"Test Result: {status}")
        logger.info("_________ end of conversation _________")

    def test_chatbot_responds(self):
        """Test if chatbot responds to user input"""
        conversation = []
        status = "PASS"
        self.clear_chat_history()

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
        self.clear_chat_history()
        
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

    def test_ask_about_researcher(self):
        """Tests if chatbot can find researcher based on the exact name"""
        conversation = []
        status = "PASS"
        self.clear_chat_history()
        
        user_message = "Who is Mia Martin?"
        response = self.message_ai(user_message)
        ai_response = MessageSerializer(data=response.data)
        if ai_response.is_valid():
            conversation.append({"user_input": user_message, "ai_response": ai_response.validated_data.get("content")})
        else:
            status = "FAIL"

        self.log_conversation("Ask Abt Researcher", status, conversation)

    def test_ask_about_researcher_wrong_name(self):
        """Tests if chatbot can find researcher based on the misspealed name"""
        conversation = []
        status = "PASS"
        self.clear_chat_history()
        
        user_message = "Who is Mio Marton?"
        response = self.message_ai(user_message)
        ai_response = MessageSerializer(data=response.data)
        if ai_response.is_valid():
            conversation.append({"user_input": user_message, "ai_response": ai_response.validated_data.get("content")})
        else:
            status = "FAIL"

        self.log_conversation("Misspealled Researcher", status, conversation)

    def test_ask_about_researcher_from_memory(self):
        """Tests if chatbot can find information about researcher from memory context"""
        conversation = []
        status = "PASS"
        self.clear_chat_history()
        
        user_message = "Could you tell me what researchers there are at OsloMet?"
        response = self.message_ai(user_message)
        ai_response = MessageSerializer(data=response.data)
        if ai_response.is_valid():
            conversation.append({"user_input": user_message, "ai_response": ai_response.validated_data.get("content")})
        else:
            status = "FAIL"

        user_message = "I want to know more about Emily"
        response = self.message_ai(user_message)
        ai_response = MessageSerializer(data=response.data)
        if ai_response.is_valid():
            conversation.append({"user_input": user_message, "ai_response": ai_response.validated_data.get("content")})
        else:
            status = "FAIL"

        self.log_conversation("Ask Abt Researcher Memory", status, conversation)

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
