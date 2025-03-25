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
    # events endpoints
    path('events/', view = EventsEndpoint.as_view()),
    path('events/<int:id>/', view = EventByID.as_view()),
]