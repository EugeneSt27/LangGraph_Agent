import asyncio
from dotenv import load_dotenv
import os
load_dotenv()

from utils.llm_client import load_llm
from nodes.planner_node import PlannerNode

async def async_main():
    llm = load_llm()

    planner = PlannerNode(llm)

    test_inputs = [
        "Почему у монстеры сохнут листья?",
        "В горшке у бегонии завелись мошки. Как их вывести?" 
    ]

    for text in test_inputs:
        print("=== INPUT ===")
        print(text)
        try:
            plan = await planner.run(text)
            print("Parsed plan:")
            # model_dump() возвращает словарь
            print(plan.model_dump())
        except Exception as e:
            print("Planner failed:", e)
        print()

if __name__ == "__main__":
    asyncio.run(async_main())