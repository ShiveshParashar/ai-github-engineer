from app.tools.dependency_tools import (
    analyze_dependencies
)


def dependency_agent(repository_path: str):

    return analyze_dependencies(
        repository_path
    )