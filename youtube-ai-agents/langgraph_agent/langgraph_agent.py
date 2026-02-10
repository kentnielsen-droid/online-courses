from dotenv import load_dotenv
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.runnables.graph import MermaidDrawMethod
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


load_dotenv()


LOCAL_MODEL = "qwen3"
CLOUD_MODEL = "gemini-2.5-flash-lite"

local_llm = init_chat_model(model=LOCAL_MODEL, model_provider="ollama")
# cloud_llm = init_chat_model(model=CLOUD_MODEL)


class MessageClassifier(BaseModel):
    message_type: Literal["emotional", "logical"] = Field(
        ...,
        description="Classify if the message requires an emotional or logical response.",
    )


class State(TypedDict):
    messages: Annotated[list, add_messages]
    message_type: str | None


# Init graph
graph_builder = StateGraph(State)


# defining node functionality
def classify_message(state: State):
    last_message = state["messages"][-1]
    classifier_llm = local_llm.with_structured_output(MessageClassifier)

    result = classifier_llm.invoke(
        [
            {
                "role": "system",
                "content": """Classify the users message as either:
                                - 'emotional': if the user asks for emotional support, deals with feelings, or personal problems.
                                - 'logical': if the user asks for facts, information, logical analysis, objective problems, or practical solutions.
                            """,
            },
            {"role": "user", "content": last_message.content},
        ]
    )
    return {"message_type": result.message_type}


def router(state: State):
    message_type = state.get("message_type", "logical")
    if message_type == "emotional":
        return {"next": "emotional"}

    return {"next": "logical"}


def emotional_agent(state: State):
    last_message = state["messages"][-1]
    messages = [
        {
            "role": "system",
            "content": """You are a compassionate therapist. Focus on the emotional aspects of the user's message.
                        Show empathy, validate their feelings, and help them process their emotions.
                        Ask thoughtful questions to help them explore their feelings more deeply.
                        Avoid giving logical solutions unless explicitly asked.""",
        },
        {"role": "user", "content": last_message.content},
    ]

    reply = local_llm.invoke(messages)
    return {"messages": [{"role": "assistant", "content": reply.content}]}


def logical_agent(state: State):
    last_message = state["messages"][-1]
    messages = [
        {
            "role": "system",
            "content": """You are a purely logical assistant. Focus only on facts and information. 
            Provide clear, concise answers based on logic and evidence. 
            Do not address emotions or provide emotional support. 
            Be direct and straightforward in your responses.""",
        },
        {"role": "user", "content": last_message.content},
    ]

    reply = local_llm.invoke(messages)
    return {"messages": [{"role": "assistant", "content": reply.content}]}


# Adding graph nodes and edges
graph_builder.add_node("classifier", classify_message)
graph_builder.add_node("router", router)
graph_builder.add_node("emotional", emotional_agent)

graph_builder.add_node("logical", logical_agent)
graph_builder.add_edge(START, "classifier")
graph_builder.add_edge("classifier", "router")
graph_builder.add_conditional_edges(
    "router",
    lambda state: state.get("next"),
    {"emotional": "emotional", "logical": "logical"},
)
graph_builder.add_edge("emotional", END)
graph_builder.add_edge("logical", END)
# Compile graph
graph = graph_builder.compile()


def run_chatbot():
    state = {"messages": [], "message_type": None}

    while True:
        user_input = input("Enter a message (q to quit): ")
        if user_input.lower().strip() == "q":
            break

        state["messages"] = state.get("messages", []) + [
            {"role": "user", "content": user_input}
        ]
        state = graph.invoke(state)

        if state.get("messages") and len(state["messages"]) > 0:
            last_message = state["messages"][-1]
            print(f"Assistant: {last_message}")


if __name__ == "__main__":
    run_chatbot()
