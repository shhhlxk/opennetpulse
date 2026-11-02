
import socket
import time

from opennetpulse.analysis.metrics import calculate_metrics


def monitor_host(host, port=443, interval=5, duration=60, timeout=5):
    """
    Continuously monitor a host using TCP connections.

    Returns:
        dict: Monitoring results and performance statistics.
    """

    if not host:
        raise ValueError("Host cannot be empty.")

    if not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
        raise ValueError("Port must be between 1 and 65535.")

    if interval <= 0 or duration <= 0 or timeout <= 0:
        raise ValueError("Interval, duration and timeout must be positive.")

    measurements = []

    start_time = time.monotonic()
    end_time = start_time + duration
    next_measurement = start_time

    while next_measurement < end_time:

        current_time = time.monotonic()

        if current_time < next_measurement:
            time.sleep(next_measurement - current_time)

        if time.monotonic() >= end_time:
            break

        measurement_start = time.perf_counter()

        try:
            with socket.create_connection(
                (host, port),
                timeout=timeout
            ):
                measurement_end = time.perf_counter()

                latency = (
                    measurement_end - measurement_start
                ) * 1000

                result = {
                    "timestamp": time.time(),
                    "status": "success",
                    "latency_ms": round(latency, 2),
                    "error": None
                }

        except (socket.timeout, TimeoutError, OSError) as error:

            result = {
                "timestamp": time.time(),
                "status": "failed",
                "latency_ms": None,
                "error": str(error)
            }

        measurements.append(result)

        next_measurement += interval

    total = len(measurements)

    successful = sum(
        1 for item in measurements
        if item["status"] == "success"
    )

    failed = total - successful

    packet_loss = (
        (failed / total) * 100
        if total else 0
    )

    latencies = [
        item["latency_ms"]
        for item in measurements
        if item["status"] == "success"
    ]

    metrics = calculate_metrics(latencies)

    return {
        "host": host,
        "port": port,
        "total_measurements": total,
        "successful_measurements": successful,
        "failed_measurements": failed,
        "packet_loss_percent": round(packet_loss, 2),
        "metrics": metrics,
        "measurements": measurements
    }
