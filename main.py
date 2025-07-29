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

@function_tool
async def get_weather(city: str) -> str:
    """
    Returns weather information for a given city.

    Args:
        city: Name of the city to get the weather for.
    """
    # Simulated weather data
    return f"The weather in {city} is sunny."

@function_tool
async def piaic(student_name: str) -> str:
    """
    Returns PIAIC information for a given student.

    Args:
        student_name: Name of the student to get the PIAIC information for.
    """
    # Simulated PIAIC data
    return f"{student_name} is enrolled in PIAIC."


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        tools=[get_weather, piaic],  
    )
    result = await Runner.run(agent, input="is umair is enroll in piaic?", run_config=config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
