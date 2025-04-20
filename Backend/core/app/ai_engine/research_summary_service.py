from langchain.llms import Ollama  # or OpenAI, etc.
from django.conf import settings

llm = Ollama(model=settings.AI_MODEL_NAME)

def summarize_text(text: str) -> str:
    print("SUMMARIZING")
    prompt = f"Summarize the following research paper in less than 500 characters, don't say here is a summary, return only summary:\n\n{text}"
    return llm(prompt).strip()

def extract_keywords(text: str) -> str:
    print("KEYWORDS")
    prompt = f"Extract 5-10 keywords from this research paper separated by commas, return only keywords separated by commas no comments:\n\n{text}"
    return llm(prompt).strip()