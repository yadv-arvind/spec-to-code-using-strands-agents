import subprocess
import sys

from strands import tool

from paths import SANDBOX_DIR


@tool
def run_pytest(test_path: str) -> str:
    """Run pytest against a test file and return combined stdout/stderr.

    Args:
        test_path: Path to the test file to execute, e.g. 'test_foo.py'
    """
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_path, "-v"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=SANDBOX_DIR,
    )
    return result.stdout + result.stderr
