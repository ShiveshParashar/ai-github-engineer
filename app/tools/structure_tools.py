import os


IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    ".idea",
    ".pytest_cache",
    "dist",
    "build",
    ".mypy_cache",
}


def get_project_structure(repository_path: str):

    structure = []

    for root, dirs, files in os.walk(repository_path):

        # Ignore unnecessary directories
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORE_DIRS
        ]

        relative_root = os.path.relpath(
            root,
            repository_path
        )

        if relative_root == ".":
            level = 0
        else:
            level = relative_root.count(os.sep) + 1

        indent = "    " * level

        # Add directory
        if relative_root != ".":
            structure.append(
                f"{indent}{os.path.basename(root)}/"
            )

        # Add files
        for file in sorted(files):

            structure.append(
                f"{indent}    {file}"
            )

    return structure[:300]