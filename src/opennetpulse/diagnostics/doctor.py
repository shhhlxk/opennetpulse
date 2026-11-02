
import importlib
import importlib.metadata
import platform
import shutil
import sys


def run_doctor():
    """
    Inspect the local environment and OpenNetPulse installation.
    """

    checks = []

    # 1. Python version
    python_version = sys.version_info
    python_ok = python_version >= (3, 10)

    checks.append({
        "name": "Python Version",
        "status": "pass" if python_ok else "fail",
        "details": platform.python_version()
    })

    # 2. Operating system
    checks.append({
        "name": "Operating System",
        "status": "pass",
        "details": platform.system() + " " + platform.release()
    })

    # 3. OpenNetPulse installation
    try:
        version = importlib.metadata.version("opennetpulse")

        checks.append({
            "name": "Package Installation",
            "status": "pass",
            "details": f"Version {version}"
        })

    except importlib.metadata.PackageNotFoundError:

        checks.append({
            "name": "Package Installation",
            "status": "fail",
            "details": "OpenNetPulse is not installed."
        })

    # 4. Internal module imports
    modules = [
        "opennetpulse.diagnostics.dns",
        "opennetpulse.diagnostics.http",
        "opennetpulse.diagnostics.tcp",
        "opennetpulse.analysis.metrics",
        "opennetpulse.reporting.json_report"
    ]

    for module in modules:
        try:
            importlib.import_module(module)

            status = "pass"
            details = "Module loaded successfully."

        except Exception as error:
            status = "fail"
            details = str(error)

        checks.append({
            "name": module,
            "status": status,
            "details": details
        })

    # 5. Available system diagnostic tools
    tools = ["ping"]

    if platform.system() == "Windows":
        tools.append("tracert")
    else:
        tools.append("traceroute")

    for tool in tools:
        location = shutil.which(tool)

        checks.append({
            "name": tool,
            "status": "pass" if location else "warning",
            "details": location or "Tool not found."
        })

    # 6. Overall health
    if any(check["status"] == "fail" for check in checks):
        overall_status = "unhealthy"

    elif any(check["status"] == "warning" for check in checks):
        overall_status = "warning"

    else:
        overall_status = "healthy"

    return {
        "status": overall_status,
        "checks": checks
    }
