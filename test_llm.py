import asyncio
from utils.llm_client import load_llm
from langchain_core.messages import HumanMessage


async def main():
	llm = load_llm()
	resp = await llm.ainvoke([HumanMessage(content="how are you?")])
	print(resp.content)


if __name__ == "__main__":
	asyncio.run(main())