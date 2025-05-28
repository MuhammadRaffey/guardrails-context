from agents import (Agent,
                    Runner,
                    RunConfig,
                    OpenAIChatCompletionsModel,
                    AsyncOpenAI,
                    function_tool,
                    RunContextWrapper,
                    set_tracing_disabled,
                    TResponseInputItem,
                    GuardrailFunctionOutput,
                    InputGuardrailTripwireTriggered,
                    OutputGuardrailTripwireTriggered,
                    input_guardrail,
                    output_guardrail,
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
class MathHomeworkOutput:
    is_math_homework: bool
    reasoning: str
    answer: str

guardrail_agent = Agent( 
    name="Guardrail check",
    instructions="Check if the user is asking you to solve a math problem.",
    output_type=MathHomeworkOutput,
)

# output=Runner.run_sync(
#     guardrail_agent,
#     "What is 2 times 10",
#     run_config=config,
# )
# print("Is Math Homework?",output.final_output.is_math_homework)
# print("Reasoning:",output.final_output.reasoning)
# print("Answer:",output.final_output.answer)

@input_guardrail
async def math_homework_guardrail(ctx:RunContextWrapper[None],agent:Agent,input:str|list[TResponseInputItem])->GuardrailFunctionOutput:
    result=await Runner.run(
        guardrail_agent,
        input,
        run_config=config,
        context=ctx.context,
    )
    # print("\n\nGuardrail Result:",result.final_output)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_math_homework,
    )

agent=Agent(
    name="Math Homework Agent",
    instructions="You are a math homework agent. You are given a math homework question and you need to solve it. you answer in plain text.",
    input_guardrails=[math_homework_guardrail],
    
    )

async def main():
    try:
        output=await Runner.run(
            agent,
            "What is the capital of Pakistan?",
            run_config=config,
        )
        print("Final Output:",output.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("Input Guardrail Tripwire Triggered:",e)
   

if __name__=="__main__":
    asyncio.run(main())