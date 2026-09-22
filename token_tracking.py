"""
Module 2: Context Management
Understand token accumulation as conversations grow.
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

# Create model and agent
model = BedrockModel(
    model_id=inference_profile_arn,
    region_name="us-east-1",
    temperature=0.3,
)

agent = Agent(
    model=model,
    system_prompt="You are a helpful assistant. Keep responses brief.",
    tools=[],
)

print("=" * 70)
print("MODULE 2: CONTEXT MANAGEMENT - Token Accumulation")
print("=" * 70)

# Track tokens across turns
turns = [
    "What is Python?",
    "Name 2 Python data structures.",
    "Explain how those data structures differ.",
    "Which would you use for a shopping cart, and why?",
]

total_tokens_sent = 0
cumulative_tokens = []

print("\nTracking token growth across 4 turns:")
print("-" * 70)

for i, message in enumerate(turns, 1):
    response = agent(message)

    input_tokens = response.metadata['usage']['inputTokens']
    output_tokens = response.metadata['usage']['outputTokens']
    total_tokens_this_call = response.metadata['usage']['totalTokens']

    total_tokens_sent += total_tokens_this_call
    cumulative_tokens.append(total_tokens_this_call)

    print(f"\nTurn {i}: '{message[:50]}...'")
    print(f"  Input tokens (history + new):  {input_tokens}")
    print(f"  Output tokens (response):      {output_tokens}")
    print(f"  Total this call:               {total_tokens_this_call}")
    print(f"  Cumulative sent so far:        {total_tokens_sent}")

# Analysis
print("\n" + "=" * 70)
print("TOKEN ACCUMULATION ANALYSIS")
print("=" * 70)

print(f"\nTokens per turn: {cumulative_tokens}")
print(f"Total tokens sent: {total_tokens_sent}")
print(f"Average per turn: {total_tokens_sent / len(turns):.0f}")

# Growth pattern
print("\nGrowth pattern:")
for i in range(1, len(cumulative_tokens)):
    prev = cumulative_tokens[i-1]
    curr = cumulative_tokens[i]
    pct_change = ((curr - prev) / prev * 100) if prev > 0 else 0
    print(f"  Turn {i} → Turn {i+1}: {prev} → {curr} ({pct_change:+.1f}%)")

print("\n" + "=" * 70)
print("KEY INSIGHTS: CONTEXT MANAGEMENT")
print("=" * 70)
print(f"""
Why tokens grow:
- Turn 1: X tokens (initial message + response)
- Turn 2: Y tokens (Turn 1 context + new message + response)
- Turn 3: Z tokens (Turn 1-2 context + new message + response)
- Turn 4: W tokens (Turn 1-3 context + new message + response)

In this session:
- Total sent: {total_tokens_sent} tokens
- If Bedrock costs $0.50 per 1M tokens (input):
  - Cost so far: ${total_tokens_sent * 0.50 / 1_000_000:.4f}

For Module 3's TDD loop (4-5 attempts per spec):
- 1 spec with 5 attempts ≈ {total_tokens_sent * 5} tokens = ${total_tokens_sent * 5 * 0.50 / 1_000_000:.4f}
- 100 specs = {total_tokens_sent * 5 * 100} tokens = ${total_tokens_sent * 5 * 100 * 0.50 / 1_000_000:.2f}

Lesson:
✓ Track tokens early (prevents surprises later)
✓ Understand cost per iteration
✓ Context window limits (model max: 200K-1M tokens)
✓ Long sessions = exponential cost growth
""")

print("\n" + "=" * 70)
print("agent.messages structure (what actually gets sent)")
print("=" * 70)
print(f"\nTotal messages stored on agent: {len(agent.messages)}")
for i, msg in enumerate(agent.messages, 1):
    role = msg.get('role', '?')
    content = msg.get('content', '')
    if isinstance(content, list):
        text_preview = ''.join([
            b.get('text', '')[:40]
            for b in content
            if isinstance(b, dict) and 'text' in b
        ])
    else:
        text_preview = str(content)[:40]

    print(f"[{i}] {role:9} → {text_preview}...")
