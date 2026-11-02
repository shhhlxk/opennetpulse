
import argparse
from datetime import datetime
from urllib.parse import urlsplit

from opennetpulse.diagnostics.dns import check_dns
from opennetpulse.diagnostics.http import check_http
from opennetpulse.diagnostics.tcp import check_tcp
from opennetpulse.diagnostics.doctor import run_doctor
from opennetpulse.diagnostics.trace import (
    trace_route,
    parse_trace_output
)

from opennetpulse.monitoring.monitor import monitor_host

from opennetpulse.reporting.json_report import (
    create_report,
    save_report
)


def run_diagnostics(target, port=None, timeout=10, output="report.json"):
    """Run DNS, HTTP and TCP diagnostics for a target."""

    if "://" not in target:
        target_url = f"https://{target}"
    else:
        target_url = target

    parsed_url = urlsplit(target_url)
    host = parsed_url.hostname

    if not host:
        print("Error: Invalid target.")
        return 1

    try:
        if port is None:
            port = parsed_url.port
    except ValueError:
        print("Error: Invalid port in target URL.")
        return 1

    if port is None:
        port = 443 if parsed_url.scheme == "https" else 80

    print("\nOPENNETPULSE NETWORK DIAGNOSTICS")
    print("=" * 40)
    print(f"Target: {target}")
    print(f"Host: {host}")
    print(f"TCP Port: {port}")

    print("\n[1] DNS DIAGNOSTICS")
    dns_result = check_dns(host)

    print("Status:", dns_result["status"])
    print("IP Addresses:", dns_result["ip_addresses"])
    print("Resolution Time:", dns_result["resolution_time_ms"], "ms")

    print("\n[2] HTTP DIAGNOSTICS")
    http_result = check_http(target_url, timeout=timeout)

    print("Status:", http_result["status"])
    print("HTTP Status Code:", http_result["status_code"])
    print("Response Time:", http_result["response_time_ms"], "ms")

    print("\n[3] TCP DIAGNOSTICS")
    tcp_result = check_tcp(host, port, timeout=timeout)

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


def run_monitoring(target, port=None, interval=5, duration=60, timeout=5):
    """Run continuous TCP monitoring for a target."""

    if "://" in target:
        try:
            parsed_url = urlsplit(target)
            host = parsed_url.hostname

            if parsed_url.scheme not in ("http", "https") or not host:
                print("Error: Invalid monitoring URL.")
                return 1

            if port is None:
                port = parsed_url.port

            if port is None:
                port = 443 if parsed_url.scheme == "https" else 80

        except ValueError:
            print("Error: Invalid URL or port.")
            return 1

    else:
        host = target

        if port is None:
            port = 443

    print("\nOPENNETPULSE NETWORK MONITOR")
    print("=" * 45)
    print("Target:", host)
    print("TCP Port:", port)
    print("Interval:", interval, "seconds")
    print("Duration:", duration, "seconds")
    print("Monitoring started...\n")

    try:
        result = monitor_host(
            host=host,
            port=port,
            interval=interval,
            duration=duration,
            timeout=timeout
        )

    except ValueError as error:
        print("Error:", error)
        return 1

    print("MONITORING RESULTS")
    print("=" * 45)

    for measurement in result["measurements"]:
        readable_time = datetime.fromtimestamp(
            measurement["timestamp"]
        ).strftime("%H:%M:%S")

        if measurement["status"] == "success":
            print(
                f"[{readable_time}] "
                f"Latency: {measurement['latency_ms']} ms"
            )
        else:
            print(
                f"[{readable_time}] "
                f"Connection failed: {measurement['error']}"
            )

    print("\nSUMMARY")
    print("-" * 45)
    print("Total Measurements:", result["total_measurements"])
    print("Successful:", result["successful_measurements"])
    print("Failed:", result["failed_measurements"])
    print("Connection Failure Rate:", result["packet_loss_percent"], "%")

    metrics = result["metrics"]

    print("\nNETWORK PERFORMANCE")
    print("-" * 45)
    print("Average:", metrics["average_ms"], "ms")
    print("Minimum:", metrics["minimum_ms"], "ms")
    print("Maximum:", metrics["maximum_ms"], "ms")
    print("Median:", metrics["median_ms"], "ms")
    print("P95:", metrics["p95_ms"], "ms")
    print("P99:", metrics["p99_ms"], "ms")
    print("Jitter-like variation:", metrics["jitter_ms"], "ms")

    print("\nMONITORING COMPLETED")
    print("=" * 45)

    return 0


