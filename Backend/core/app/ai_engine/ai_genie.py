from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_ollama import OllamaLLM

from .tools import FindEventTool, FindResearcherTool, FindResearchTool, ListEventsTool, ListResearchersTool, ListResearchTool
from app.ai_engine import consts


class AIGenie():
    def __init__(self, memory : ConversationBufferMemory) -> None:
        self.llm = OllamaLLM(model="llama3.1", temperature=0)

        self.tools = [FindResearcherTool(), FindEventTool(), FindResearchTool(), ListEventsTool(), ListResearchersTool(), ListResearchTool()]

        self.memory = memory
        
    def _handle_parsing_error(error: Exception, input_text: str) -> str:
        return """Add missing double quotas"""

    def run(self, user_input : str):
        agent = initialize_agent(tools=self.tools, 
                                 llm=self.llm, 
                                 memory=self.memory, 
                                 verbose=True, 
                                 agent="chat-conversational-react-description",
                                 handle_parsing_errors=consts.HANDLE_PARSING_ERROR_PROMPT,
                                 agent_kwargs={"system_message": consts.SYSTEM_PROMPT})
        
        ai_response = agent.run(user_input)
        return ai_response