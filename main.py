from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

def get_weather(city):
    return f"Weather in {city} is cloudy and is 30°C."

get_weather_function = {
    "type": "function",
    "name": "get_weather",
    "description": "Retrieves the current weather for the given city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "The city name, e.g. San Francisco",}
        },
        "required": ["city"],
    },
}

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.interactions.create(
    model="gemini-3.6-flash",
    input="how is the weather in islamabad",
    tools=[get_weather_function],
)

for item in response.steps:
    if item.type == "function_call":
        print(f"Function to call: {item.name}")
        print(f"Arguments: {item.arguments}")

        if item.name == "get_weather":
            result = get_weather(**item.arguments)
            print(f"Function execution result: {result}")

        final_response = client.interactions.create(
            model="gemini-3.6-flash",
            input=[
                    {
                        "type": "function_result",
                        "name": item.name,
                        "call_id": item.id,
                        "result": [{"type": "text", "text": json.dumps(result)}],
                    }
                ],
            tools=[get_weather_function],
            previous_interaction_id=response.id,
        )
        print(final_response.output_text)

# from google import genai
# from dotenv import load_dotenv
# import os

# load_dotenv()

# client = genai.Client(
#     api_key=os.getenv("GEMINI_API_KEY")
# )
# interaction = client.interactions.create(
#     model="gemini-3.5-flash-lite",
#     input="Who won Euro 2024?",
#     tools=[
#         {"type": "google_search"}
#     ]
# )

# print(interaction.output_text)