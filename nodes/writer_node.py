import json
from langchain_core.messages import SystemMessage, HumanMessage
from models.diagnosis_models import DiagnosisDraft

SYSTEM_PROMPT = """
Ты — эксперт по комнатным растениям. 
На основе структурированного диагноза подготовь:

1) Красивый, читабельный текст для обычного пользователя:
   - дружелюбный тон
   - чёткие шаги
   - пояснения
   - без JSON, только текст

2) После текста выведи строку:
   ---
   JSON:
   <сюда помести тот же самый JSON, что был передан тебе>

Не добавляй других комментариев.
"""

class WriterNode:
    def __init__(self, llm):
        self.llm = llm

    async def run(self, plant_name: str, symptoms: list, diagnosis: DiagnosisDraft):
        """
        Вход:
         - имя растения
         - симптомы
         - DiagnosisDraft объект
        
        Выход:
         - строка (красивый текст + JSON)
        """
        payload = {
            "plant_name": plant_name,
            "symptoms": symptoms,
            "diagnosis": diagnosis.model_dump()
        }

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=json.dumps(payload, ensure_ascii=False, indent=2))
        ]

        response = await self.llm.ainvoke(messages)
        return response.content
