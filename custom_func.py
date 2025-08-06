import asyncio
from typing import Any
from pydantic import BaseModel
from agents import Agent, Runner, RunContextWrapper, FunctionTool, RunConfig
import asyncio
import json
from typing_extensions import Any
from agents import Agent, FunctionTool, RunContextWrapper, function_tool, Runner
from agents.run import RunConfig  # Make sure config is defined or dummy created
from agents import Agent, Runner, RunContextWrapper, function_tool, OpenAIChatCompletionsModel, AsyncOpenAI
from dotenv import load_dotenv
import os
from agents.run import RunConfig
import asyncio
from agents import enable_verbose_stdout_logging

enable_verbose_stdout_logging()

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

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True

)

# Step 1: Define input schema using Pydantic
# def do_some_work(data: str) -> str:
#     return data


# class FunctionArgs(BaseModel):
#     username: str = "umair"
#     age: int = 20


# async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
#     parsed = FunctionArgs.model_validate_json(args)
#     return do_some_work(data=f"{parsed.username} is {parsed.age} years old")


# tool = FunctionTool(
#     name="process_user",
#     description="Processes extracted user data",
#     params_json_schema=FunctionArgs.model_json_schema(),
#     on_invoke_tool=run_function,
# )

# agent = Agent(name="umair", instructions="You are a helpful assistant",tools=[tool])

# # Step 5: Run with input
# async def main():
#     run = await Runner.run(agent, input="now tell me what is my age and name", run_config=config)
#     print("Final Output:", run.final_output)

def user_data(data: str) -> str:
    return data

class UmairArgs(BaseModel):
    username: str = "umair"
    age: int = 20

async def umair_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = UmairArgs.model_validate_json(args)
    return user_data(data=f"{parsed.username} is {parsed.age} years old")

tool = FunctionTool(
    name="assistant",
    description="Provide user data",
    params_json_schema=UmairArgs.model_json_schema(),
    on_invoke_tool=umair_function,
)   

agent = Agent(name="umair", instructions="You are a helpful assistant", tools=[tool])

async def main():
    result = await Runner.run(agent, input="my name is umair and I am 20 years old, now tell me what is my age and name", run_config=config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
