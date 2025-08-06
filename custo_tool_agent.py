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

# Define your tools here
@function_tool
async def example_tool(param: str) -> str:
    """An example tool function"""
    return f"Processed: {param}"

async def run_my_agent() -> str:
    """A tool that runs the agent with custom configs"""

    agent = Agent(
        name="My agent", 
        instructions="You are a helpful assistant that can process requests using available tools.",
        tools=[example_tool],  # Add your tools here
        model=model
    )

    result = await Runner.run(
        agent,
        input="Hello, can you help me?",
        max_turns=5
    )
    print(result.final_output)
    return result.final_output

if __name__ == "__main__":
    asyncio.run(run_my_agent())