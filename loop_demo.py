import os
from pathlib import Path
from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel

# Load from .env.local
env_file = Path(__file__).parent / ".env.local"
load_dotenv(env_file)

inference_profile_arn = os.getenv("BEDROCK_INFERENCE_PROFILE_ARN")

model = BedrockModel(
    model_id=inference_profile_arn,
    region_name="us-east-1",
    temperature=0.3,
)
agent = Agent(model=model, system_prompt="You are terse. Answer in one sentence.")

r1 = agent("My favorite language is Python.")
print("Turn 1:", r1.message)

r2 = agent("What's my favorite language?")
print("Turn 2:", r2.message)

for m in agent.messages:
    print(m["role"], "->", str(m["content"])[:80])
