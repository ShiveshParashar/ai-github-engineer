import os


def detect_tests(repository_path: str):

    test_files = []

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

            if (
                file.startswith("test_")
                or file.endswith("_test.py")
                or "test" in file.lower()
            ):
                test_files.append(
                    os.path.join(root, file)
                )

    return {
        "tests_found": len(test_files) > 0,
        "test_file_count": len(test_files),
        "test_files": test_files
    }