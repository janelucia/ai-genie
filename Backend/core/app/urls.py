from django.urls import path
from .views import *

urlpatterns = [
    path('home/', view = Home.as_view()),
    # research endpoints
    path('research/', view = ResearchEndpoint.as_view()),
    path('research/<int:id>/', view = ResearchByID.as_view()),
    # researchers endpoints
    path('researchers/', view = ResearchersEndpoint.as_view()),
    path('researchers/<int:id>/', view = ResearcherByID.as_view()),
    path('multi-edit-researchers/', view = MultiEditResearchers.as_view()),
    # events endpoints
    path('events/', view = EventsEndpoint.as_view()),
    path('events/<int:id>/', view = EventByID.as_view()),
    path('multi-edit-events/', view = MultiEditEvents.as_view()),
    # chats endpoints
    path('chats/', view = ChatsEndpoint.as_view()),
    path('chats/<int:id>/', view = ChatByID.as_view()),
    # messages endpoints
    path('message-ai/', view = AddMessageWithAIResponse.as_view()),
]