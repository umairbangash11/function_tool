from agents import Agent, Runner, RunContextWrapper, FunctionTool, OpenAIChatCompletionsModel, AsyncOpenAI
from dotenv import load_dotenv
import os
from agents.run import RunConfig
import asyncio
from agents import enable_verbose_stdout_logging
from pydantic import BaseModel
from typing import Any

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

# def do_some_work(data: str) -> str:
#     return "done"


# class FunctionArgs(BaseModel):
#     username: str
#     age: int


# async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
#     parsed = FunctionArgs.model_validate_json(args)
#     return do_some_work(data=f"{parsed.username} is {parsed.age} years old")


# weather_tool = FunctionTool(
#     name="custom_weather",
#     description="Provides weather info using custom logic.",
#     params_json_schema=FunctionArgs.model_json_schema(),
#     on_invoke_tool=run_function,
# )

# Simulated weather processing function
# def get_weather_data(city: str) -> str:
#     # You can put actual API calls here, but for now we simulate
#     return f"The weather in {city} is sunny."

# # Pydantic model for tool arguments
# class WeatherArgs(BaseModel):
#     city: str

# # Tool invocation function
# async def run_weather_tool(ctx: RunContextWrapper[Any], args: str) -> str:
#     parsed = WeatherArgs.model_validate_json(args)
#     return get_weather_data(parsed.city)

# # Define the FunctionTool (Weather Tool)
# weather_tool = FunctionTool(
#     name="custom_weather",
#     description="Provides weather information for a given city.",
#     params_json_schema=WeatherArgs.model_json_schema(),
#     on_invoke_tool=run_weather_tool,
# )

# def piaic(student_name: str | None) -> str:
#     return f"{student_name} is learning AI"

# class Piaic(BaseModel):
#     student_name: str
    

# async def run_piaic(ctx: RunContextWrapper[Any], args: str) -> str:
#     parsed = Piaic.model_validate_json(args)
#     return piaic(parsed.student_name)

# piaic_tool = FunctionTool(
#     name="piaic",
#     description="Provide Info about students",
#     params_json_schema=Piaic.model_json_schema(),
#     on_invoke_tool=run_piaic,
# )

# def todo(task: str):
#     return f"{task} is done"

# class Todo(BaseModel):
#     task: str

# async def run_todo(ctx: RunContextWrapper[Any], args: str) -> str:
#     parsed = Todo.model_validate_json(args)
#     return todo(parsed.task)

# todo_tool = FunctionTool(
#     name="todo",
#     description="Write everyday tasks",
#     params_json_schema=Todo.model_json_schema(),
#     on_invoke_tool = run_todo,
# )

# def food_info(fruit_name: str) -> str:
#     return f"{fruit_name} is delicious"

# class Food(BaseModel):
#     fruit_name: str

# def food_info(ctx: RunContextWrapper[Any], args: str) -> str:
#     parsed = Food.model_validate_json(args)
#     return f"{parsed.fruit_name} is delicious"

# food_tool = FunctionTool(
#     name="food_info",
#     description="Provide food info",
#     params_json_schema=Food.model_json_schema(),
#     on_invoke_tool=food_info,
# )

def do_some_work(data: str) -> str:
    return "done"


class FunctionArgs(BaseModel):
    username: str  
    age: int 


async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return do_some_work(data=f"{parsed.username} is {parsed.age} years old")


tool = FunctionTool(
    name="process_user",
    description="Processes extracted user data",
    params_json_schema=FunctionArgs.model_json_schema(),
    on_invoke_tool=run_function,
)


async def main():
    agent = Agent(
        name="umair",
        instructions="You are a helpful assistant. if You must use tools to process user data like name and age.", 
        tools=[tool],
        model=model
)
    result = await Runner.run(
        agent,
        input="my name is john and my age is 20 year old now tell me what is my age?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())



