from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


def load_llm():
    """Создаёт настроенный ChatOpenAI клиент для всех узлов"""
    load_dotenv()

    base_url = os.getenv("LITELLM_BASE_URL")
    api_key = os.getenv("LITELLM_API_KEY")
    model = os.getenv("MODEL_NAME")

    llm = ChatOpenAI(
        base_url=base_url,
        api_key=api_key,
        model=model,
        streaming=True,   # streaming=True можно включить позже
        temperature=0.0
    )

    return llm