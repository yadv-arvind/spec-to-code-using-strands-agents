"""
Module 2: State Persistence
Demonstrate multi-turn conversations with state accumulation.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel

# Load environment
env_file = Path(__file__).parent / ".env.local"
if env_file.exists():
    load_dotenv(env_file)

inference_profile_arn = os.getenv("BEDROCK_INFERENCE_PROFILE_ARN")
if not inference_profile_arn:
    raise ValueError("BEDROCK_INFERENCE_PROFILE_ARN not set in .env.local")

# Create model and agent (SINGLE instance — this is key)
model = BedrockModel(
    model_id=inference_profile_arn,
    region_name="us-east-1",
    temperature=0.3,
)

agent = Agent(
    model=model,
    system_prompt="You are a helpful assistant. Keep responses brief (1-2 sentences).",
    tools=[],
)

print("=" * 70)
print("MODULE 2: STATE PERSISTENCE - Multi-turn Conversations")
print("=" * 70)

# TURN 1: Establish context
print("\n[TURN 1] Setting context:")
print("-" * 70)
message1 = "My favorite programming language is Python, and I like functional programming."
print(f"User: {message1}")

response1 = agent(message1)
print(f"Agent: {response1.message}")
print(f"Tokens accumulated: {response1.metadata['usage']['totalTokens']}")

# TURN 2: Reference first message without repeating
print("\n[TURN 2] Agent remembers turn 1:")
print("-" * 70)
message2 = "What language did I just mention?"
print(f"User: {message2}")

response2 = agent(message2)
print(f"Agent: {response2.message}")
print(f"Tokens accumulated: {response2.metadata['usage']['totalTokens']}")

# TURN 3: Build on conversation history
print("\n[TURN 3] Building on conversation history:")
print("-" * 70)
message3 = "Name 3 Python libraries that support functional programming."
print(f"User: {message3}")

response3 = agent(message3)
print(f"Agent: {response3.message}")
print(f"Tokens accumulated: {response3.metadata['usage']['totalTokens']}")

# TURN 4: Check context is maintained
print("\n[TURN 4] Verify context across turns:")
print("-" * 70)
message4 = "Why do you think I like functional programming with Python?"
print(f"User: {message4}")

response4 = agent(message4)
print(f"Agent: {response4.message}")
print(f"Tokens accumulated: {response4.metadata['usage']['totalTokens']}")

# Show what's on the Agent
print("\n" + "=" * 70)
print("CONVERSATION HISTORY (stored on Agent object)")
print("=" * 70)
print(f"Total messages in agent.messages: {len(agent.messages)}")
for i, msg in enumerate(agent.messages, 1):
    role = msg.get('role', 'unknown')
    # Content can be text or list of content blocks
    content = msg.get('content', '')
    if isinstance(content, list):
        # Extract text from content blocks
        text = ' '.join([
            block.get('text', '')
            for block in content
            if isinstance(block, dict) and 'text' in block
        ])
    else:
        text = str(content)[:60] + "..." if len(str(content)) > 60 else str(content)

    print(f"\n[{i}] Role: {role}")
    print(f"    Content: {text}")

# Key insight
print("\n" + "=" * 70)
print("KEY INSIGHT: STATE PERSISTENCE")
print("=" * 70)
print("""
✓ Same Agent instance across 4 calls
✓ Each call re-sends entire conversation history to model
✓ Model has full context from all previous turns
✓ Tokens accumulate: Turn 1 (X) → Turn 2 (X+Y) → Turn 3 (X+Y+Z) → ...

This is why:
- Module 3's TDD loop can call agent() 4-5 times per spec
- You need to track tokens and context window
- Each turn gets more expensive (more history to send)

Next: Learn STREAMING to watch the loop happen live.
""")