def display_doctor():
    """Display OpenNetPulse environment health checks."""

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


def run_tracing(target, max_hops=30, hop_timeout=1000):
    """Run traceroute and display structured hop results."""

    print("\nOPENNETPULSE ROUTE TRACE")
    print("=" * 50)
    print("Target:", target)
    print("Maximum hops:", max_hops)
    print("Probe timeout:", hop_timeout, "ms")
    print("\nTracing route...\n")

    result = trace_route(
        target=target,
        max_hops=max_hops,
        timeout_ms=hop_timeout
    )

    if result["status"] != "success":
        print("Trace status:", result["status"].upper())
        print("Error:", result.get("error"))
        return 1

    hops = parse_trace_output(result.get("output") or "")

    if not hops:
        print("No hop records could be parsed.")
        print("\nRaw traceroute output:")
        print(result.get("output") or "No output available.")
        return 1

    print(f"{'HOP':<6}{'ADDRESS':<25}{'PROBE TIMES (ms)':<25}{'AVERAGE':<10}")
    print("-" * 66)

    for hop in hops:
        address = hop["address"] or "No response"

        probe_times = [
            "*" if value is None else str(value)
            for value in hop["response_times_ms"]
        ]

        probe_display = " / ".join(probe_times)

        average = (
            f"{hop['average_ms']} ms"
            if hop["average_ms"] is not None
            else "N/A"
        )

        print(
            f"{hop['hop']:<6}"
            f"{address:<25}"
            f"{probe_display:<25}"
            f"{average:<10}"
        )

    print("\nTOTAL HOPS:", len(hops))
    print("Responding hops:", sum(
        1 for hop in hops if hop["status"] == "success"
    ))
    print("Non-responding hops:", sum(
        1 for hop in hops if hop["status"] == "timeout"
    ))

    print("\nROUTE TRACE COMPLETED")
    print("=" * 50)

    return 0


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

    # MONITOR COMMAND
    monitor_parser = subparsers.add_parser(
        "monitor",
        help="Continuously monitor network performance."
    )

    monitor_parser.add_argument(
        "target",
        help="Hostname, IP address or HTTP/HTTPS URL."
    )

    monitor_parser.add_argument(
        "--port",
        type=int,
        help="TCP port to monitor."
    )

    monitor_parser.add_argument(
        "--interval",
        type=float,
        default=5,
        help="Seconds between measurements."
    )

    monitor_parser.add_argument(
        "--duration",
        type=float,
        default=60,
        help="Total monitoring duration in seconds."
    )

    monitor_parser.add_argument(
        "--timeout",
        type=float,
        default=5,
        help="Maximum TCP connection timeout in seconds."
    )

    # TRACE COMMAND
    trace_parser = subparsers.add_parser(
        "trace",
        help="Trace the network route to a destination."
    )

    trace_parser.add_argument(
        "target",
        help="Hostname or IP address to trace."
    )

    trace_parser.add_argument(
        "--max-hops",
        type=int,
        default=30,
        help="Maximum number of hops (1-64)."
    )

    trace_parser.add_argument(
        "--hop-timeout",
        type=int,
        default=1000,
        help="Timeout for each probe in milliseconds."
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

    elif args.command == "monitor":

        if args.interval <= 0:
            parser.error("--interval must be greater than zero.")

        if args.duration <= 0:
            parser.error("--duration must be greater than zero.")

        if args.timeout <= 0:
            parser.error("--timeout must be greater than zero.")

        if args.port is not None and not 1 <= args.port <= 65535:
            parser.error("--port must be between 1 and 65535.")

        return run_monitoring(
            target=args.target,
            port=args.port,
            interval=args.interval,
            duration=args.duration,
            timeout=args.timeout
        )

    elif args.command == "trace":

        if not 1 <= args.max_hops <= 64:
            parser.error("--max-hops must be between 1 and 64.")

        if not 1 <= args.hop_timeout <= 60000:
            parser.error("--hop-timeout must be between 1 and 60000.")

        return run_tracing(
            target=args.target,
            max_hops=args.max_hops,
            hop_timeout=args.hop_timeout
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
