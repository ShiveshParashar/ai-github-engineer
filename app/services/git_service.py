import os
import shutil

from git import Repo


REPOSITORY_DIR = "repositories"


def clone_repository(
    repository_url: str
) -> str:

    os.makedirs(
        REPOSITORY_DIR,
        exist_ok=True
    )

    repository_name = (
        repository_url
        .rstrip("/")
        .split("/")[-1]
    )

    if repository_name.endswith(
        ".git"
    ):

        repository_name = (
            repository_name[:-4]
        )

    repository_path = os.path.join(
        REPOSITORY_DIR,
        repository_name
    )

    # Remove previous clone
    if os.path.exists(
        repository_path
    ):

        shutil.rmtree(
            repository_path
        )

    # Clone
    Repo.clone_from(
        repository_url,
        repository_path
    )

    return repository_path