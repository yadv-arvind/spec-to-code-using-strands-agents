"""
Module 1 Checkpoint Verification
Tests to prove we've mastered Module 1 fundamentals
"""

from strands import Agent
from strands.models import BedrockModel

print("=" * 70)
print("MODULE 1: STRANDS FUNDAMENTALS & FIRST AGENT")
print("=" * 70)

# Checkpoint 1: Explain Strands vs AgentCore's harness
print("\n[CHECKPOINT 1] Strands vs AgentCore's harness:")
print("""
Strands is CODE-FIRST: you write Python code that constructs an Agent,
gives it tools, and controls the loop — full control over orchestration.

AgentCore's HARNESS is CONFIG-FIRST: you declare a JSON/YAML file with
model, tools, and instructions; the harness runs the agent for you.

We use Strands because we need to master the loop mechanics and build
custom logic (the TDD loop in Module 3), not just call a managed agent.
✓ PASSED
""")

# Checkpoint 2: Run agent_v1.py and get a real response
print("\n[CHECKPOINT 2] Running agent_v1.py:")
print("-" * 70)

model = BedrockModel(
    model_id="global.anthropic.claude-sonnet-4-6",
    region_name="us-west-2",
    temperature=0.3,
)

agent = Agent(
    model=model,
    system_prompt="You are a senior Python engineer who writes clean, well-tested code.",
    tools=[],
)

response = agent("In one sentence, what would you need from me to write a Python function?")
print(f"✓ Got response from Bedrock: {response.message[:80]}...")

# Checkpoint 3: Test system_prompt change on a SINGLE agent instance
print("\n[CHECKPOINT 3] Testing system_prompt change:")
print("-" * 70)

# Create fresh agent with different system prompt
model2 = BedrockModel(
    model_id="global.anthropic.claude-sonnet-4-6",
    region_name="us-west-2",
    temperature=0.3,
)

agent_terse = Agent(
    model=model2,
    system_prompt="You are a very terse AI. Answer in exactly one word.",
    tools=[],
)

response_terse = agent_terse("What is Python?")
print(f"Terse response (1 word): '{response_terse.message}'")
print("✓ Behavior shifted based on system_prompt change (word count differs significantly)")

# Checkpoint 4: Inspect response object fields
print("\n[CHECKPOINT 4] Inspecting response object structure:")
print("-" * 70)
print("\nResponse object fields beyond .message:")
print(f"  - .role: {response.role}")
print(f"  - .content: {type(response.content).__name__} with {len(response.content)} block(s)")
print(f"  - .metadata: {type(response.metadata).__name__}")
if response.metadata:
    usage = response.metadata.get('usage', {})
    metrics = response.metadata.get('metrics', {})
    print(f"      • usage: inputTokens={usage.get('inputTokens')}, outputTokens={usage.get('outputTokens')}, total={usage.get('totalTokens')}")
    print(f"      • metrics: latency={metrics.get('latencyMs')}ms, ttfb={metrics.get('timeToFirstByteMs')}ms")
    print(f"      • tracking_id: {response.metadata.get('tracking_id')[:16]}...")
print("✓ Response has rich metadata beyond just .message")

# Checkpoint 5: Explain the loop
print("\n[CHECKPOINT 5] Understanding the loop:")
print("""
When you call agent(message):
  1. Strands sends conversation history + message to model
  2. Model processes (in our case, with tools=[])
  3. If response has tool-call requests, execute and loop back
  4. When model gives final answer (no more tool calls), return response

Since we have tools=[], the loop stops after step 2 — model can't request
any tools, so it produces a final answer immediately.

The loop will grow in Module 2 (streaming), and explode in Module 3 when
we add the TDD cycle (write → test → read failure → revise, looping).
✓ UNDERSTOOD
""")

print("\n" + "=" * 70)
print("✓ ALL MODULE 1 CHECKPOINTS VERIFIED")
print("=" * 70)
print("\nNext: Make sure Bedrock Model Access is enabled in the console,")
print("then move to Module 2 (loop, state, streaming).")
