import os
import httpx
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed


load_dotenv()

TREFLE_API_KEY = os.getenv("TREFLE_API_KEY")
PERENUAL_API_KEY = os.getenv("PERENUAL_API_KEY")


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def fetch_trefle(plant_name: str):
    """
    Делает запрос к Trefle и возвращает JSON первого найденного растения.
    Использует retry, чтобы обрабатывать сетевые ошибки.
    """
    url = f"https://trefle.io/api/v1/plants?token={TREFLE_API_KEY}&q={plant_name}"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, timeout=10)
        r.raise_for_status() # выброс исключения для плохих ответов

        data = r.json()

        if "data" not in data or len(data["data"]) == 0:
            return None  # ничего не найдено

        return data["data"][0]


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def fetch_perenual(plant_name: str):
    """
    Поиск растения в Perenual.
    """
    url = f"https://perenual.com/api/species-list?key={PERENUAL_API_KEY}&q={plant_name}"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, timeout=10)
        r.raise_for_status()

        data = r.json()

        if "data" not in data or len(data["data"]) == 0:
            return None

        return data["data"][0]