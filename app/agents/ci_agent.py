from app.tools.ci_tools import analyze_ci


def ci_agent(repository_path: str):

    return analyze_ci(
        repository_path
    )