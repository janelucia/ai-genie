from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class ResearcherSerializer(serializers.ModelSerializer):
    related_research = serializers.SerializerMethodField()

    class Meta:
        model = Researcher
        fields = ["id", "firstname", "surname", "img", "position", "about", "email", "linkedin", "keywords", "related_research"]
    
    def get_related_research(self, obj):
        return list(obj.related_research.values("id", "name", "summary", "source_file"))

class ResearchSerializer(serializers.ModelSerializer):
    researchers_related = serializers.SerializerMethodField()
    
    class Meta:
        model = Research
        fields = ["id", "name", "summary", "source_file", "keywords", "researchers_related"]
    
    def get_researchers_related(self, obj):
        return list(obj.researchers_related.values("id", "firstname", "surname", "img"))

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

# Non Model Serializers

class EmailSerializer(serializers.Serializer):
    address = serializers.EmailField(required=True)
    subject = serializers.CharField(max_length=255, required=True)
    message = serializers.CharField(required=True)
