
import socket
import time


def check_tcp(host, port, timeout=5):
    """
    Measure the time required to establish a TCP connection.

    Args:
        host (str): Server hostname or IP address.
        port (int): TCP port number.
        timeout (int): Maximum connection waiting time.

    Returns:
        dict: TCP diagnostic results.
    """

    start_time = time.perf_counter()

    try:
        with socket.create_connection(
            (host, port),
            timeout=timeout
        ):

            end_time = time.perf_counter()

            connection_time = (end_time - start_time) * 1000

            return {
                "host": host,
                "port": port,
                "status": "success",
                "connection_time_ms": round(connection_time, 2),
                "error": None
            }

    except (socket.timeout, TimeoutError, OSError) as error:

        end_time = time.perf_counter()

        connection_time = (end_time - start_time) * 1000

        return {
            "host": host,
            "port": port,
            "status": "failed",
            "connection_time_ms": round(connection_time, 2),
            "error": str(error)
        }

