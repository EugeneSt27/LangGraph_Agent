from langchain_core.messages import SystemMessage, HumanMessage

class TranslationNode:
    """
    Узел, который переводит название растения на английский язык,
    т.к. оба API работают только с английскими названиями.
    Использует LLM для перевода одного слова или короткой фразы.
    """
class TranslationNode:
    def __init__(self, llm):
        self.llm = llm

    async def run(self, plant_name: str) -> str:
        system = SystemMessage(
            content="""
Ты — профессиональный ботанический переводчик.
Переводи русское название растения на английское common name.
Формат ответа: только одно английское название, без точек, без лишнего текста.
Если есть несколько вариантов — выбери самый распространённый.
"""
        )
        human = HumanMessage(content=plant_name)

        resp = await self.llm.ainvoke([system, human])
        return resp.content.strip().lower()
