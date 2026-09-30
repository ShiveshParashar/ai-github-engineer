from app.services.github_service import detect_languages
from app.tools.git_tools import (
    get_current_branch,
    get_commit_count,
    get_recent_commits
)
from app.tools.ci_tools import detect_ci
from app.tools.test_tools import detect_tests


def repository_agent(repository_path: str):

    languages = detect_languages(repository_path)

    branch = get_current_branch(repository_path)

    commit_count = get_commit_count(repository_path)

    recent_commits = get_recent_commits(repository_path)

    ci = detect_ci(repository_path)

    tests = detect_tests(repository_path)

    return {
        "repository_path": repository_path,
        "languages": languages,
        "current_branch": branch,
        "commit_count": commit_count,
        "recent_commits": recent_commits,
        "ci": ci,
        "tests": tests
    }