import json
import os
from datetime import datetime


def save_report(
    report: dict,
    repository_name: str
):

    os.makedirs(
        "reports",
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"{repository_name}_{timestamp}.json"
    )

    path = os.path.join(
        "reports",
        filename
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            default=str
        )

    return path