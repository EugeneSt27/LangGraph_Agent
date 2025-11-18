import json
import re
from typing import Any

from langchain_core.messages import SystemMessage, HumanMessage
from models.planner_models import DiagnosisPlan


SYSTEM_PROMPT = """
Ты — лучший планировщик-аналитик, задача которого — строго извлечь из пользовательского текста
информацию о растении и связанных симптомах. ВАЖНО:
1) Извлекай ТОЛЬКО ту информацию, которая явно указана пользователем.
2) НЕЛЬЗЯ придумывать названия растений, симптомы или степень тяжести.
3) Если какое-то поле не указано — верни null (или пустой список для symptoms).
4) Верни ТОЛЬКО валидный JSON, соответствующий схеме:
{
  "plant_name": string | null,
  "symptoms": [string],
  "severity": string | null,
  "additional_notes": string | null
}
Ни в коем случае не добавляй поясняющий текст - нужен ТОЛЬКО JSON по схеме выше.
"""

class PlannerNode:
    """
    Асинхронный узел-планировщик.
    Принимает: user_text (str), llm (LangChain LLM объект, у которого есть .ainvoke)
    Возвращает: экземпляр DiagnosisPlan (pydantic)
    """

    def __init__(self, llm):
        self.llm = llm

    async def run(self, user_text: str) -> DiagnosisPlan:
        """
        Основная точка входа (асинхронная).
        Отправляет system + user message в llm через ainvoke и ожидает строгий JSON.
        Валидирует JSON через Pydantic и возвращает объект.
        """
        system_msg = SystemMessage(content=SYSTEM_PROMPT)
        human_msg = HumanMessage(content=user_text)

        # Асинхронный вызов LLM
        response = await self.llm.ainvoke([system_msg, human_msg])
        content = getattr(response, "content", None)
        
        # Парсим JSON
        parsed_json = self._extract_json(content)

        # Валидируем через Pydantic
        try:
            plan = DiagnosisPlan.model_validate(parsed_json)
        except Exception as e:
            raise ValueError(f"PlannerNode: failed to validate JSON from LLM. Error: {e}\nRaw LLM output:\n{content}")

        return plan

    def _extract_json(self, raw_text: str) -> Any:
        """
        Надёжно вытащить JSON из текста LLM.
        Ищем первую '{' и последний '}', затем json.loads.
        Дополнительно делаем простую «очистку» от лишних символов.
        """
        if not raw_text:
            raise ValueError("Empty LLM response")

        start = raw_text.find("{")
        end = raw_text.rfind("}")
        # Если не нашли, пробуем регулярку
        if start == -1 or end == -1 or start > end:
            # \{ начало JSON, (?:.|\s)* — любой символ или пробелы внутри, \} конец JSON
            match = re.search(r"(\{(?:.|\s)*\})", raw_text)
            if match:
                json_text = match.group(1)
            else:
                raise ValueError(f"Could not find JSON object in LLM output: {raw_text}")
        else:
            json_text = raw_text[start:end+1]

        try:
            parsed = json.loads(json_text)
        except json.JSONDecodeError as e:
            # Иногда LLM вставляет trailing commas или другие мелочи
            raise ValueError(f"JSON parse error: {e}\nJSON text was:\n{json_text}\nFull LLM output:\n{raw_text}")

        return parsed