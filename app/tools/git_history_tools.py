import subprocess


def run_git_command(repository_path: str, command: list[str]):

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


def get_total_commits(repository_path: str):

    result = run_git_command(
        repository_path,
        ["rev-list", "--count", "HEAD"]
    )

    return result["stdout"].strip()


def get_current_branch(repository_path: str):

    result = run_git_command(
        repository_path,
        ["branch", "--show-current"]
    )

    return result["stdout"].strip()


def get_branches(repository_path: str):

    result = run_git_command(
        repository_path,
        ["branch", "--format=%(refname:short)"]
    )

    return [
        branch.strip()
        for branch in result["stdout"].splitlines()
        if branch.strip()
    ]


def get_recent_commits(
    repository_path: str,
    limit: int = 20
):

    result = run_git_command(
        repository_path,
        [
            "log",
            f"-{limit}",
            "--pretty=format:%H|%an|%ad|%s",
            "--date=iso"
        ]
    )

    commits = []

    for line in result["stdout"].splitlines():

        parts = line.split("|", 3)

        if len(parts) != 4:
            continue

        commits.append({
            "hash": parts[0],
            "author": parts[1],
            "date": parts[2],
            "message": parts[3]
        })

    return commits
def get_contributors(repository_path: str):

    result = run_git_command(
        repository_path,
        [
            "shortlog",
            "-s",
            "-n",
            "HEAD"
        ]
    )

    contributors = []

    for line in result["stdout"].splitlines():

        line = line.strip()

        if not line:
            continue

        parts = line.split("\t", 1)

        if len(parts) != 2:
            continue

        contributors.append({
            "commits": int(parts[0].strip()),
            "author": parts[1].strip()
        })

    return contributors

def get_frequently_modified_files(
    repository_path: str,
    limit: int = 15
):

    result = run_git_command(
        repository_path,
        [
            "log",
            "--name-only",
            "--pretty=format:"
        ]
    )

    file_counts = {}

    for line in result["stdout"].splitlines():

        file_path = line.strip()

        if not file_path:
            continue

        file_counts[file_path] = (
            file_counts.get(file_path, 0) + 1
        )

    sorted_files = sorted(
        file_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return [
        {
            "file": file_path,
            "changes": count
        }
        for file_path, count in sorted_files[:limit]
    ]
from datetime import datetime, timezone


def get_latest_commit(repository_path: str):

    result = run_git_command(
        repository_path,
        [
            "log",
            "-1",
            "--pretty=format:%H|%an|%ad|%s",
            "--date=iso"
        ]
    )

    line = result["stdout"].strip()

    if not line:
        return None

    parts = line.split("|", 3)

    if len(parts) != 4:
        return None

    return {
        "hash": parts[0],
        "author": parts[1],
        "date": parts[2],
        "message": parts[3]
    }
def analyze_git_history(repository_path: str):

    total_commits = get_total_commits(
        repository_path
    )

    current_branch = get_current_branch(
        repository_path
    )

    branches = get_branches(
        repository_path
    )

    recent_commits = get_recent_commits(
        repository_path
    )

    contributors = get_contributors(
        repository_path
    )

    frequently_modified_files = (
        get_frequently_modified_files(
            repository_path
        )
    )

    latest_commit = get_latest_commit(
        repository_path
    )

    return {
        "total_commits": total_commits,
        "current_branch": current_branch,
        "branches": branches,
        "contributor_count": len(
            contributors
        ),
        "contributors": contributors,
        "recent_commits": recent_commits,
        "latest_commit": latest_commit,
        "frequently_modified_files":
            frequently_modified_files
    }