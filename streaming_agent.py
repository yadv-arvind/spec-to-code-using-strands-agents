"""
Module 2: Streaming
Watch the agent loop happen live with async events.
"""
import asyncio
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

# Create model and agent
model = BedrockModel(
    model_id=inference_profile_arn,
    region_name="us-east-1",
    temperature=0.3,
)

agent = Agent(
    model=model,
    system_prompt="You are a helpful assistant.",
    tools=[],
)

print("=" * 70)
print("MODULE 2: STREAMING - Watch tokens arrive live")
print("=" * 70)

async def stream_example():
    """Stream response events in real-time."""
    print("\nStreaming response (tokens arrive one by one):")
    print("-" * 70)

    event_count = 0
    token_count = 0

    # stream_async returns an async iterator over events
    async for event in agent.stream_async("Count from 1 to 5, explaining each number briefly."):
        event_count += 1

        # Events can contain different types of data
        # Text events have 'data' key with token content
        if isinstance(event, dict) and "data" in event:
            token_count += 1
            print(event["data"], end="", flush=True)

        # You could also handle other event types here
        # (tool calls, stop reasons, etc. — not present with empty tools)

    print("\n\n" + "-" * 70)
    print(f"Event count: {event_count}")
    print(f"Tokens printed: {token_count}")

# Run the async streaming
print("\nExample 1: Basic Streaming")
asyncio.run(stream_example())

print("\n" + "=" * 70)
print("Example 2: Stream with state persistence")
print("=" * 70)

async def multi_turn_streaming():
    """Stream multiple turns to show state persists."""
    print("\n[TURN 1] (streaming)")
    print("-" * 70)
    print("User: Tell me one cool fact about Python.")
    print("Agent: ", end="", flush=True)

    # First message
    async for event in agent.stream_async("Tell me one cool fact about Python."):
        if isinstance(event, dict) and "data" in event:
            print(event["data"], end="", flush=True)

    print("\n")

    # Second message (state persists)
    print("\n[TURN 2] (streaming)")
    print("-" * 70)
    print("User: Can you name 2 libraries mentioned in your previous response?")
    print("Agent: ", end="", flush=True)

    async for event in agent.stream_async("Can you name 2 libraries mentioned in your previous response?"):
        if isinstance(event, dict) and "data" in event:
            print(event["data"], end="", flush=True)

    print("\n")

# Run multi-turn streaming
asyncio.run(multi_turn_streaming())

print("\n" + "=" * 70)
print("KEY INSIGHTS: STREAMING")
print("=" * 70)
print("""
✓ Streaming uses async/await: async for event in agent.stream_async(...)
✓ Events arrive as tokens are generated (real-time)
✓ No waiting for full response
✓ State persists across streamed calls (same Agent instance)

When to use streaming:
- User-facing chat (show responses as they arrive)
- Debugging (watch the loop unfold)
- Long responses (show progress)

When NOT to use:
- You need the full response immediately
- Building intermediate structures

In Module 3:
- You'll stream the TDD loop: write → test → read failure → revise
- Watch as the agent writes code, runs tests, reads actual error output
- See it iterate until tests pass
""")
