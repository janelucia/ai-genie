from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema

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