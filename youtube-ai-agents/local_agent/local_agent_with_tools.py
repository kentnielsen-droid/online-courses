import os
import json
from typing import TypedDict
from dotenv import load_dotenv
from imap_tools import MailBox, AND
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END

load_dotenv()

IMAP_HOST = os.getenv("IMAP_SERVER")
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASS = os.getenv("IMAP_PASS")
IMAP_FOLDER = "INBOX"

CHAT_MODEL: str = "smollm2"


class ChatState(TypedDict):
    messages: list


def connect():
    mail_box = MailBox(IMAP_HOST)
    mail_box.login(IMAP_USER, IMAP_PASS, initial_folder=IMAP_FOLDER)

    return mail_box


@tool
def list_unread_emails():
    """Return a bullet list of every UNREAD message's UID, subject, date and sender"""

    print("List Unread Emails Tool Called")

    with connect() as mb:
        unread = list(
            mb.fetch(criteria=AND(seen=False), headers_only=True, mark_seen=False)
        )

    if not unread:
        return "You have no unread messages."

    response = json.dumps(
        [
            {
                "uid": mail.uid,
                "date": mail.date.astimezone().strftime("%Y-%m-%d %H:%M"),
                "subject": mail.subject,
                "sender": mail.from_,
            }
            for mail in unread
        ]
    )

    return response


@tool
def summarize_email(uid):
    """Summarize a single e-mail given it's IMAP UID. Return a short summary of the e-mails content / body in plain text."""

    print("Summarize E-Mail Tool Called on", uid)

    with connect() as mb:
        mail = next(mb.fetch(AND(uid=uid), mark_seen=False), None)

        if not mail:
            return f"Could not summarize e-mail with UID {uid}."

        prompt = (
            "Summarize this e-mail concisely:\n\n"
            f"Subject: {mail.subject}\n"
            f"Sender: {mail.from_}\n"
            f"Date: {mail.date}\n\n"
            f"{mail.text or mail.html}"
        )

        return raw_llm.invoke(prompt).content


llm = init_chat_model(CHAT_MODEL, model_provider="ollama")
llm = llm.bind_tools([list_unread_emails, summarize_email])

raw_llm = init_chat_model(CHAT_MODEL, model_provider="ollama")


def llm_node(state):
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}


def router(state):
    last_message = state["messages"][-1]
    return "tools" if getattr(last_message, "tool_calls", None) else "end"


tool_node = ToolNode([list_unread_emails, summarize_email])


def tools_node(state):
    result = tool_node.invoke(state)

    return {"messages": state["messages"] + result["messages"]}


builder = StateGraph(ChatState)
builder.add_node("llm", llm_node)
builder.add_node("tools", tools_node)
builder.add_edge(START, "llm")
builder.add_edge("tools", "llm")
builder.add_conditional_edges("llm", router, {"tools": "tools", "end": END})

graph = builder.compile()


if __name__ == "__main__":
    state = {"messages": []}
    while True:
        print("\n")
        print("-" * 50)
        question: str = str(input("Ask your question (q to quit): "))
        print("\n\n")
        if question.lower().strip() == "q":
            break
        state["messages"].append({"role": "user", "content": question})
        state = graph.invoke(state)

        print(state["messages"][-1].content, "\n")
