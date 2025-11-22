import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

from utils.llm_client import load_llm
from nodes.planner_node import PlannerNode
from nodes.perenual_node import PerenualNode
from nodes.trefle_node import TrefleNode
from nodes.translation_node import TranslationNode
from nodes.diagnosis_node import DiagnosisNode


async def async_main():
    llm = load_llm()
    planner = PlannerNode(llm)

    # 1) Planner
    plan = await planner.run(
        "В горшке в бегонии появились мошки и как будто плесень в земле. Она месяц стояла на балконе зимой, я про нее забыл"
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

    # 5) Диагностика и вызов поисковика при необходимости
    diag = DiagnosisNode(llm)
    diagnosis = await diag.run(
        plan.plant_name,
        plan.symptoms,
        t_data.model_dump() if t_data else {},
        p_data.model_dump() if p_data else {},
    )

    print(diagnosis.model_dump())

if __name__ == "__main__":
    asyncio.run(async_main())