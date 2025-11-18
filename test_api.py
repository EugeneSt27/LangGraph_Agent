import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def test_trefle():
    url = f"https://trefle.io/api/v1/plants?token={os.getenv('TREFLE_API_KEY')}&q=ficus"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()
        print(data.keys())
        print(data["data"][0].keys())  # первые ключи внутри результата

async def test_perenual():
    url = f"https://perenual.com/api/species-list?key={os.getenv('PERENUAL_API_KEY')}&q=ficus"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()

        print("Top-level keys:", data.keys())
        # Проверяем наличие растений
        if "data" in data and len(data["data"]) > 0:
            first_plant = data["data"][0]
            print("Keys of first plant:", first_plant.keys())
        else:
            print("No plant data returned")

import asyncio
print('TREFLE')
asyncio.run(test_trefle())
print('PERENUAL')
asyncio.run(test_perenual())