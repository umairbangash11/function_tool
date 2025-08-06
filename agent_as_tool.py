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

# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True

# )

fruit_agent = Agent(
    name="Fruit agent",
    instructions="You give information about fruits",
    model=model,
)

piaic_agent = Agent(
    name="Piaic agent",
    instructions="You give information about PIAIC",
    model=model,
)

triage_agent = Agent(
    name="TriageAgent",
    instructions=(
        "You are a triage agent.",
        "You use the tools given to you if someone querry about fruits you answer it and if someone querry about piaic you respond by calling the tool."
        "If asked for multiple querries, you call the relevant tools."
    ),
    tools=[
        fruit_agent.as_tool(
            tool_name="fruit_info",
            tool_description="Gives information about fruits",
        ),
        piaic_agent.as_tool(
            tool_name="piaic_info",
            tool_description="Gives information about PIAIC",
        ),
    ],
    model=model,
)


async def main():
    result = await Runner.run(triage_agent, input="what is the taste of apple and my name is umair i am enroll in piaic in 2023 now tell is i am enroll in piaic?.",)
    print("Result_final_Output:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())