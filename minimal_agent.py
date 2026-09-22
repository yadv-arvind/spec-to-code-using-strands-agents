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

agent = Agent(
    model=model,
    system_prompt="You are a senior Python engineer who writes clean, well-tested code.",
    tools=[],  # empty on purpose — Module 1 just proves the loop works
)

response = agent("In one sentence, what would you need from me to write a Python function?")
print("Response:", response.message)
