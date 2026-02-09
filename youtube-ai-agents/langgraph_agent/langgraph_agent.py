from dotenv import load_dotenv
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.runnables.graph import MermaidDrawMethod
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


load_dotenv()


LOCAL_MODEL = "smollm2"
CLOUD_MODEL = "gemini-2.5-flash-lite"

local_llm = init_chat_model(model=LOCAL_MODEL, model_provider="ollama")
# cloud_llm = init_chat_model(model=CLOUD_MODEL)


class State(TypedDict):
    messages: Annotated[list, add_messages]


# Init graph
graph_builder = StateGraph(State)


# defining node functionality
def chatbot(state: State):
    return {"messages": [local_llm.invoke(state["messages"])]}


# Adding graph nodes and edges
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
# Compile graph
graph = graph_builder.compile()

user_input = input("Enter a message: ")
state = graph.invoke({"messages": [{"role": "user", "content": user_input}]})

print(state["messages"][-1].content)
