from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class ResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research
        fields = "__all__"

class ResearcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Researcher
        fields = "__all__"