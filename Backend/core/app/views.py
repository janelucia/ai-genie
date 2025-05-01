from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.core.mail import send_mail
from django.conf import settings

from .ai_engine.memory import create_memory
from .ai_engine.ai_genie import AIGenie
from .ai_engine.vector_db_service import VectorDatabaseService

# Create your views here.
class Home(APIView):
    def get(self, request):
        return Response({'message': 'works!'}, status = status.HTTP_200_OK)
    
#______________EVENTS ENDPOINTS______________

class EventsEndpoint(APIView):
    @swagger_auto_schema(
        operation_description="List all events",
        responses={200: EventSerializer(many=True)}
    )
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new event",
        request_body=EventSerializer,
        responses={
            201: EventSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MultiEditEvents(APIView):
    @swagger_auto_schema(
        request_body=EventSerializer(many=True),
        responses={201: EventSerializer(many=True), 400: 'Bad Request'}
    )
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

    @swagger_auto_schema(
        operation_description="Retrieve event by ID",
        responses={200: EventSerializer, 404: 'Not Found'}
    )
    def get(self, request, id):
        event = self.get_object(id)
        if event:
            serializer = EventSerializer(event)
            return Response(serializer.data)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=EventSerializer,
        responses={200: EventSerializer, 400: 'Bad Request', 404: 'Not Found'}
    )
    def put(self, request, id):
        event = self.get_object(id)
        if event:
            serializer = EventSerializer(event, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete event by ID",
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def delete(self, request, id):
        event = self.get_object(id)
        if event:
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
#______________RESEARCH ENDPOINTS______________

class ResearchEndpoint(APIView):
    @swagger_auto_schema(
        operation_description="List all research entries",
        responses={200: ResearchSerializer(many=True)}
    )
    def get(self, request):
        research = Research.objects.prefetch_related('researchers_related').all()
        serializer = ResearchSerializer(research, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description='''Create a new research 
        [for this one 'source_file' field is also mandatory but automaatic documentation doesn't support it yet]
        [source_file should be of a pdf file format of an actual research paper]''',
        request_body=ResearchSerializer,
        responses={
            201: ResearchSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = ResearchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResearchByID(APIView):
    def get_object(self, id):
        try:
            return Research.objects.prefetch_related('researchers_related').get(id=id)
        except Research.DoesNotExist:
            return None
    
    @swagger_auto_schema(
        operation_description="Retrieve research by ID",
        responses={200: ResearcherSerializer, 404: 'Not Found'}
    )
    def get(self, request, id):
        research = self.get_object(id)
        if research:
            serializer = ResearchSerializer(research)
            return Response(serializer.data)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        request_body=ResearcherSerializer,
        responses={200: ResearcherSerializer, 400: 'Bad Request', 404: 'Not Found'}
    )
    def put(self, request, id):
        research = self.get_object(id)
        if research:
            serializer = ResearchSerializer(research, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        operation_description="Delete research by ID",
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def delete(self, request, id):
        research = self.get_object(id)
        if research:
            research.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

#______________RESEARCHERS ENDPOINTS______________

class ResearchersEndpoint(APIView):
    @swagger_auto_schema(
        operation_description="List all researchers",
        responses={200: ResearcherSerializer(many=True)}
    )
    def get(self, request):
        '''Lists all the researchers'''
        researchers = Researcher.objects.prefetch_related('related_research').all()
        serializer = ResearcherSerializer(researchers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(
        request_body=ResearcherSerializer,
        responses={201: ResearcherSerializer, 400: 'Bad Request'}
    )
    def post(self, request):
        '''Create a new researcher'''
        serializer = ResearcherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MultiEditResearchers(APIView):
    @swagger_auto_schema(
        request_body=ResearcherSerializer(many=True),
        responses={201: ResearcherSerializer(many=True), 400: 'Bad Request'}
    )
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

    @swagger_auto_schema(
        operation_description="Retrieve a researcher by ID",
        responses={
            200: ResearcherSerializer,
            404: 'Not found'
        }
    )
    def get(self, request, id):
        researcher = self.get_object(id)
        if researcher:
            serializer = ResearcherSerializer(researcher)
            return Response(serializer.data)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Add a researcher",
        request_body=ResearcherSerializer,
        responses={
            200: ResearcherSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        }
    )
    def put(self, request, id):
        researcher = self.get_object(id)
        if researcher:
            serializer = ResearcherSerializer(researcher, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a researcher by ID",
        request_body=ResearcherSerializer,
        responses={
            204: 'Deleted',
            404: 'Not Found'
        }
    )
    def delete(self, request, id):
        researcher = self.get_object(id)
        if researcher:
            researcher.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
#______________CHATS ENDPOINTS______________

class ChatsEndpoint(APIView):
    @swagger_auto_schema(
        operation_description="List all chats",
        responses={200: ChatSerializer(many=True), 404: 'Not Found'}
    )
    def get(self, request):
        '''Lists all the chats'''
        chats = Chat.objects.all()
        if chats.exists():
            chats_serializer = ChatSerializer(chats, many=True)
            return Response(chats_serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        request_body=ChatSerializer,
        responses={201: ChatSerializer, 400: 'Bad Request'}
    )
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
    
    @swagger_auto_schema(
        operation_description="Retrieve a chat and its messages by ID",
        responses={200: openapi.Response(
            description="Chat and messages",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "chat": openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "created": openapi.Schema(type=openapi.TYPE_STRING),
                    }),
                    "messages": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "content": openapi.Schema(type=openapi.TYPE_STRING),
                            "chat": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "ai_response": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            "created": openapi.Schema(type=openapi.TYPE_STRING),
                        })
                    )
                }
            )
        ), 404: 'Not Found'}
    )
    def get(self, request, id):
        '''Gets all the messages from the chat'''
        chat = self.get_object(id)
        if chat:
            chat_serializer = ChatSerializer(chat)
            messages = Message.objects.filter(chat=chat).order_by("created")
            message_serializer = MessageSerializer(messages, many=True)
            return Response({
                "chat": chat_serializer.data,
                "messages": message_serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)
    
#______________MESSAGES ENDPOINTS______________

class ClearMessagesByChatID(APIView):
    @swagger_auto_schema(
        operation_description="Delete all messages in a chat",
        responses={204: 'No Content', 404: 'Chat not found'}
    )
    def delete(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)

        Message.objects.filter(chat=chat).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AddMessageWithAIResponse(APIView):
    @swagger_auto_schema(
        request_body=MessageSerializer,
        operation_description="Add a message and get an AI response",
        responses={201: MessageSerializer, 400: 'Bad Request', 404: 'Chat not found'}
    )
    def post(self, request, chat_id):
        # Check if the chat exists
        if not Chat.objects.filter(id=chat_id).exists():
            return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        data['chat'] = chat_id
        user_message_serializer = MessageSerializer(data=data)

        if user_message_serializer.is_valid():
            user_message = user_message_serializer.validated_data
            # AI stuff
            memory = create_memory(chat_id)
            ai_genie_agent = AIGenie(memory)
            ai_response_content = ai_genie_agent.run(user_message['content']) # agent being called
            ai_message_data = {
                "content": ai_response_content,
                "chat": chat_id,
                "ai_response": True
            }

            # Switch to Echo functionality if you don't have AI
#             ai_message_data = {
#                            "content": "Echo: " + user_message['content'],
#                           "chat": chat_id,
#                          "ai_response": True
#                     }

            ai_message_serializer = MessageSerializer(data=ai_message_data)

            # Saving both messages
            user_message_serializer.save()
            if ai_message_serializer.is_valid():
                ai_message_serializer.save() 

                return Response(ai_message_serializer.data, status=status.HTTP_201_CREATED)
            return Response(ai_message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(user_message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#______________EMAIL ENDPOINTS______________

class EmailView(APIView):
    @swagger_auto_schema(
        request_body=EmailSerializer,
        operation_description="Send and email through backend",
        responses={200: "{'result': 'Email sent successfully'}", 
                   400: "{'result': 'All fields are required', 'errors': 'errors'}", 
                   503: "{'result': 'Error sending', 'email: error_message'}"}
    )
    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        
        if serializer.is_valid():
            address = serializer.validated_data['address']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']

            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
                return Response({'result': 'Email sent successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'result': f'Error sending email: {e}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        return Response({'result': 'All fields are required', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


#______________FILES RETRIVAL______________

class VectorDB(APIView):
    def get(self, request):
        vectorstore = VectorDatabaseService()
        limit = request.query_params.get("limit")
        files = vectorstore.list_files(limit=limit)
        return Response(files, status=status.HTTP_200_OK)

# class TestFileRetrivalOfDocuments(APIView):
#     def get_object(self, id):
#         try:
#             return Research.objects.get(id=id)
#         except Research.DoesNotExist:
#             return None
    
#     def get(self, request, file):
#         vectorstore = VectorDatabaseService()
#         # vectorstore.drop_collection()
#         # vectorstore.add_file("rector.pdf")
#         # vectorstore.add_file("NumericalMethodsResearchPaper.pdf")
#         print("ID IN VIEW: " + str(id(vectorstore)))
#         print("________________________________")
#         results = vectorstore.file_exists(file_path=file)
#         # results = vectorstore.find_similar("What it cubic spline?", source=file, top_k=2)
#         # for i, res in enumerate(results):
#         #     print(f"\nResult {i + 1}:")
#         #     print(f"Score: {res['score']}")
#         #     print(f"Title: {res['research_title']}")
#         #     print(f"Text: {res['text']}...")
#         return Response(results, status=status.HTTP_200_OK)