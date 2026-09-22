import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel

# Load from .env.local
env_file = Path(__file__).parent / ".env.local"
load_dotenv(env_file)

model = BedrockModel(
    model_id=os.getenv("BEDROCK_INFERENCE_PROFILE_ARN"),
    region_name="us-east-1",
)

agent = Agent(model=model, system_prompt="You are a helpful assistant.")

async def main():
    async for event in agent.stream_async("Count from 1 to 5, explaining each number briefly."):
        if "data" in event:
            print(event["data"], end="", flush=True)

asyncio.run(main())
