import os
import json
import re


def detect_dependency_files(repository_path: str):

    dependency_files = []

    known_files = [
        "requirements.txt",
        "requirements-dev.txt",
        "pyproject.toml",
        "Pipfile",
        "Pipfile.lock",
        "package.json",
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "pom.xml",
        "build.gradle",
        "go.mod",
        "Cargo.toml",
    ]

    for root, dirs, files in os.walk(repository_path):

        dirs[:] = [
            d for d in dirs
            if d not in {
                ".git",
                "node_modules",
                "venv",
                ".venv"
            }
        ]

        for file in files:

            if file in known_files:

                dependency_files.append(
                    os.path.relpath(
                        os.path.join(root, file),
                        repository_path
                    )
                )

    return dependency_files
def parse_requirements(repository_path: str):

    requirements_path = os.path.join(
        repository_path,
        "requirements.txt"
    )

    if not os.path.exists(requirements_path):
        return []

    dependencies = []

    with open(
        requirements_path,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            dependencies.append(line)

    return dependencies
def parse_package_json(repository_path: str):

    package_path = os.path.join(
        repository_path,
        "package.json"
    )

    if not os.path.exists(package_path):
        return {}

    with open(
        package_path,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return {
        "dependencies": data.get(
            "dependencies",
            {}
        ),
        "dev_dependencies": data.get(
            "devDependencies",
            {}
        )
    }
def analyze_dependencies(repository_path: str):

    dependency_files = detect_dependency_files(
        repository_path
    )

    requirements = parse_requirements(
        repository_path
    )

    package_json = parse_package_json(
        repository_path
    )

    return {
        "dependency_files": dependency_files,
        "python_dependencies": requirements,
        "npm_dependencies": package_json
    }