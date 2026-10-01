import os


LANGUAGE_EXTENSIONS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".java": "Java",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".h": "C/C++",
    ".hpp": "C++",
    ".c": "C",
    ".go": "Go",
    ".rs": "Rust",
    ".php": "PHP",
    ".rb": "Ruby",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".dart": "Dart",
    ".sql": "SQL",
}


IGNORE_DIRS = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    ".idea",
    ".pytest_cache",
    "dist",
    "build",
}


def detect_languages(repository_path: str):

    languages = {}

    for root, dirs, files in os.walk(repository_path):

        dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORE_DIRS
        ]

        for file in files:

            extension = os.path.splitext(
                file
            )[1].lower()

            if extension in LANGUAGE_EXTENSIONS:

                language = LANGUAGE_EXTENSIONS[
                    extension
                ]

                languages[language] = (
                    languages.get(language, 0) + 1
                )

    return languages