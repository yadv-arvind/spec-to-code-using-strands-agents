import subprocess
from strands import tool
from strands_tools import python_repl, file_write

@tool
def run_pytest(test_path: str) -> str:
    """Run pytest against a test file and return combined stdout/stderr.

    Args:
        test_path: Path to the test file to execute, e.g. 'sandbox/test_foo.py'
    """
    result = subprocess.run(
        ["pytest", test_path, "-v"], capture_output=True, text=True, timeout=30
    )
    return result.stdout + result.stderr
