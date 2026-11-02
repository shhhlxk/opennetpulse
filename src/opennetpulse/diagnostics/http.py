
import time
import socket

from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit


def check_http(url, timeout=10):
    """
    Measure the time taken to receive HTTP response headers.

    Args:
        url (str): Website URL.
        timeout (int): Maximum waiting time in seconds.

    Returns:
        dict: HTTP diagnostic results.
    """

    # Validate URL
    parsed_url = urlsplit(url)

    if parsed_url.scheme not in ("http", "https") or not parsed_url.hostname:
        return {
            "url": url,
            "status": "invalid_url",
            "status_code": None,
            "response_time_ms": None,
            "final_url": None,
            "error": "A valid HTTP or HTTPS URL is required."
        }

    # Create HTTP request
    request = Request(
        url,
        headers={
            "User-Agent": "OpenNetPulse/0.1.0"
        },
        method="GET"
    )

    start_time = time.perf_counter()

    try:
        with urlopen(request, timeout=timeout) as response:

            end_time = time.perf_counter()

            response_time = (end_time - start_time) * 1000

            status_code = response.status

            return {
                "url": url,
                "status": "success" if status_code < 400 else "http_error",
                "status_code": status_code,
                "response_time_ms": round(response_time, 2),
                "final_url": response.url,
                "error": None
            }

    except HTTPError as error:

        end_time = time.perf_counter()

        response_time = (end_time - start_time) * 1000

        return {
            "url": url,
            "status": "http_error",
            "status_code": error.code,
            "response_time_ms": round(response_time, 2),
            "final_url": error.url,
            "error": str(error)
        }

    except (URLError, TimeoutError, socket.timeout, OSError) as error:

        end_time = time.perf_counter()

        response_time = (end_time - start_time) * 1000

        return {
            "url": url,
            "status": "failed",
            "status_code": None,
            "response_time_ms": round(response_time, 2),
            "final_url": None,
            "error": str(error)
        }

