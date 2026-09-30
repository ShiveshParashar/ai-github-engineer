from app.tools.test_runner import analyze_tests


def test_agent(repository_path: str):

    return analyze_tests(
        repository_path
    )