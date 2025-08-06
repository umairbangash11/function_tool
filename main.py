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

# @function_tool
# async def get_weather(city: str) -> str:
#     """
#     Returns weather information for a given city.

#     Args:
#         city: Name of the city to get the weather for.
#     """
#     # Simulated weather data
#     return f"The weather in {city} is sunny."

# @function_tool
# async def piaic(student_name: str) -> str:
#     """
#     Returns PIAIC information for a given student.

#     Args:
#         student_name: Name of the student to get the PIAIC information for.
#     """
#     # Simulated PIAIC data
#     return f"{student_name} is enrolled in PIAIC."

# @function_tool
# async def math(a: int, b: int, operation: str) -> float:
#     """
#     Perform a math operation between two numbers.

#     Args:
#         a: The first number.
#         b: The second number.
#         operation: The operation to perform. One of: add, subtract, multiply, divide.
#     """
#     if operation == "add":
#         return a + b
#     elif operation == "subtract":
#         return a - b
#     elif operation == "multiply":
#         return a * b
#     elif operation == "divide":
#         if b == 0:
#             return "Cannot divide by zero"
#         return a / b
#     else:
#         return "Unknown operation"
# @function_tool
# async def car(model: str = "toyota",  year: int = 2025, price: int = 10000) -> str:
   
#     # Simulated car data
#     return f"The car {model} from {year} is priced at {price}." 

# @function_tool
# async def buyer(name: str) -> str:
#     """
#     Returns buyer information for a given name.

#     Args:
#         name: Name of the buyer to get the information for.
#     """
#     # Simulated buyer data
#     return f"{name} is a buyer."

# @function_tool
# async def car_buying_process(name: str, price: int, model: str):
#     """
#     Returns car buying process information for a given name.

#     Args:
#         name: Name of the buyer to get the information for.
#         price: Price of the car.
#         model: Model of the car.
#     """
#     # Simulated buyer data
#     return f"{name} bought a {model} car for {price}."

# @function_tool
# async def piaic(student_name: str) -> str:
#     """
#     Returns PIAIC information for a given student.

#     Args:
#         student_name: Name of the student to get the PIAIC information for.
#     """
#     # Simulated PIAIC data
#     return f"{student_name} is enrolled in PIAIC."

# @function_tool
# async def weather(city: str) -> str:
#     """
#     Returns weather information for a given city.

#     Args:
#         city: Name of the city to get the weather for.
#     """
#     # Simulated weather data
#     return f"The weather in {city} is sunny."


#this will only give info about fruits not meals
# @function_tool
# async def fruits(fruit_name: str, meal: str, amount:int, price: int):
#     """
#     Return the fruits information and meal informmation also.

#     Args:
#         fruit_name: Name of the fruit to get the taste.
#         price: Price of the fruit.
#     """
#     return f"The name of fruit is{fruit_name} and the meal is {meal} also amount is{amount} and price is{price}"

@function_tool
async def food_info(fruit_name: str, price: int, meal: str, amount: int):
    """
    Return information about fruits or meals.
    
    Args:
        fruit_name: Name of the fruit.
        meal: Name of the meal.
        amount: Amount of dish.
        price: Price of the item.
    """
    #this will give the price and amount same for apple not amount apply on meal
    # return f"The item {fruit_name or meal} has amount {amount} and costs {price}."

    # when you set the price for fruit you put {fruit_name} first after that you set the {price} for fruit.
    #if you set the amount for meal {meal} and then come  {amount}
    return f"The fruit is {fruit_name}, and price is {price}, the meal is {meal}, amount is {amount}."



# async def main():
#     agent = Agent(
#         name="car_buying_agent",
#         instructions="you are helpful assistant someone do a query related to car buying, piaic and weather. you can answer the query.",
#         tools=[fruits],
#         model=model,
#     )

async def main():
    agent = Agent(
        name="taste",
        instructions="You are an assistant who can provide information about fruits and meals using tools.",

        tools=[food_info],
        model=model

    )


    result = await Runner.run(agent, input="i like beef polao and the amount of beef polao is 120. and i like apple too and the price of apple is 300")
    print(result.final_output)


    # result = await Runner.run(agent, input="My name is Umair, I want to buy a Toyota Corolla, model 2013, price 1000 and tell me Umair is enroll in piaic also tell the weather of karachi")
    # print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
