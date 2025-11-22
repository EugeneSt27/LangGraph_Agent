# graph.py
import asyncio
from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END

# Импортируем узлы
from nodes.planner_node import PlannerNode
from nodes.translation_node import TranslationNode
from nodes.trefle_node import TrefleNode
from nodes.perenual_node import PerenualNode
from nodes.diagnosis_node import DiagnosisNode
from nodes.writer_node import WriterNode

from utils.llm_client import load_llm


# ----------- STATE ----------------------

class AgentState(TypedDict, total=False):
    user_query: str
    plan: dict
    english_name: str
    trefle: Optional[dict]
    perenual: Optional[dict]
    diagnosis: dict
    final_text: str


# ----------- NODE FUNCTIONS --------------

async def planner_node(state: AgentState):
    llm = load_llm()
    planner = PlannerNode(llm)
    plan = await planner.run(state["user_query"])
    return {"plan": plan.model_dump()}


async def translator_node(state: AgentState):
    llm = load_llm()
    translator = TranslationNode(llm)
    eng = await translator.run(state["plan"]["plant_name"])
    return {"english_name": eng}


async def trefle_node(state: AgentState):
    node = TrefleNode()
    data = await node.run(state["english_name"])
    return {"trefle": data.model_dump() if data else None}


async def perenual_node(state: AgentState):
    node = PerenualNode()
    data = await node.run(state["english_name"])
    return {"perenual": data.model_dump() if data else None}


async def diagnosis_node(state: AgentState):
    llm = load_llm()
    diag = DiagnosisNode(llm)

    diagnosis = await diag.run(
        plant_name=state["plan"]["plant_name"],
        symptoms=state["plan"]["symptoms"],
        trefle_data=state["trefle"],
        perenual_data=state["perenual"],
    )

    return {"diagnosis": diagnosis.model_dump()}


async def writer_node(state: AgentState):
    llm = load_llm()
    writer = WriterNode(llm)

    final_text = await writer.run(
        state["plan"]["plant_name"],
        state["plan"]["symptoms"],
        writer_input := DiagnosisNode(llm)  # incorrect?
    )


# исправление: writer_input должен быть diagnosis, не DiagnosisNode

async def writer_node(state: AgentState):
    llm = load_llm()
    writer = WriterNode(llm)

    from models.diagnosis_models import DiagnosisDraft
    diagnosis_obj = DiagnosisDraft(**state["diagnosis"])

    final_text = await writer.run(
        plant_name=state["plan"]["plant_name"],
        symptoms=state["plan"]["symptoms"],
        diagnosis=diagnosis_obj
    )

    return {"final_text": final_text}


# ----------- GRAPH SETUP ------------------

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("translator", translator_node)

    # параллельные API-вызовы
    graph.add_node("trefle", trefle_node)
    graph.add_node("perenual", perenual_node)

    graph.add_node("diagnosis", diagnosis_node)
    graph.add_node("writer", writer_node)

    # переходы
    graph.set_entry_point("planner")
    graph.add_edge("planner", "translator")
    graph.add_edge("translator", "trefle")
    graph.add_edge("translator", "perenual")

    # после обоих API — идём в diagnosis
    graph.add_edge("trefle", "diagnosis")
    graph.add_edge("perenual", "diagnosis")

    graph.add_edge("diagnosis", "writer")
    graph.add_edge("writer", END)

    return graph.compile()
