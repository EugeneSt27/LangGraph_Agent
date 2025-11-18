import asyncio
from dotenv import load_dotenv
import os
load_dotenv()

from utils.llm_client import load_llm
from nodes.planner_node import PlannerNode
from nodes.perenual_node import PerenualNode
from nodes.trefle_node import TrefleNode
from nodes.translation_node import TranslationNode

async def async_main():
    llm = load_llm()
    planner = PlannerNode(llm)

    # 1) Определяем растение и симптомы
    plan = await planner.run("В горшке у спатифиллума завелись мошки, бегония начала сохнуть. Что делать?")
    print("Planner returned:", plan.model_dump())

    # 2) Переводим название растения на английский
    translator = TranslationNode(llm)

    english_name = await translator.run(plan.plant_name)
    print("English:", english_name)

    # 3) API вызовы
    trefle_node = TrefleNode()
    perenual_node = PerenualNode()

    t_data, p_data = await asyncio.gather(
        trefle_node.run(english_name),
        perenual_node.run(english_name)
    )

    print("Trefle:", t_data.model_dump() if t_data else None)
    print("Perenual:", p_data.model_dump() if p_data else None)
    

if __name__ == "__main__":
    asyncio.run(async_main())