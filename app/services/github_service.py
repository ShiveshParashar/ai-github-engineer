import os


LANGUAGE_EXTENSIONS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".go": "Go",
    ".rs": "Rust",
    ".php": "PHP",
    ".rb": "Ruby",
    ".kt": "Kotlin",
}


def detect_languages(repository_path: str):

    languages = {}

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

            extension = os.path.splitext(file)[1]

            if extension in LANGUAGE_EXTENSIONS:

                language = LANGUAGE_EXTENSIONS[extension]

                languages[language] = (
                    languages.get(language, 0) + 1
                )

    return languages