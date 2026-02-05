from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool
from datetime import datetime

load_dotenv()

LOCAL_CHAT_MODEL: str = "llama3.2"
CLOUD_CHAT_MODEL: str = "gemini-3-flash-preview"


class ResearchRespone(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


local_llm: ChatOllama = ChatOllama(model=LOCAL_CHAT_MODEL)
cloud_llm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(model=CLOUD_CHAT_MODEL)


@tool
def save_txt_note(data: str, filename: str = "output.txt"):
    """
    Store or append a text file with the newest research information.

    :param data: The information to be stored in text format.
    :type data: str
    :param filename: The name of the file.
    :type filename: str
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}"


@tool
def web_search(query: str):
    """
    Search the web for information.
    Args:
        query: Search terms to look for on the world wide web.
    """
    search = DuckDuckGoSearchRun()
    return str(search.invoke(query))


@tool
def wiki_search(query: str):
    """
    Look up knowledge for research on Wikipedia.
    Args:
        query: Search terms to look for on the world wide web.
    """
    wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
    wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)
    return wiki_tool.invoke(query)


system_prompt = """
You are a research assistant that will help generate a research paper. 
Answer the user query and use neccessary tools.
"""

agent = create_agent(
    model=cloud_llm,
    tools=[web_search, wiki_search, save_txt_note],
    system_prompt=system_prompt,
    response_format=ResearchRespone,
)
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "what is the capital of Spain according to Wikipedia? Please save to results to a txt file.",
            }
        ]
    }
)

structured_response: ResearchRespone = response.get("structured_response")
print(structured_response)
print(structured_response.topic)
