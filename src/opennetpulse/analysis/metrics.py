
import statistics


def calculate_metrics(latencies):
    """
    Calculate network latency statistics.

    Args:
        latencies (list): List of latency values in milliseconds.

    Returns:
        dict: Calculated network performance metrics.
    """

    # Remove invalid and negative measurements
    valid_latencies = [
        value for value in latencies
        if isinstance(value, (int, float))
        and not isinstance(value, bool)
        and value >= 0
    ]

    if not valid_latencies:
        return {
            "sample_count": 0,
            "minimum_ms": None,
            "maximum_ms": None,
            "average_ms": None,
            "median_ms": None,
            "p95_ms": None,
            "p99_ms": None,
            "jitter_ms": None
        }

    sorted_latencies = sorted(valid_latencies)

    count = len(sorted_latencies)

    # Calculate basic metrics
    minimum = min(sorted_latencies)
    maximum = max(sorted_latencies)
    average = statistics.mean(sorted_latencies)
    median = statistics.median(sorted_latencies)

    # Calculate percentiles using nearest-rank method
    def percentile(data, percentile_value):
        index = max(
            0,
            int((percentile_value / 100) * len(data) + 0.999999) - 1
        )

        return data[min(index, len(data) - 1)]

    p95 = percentile(sorted_latencies, 95)
    p99 = percentile(sorted_latencies, 99)

    # Calculate mean absolute difference between
    # consecutive latency measurements
    if count > 1:
        differences = [
            abs(valid_latencies[i] - valid_latencies[i - 1])
            for i in range(1, count)
        ]

        jitter = statistics.mean(differences)

    else:
        jitter = 0

    return {
        "sample_count": count,
        "minimum_ms": round(minimum, 2),
        "maximum_ms": round(maximum, 2),
        "average_ms": round(average, 2),
        "median_ms": round(median, 2),
        "p95_ms": round(p95, 2),
        "p99_ms": round(p99, 2),
        "jitter_ms": round(jitter, 2)
    }

