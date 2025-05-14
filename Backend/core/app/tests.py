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
    filename=datetime.now().strftime("chatbot_test_%Y_%m-%d_%H-%M-%S.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class ChatbotIntegrationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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
        logger.info("--TEST ENDED--\n")

    def clear_chat_history(self):
        """Clears the chat history for the test chat session"""
        self.client.post(f"/api/clear/{self.chat.id}", content_type="application/json")

    def message_ai(self, user_message):
        return self.client.post(
            self.ai_message_endpoint,
            json.dumps({"content": user_message, "ai_response": False}),
            content_type="application/json"
        )

    def send_and_validate(self, user_message, conversation):
        response = self.message_ai(user_message)
        ai_response = MessageSerializer(data=response.data)
        if ai_response.is_valid():
            ai_response_content = ai_response.validated_data.get("content")
            conversation.append({"user_input": user_message, "ai_response": ai_response_content})
            return ai_response_content, "PASS"
        return None, "FAIL"

    def log_conversation(self, test_name, status, conversation):
        """Logs test conversations using the logging module"""
        logger.info(f"_________ conversation for: {test_name} _________")
        for message in conversation:
            logger.info(f"User: {message['user_input']}")
            logger.info(f"AI: {message['ai_response']}")
        logger.info(f"Test Result: {status}")
        logger.info("_________ end of conversation _________")

    # ---------------- BASIC FUNCTIONALITY TESTS ----------------

    def test_chatbot_responds(self):
        conversation = []
        status = "PASS"
        self.clear_chat_history()

        user_message = "Hello, what research is available?"
        _, status = self.send_and_validate(user_message, conversation)

        self.log_conversation("[Basic] Chatbot Responds", status, conversation)

    def test_chat_memory(self):
        conversation = []
        status = "PASS"
        self.clear_chat_history()

        messages = [
            "What is AI Lab?",
            "Can you tell me more?"
        ]
        for user_message in messages:
            _, status = self.send_and_validate(user_message, conversation)
            if status == "FAIL":
                break

        self.log_conversation("[Basic] Chat Memory", status, conversation)

    def test_invalid_chat_id(self):
        status = "PASS"
        user_message = "Hello!"
        response = self.client.post(
            self.ai_message_endpoint,
            json.dumps({"chat": -1, "content": user_message}),
            content_type="application/json"
        )
        self.log_conversation("[Basic] Invalid Chat ID", status, [])

    # ---------------- RESEARCHER-RELATED TESTS ----------------

    def test_ask_about_researcher(self):
        conversation = []
        status = "PASS"
        self.clear_chat_history()

        user_message = "Who is Mia Martin?"
        _, status = self.send_and_validate(user_message, conversation)

        self.log_conversation("[Researcher] Ask About Researcher", status, conversation)

    def test_ask_about_researcher_wrong_name(self):
        conversation = []
        status = "PASS"
        self.clear_chat_history()

        user_message = "Who is Mia Marton?"
        _, status = self.send_and_validate(user_message, conversation)

        self.log_conversation("[Researcher] Misspelled Researcher", status, conversation)

    def test_ask_about_researcher_from_memory(self):
        conversation = []
        status = "PASS"
        self.clear_chat_history()

        messages = [
            "Could you tell me what researchers there are at OsloMet?",
            "I want to know more about Emily"
        ]
        for user_message in messages:
            _, status = self.send_and_validate(user_message, conversation)
            if status == "FAIL":
                break

        self.log_conversation("[Researcher] Researcher from Memory", status, conversation)

    def test_list_researchers(self):
        conversation = []
        status = "PASS"
        self.clear_chat_history()

        user_message = "Can you tell me what researchers work here?"
        _, status = self.send_and_validate(user_message, conversation)

        self.log_conversation("[Researcher] List Researchers", status, conversation)

    # ---------------- EVENT-RELATED TESTS ----------------

    def test_find_event_wrong_name(self):
        conversation = []
        status = "PASS"
        self.clear_chat_history()

        user_message = "I am looking for AI Conference"
        _, status = self.send_and_validate(user_message, conversation)

        self.log_conversation("[Event] Find Event", status, conversation)

    def test_find_event(self):
        conversation = []
        status = "PASS"
        self.clear_chat_history()

        user_messages = [
            "I am looking for Blockchain & Finance Summit",
            "How can I cntact organiser?"]
        for msg in user_messages:
            _, status = self.send_and_validate(msg, conversation)

        self.log_conversation("[Event] Find Event", status, conversation)

    def test_event_on_specific_day(self):
        conversation = []
        status = "PASS"
        self.clear_chat_history()

        user_message = "What event was happening last Tuesday?"
        _, status = self.send_and_validate(user_message, conversation)

        self.log_conversation("Event on Specific Day", status, conversation)

    def test_event_link_and_organizer_contact(self):
        conversation = []
        status = "PASS"
        self.clear_chat_history()

        messages = [
            "What event was happening last Tuesday?",
            "How can I contact organiser?"
        ]
        for user_message in messages:
            _, status = self.send_and_validate(user_message, conversation)
            if status == "FAIL":
                break

        self.log_conversation("Event Link and Organizer Contact", status, conversation)


    def test_list_events(self):
        conversation = []
        status = "PASS"
        self.clear_chat_history()

        user_message = "What events are happening?"
        _, status = self.send_and_validate(user_message, conversation)

        self.log_conversation("[Event] List Events", status, conversation)

    # ---------------- RESEARCH-RELATED TESTS ----------------

    def test_find_research(self):
        conversation = []
        status = "PASS"
        self.clear_chat_history()

        user_message = "Is there research about work ethics?"
        _, status = self.send_and_validate(user_message, conversation)

        self.log_conversation("[Research] Find Research", status, conversation)

    def test_find_non_existent_research(self):
        conversation = []
        status = "PASS"
        self.clear_chat_history()

        user_message = "Is there research about ai in turtle protection?"
        _, status = self.send_and_validate(user_message, conversation)

        self.log_conversation("[Research] Find Research", status, conversation)

    def test_list_research(self):
        conversation = []
        status = "PASS"
        self.clear_chat_history()

        user_message = "What kind of research is being performed?"
        _, status = self.send_and_validate(user_message, conversation)

        self.log_conversation("[Research] List Research", status, conversation)

    def test_research_details(self):
        conversation = []
        status = "PASS"
        self.clear_chat_history()

        user_message = "What are the conclusions of Quantum Computing research paper?"
        _, status = self.send_and_validate(user_message, conversation)

        self.log_conversation("[Research] Research Details", status, conversation)
