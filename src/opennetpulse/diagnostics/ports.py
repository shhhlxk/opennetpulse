
import math
import socket
import time


def scan_port(host, port, timeout=1.0):
    """Check whether a TCP port accepts a connection."""

    if not isinstance(host, str) or not host.strip():
        raise ValueError("Host cannot be empty.")

    if (
        not isinstance(port, int)
        or isinstance(port, bool)
        or not 1 <= port <= 65535
    ):
        raise ValueError("Port must be between 1 and 65535.")

    if (
        not isinstance(timeout, (int, float))
        or isinstance(timeout, bool)
        or not math.isfinite(timeout)
        or timeout <= 0
    ):
        raise ValueError("Timeout must be a positive finite number.")

    start_time = time.perf_counter()

    try:
        with socket.create_connection(
            (host.strip(), port),
            timeout=timeout
        ):
            latency = (time.perf_counter() - start_time) * 1000

            return {
                "port": port,
                "status": "open",
                "latency_ms": round(latency, 2),
                "error": None
            }

    except ConnectionRefusedError:
        return {
            "port": port,
            "status": "closed",
            "latency_ms": None,
            "error": "Connection refused."
        }

    except (socket.timeout, TimeoutError):
        return {
            "port": port,
            "status": "timeout",
            "latency_ms": None,
            "error": "Connection timed out."
        }

    except OSError as error:
        return {
            "port": port,
            "status": "error",
            "latency_ms": None,
            "error": str(error)
        }


def scan_ports(host, ports, timeout=1.0):
    """Scan a list of TCP ports on a target host."""

    if not isinstance(ports, (list, tuple)) or not ports:
        raise ValueError("Provide at least one port to scan.")

    results = [
        scan_port(host, port, timeout)
        for port in ports
    ]

    return {
        "host": host.strip(),
        "total_ports": len(results),
        "open_ports": sum(
            1 for result in results
            if result["status"] == "open"
        ),
        "closed_ports": sum(
            1 for result in results
            if result["status"] == "closed"
        ),
        "timeout_ports": sum(
            1 for result in results
            if result["status"] == "timeout"
        ),
        "results": results
    }
