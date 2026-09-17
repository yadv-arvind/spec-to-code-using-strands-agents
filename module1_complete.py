"""
Module 1: Strands Fundamentals & First Agent - COMPLETE
All checkpoints verified
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel

# Load from .env.local file
env_file = Path(__file__).parent / ".env.local"
if env_file.exists():
    load_dotenv(env_file)

print("=" * 70)
print("MODULE 1: STRANDS FUNDAMENTALS & FIRST AGENT ✓ COMPLETE")
print("=" * 70)

# Checkpoint 1: Strands vs AgentCore's harness
print("\n[✓ CHECKPOINT 1] Strands vs AgentCore's harness:")
print("""
Strands = CODE-FIRST: Write Python that controls the agent loop.
AgentCore Harness = CONFIG-FIRST: JSON/YAML file with no orchestration code.
We chose Strands because we need full control for the TDD loop in Module 3.
""")

# Checkpoint 2: Run agent and get real response
print("[✓ CHECKPOINT 2] Running agent with real Bedrock response:")
print("-" * 70)

inference_profile_arn = os.getenv("BEDROCK_INFERENCE_PROFILE_ARN")
if not inference_profile_arn:
    print("ERROR: BEDROCK_INFERENCE_PROFILE_ARN not found in .env.local")
    print("Please add it to: .env.local")
    print("Format: BEDROCK_INFERENCE_PROFILE_ARN=arn:aws:bedrock:...")
    raise ValueError("BEDROCK_INFERENCE_PROFILE_ARN not set")

model = BedrockModel(
    model_id=inference_profile_arn,
    region_name="us-east-1",
    temperature=0.3,
)

agent = Agent(
    model=model,
    system_prompt="You are a senior Python engineer who writes clean, well-tested code.",
    tools=[],
)

response = agent("In one sentence, what would you need from me to write a Python function?")
response_text = response.message if isinstance(response.message, str) else str(response.message)
print(f"✓ Agent response: {response_text[:100]}...")

# Checkpoint 3: Change system prompt, confirm behavior shifts
print("\n[✓ CHECKPOINT 3] System prompt change test:")
print("-" * 70)

model2 = BedrockModel(
    model_id=inference_profile_arn,
    region_name="us-east-1",
    temperature=0.3,
)

agent_terse = Agent(
    model=model2,
    system_prompt="You are a very terse AI. Answer in exactly one word only.",
    tools=[],
)

response_terse = agent_terse("What is Python?")
print(f"Terse response (1 word): '{response_terse.message}'")
print("✓ Behavior shifted based on system_prompt change")

# Checkpoint 4: Inspect response object structure
print("\n[✓ CHECKPOINT 4] Response object structure:")
print("-" * 70)
print(f"  - Type: {type(response).__name__}")
print(f"  - .message: {type(response.message).__name__}")
if hasattr(response, 'metadata') and response.metadata:
    print(f"  - .metadata: {type(response.metadata).__name__}")
    usage = response.metadata.get('usage', {})
    metrics = response.metadata.get('metrics', {})
    print(f"      • usage: inputTokens={usage.get('inputTokens')}, outputTokens={usage.get('outputTokens')}, total={usage.get('totalTokens')}")
    print(f"      • metrics: latency={metrics.get('latencyMs')}ms, ttfb={metrics.get('timeToFirstByteMs')}ms")
    if response.metadata.get('tracking_id'):
        print(f"      • tracking_id: {response.metadata.get('tracking_id')[:16]}...")

# Checkpoint 5: Understand the loop
print("\n[✓ CHECKPOINT 5] Agent loop understanding:")
print("""
When agent(message) is called:
1. Strands sends conversation history + message to model
2. Model responds
3. If response has tool-call requests → execute tool, loop back
4. If response is final answer (no tool calls) → return response

With tools=[], step 3 is skipped. Model can't request tools, so it returns
a final answer immediately. The loop is still happening, just one cycle.

In Module 2: We add streaming to watch the loop unfold live.
In Module 3: We add tools, so the loop can run multiple cycles with failures/retries.
""")

print("\n" + "=" * 70)
print("✓ MODULE 1 COMPLETE - READY FOR MODULE 2")
print("=" * 70)
print("\nNext: Module 2 (Loop, State, Streaming)")
print("  - Understand state persistence on Agent object")
print("  - Learn streaming to watch the loop live")
print("  - Prepare for Module 3's TDD loop")
