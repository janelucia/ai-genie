from langchain.tools import BaseTool
from typing import Dict, Tuple, Type, Optional, Union
from pydantic import BaseModel, Field
from ..models import Researcher, Event, Research
from rapidfuzz import process
from app.ai_engine import consts
from app.ai_engine.vector_db_service import VectorDatabaseService


class EmptyInput(BaseModel):
    arg : str = Field(description="Should be empty")
    pass

#_________________RESEARCHERS TOOLS_________________

class FindResearcherInput(BaseModel):
    name: str = Field(description="The name of the researcher (firstname or surname)")

class FindResearcherTool(BaseTool):
    name : str = "FindResearcher"
    description : str  = "Finds a researcher by firstname, surname or both in the database. Also used when user asks about research that the person performs or when user wants to know more about researcher"
    args_schema : Type[BaseModel] = FindResearcherInput

    def _run(self, name: str): # could be changed to include rapidfuzz
        name_parts = name.strip().split()

        if len(name_parts) == 2:
            firstname, surname = name_parts
            researchers = Researcher.objects.filter(firstname__icontains=firstname, surname__icontains=surname)
        else:
            researchers = Researcher.objects.filter(firstname__icontains=name) | Researcher.objects.filter(surname__icontains=name)

        if not researchers.exists():
            return "No researcher found."
        
        result = []
        for r in researchers:
            research_names = [research.name for research in r.related_research.all()]
            result.append({"name": f"{r.firstname} {r.surname}", "research": research_names})
        
        
        return result
    
class ListResearchersTool(BaseTool):
    name : str = "ListResearchers"
    description : str = "Lists all researchers. Usefull when user wants to know what researchers work for ai Lab"
    args_schema: Type[BaseModel] = EmptyInput

    def _run(self, arg):
        researchers = Researcher.objects.all()
        if not researchers.exists():
            return "No events are happening in the future."
        
        researchers_to_return = [f"{res.firstname} {res.surname}" for res in researchers]
        return researchers_to_return
    
#_________________EVENTS TOOLS_________________

class FindEventInput(BaseModel):
    name: str = Field(description="The name of the event")

class FindEventTool(BaseTool):
    name : str = "FindEvent"
    description : str  = "Finds an event by name in the database."
    args_schema : Type[BaseModel] = FindEventInput

    def _run(self, name: str):
        name = name.strip("'")
        events_list = Event.objects.all()
        events_name_list =[event.name for event in events_list]

        result = process.extractOne(name, events_name_list, score_cutoff=10)

        if result is None:
            return "No research found."

        _, _, index = result
        best_event = events_list[index]

        return [{"name": best_event.name, "date": best_event.date}]
    
class ListEventsTool(BaseTool):
    name : str = "ListEvents"
    description : str = "Lists all events. Use if user wants to know what events are happening at AI Lab."
    args_schema: Type[BaseModel] = EmptyInput

    def _run(self, arg):
        events = Event.objects.all().values("name", "date")
        if not events.exists():
            return "No events found."
        
        return events
    
#_________________RESEARCH TOOLS_________________

class FindResearchInput(BaseModel):
    title: str = Field(description="The title of the research paper without quotations")

class FindResearchTool(BaseTool):
    name: str = "FindResearch"
    description: str = "Finds research by its title in the database, also used to find authors of the research."
    args_schema: Type[BaseModel] = FindResearchInput

    def _run(self, title: str):
        research_list = Research.objects.all()
        research_titles = [research.name for research in research_list]

        result = process.extractOne(title, research_titles, score_cutoff=10)
    
        if result is None:
            return "No research found."

        _, _, index = result
        best_research = research_list[index]
        researchers = [f"{res.firstname} {res.surname}" for res in best_research.researchers_related.all()]

        return [{"name": best_research.name, "summary": best_research.summary, "researchers": researchers}]

class ListResearchTool(BaseTool):
    name : str = "ListResearch"
    description : str = "Lists all research. Use it when user asks what research is being perfomed at ai lab"
    args_schema: Type[BaseModel] = EmptyInput

    def _run(self, arg):
        research = Research.objects.all().values("name")
        if not research.exists():
            return "No research is being performed at the moment."
        
        return research
    
class ResearchDetailsInput(BaseModel):
    context: str = Field(
        description="Provide two parts: a question and the research paper title, separated by a '|' character. For example: 'Research_Paper_Title.pdf | What is the main contribution?', do not create your own use question, cite user"
    )

class ResearchDetailsTool(BaseTool):
    name: str = "GetDetails"
    description: str = (
        "Use this tool to answer questions about details (such as results, conclusion, metholodogies) of research papers"
        "You must provide a question and the paper's title, separated by '|'."
        "If output is empty it means that research paper doesnt have an answer to the question"
    )
    args_schema: Type[BaseModel] = ResearchDetailsInput

    def extract_file_name(self, path : str):
        return path[(path.find("/")+1):]

    def _run(self, context: str):
        parts = [p.strip() for p in context.split('|', maxsplit=1)]  # clean whitespace
        if len(parts) == 2:
            research_title, user_question = parts
            research_list = Research.objects.all()
            research_titles = [research.name for research in research_list]

            result = process.extractOne(research_title, research_titles, score_cutoff=10)
            _, _, index = result
            research_title = self.extract_file_name(str(research_list[index].source_file))
        else:
            user_question = parts[0]
            research_title = None

        vector_service = VectorDatabaseService()  # Singleton or injected service
        print(f"USER QUESTION: {user_question}")
        print(f"RESEARCH PAPER: {research_title}")
        results = vector_service.find_similar(query=user_question, source=research_title, top_k=2)
        return results