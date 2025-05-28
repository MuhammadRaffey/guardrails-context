from agents import (Agent,
                    Runner,
                    RunConfig,
                    OpenAIChatCompletionsModel,
                    AsyncOpenAI,
                    function_tool,
                    RunContextWrapper,
                    set_tracing_disabled
                    )
from dotenv import load_dotenv,find_dotenv
from  openai.types.responses import ResponseTextDeltaEvent
import os
import asyncio
from dataclasses import dataclass

set_tracing_disabled(disabled=True)
_=load_dotenv(find_dotenv())

client=AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
model = OpenAIChatCompletionsModel(
   model="meta-llama/llama-4-scout-17b-16e-instruct",
   openai_client=client,
)

config=RunConfig(
    model=model,
    model_provider=client,
)

@dataclass
class UserInfo:  
    """A data class representing user information.
    
    Attributes:
        name (str): The name of the user
        uid (int): The unique identifier of the user
        age (int): The age of the user
    """
    name: str
    uid: int
    age: int

@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
    """Fetches and returns the age information for a user.
    
    Args:
        wrapper (RunContextWrapper[UserInfo]): A wrapper containing the user information context
        
    Returns:
        str: A formatted string containing the user's name and age
    """
    return f"User {wrapper.context.name} is {wrapper.context.age} years old"

async def main():
    user_info = UserInfo(name="Muhammad Raffey", uid=123,age=20)

    agent = Agent[UserInfo](  
        name="Assistant",
        tools=[fetch_user_age],
        instructions="You are a helpful assistant that can answer questions and help with tasks. You respond in very well written English.Do not display result in json format",
    )
    while True:
        usrInp=input("Enter your question: ")
        if usrInp.lower() == "exit":
            break
        
        result =  Runner.run_streamed(  
            starting_agent=agent,
            input=usrInp,
            context=user_info,
            run_config=config,
        )
        print()
        async for event in result.stream_events():
            if event.type=="raw_response_event"  and isinstance(event.data,ResponseTextDeltaEvent):
                token=event.data.delta
                print(token,end="",flush=True)
        print("\n-------------------------------\n")
if __name__ == "__main__":
    asyncio.run(main())