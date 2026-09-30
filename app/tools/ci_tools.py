import os
import yaml


def get_workflow_directory(repository_path: str):

    return os.path.join(
        repository_path,
        ".github",
        "workflows"
    )


def find_workflow_files(repository_path: str):

    workflow_directory = get_workflow_directory(
        repository_path
    )

    if not os.path.exists(workflow_directory):
        return []

    workflow_files = []

    for file in os.listdir(workflow_directory):

        if file.endswith((".yml", ".yaml")):

            workflow_files.append(
                os.path.join(
                    workflow_directory,
                    file
                )
            )

    return workflow_files


def load_workflow(workflow_path: str):

    with open(
        workflow_path,
        "r",
        encoding="utf-8"
    ) as file:

        return yaml.safe_load(file)
def analyze_triggers(workflow):

    triggers = workflow.get("on", [])

    if isinstance(triggers, str):
        triggers = [triggers]

    if triggers is None:
        triggers = []

    if isinstance(triggers, dict):
        triggers = list(triggers.keys())

    return triggers
def analyze_jobs(workflow):

    jobs = workflow.get("jobs", {})

    results = []

    for job_name, job_data in jobs.items():

        results.append({
            "name": job_name,
            "runs_on": job_data.get("runs-on"),
            "steps": len(
                job_data.get("steps", [])
            )
        })

    return results
def analyze_steps(workflow):

    results = []

    jobs = workflow.get("jobs", {})

    for job_name, job_data in jobs.items():

        steps = job_data.get("steps", [])

        for step in steps:

            results.append({
                "job": job_name,
                "name": step.get("name"),
                "uses": step.get("uses"),
                "run": step.get("run")
            })

    return results
def detect_operations(workflow):

    operations = {
        "testing": False,
        "building": False,
        "deployment": False,
        "linting": False,
        "security": False
    }

    jobs = workflow.get("jobs", {})

    for job_data in jobs.values():

        for step in job_data.get("steps", []):

            run_command = step.get("run", "")

            if not isinstance(run_command, str):
                run_command = ""

            text = (
                run_command
                + " "
                + str(step.get("uses", ""))
                + " "
                + str(step.get("name", ""))
            ).lower()

            if any(
                x in text
                for x in [
                    "pytest",
                    "npm test",
                    "jest",
                    "go test",
                    "mvn test"
                ]
            ):
                operations["testing"] = True

            if any(
                x in text
                for x in [
                    "docker build",
                    "npm run build",
                    "mvn package",
                    "gradle build"
                ]
            ):
                operations["building"] = True

            if any(
                x in text
                for x in [
                    "deploy",
                    "vercel",
                    "render",
                    "aws",
                    "kubectl"
                ]
            ):
                operations["deployment"] = True

            if any(
                x in text
                for x in [
                    "flake8",
                    "ruff",
                    "black",
                    "eslint",
                    "pylint"
                ]
            ):
                operations["linting"] = True

            if any(
                x in text
                for x in [
                    "bandit",
                    "trivy",
                    "snyk",
                    "codeql"
                ]
            ):
                operations["security"] = True

    return operations
def analyze_ci(repository_path: str):

    workflow_files = find_workflow_files(
        repository_path
    )

    if not workflow_files:

        return {
            "ci_found": False,
            "workflow_count": 0,
            "workflows": [],
            "message": "No GitHub Actions workflows detected."
        }

    workflows = []

    for workflow_path in workflow_files:

        try:

            workflow = load_workflow(
                workflow_path
            )

            workflows.append({
                "file": os.path.basename(
                    workflow_path
                ),
                "name": workflow.get(
                    "name"
                ),
                "triggers": analyze_triggers(
                    workflow
                ),
                "jobs": analyze_jobs(
                    workflow
                ),
                "steps": analyze_steps(
                    workflow
                ),
                "operations": detect_operations(
                    workflow
                )
            })

        except Exception as e:

            workflows.append({
                "file": os.path.basename(
                    workflow_path
                ),
                "error": str(e)
            })

    return {
        "ci_found": True,
        "workflow_count": len(
            workflow_files
        ),
        "workflows": workflows
    }