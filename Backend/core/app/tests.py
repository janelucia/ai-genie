import json
from django.test import TestCase
from rest_framework.test import APIClient
from app.models import Chat

class ChatbotIntegrationTest(TestCase):
    def setUp(self):
        """Create a test chat session and setup report file"""
        self.client = APIClient()
        self.chat = Chat.objects.create()
        self.report_path = "chatbot_test_report.txt"
        
        # Clear report file before running tests
        with open(self.report_path, "w") as f:
            f.write("-- Chatbot Test Report --\n\n")

    def clear_chat_history(self):
        """Clears the chat history for the test chat session"""
        self.client.post("/api/chat/clear/", json.dumps({"chat": self.chat.id}), content_type="application/json")

    def log_conversation(self, test_name, user_input, ai_response, status):
        """Logs test conversations to a text file"""
        with open(self.report_path, "a") as f:
            f.write(f"📌 Test Case: {test_name}\n")
            f.write(f"👤 User: {user_input}\n")
            f.write(f"🤖 AI: {ai_response}\n")
            f.write(f"✅ Test Result: {status}\n")
            f.write("-" * 40 + "\n")

    def test_chatbot_responds(self):
        """Test if chatbot responds to user input"""
        user_message = "Hello, what research is available?"
        response = self.client.post(
            "/api/chat/message/",
            json.dumps({"chat": self.chat.id, "content": user_message}),
            content_type="application/json"
        )

        ai_response = response.data.get("ai_response", {}).get("content", "No response")
        status = "PASS" if response.status_code == 201 and ai_response else "FAIL"
        
        self.log_conversation("Chatbot Responds", user_message, ai_response, status)
        self.assertEqual(response.status_code, 201)

    def test_chat_memory(self):
        """Ensure chatbot remembers previous messages"""
        self.client.post(
            "/api/chat/message/",
            json.dumps({"chat": self.chat.id, "content": "What is AI Lab?"}),
            content_type="application/json"
        )

        user_message = "Can you tell me more?"
        response = self.client.post(
            "/api/chat/message/",
            json.dumps({"chat": self.chat.id, "content": user_message}),
            content_type="application/json"
        )

        if response:
            ai_response = response.data.get("ai_response", {}).get("content", "No response")
            status = "PASS" if "AI Lab" in ai_response else "FAIL"
        else:
            status = "FAIL"

        self.log_conversation("Chat Memory", user_message, ai_response, status)
        self.assertIn("AI Lab", ai_response)

    def test_invalid_chat_id(self):
        """Test error handling for non-existent chat"""
        user_message = "Hello!"
        response = self.client.post(
            "/api/chat/message/",
            json.dumps({"chat": 9999, "content": user_message}),
            content_type="application/json"
        )

        ai_response = response.data.get("error", "No response")
        status = "PASS" if response.status_code == 404 else "FAIL"
        
        self.log_conversation("Invalid Chat ID", user_message, ai_response, status)
        self.assertEqual(response.status_code, 404)

    def test_empty_message(self):
        """Ensure chatbot rejects empty messages"""
        user_message = ""
        response = self.client.post(
            "/api/chat/message/",
            json.dumps({"chat": self.chat.id, "content": user_message}),
            content_type="application/json"
        )

        ai_response = response.data.get("error", "No response")
        status = "PASS" if response.status_code == 400 else "FAIL"
        
        self.log_conversation("Empty Message", "(empty)", ai_response, status)
        self.assertEqual(response.status_code, 400)
