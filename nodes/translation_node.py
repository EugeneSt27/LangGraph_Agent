from langchain_core.messages import SystemMessage, HumanMessage

class TranslationNode:
    """
    Узел, который переводит название растения на английский язык,
    т.к. оба API работают только с английскими названиями.
    Использует LLM для перевода одного слова или короткой фразы.
    """

    def __init__(self, llm):
        self.llm = llm

    async def run(self, plant_name: str) -> str:
        system = SystemMessage(
            content="""
Ты — ботанический ассистент.
Твоя задача: перевести русское название растения в научное латинское название (scientific name).

Требования:
- Ответ должен содержать ТОЛЬКО научное название.
- НЕ используй английские common names.
- НЕ добавляй пояснений.
- НЕ выдумывай, если неизвестно — напиши 'unknown'.
- Используй двоичную номенклатуру (род + вид), если возможно.
"""
        )
        human = HumanMessage(content=plant_name)

        resp = await self.llm.ainvoke([system, human])

        # resp — AIMessage, точный перевод в .content
        return resp.content.strip().lower()