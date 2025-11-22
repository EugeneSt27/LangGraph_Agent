# utils/search_api.py
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

async def search_web(query: str) -> str:
    """
    Реальный поиск через Tavily API.
    Возвращает текстовое summary.
    """
    if not TAVILY_API_KEY:
        return f"No Tavily API key. Cannot search: {query}"

    url = "https://api.tavily.com/search"

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "n_tokens": 2048,
    }

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()

    # Собираем краткое summary
    chunks = []
    for item in data.get("results", []):
        snippet = item.get("content") or item.get("title") or ""
        if snippet:
            chunks.append(snippet)

    if not chunks:
        return "Search returned no useful results."

    return "\n".join(chunks[:4])  # берём первые 4 фрагмента
