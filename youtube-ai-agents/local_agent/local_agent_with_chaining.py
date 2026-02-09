from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain.agents.structured_output import ToolStrategy
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_community.tools import (
    WikipediaQueryRun,
    DuckDuckGoSearchRun,
    OpenWeatherMapQueryRun,
)
from langchain_community.utilities import WikipediaAPIWrapper, OpenWeatherMapAPIWrapper
from langchain.tools import tool
from datetime import datetime
from typing import Union, Optional
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

load_dotenv()

LOCAL_CHAT_MODEL: str = "qwen3"
CLOUD_CHAT_MODEL: str = "gemini-3-flash-preview"


class WeatherRequest(BaseModel):
    description: str = Field(description="A raw description of the weather request")
    is_weather_request: bool = Field(
        description="A boolean describing if the request in about the weather or not"
    )
    confidence_score: float = Field(description="Confidence score between 0 and 1")


class WeatherDetails(BaseModel):
    temperature: float = Field(
        description="The current temperature for the specified location"
    )
    wind_speed: float = Field(
        description="The current wind speed for the specified location"
    )
    humidity: float = Field(description="The current humidity for a specified location")


class WeatherResponse(BaseModel):
    response: str = Field(
        description="A natural language response to the user's question"
    )


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


@tool
def get_weather(query: str) -> Optional[WeatherResponse]:
    """
    Confirms the data request is about the weather and gets the weather data for a specified location.
    Args:
        query: The users question regarding the weather
    """

    def is_weather_request(query: str) -> WeatherRequest:
        logger.info("Starting weather extraction analysis")
        logger.debug(f"Input text: {query}")

        today = datetime.now()
        date_context = f"Today is {today.strftime('%A, %B %d, %Y')}."

        agent = create_agent(
            model=local_llm,
            system_prompt=f"{date_context}, Analyze if the text describes a weather request.",
            response_format=WeatherRequest,
        )
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": query,
                    }
                ]
            }
        )
        structued_result: WeatherRequest = result.get("structured_response")
        logger.info(
            f"Extraction complete - Is weather request: {structued_result.is_weather_request}, Confidence: {structued_result.confidence_score:.2f}"
        )
        return structued_result

    def weather_details(description: str) -> WeatherDetails:
        @tool
        def _get_weather(query: str):
            """
            Gets the weather data for a specified location.
            Args:
                query: Location of where to get the weather information from.
            """
            weather_wrapper = OpenWeatherMapAPIWrapper()
            weather = OpenWeatherMapQueryRun(api_wrapper=weather_wrapper)
            location_weather = weather.invoke(query)
            print("\n\n")
            print(location_weather)
            print("\n\n")
            return location_weather

        logger.info("Starting weather details extraction")

        today = datetime.now()
        date_context = f"Today is {today.strftime('%A, %B %d, %Y')}."

        agent = create_agent(
            model=cloud_llm,
            system_prompt=f"{date_context}, Extract detailed weather infotmation. When dates reference 'next Tuesday' or similar relative dates, use this current date as reference.",
            response_format=WeatherDetails,
            tools=[_get_weather],
        )
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": description,
                    }
                ]
            }
        )
        structued_result: WeatherDetails = result.get("structured_response")
        logger.info(
            f"Extracted weather details - Temperature: {structued_result.temperature}, Wind Speed: {structued_result.wind_speed}, Humidity: {structued_result.humidity}"
        )
        return structued_result

    def weather_response(weather: WeatherDetails) -> WeatherResponse:
        logger.info("Weather reply message")

        agent = create_agent(
            model=local_llm,
            system_prompt="Respond with a natural reply to the information specified.",
            response_format=WeatherResponse,
        )
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": f"{str(weather)}",
                    }
                ]
            }
        )
        structued_result: WeatherDetails = result.get("structured_response")
        logger.info("Weather reply message successfully sent")
        return structued_result

    logger.info("Processing weather request")
    logger.debug(f"Raw input: {query}")

    inital_weather = is_weather_request(query)

    if not inital_weather.is_weather_request or inital_weather.confidence_score < 0.7:
        logger.warning(
            f"Gate check failed - is_weather_request: {inital_weather.is_weather_request}, confidence: {inital_weather.confidence_score:.2f}"
        )
        return None

    logger.info("Gate check passed, proceeding with processing")

    weather_details = weather_details(inital_weather.description)
    response = weather_response(weather_details)

    logger.info("Weather request processing completed successfully")
    return response


system_prompt = """
You are an assistant that will help answer the user query and use neccessary tools.
"""

agent = create_agent(
    model=cloud_llm,
    tools=[get_weather, web_search, wiki_search, save_txt_note],
    system_prompt=system_prompt,
    response_format=WeatherResponse,
)
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is the current weather in Barcelona?",
            }
        ]
    }
)

structured_response: Union[ResearchRespone, WeatherResponse] = response.get(
    "structured_response"
)
print(structured_response)
print("\n\n")
print("-" * 50)
print("\n\n")
print(response)


agent = create_agent(
    model=local_llm,
    tools=[get_weather, web_search, wiki_search, save_txt_note],
    system_prompt=system_prompt,
)
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "How many lives in Barcelona according to Wikipedia? Please save to results to a txt file.",
            }
        ]
    }
)

structured_response: Union[ResearchRespone, WeatherResponse] = response.get(
    "structured_response"
)
print(structured_response)
print("\n\n")
print("-" * 50)
print("\n\n")
print(response)
