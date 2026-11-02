
import platform
import re
import shutil
import subprocess


def trace_route(target, max_hops=30, timeout_ms=1000):
    """Trace the network route using the Windows tracert utility."""

    if not isinstance(target, str) or not target.strip():
        raise ValueError("Target cannot be empty.")

    if (
        not isinstance(max_hops, int)
        or isinstance(max_hops, bool)
        or not 1 <= max_hops <= 64
    ):
        raise ValueError("Maximum hops must be between 1 and 64.")

    if (
        not isinstance(timeout_ms, int)
        or isinstance(timeout_ms, bool)
        or not 1 <= timeout_ms <= 60000
    ):
        raise ValueError("Timeout must be between 1 and 60000 milliseconds.")

    target = target.strip()

    if platform.system() != "Windows":
        return {
            "target": target,
            "status": "unsupported",
            "output": None,
            "error": "This implementation currently supports Windows only."
        }

    tracert_path = shutil.which("tracert")

    if not tracert_path:
        return {
            "target": target,
            "status": "failed",
            "output": None,
            "error": "Windows tracert utility was not found."
        }

    command = [
        tracert_path,
        "-d",
        "-h", str(max_hops),
        "-w", str(timeout_ms),
        target
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=(max_hops * timeout_ms / 1000) + 15,
            check=False
        )

        return {
            "target": target,
            "status": "success" if result.returncode == 0 else "failed",
            "return_code": result.returncode,
            "output": result.stdout.strip(),
            "error": result.stderr.strip() or None
        }

    except subprocess.TimeoutExpired:
        return {
            "target": target,
            "status": "timeout",
            "output": None,
            "error": "Traceroute execution exceeded the time limit."
        }

    except OSError as error:
        return {
            "target": target,
            "status": "failed",
            "output": None,
            "error": str(error)
        }


def parse_trace_output(output):
    """Parse Windows tracert output into structured hop records."""

    if not isinstance(output, str):
        raise ValueError("Traceroute output must be a string.")

    hops = []

    time_token = r"(?:\*|<\s*\d+\s*ms|\d+\s*ms)"

    pattern = re.compile(
        r"^\s*(\d+)\s+"
        r"(" + time_token + r")\s+"
        r"(" + time_token + r")\s+"
        r"(" + time_token + r")\s+"
        r"(.*?)\s*$",
        re.IGNORECASE
    )

    for line in output.splitlines():

        match = pattern.match(line)

        if not match:
            continue

        hop_number = int(match.group(1))
        raw_times = match.group(2, 3, 4)
        destination = match.group(5).strip()

        response_times = []

        for value in raw_times:

            value = value.strip()

            if value == "*":
                response_times.append(None)

            elif value.startswith("<"):
                # Approximation: less than 1 ms is represented as 0.5 ms.
                response_times.append(0.5)

            else:
                milliseconds = re.fullmatch(
                    r"(\d+)\s*ms",
                    value,
                    re.IGNORECASE
                )

                if not milliseconds:
                    response_times.append(None)
                else:
                    response_times.append(float(milliseconds.group(1)))

        responding_times = [
            value for value in response_times
            if value is not None
        ]

        address = (
            None
            if destination.lower() == "request timed out."
            else destination or None
        )

        hops.append({
            "hop": hop_number,
            "address": address,
            "response_times_ms": response_times,
            "average_ms": (
                round(
                    sum(responding_times) / len(responding_times),
                    2
                )
                if responding_times else None
            ),
            "status": "success" if responding_times else "timeout"
        })

    return hops
