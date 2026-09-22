import asyncio
import os
from strands import Agent
from strands.models import BedrockModel

# Read inference profile ARN from environment variable
inference_profile_arn = os.getenv("BEDROCK_INFERENCE_PROFILE_ARN")
if not inference_profile_arn:
    raise ValueError("BEDROCK_INFERENCE_PROFILE_ARN environment variable not set. Please export it before running.")

model = BedrockModel(
    model_id=inference_profile_arn,
    region_name="us-east-1",
    temperature=0.3,
)

agent = Agent(model=model, system_prompt="You are a helpful assistant.")

async def main():
    async for event in agent.stream_async("Count from 1 to 5, explaining each number briefly."):
        if "data" in event:
            print(event["data"], end="", flush=True)

asyncio.run(main())
