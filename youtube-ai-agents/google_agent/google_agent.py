from google import genai
from google.genai import types
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

client = genai.Client()


class WeatherResponse(BaseModel):
    temperature: float = Field(
        description="The current temperature in celsius for the given location."
    )
    response: str = Field(
        description="A natural language response to the user's question."
    )


def get_weather(latitude: float, longitude: float):
    """
    This is a publically available API that returns the weather data for a given latitude and longitude coordinates

    :param latitude: The Latitude coordinate
    :type latitude: float
    :param longitude: The Longitude coordinate
    :type longitude: float
    """
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]


get_weather_function = {
    "name": "get_weather",
    "description": "Gets the current weather information for a specified location.",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {
                "type": "number",
                "description": "The latitude coordinate.",
            },
            "longitude": {
                "type": "number",
                "description": "The longitude coordinate.",
            },
        },
        "required": ["latitude", "longitude"],
    },
}

tools = types.Tool(function_declarations=[get_weather_function])
config = types.GenerateContentConfig(tools=[tools])
contents = [
    types.Content(
        role="user",
        parts=[
            types.Part(
                text="What is the weather like for the coordinates 52.52, 13.419998?"
            )
        ],
    )
]

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=contents,
    config=config,
)


if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print(f"Function to call: {function_call.name}")
    print(f"Arguments: {function_call.args}")
    if function_call.name == "get_weather":
        result = get_weather(**function_call.args)
        function_response_part = types.Part.from_function_response(
            name=function_call.name, response={"result": result}
        )
        contents.append(response.candidates[0].content)
        contents.append(types.Content(role="user", parts=[function_response_part]))

else:
    print("No function call found in the response.")
    print(response.text)


config = types.GenerateContentConfig(
    tools=[tools], response_json_schema=WeatherResponse.model_json_schema()
)
final_response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    config=config,
    contents=contents,
)

print(final_response.text)
