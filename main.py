import asyncio
from graph import build_graph

async def async_main():
    # создаём граф
    graph = build_graph()

    # визуализация графа не работает, graphviz не устанавливается
    #graph.get_graph().draw_png("agent_graph.png")
    #print("Graph saved as agent_graph.png")

    # ---- запускаем агента ----
    user_query = "У хойи в горшке завелись мошки и она начала сбрасывать листья. Что делать?"
    result = await graph.ainvoke({
        "user_query": user_query
    })

    # ----- вывод результата -----

    print("\n===== Финальный ответ =====\n")
    print(result["final_text"])

    print("\n===== Диагноз (JSON) =====\n")
    print(result["diagnosis"])


if __name__ == "__main__":
    asyncio.run(async_main())
