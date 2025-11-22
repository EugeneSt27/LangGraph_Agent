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

    # 1) Planner
    plan = await planner.run(
        "В горшке у спатифиллума завелись мошки и начали желтеть листья. Что делать?"
    )
    print("Planner returned:", plan.model_dump())

    # 2) Перевод названия растения на английский
    translator = TranslationNode(llm)
    scientific_name = await translator.run(plan.plant_name)
    print("Scientific:", scientific_name)

    # 3) API вызовы (асинхронно, но безопасно)
    trefle_node = TrefleNode()
    perenual_node = PerenualNode()

    t_res, p_res = await asyncio.gather(
        trefle_node.run(scientific_name),
        perenual_node.run(scientific_name),
        return_exceptions=True
    )

    # 4) Обработка результатов
    if isinstance(t_res, Exception):
        print("Trefle failed:", t_res)
        t_data = None
    else:
        t_data = t_res

    if isinstance(p_res, Exception):
        print("Perenual failed:", p_res)
        p_data = None
    else:
        p_data = p_res

    print("Trefle:", t_data.model_dump() if t_data else None)
    print("Perenual:", p_data.model_dump() if p_data else None)


if __name__ == "__main__":
    asyncio.run(async_main())