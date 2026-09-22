import os
from pathlib import Path
from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel
from strands_tools import python_repl, file_write
from tools import run_pytest

env_file = Path(__file__).parent / ".env.local"
load_dotenv(env_file)

SYSTEM_PROMPT = """You are strands-spec-to-code-agent, an engineering agent that
turns a small Python function spec into working, tested code saved to ./sandbox/.

For every spec:
1. Write the implementation to sandbox/<name>.py and a pytest test file to
   sandbox/test_<name>.py using file_write.
2. Run the tests immediately using run_pytest.
3. If any test fails, read the ACTUAL failure output, fix only what's broken,
   and re-run. Do not rewrite passing code. Do not guess — use the real output.
4. Repeat step 3 at most 4 times total. If still failing after 4 attempts,
   stop and report the last failure verbatim plus what you tried.
5. Never claim tests pass without having just run them this turn.
"""

inference_profile_arn = os.getenv("BEDROCK_INFERENCE_PROFILE_ARN")

model = BedrockModel(
    model_id=inference_profile_arn,
    region_name="us-east-1",
    temperature=0.3,
)

agent = Agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[python_repl, file_write, run_pytest],
)

response = agent(
    "Spec: write a function `is_valid_email(addr: str) -> bool` that returns "
    "True for syntactically valid email addresses and False otherwise. "
    "Cover at least: missing @, missing domain, and a valid case."
)
print(response.message)
