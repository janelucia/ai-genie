from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from ..models import Researcher, Event, Research

#_________________RESEARCHERS TOOLS_________________

class FindResearcherInput(BaseModel):
    name: str = Field(description="The name of the researcher (firstname or surname)")

class FindResearcherTool(BaseTool):
    name : str = "FindResearcher"
    description : str  = "Finds a researcher by name in the database."
    args_schema : Type[BaseModel] = FindResearcherInput

    def _run(self, name: str):
        name_parts = name.strip().split()

        if len(name_parts) == 2:
            firstname, surname = name_parts
            researchers = Researcher.objects.filter(firstname__icontains=firstname, surname__icontains=surname)
        else:
            researchers = Researcher.objects.filter(firstname__icontains=name) | Researcher.objects.filter(surname__icontains=name)

        if not researchers.exists():
            return "No researcher found."
        return [{"id": r.id, "name": f"{r.firstname} {r.surname}"} for r in researchers]
    
#_________________EVENTS TOOLS_________________

class FindEventInput(BaseModel):
    name: str = Field(description="The name of the event")

class FindEventTool(BaseTool):
    name : str = "FindEvent"
    description : str  = "Finds an event by name in the database."
    args_schema : Type[BaseModel] = FindEventInput

    def _run(self, name: str):
        events = Event.objects.filter(name__icontains=name)
        if not events.exists():
            return "No event found."
        return [{"id": e.id, "name": e.name, "date": e.date} for e in events]
    

#_________________RESEARCH TOOLS_________________

class FindResearchInput(BaseModel):
    name: str = Field(description="The name of the research paper")

class FindResearchTool(BaseTool):
    name : str  = "FindResearch"
    description : str = "Finds research by name in the database."
    args_schema : Type[BaseModel] = FindResearchInput

    def _run(self, name: str):
        research = Research.objects.filter(name__icontains=name)
        if not research.exists():
            return "No research found."
        return [{"id": r.id, "name": r.name, "summary": r.summary} for r in research]

