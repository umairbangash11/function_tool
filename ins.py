import asyncio
import json
from typing_extensions import Any, TypedDict
from agents import Agent, FunctionTool, RunContextWrapper, function_tool, Runner
from agents.run import RunConfig  # Make sure config is defined or dummy created
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

# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True

# )


# ----- TOOL FUNCTION -----
# @function_tool
# async def buyer(name: str) -> str:
#     """
#     Returns buyer information for a given name.

#     Args:
#         name: Name of the buyer to get the information for.
#     """
#     return f"{name} is a buyer."

class Weather(TypedDict):
    city: str


@function_tool
async def get_weather(city: str) -> str:
    """Get the weather for a city.
    
    args:
        city (str): The city to get the weather for.

    returns:
        str: The weather for the city.
    """
    return f"The weather in {city} is sunny."




# ----- MAIN FUNCTION -----
async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        tools=[get_weather],
        model=model,
    )

    # Optional: Inspect tools
    # for tool in agent.tools:
    #     if isinstance(tool, FunctionTool):
    #         print("📦 Tool Name:", tool.name)
    #         print("📝 Description:", tool.description)
    #         print("📘 Params Schema:\n", json.dumps(tool.params_json_schema, indent=2))
    #         print()

    for tool in agent.tools:
        if isinstance(tool, FunctionTool):
            print("📦 Tool Name:",tool.name)
            print("📝 Description:",tool.description)
            print("📘 Params Schema:\n",json.dumps(tool.params_json_schema, indent=2))
            print()



    # Run the agent (make sure config is defined properly or skip it for now)
    result = await Runner.run(agent, input="what is the weather in karachi?")
    print("\n🎯 Final Output:\n", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
