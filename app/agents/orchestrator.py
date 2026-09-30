from app.agents.repository_agent import repository_agent
from app.services.llm_service import generate_repository_summary
from app.agents.dependency_agent import (
    dependency_agent
)
from app.agents.repository_agent import repository_agent
from app.agents.dependency_agent import dependency_agent
from app.agents.test_agent import test_agent
from app.agents.ci_agent import ci_agent
def run_repository_analysis(repository_path: str):

    repository_data = repository_agent(
        repository_path
    )

    dependency_data = dependency_agent(
        repository_path
    )

    test_data = test_agent(
        repository_path
    )

    ci_data = ci_agent(
        repository_path
    )

    return {
        "repository_analysis": repository_data,
        "dependency_analysis": dependency_data,
        "test_analysis": test_data,
        "ci_analysis": ci_data
    }
def run_repository_analysis(repository_path: str):

    repository_data = repository_agent(
        repository_path
    )

    dependency_data = dependency_agent(
        repository_path
    )

    test_data = test_agent(
        repository_path
    )

    return {
        "repository_analysis": repository_data,
        "dependency_analysis": dependency_data,
        "test_analysis": test_data
    }
    
def run_repository_analysis(repository_path: str):

    repository_data = repository_agent(
        repository_path
    )

    dependency_data = dependency_agent(
        repository_path
    )

    return {
        "repository_analysis": repository_data,
        "dependency_analysis": dependency_data
    }

def run_repository_analysis(repository_path: str):

    repository_data = repository_agent(
        repository_path
    )

    summary = generate_repository_summary(
        repository_data
    )

    return {
        "repository_analysis": repository_data,
        "ai_summary": summary
    }