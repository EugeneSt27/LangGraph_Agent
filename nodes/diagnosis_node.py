import json
from langchain_core.messages import SystemMessage, HumanMessage
from models.diagnosis_models import DiagnosisDraft
from utils.search_api import search_web  # реальный поисковый инструмент

SYSTEM_PROMPT = """
Ты — диагност растений. У тебя есть данные из двух API: Trefle и Perenual.
Твоя задача:

1. Оцени релевантность каждого API-ответа от 0 до 1.
2. Если обе оценки ниже 0.5, запроси действие Action:
   {"tool_call": {"name": "search_web", "input": "<запрос>"}}

3. После получения observation сформируй итоговый диагноз:

Формат финального ответа (строго JSON):
{
  "summary": "...",
  "possible_causes": ["..."],
  "recommended_actions": ["..."],
  "confidence": 0.0
}
"""

def extract_json(text: str):
    start = text.find("{")
    end = text.rfind("}")
    return json.loads(text[start:end+1])

class DiagnosisNode:
    def __init__(self, llm):
        self.llm = llm

    async def run(self, plant_name, symptoms, trefle_data, perenual_data):
        # Состояние
        payload = {
            "plant_name": plant_name,
            "symptoms": symptoms,
            "trefle_data": trefle_data,
            "perenual_data": perenual_data,
        }

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=json.dumps(payload, ensure_ascii=False))
        ]

        # Первый шаг: LLM решает, нужны ли инструменты
        resp = await self.llm.ainvoke(messages)
        content = resp.content.strip()

        try:
            data = extract_json(content)
        except:
            raise ValueError("LLM did not return JSON: " + content)

        # Если LLM запросил инструмент
        if "tool_call" in data:
            tool = data["tool_call"]
            if tool["name"] != "search_web":
                raise ValueError("Unknown tool: " + tool["name"])
            
            query = tool["input"]

            # РЕАЛЬНЫЙ поиск
            observation = await search_web(query)

            # Добавляем observation в историю
            messages.append(HumanMessage(content=f"Observation: {observation}"))

            # Второй вызов LLM — итоговый диагноз
            final_resp = await self.llm.ainvoke(messages)
            final_json = extract_json(final_resp.content.strip())
            return DiagnosisDraft(**final_json)

        # Если инструмент не нужен — финальный диагноз уже есть
        return DiagnosisDraft(**data)
