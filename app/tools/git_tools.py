import os
import subprocess


def run_git_command(
    repository_path: str,
    command: list[str]
):

    result = subprocess.run(
        ["git"] + command,
        cwd=repository_path,
        capture_output=True,
        text=True
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "return_code": result.returncode
    }


def get_current_branch(repository_path: str):

    result = run_git_command(
        repository_path,
        ["branch", "--show-current"]
    )

    return result["stdout"].strip()


def get_commit_count(repository_path: str):

    result = run_git_command(
        repository_path,
        ["rev-list", "--count", "HEAD"]
    )

    return result["stdout"].strip()


def get_recent_commits(repository_path: str):

    result = run_git_command(
        repository_path,
        [
            "log",
            "--oneline",
            "-10"
        ]
    )

    return result["stdout"].splitlines()