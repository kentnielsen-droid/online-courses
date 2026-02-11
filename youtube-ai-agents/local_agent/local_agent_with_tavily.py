from tavily import TavilyClient
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
import asyncio
import os

load_dotenv()

local_llm = ChatOllama(model="qwen3")
client = TavilyClient()

# server_params = StdioServerParameters(
#     command="uv",
#     env={"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY")},
#     args=["tavily-mcp"],
# )


# async def main():
#     async with stdio_client(server_params) as (read, write):
#         async with ClientSession(read, write) as session:
#             await session.initialize()
#             tools = await load_mcp_tools(session)
#             agent = create_agent(local_llm, tools)

#             messages = [
#                 {
#                     "role": "system",
#                     "content": """You are a helpful assistent that can scrape website, crawl pages, and extract data using Tavily tools.
#                     Think step by step and use appropriate tools to help the user.""",
#                 }
#             ]

#             print("Available tools - " * [tool.name for tool in tools])
#             print("-" * 60)

#             while True:
#                 user_input = input("Enter question (q to quit): ")
#                 if user_input.strip().lower() == "q":
#                     break

#                 messages.append([{"role": "user", "content": user_input}])
#                 try:
#                     agent_response = await agent.ainvoke({"messages": messages})

#                     ai_message = agent_response["messages"][-1].content
#                     print(f"\nAgent: {ai_message}")
#                 except Exception as e:
#                     print(f"Error: {e}")


# if __name__ == "__main__":
#     asyncio.run(main())


# # tavily_client = TavilyClient()
