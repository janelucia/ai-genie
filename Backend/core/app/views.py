from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema

from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_ollama import OllamaLLM
from .ai_engine.tools import FindEventTool, FindResearcherTool, FindResearchTool

#______________Initialize things on start______________ < ---- shall be moved somewhere else

SYSTEM_PROMPT = """You are an AI assistant specialized in research retrieval and event analysis. 
Be casual as you perform this roles for guests of AI Lab
Use available tools to answer questions accurately. Maintain professionalism in responses. 
Never put research titles in quotation.
Always put action input in "" """


llm = OllamaLLM(model="mistral", temperature=0.7)  # Or use "deepseek"

# Setup memory
memory = ConversationBufferMemory(memory_key="chat_history",
                                  return_messages=True)

tools = [FindResearcherTool(), FindEventTool(), FindResearchTool()]
agent = initialize_agent(tools=tools, 
                         llm=llm,
                         memory=memory, 
                         verbose=True,
                         agent="chat-conversational-react-description",
                         agent_kwargs={"system_message": SYSTEM_PROMPT})


# Create your views here.
class Home(APIView):
    def get(self, request):
        return Response({'message': 'works!'}, status = status.HTTP_200_OK)
    
#______________EVENTS ENDPOINTS______________

class EventsEndpoint(APIView):
    def get(self, request):
        '''Lists all the events'''
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=EventSerializer)
    def post(self, request):
        '''Create a new event'''
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MultiEditEvents(APIView):
    def post(self, request):
        serializer = EventSerializer(data = request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EventByID(APIView):
    def get_object(self, id):
        try:
            return Event.objects.get(id=id)
        except Event.DoesNotExist:
            return None

    def get(self, request, id):
        event = self.get_object(id)
        if event:
            serializer = EventSerializer(event)
            return Response(serializer.data)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=EventSerializer)
    def put(self, request, id):
        event = self.get_object(id)
        if event:
            serializer = EventSerializer(event, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        event = self.get_object(id)
        if event:
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
#______________RESEARCH ENDPOINTS______________

class ResearchEndpoint(APIView):
    def get(self, request):
        '''Lists all the research'''
        research = Research.objects.all()
        serializer = ResearchSerializer(research, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=ResearchSerializer)
    def post(self, request):
        '''Create a new research 
        [for this one 'source_file' field is also mandatory but automaatic documentation doesn't support it yet]
        [source_file should be of a pdf file format of an actual research paper]'''
        serializer = ResearchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResearchByID(APIView):
    def get_object(self, id):
        try:
            return Research.objects.get(id=id)
        except Research.DoesNotExist:
            return None
    
    def get(self, request, id):
        research = self.get_object(id)
        if research:
            serializer = ResearchSerializer(research)
            return Response(serializer.data)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(request_body=ResearchSerializer)
    def put(self, request, id):
        research = self.get_object(id)
        if research:
            serializer = ResearchSerializer(research, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, id):
        research = self.get_object(id)
        if research:
            research.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

#______________RESEARCHERS ENDPOINTS______________

class ResearchersEndpoint(APIView):
    def get(self, request):
        '''Lists all the researchers'''
        researchers = Researcher.objects.all()
        serializer = ResearcherSerializer(researchers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=ResearcherSerializer)
    def post(self, request):
        '''Create a new researcher'''
        serializer = ResearcherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MultiEditResearchers(APIView):
    def post(self, request):
        serializer = ResearcherSerializer(data = request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResearcherByID(APIView):
    def get_object(self, id):
        try:
            return Researcher.objects.get(id=id)
        except Researcher.DoesNotExist:
            return None

    def get(self, request, id):
        researcher = self.get_object(id)
        if researcher:
            serializer = ResearcherSerializer(researcher)
            return Response(serializer.data)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=ResearcherSerializer)
    def put(self, request, id):
        researcher = self.get_object(id)
        if researcher:
            serializer = ResearcherSerializer(researcher, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        researcher = self.get_object(id)
        if researcher:
            researcher.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
#______________CHATS ENDPOINTS______________

class ChatsEndpoint(APIView):
    def get(self, request):
        '''Lists all the chats'''
        chats = Chat.objects.all()
        if chats.exists():
            chats_serializer = ChatSerializer(chats, many=True)
            return Response(chats_serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        '''Create a new chat'''
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatByID(APIView):
    def get_object(self, id):
        try:
            return Chat.objects.get(id=id)
        except Chat.DoesNotExist:
            return None
        
    def get(self, request, id):
        '''Gets all the messages from the chat'''
        chat = self.get_object(id)
        if chat:
            chat_serializer = ChatSerializer(chat)
            messages = Message.objects.filter(chat=chat)
            message_serializer = MessageSerializer(messages, many=True)
            return Response({
                "chat": chat_serializer.data,
                "messages": message_serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)
    
#______________MESSAGES ENDPOINTS______________

class AddMessageWithAIResponse(APIView):
    def post(self, request):
        chat_id = request.data.get("chat")  # Extract chat ID from request data

        # Check if the chat exists
        if not Chat.objects.filter(id=chat_id).exists():
            return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user_message_serializer = MessageSerializer(data=request.data)

        if user_message_serializer.is_valid():
            user_message = user_message_serializer.save()
            ai_response_content = agent.run(user_message.content)

            ai_message_data = {
                "content": ai_response_content,
                "chat": chat_id,
                "ai_response": True
            }
            ai_message_serializer = MessageSerializer(data=ai_message_data)

            if ai_message_serializer.is_valid():
                ai_message_serializer.save()  # Save AI response

                return Response(
                    {
                        "user_message": user_message_serializer.data,
                        "ai_response": ai_message_serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )

        return Response(user_message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)