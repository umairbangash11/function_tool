from agents import Agent, Runner, RunContextWrapper, function_tool, OpenAIChatCompletionsModel, AsyncOpenAI
from dotenv import load_dotenv
import os
from agents.run import RunConfig
import asyncio
# from agents import enable_verbose_stdout_logging

# enable_verbose_stdout_logging()

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Initialize Gemini client and model
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.0-flash",
)


import json

from typing_extensions import TypedDict, Any

from agents import Agent, FunctionTool, RunContextWrapper, function_tool


class Location(TypedDict):
    lat: float
    long: float

@function_tool  
async def fetch_weather(location: Location) -> str:
    
    """Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for.
    """
    # In real life, we'd fetch the weather from a weather API
    return "sunny"


# @function_tool(name_override="fetch_data")  
# def read_file(ctx: RunContextWrapper[Any], path: str, directory: str | None = None) -> str:
#     """Read the contents of a file.

#     Args:
#         path: The path to the file to read.
#         directory: The directory to read the file from.
#     """
#     # In real life, we'd read the file from the file system
#     return "<file contents>"


agent = Agent(
    name="Assistant",
    tools=[fetch_weather],  
    model=model,
)

for tool in agent.tools:
    if isinstance(tool, FunctionTool):
        print(tool.name)
        print(tool.description)
        print(json.dumps(tool.params_json_schema, indent=2))
        print()

async def main():
    result = await Runner.run(agent, input="What is the weather in New York?")
    print(result)

