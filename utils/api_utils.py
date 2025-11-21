import os
import httpx
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed
from urllib.parse import quote


load_dotenv()

TREFLE_API_KEY = os.getenv("TREFLE_API_KEY")
PERENUAL_API_KEY = os.getenv("PERENUAL_API_KEY")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    """
    Делает запрос к Trefle и возвращает JSON первого найденного растения.
    Использует retry, чтобы обрабатывать сетевые ошибки.
    """
async def fetch_trefle(plant_name: str):
    query = quote(plant_name)

    url = f"https://trefle.io/api/v1/plants/search?q={query}&token={TREFLE_TOKEN}"

    try:
        r = await client.get(url, timeout=30)
        data = r.json()

        # если данные есть → всё готово
        if data.get("data"):
            return data["data"][0]

        # fallback — поиск по роду
        genus = plant_name.split()[0]
        url2 = f"https://trefle.io/api/v1/plants/search?q={genus}&token={TREFLE_TOKEN}"
        r2 = await client.get(url2, timeout=30)
        data2 = r2.json()
        if data2.get("data"):
            return data2["data"][0]

        return None
    except Exception as e:
        print("TREFLE ERROR:", e)
        return None

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