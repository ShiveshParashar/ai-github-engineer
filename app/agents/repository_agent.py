from app.services.github_service import detect_languages

from app.tools.git_tools import (
    get_current_branch,
    get_commit_count,
    get_recent_commits
)

from app.tools.structure_tools import (
    get_project_structure
)


def repository_agent(repository_path: str):

    return {
        "repository_path": repository_path,

        "languages": detect_languages(
            repository_path
        ),

        "current_branch": get_current_branch(
            repository_path
        ),

        "commit_count": get_commit_count(
            repository_path
        ),

        "recent_commits": get_recent_commits(
            repository_path
        ),

        "project_structure": get_project_structure(
            repository_path
        )
    }