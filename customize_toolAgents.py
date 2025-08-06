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


# @function_tool
# async def run_my_agent() -> str:
#     """A tool that runs the agent with custom configs"""
#     return "Running My Agent as a tool."

# @function_tool
# async def fruit_name_agent() -> str:
#     """A tool that runs the agent with custom configs"""
#     return "Running Fruit Name Agent as a tool."

# async def main():
#     # Create an Agent that can call this tool
#     agent = Agent(
#         name="Main Agent",
#         instructions="If asked, use the 'run_my_agent' tool.",
#         tools=[run_my_agent, fruit_name_agent],
#         model=model,
#     )

#     # Run the Agent with a prompt that triggers the tool
#     result = await Runner.run(
#         agent,
#         input="Please execute the run_my_agent tool and also do the excution the fruit_name_agent.",
#         max_turns=5,
#         run_config=RunConfig(
#             model=model,
#             model_provider=external_client,
#             tracing_disabled=True
#         )
#     )

@function_tool
async def echo_tool(input_text: str) -> str:
    return f"Echo: {input_text}"

# Define the Agent
agent = Agent(
    name="Looper Agent",
    instructions="Keep calling the echo_tool with the last message you received.",
    tools=[echo_tool],
    model=model,

)

async def main():
    result = await Runner.run(
        agent,
        input="Start Loop",
        max_turns=10,  # Limit to 3 turns
        # run_config=RunConfig(enable_tracing=False)
    )

    print(f"\nFinal Output after hitting max_turns:\n{result.final_output}")




    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())





