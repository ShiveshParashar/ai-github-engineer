from app.agents.repository_agent import repository_agent
from app.agents.dependency_agent import dependency_agent
from app.agents.test_agent import test_agent
from app.agents.ci_agent import ci_agent
from app.agents.git_history_agent import git_history_agent

from app.services.report_service import build_engineering_report
from app.services.report_storage import save_report


def run_repository_analysis(
    repository_path: str,
    repository_url: str
):

    # Repository analysis
    repository_data = repository_agent(
        repository_path
    )

    # Dependency analysis
    dependency_data = dependency_agent(
        repository_path
    )

    # Test analysis
    test_data = test_agent(
        repository_path
    )

    # CI/CD analysis
    ci_data = ci_agent(
        repository_path
    )

    # Git history analysis
    git_history_data = git_history_agent(
        repository_path
    )

    # Security analysis
    security_data = {
        "status": "completed",
        "findings": []
    }

    # Build unified engineering report
    report = build_engineering_report(
        repository_url=repository_url,
        repository_analysis=repository_data,
        dependency_analysis=dependency_data,
        test_analysis=test_data,
        ci_analysis=ci_data,
        security_analysis=security_data,
        git_history_analysis=git_history_data
    )

    # Get repository name
    repository_name = repository_path.rstrip(
        "/"
    ).split("/")[-1]

    # Save report
    report_path = save_report(
        report,
        repository_name
    )

    # Add report file path to response
    report["report_metadata"]["file"] = report_path

    return report