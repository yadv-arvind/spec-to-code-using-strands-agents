import os

from strands import Agent

# file_write/python_repl prompt for confirmation on a TTY; a Runtime has no
# interactive user, so an unset value cancels every write.
os.environ.setdefault("BYPASS_TOOL_CONSENT", "true")

from strands_tools import file_write  # noqa: E402

from model.load import load_model
from paths import SANDBOX_DIR
from tools import run_pytest

SYSTEM_PROMPT = f"""You are strands-spec-to-code-agent, an engineering agent that
turns a small Python function spec into working, tested code saved to {SANDBOX_DIR}.

For every spec:
1. Write the implementation to {SANDBOX_DIR}/<name>.py and a pytest test file to
   {SANDBOX_DIR}/test_<name>.py using file_write. Always use these absolute paths.
2. Run the tests immediately using run_pytest.
3. If any test fails, read the ACTUAL failure output, fix only what's broken,
   and re-run. Do not rewrite passing code. Do not guess — use the real output.
4. Repeat step 3 at most 4 times total. If still failing after 4 attempts,
   stop and report the last failure verbatim plus what you tried.
5. Never claim tests pass without having just run them this turn.
"""

def create_agent() -> Agent:
    return Agent(
        model=load_model(),
        system_prompt=SYSTEM_PROMPT,
        tools=[file_write, run_pytest],
    )
