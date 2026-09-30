import os
import subprocess


def detect_test_framework(repository_path: str):

    files = os.listdir(repository_path)

    # Pytest configuration
    if "pytest.ini" in files:
        return "pytest"

    # Python project configuration
    if "pyproject.toml" in files:

        pyproject_path = os.path.join(
            repository_path,
            "pyproject.toml"
        )

        with open(
            pyproject_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read().lower()

            if "pytest" in content:
                return "pytest"

    # requirements.txt
    if "requirements.txt" in files:

        requirements_path = os.path.join(
            repository_path,
            "requirements.txt"
        )

        with open(
            requirements_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read().lower()

            if "pytest" in content:
                return "pytest"

    return None


def run_pytest(repository_path: str):

    try:

        result = subprocess.run(
            [
                "python",
                "-m",
                "pytest",
                "-q"
            ],
            cwd=repository_path,
            capture_output=True,
            text=True,
            timeout=300
        )

        return {
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "timed_out": False
        }

    except subprocess.TimeoutExpired:

        return {
            "return_code": None,
            "stdout": "",
            "stderr": "Test execution timed out.",
            "timed_out": True
        }


def analyze_tests(repository_path: str):

    framework = detect_test_framework(
        repository_path
    )

    if framework is None:

        return {
            "tests_detected": False,
            "framework": None,
            "status": "NO_TEST_FRAMEWORK"
        }

    if framework == "pytest":

        result = run_pytest(
            repository_path
        )

        if result["timed_out"]:

            status = "TIMEOUT"

        elif result["return_code"] == 0:

            status = "PASSED"

        else:

            status = "FAILED"

        return {
            "tests_detected": True,
            "framework": "pytest",
            "status": status,
            "return_code": result["return_code"],
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "timed_out": result["timed_out"]
        }