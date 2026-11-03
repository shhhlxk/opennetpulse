import unittest
from unittest.mock import patch, MagicMock

from opennetpulse.diagnostics.ports import scan_port, scan_ports


class TestScanPort(unittest.TestCase):

    @patch("opennetpulse.diagnostics.ports.socket.create_connection")
    def test_open_port(self, mock_connection):
        mock_connection.return_value.__enter__.return_value = MagicMock()

        result = scan_port("localhost", 80)

        self.assertEqual(result["status"], "open")
        self.assertEqual(result["port"], 80)
        self.assertIsInstance(result["latency_ms"], float)
        self.assertIsNone(result["error"])

    @patch(
        "opennetpulse.diagnostics.ports.socket.create_connection",
        side_effect=ConnectionRefusedError
    )
    def test_closed_port(self, mock_connection):
        result = scan_port("localhost", 80)

        self.assertEqual(result["status"], "closed")
        self.assertIsNone(result["latency_ms"])

    @patch(
        "opennetpulse.diagnostics.ports.socket.create_connection",
        side_effect=TimeoutError
    )
    def test_timeout_port(self, mock_connection):
        result = scan_port("localhost", 80)

        self.assertEqual(result["status"], "timeout")

    def test_empty_host(self):
        with self.assertRaises(ValueError):
            scan_port("", 80)

    def test_invalid_port(self):
        for port in [0, 65536, -1, True, 80.5]:
            with self.subTest(port=port):
                with self.assertRaises(ValueError):
                    scan_port("localhost", port)

    def test_invalid_timeout(self):
        for timeout in [0, -1, float("nan"), float("inf"), True]:
            with self.subTest(timeout=timeout):
                with self.assertRaises(ValueError):
                    scan_port("localhost", 80, timeout)


class TestScanPorts(unittest.TestCase):

    @patch("opennetpulse.diagnostics.ports.scan_port")
    def test_scan_summary(self, mock_scan):
        mock_scan.side_effect = [
            {
                "port": 22,
                "status": "open",
                "latency_ms": 2.5,
                "error": None
            },
            {
                "port": 80,
                "status": "closed",
                "latency_ms": None,
                "error": "Connection refused."
            },
            {
                "port": 443,
                "status": "timeout",
                "latency_ms": None,
                "error": "Connection timed out."
            }
        ]

        result = scan_ports("localhost", [22, 80, 443])

        self.assertEqual(result["total_ports"], 3)
        self.assertEqual(result["open_ports"], 1)
        self.assertEqual(result["closed_ports"], 1)
        self.assertEqual(result["timeout_ports"], 1)
        self.assertEqual(
            [item["port"] for item in result["results"]],
            [22, 80, 443]
        )

    def test_empty_ports(self):
        with self.assertRaises(ValueError):
            scan_ports("localhost", [])

    def test_invalid_ports_type(self):
        with self.assertRaises(ValueError):
            scan_ports("localhost", "80,443")


if __name__ == "__main__":
    unittest.main()