from datetime import datetime
def calculate_health_summary(
    test_analysis: dict,
    ci_analysis: dict,
    security_analysis: dict
):

    score = 100

    # Tests
    if not test_analysis.get("tests_detected", False):
        score -= 15

    elif test_analysis.get("status") == "FAILED":
        score -= 20

    # CI/CD
    if not ci_analysis.get("ci_found", False):
        score -= 15

    # Security
    security_findings = security_analysis.get(
        "findings",
        []
    )

    critical_count = sum(
        1
        for finding in security_findings
        if finding.get("severity") == "critical"
    )

    high_count = sum(
        1
        for finding in security_findings
        if finding.get("severity") == "high"
    )

    score -= critical_count * 15
    score -= high_count * 8

    score = max(0, score)

    return {
        "score": score,
        "tests": test_analysis.get(
            "status",
            "UNKNOWN"
        ),
        "ci_cd": (
            "FOUND"
            if ci_analysis.get("ci_found")
            else "NOT_FOUND"
        ),
        "critical_security_findings": critical_count,
        "high_security_findings": high_count
    }

from datetime import datetime


def build_engineering_report(
    repository_url: str,
    repository_analysis: dict,
    dependency_analysis: dict,
    test_analysis: dict,
    ci_analysis: dict,
    security_analysis: dict,
    git_history_analysis: dict
):

    health = calculate_health_summary(
        test_analysis,
        ci_analysis,
        security_analysis
    )

    return {

        "report_metadata": {
            "repository_url": repository_url,
            "generated_at": datetime.utcnow().isoformat(),
            "report_version": "1.0"
        },

        "health_summary": health,

        "repository": repository_analysis,

        "code_analysis": {
            "status": "completed"
        },

        "dependencies": dependency_analysis,

        "tests": test_analysis,

        "ci_cd": ci_analysis,

        "security": security_analysis,

        "git_history": git_history_analysis
    }