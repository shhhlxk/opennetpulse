
import argparse
from urllib.parse import urlsplit

from opennetpulse.diagnostics.dns import check_dns
from opennetpulse.diagnostics.http import check_http
from opennetpulse.diagnostics.tcp import check_tcp
from opennetpulse.diagnostics.doctor import run_doctor

from opennetpulse.reporting.json_report import (
    create_report,
    save_report
)


def run_diagnostics(target, port=None, timeout=10, output="report.json"):
    """
    Run DNS, HTTP and TCP diagnostics for a target.
    """

    if "://" not in target:
        target_url = f"https://{target}"
    else:
        target_url = target

    parsed_url = urlsplit(target_url)
    host = parsed_url.hostname

    if not host:
        print("Error: Invalid target.")
        return 1

    if port is None:
        port = parsed_url.port

    if port is None:
        port = 443 if parsed_url.scheme == "https" else 80

    print("\nOPENNETPULSE NETWORK DIAGNOSTICS")
    print("=" * 40)
    print(f"Target: {target}")
    print(f"Host: {host}")
    print(f"TCP Port: {port}")

    # DNS diagnostics
    print("\n[1] DNS DIAGNOSTICS")

    dns_result = check_dns(host)

    print("Status:", dns_result["status"])
    print("IP Addresses:", dns_result["ip_addresses"])
    print("Resolution Time:", dns_result["resolution_time_ms"], "ms")

    # HTTP diagnostics
    print("\n[2] HTTP DIAGNOSTICS")

    http_result = check_http(
        target_url,
        timeout=timeout
    )

    print("Status:", http_result["status"])
    print("HTTP Status Code:", http_result["status_code"])
    print("Response Time:", http_result["response_time_ms"], "ms")

    # TCP diagnostics
    print("\n[3] TCP DIAGNOSTICS")

    tcp_result = check_tcp(
        host,
        port,
        timeout=timeout
    )

    print("Status:", tcp_result["status"])
    print("Connection Time:", tcp_result["connection_time_ms"], "ms")

    diagnostics = {
        "dns": dns_result,
        "http": http_result,
        "tcp": tcp_result
    }

    report = create_report(
        target=target,
        diagnostics=diagnostics
    )

    save_result = save_report(report, output)

    print("\n[4] REPORT")

    if save_result["status"] == "success":
        print("Report saved to:", save_result["file_path"])
    else:
        print("Report could not be saved:", save_result["error"])

    print("\nDIAGNOSTICS COMPLETED")
    print("=" * 40)

    return 0 if save_result["status"] == "success" else 1


def display_doctor():
    """
    Display OpenNetPulse environment health checks.
    """

    result = run_doctor()

    print("\nOPENNETPULSE SYSTEM DIAGNOSTICS")
    print("=" * 45)

    for check in result["checks"]:

        status = check["status"].upper()

        print(f"\n[{status}] {check['name']}")
        print("  ", check["details"])

    print("\n" + "=" * 45)
    print("OVERALL STATUS:", result["status"].upper())
    print("=" * 45)

    return 1 if result["status"] == "unhealthy" else 0


def main():

    parser = argparse.ArgumentParser(
        prog="opennetpulse",
        description="Open-source network diagnostics toolkit."
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # CHECK COMMAND
    check_parser = subparsers.add_parser(
        "check",
        help="Run network diagnostics on a target."
    )

    check_parser.add_argument(
        "target",
        help="Domain or URL to investigate."
    )

    check_parser.add_argument(
        "--port",
        type=int,
        help="TCP port to test."
    )

    check_parser.add_argument(
        "--timeout",
        type=float,
        default=10,
        help="Timeout in seconds."
    )

    check_parser.add_argument(
        "--output",
        default="report.json",
        help="JSON report destination."
    )

    # DOCTOR COMMAND
    subparsers.add_parser(
        "doctor",
        help="Inspect OpenNetPulse system health."
    )

    args = parser.parse_args()

    if args.command == "check":

        if args.timeout <= 0:
            parser.error("--timeout must be greater than zero.")

        if args.port is not None and not 1 <= args.port <= 65535:
            parser.error("--port must be between 1 and 65535.")

        return run_diagnostics(
            target=args.target,
            port=args.port,
            timeout=args.timeout,
            output=args.output
        )

    elif args.command == "doctor":
        return display_doctor()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
