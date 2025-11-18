import os
from dotenv import load_dotenv

def load_environment():
    load_dotenv()
    config = {
        "TREFLE_API_KEY": os.getenv("TREFLE_API_KEY"),
        "PERENUAL_API_KEY": os.getenv("PERENUAL_API_KEY"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),  # если используешь
        # добавь другие ключи по необходимости
    }
    return config