
import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_NAME = "OpenNetPulse"
PROJECT_VERSION = "0.1.0"


def create_report(target, diagnostics, metrics=None):
    """
    Create a structured OpenNetPulse diagnostic report.

    Args:
        target (str): Network destination being tested.
        diagnostics (dict): DNS, HTTP and TCP results.
        metrics (dict): Calculated network performance metrics.

    Returns:
        dict: Complete diagnostic report.
    """

    report = {
        "project": PROJECT_NAME,
        "version": PROJECT_VERSION,

        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "target": target,

        "diagnostics": diagnostics,

        "metrics": metrics or {}
    }

    return report


def save_report(report, output_path="report.json"):
    """
    Save a diagnostic report as a JSON file.

    Args:
        report (dict): Diagnostic report.
        output_path (str): Destination file path.

    Returns:
        dict: Information about the saved report.
    """

    path = Path(output_path)

    # Create parent directories if necessary
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    try:
        with path.open("w", encoding="utf-8") as file:

            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False
            )

        return {
            "status": "success",
            "file_path": str(path),
            "error": None
        }

    except (OSError, TypeError, ValueError) as error:

        return {
            "status": "failed",
            "file_path": str(path),
            "error": str(error)
        }
