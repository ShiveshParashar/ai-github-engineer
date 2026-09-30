from app.tools.git_history_tools import (
    analyze_git_history
)


def git_history_agent(repository_path: str):

    return analyze_git_history(
        repository_path
    )