
import socket
import time


def check_dns(domain):
    """
    Resolve a domain name and measure DNS lookup duration.

    Args:
        domain (str): Domain name to resolve.

    Returns:
        dict: DNS diagnostic results.
    """

    start_time = time.perf_counter()

    try:
        results = socket.getaddrinfo(
            domain,
            None,
            type=socket.SOCK_STREAM
        )

        end_time = time.perf_counter()

        ip_addresses = list({
            result[4][0] for result in results
        })

        resolution_time = (end_time - start_time) * 1000

        return {
            "domain": domain,
            "status": "success",
            "ip_addresses": ip_addresses,
            "resolution_time_ms": round(resolution_time, 2),
            "error": None
        }

    except socket.gaierror as error:

        end_time = time.perf_counter()

        resolution_time = (end_time - start_time) * 1000

        return {
            "domain": domain,
            "status": "failed",
            "ip_addresses": [],
            "resolution_time_ms": round(resolution_time, 2),
            "error": str(error)
        }

