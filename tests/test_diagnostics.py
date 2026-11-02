
import unittest
from unittest.mock import patch, MagicMock

from opennetpulse.diagnostics.dns import check_dns
from opennetpulse.diagnostics.http import check_http
from opennetpulse.diagnostics.tcp import check_tcp


class TestDNSDiagnostics(unittest.TestCase):

    @patch("opennetpulse.diagnostics.dns.socket.getaddrinfo")
    def test_dns_success(self, mock_dns):

        mock_dns.return_value = [
            (2, 1, 6, "", ("142.250.183.14", 0))
        ]

        result = check_dns("google.com")

        self.assertEqual(result["status"], "success")
        self.assertIn("142.250.183.14", result["ip_addresses"])
        self.assertIsNone(result["error"])

    @patch("opennetpulse.diagnostics.dns.socket.getaddrinfo")
    def test_dns_failure(self, mock_dns):

        import socket

        mock_dns.side_effect = socket.gaierror("DNS lookup failed")

        result = check_dns("invalid.example")

        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["ip_addresses"], [])
        self.assertIsNotNone(result["error"])


class TestHTTPDiagnostics(unittest.TestCase):

    def test_invalid_url(self):

        result = check_http("not-a-valid-url")

        self.assertEqual(result["status"], "invalid_url")
        self.assertIsNone(result["status_code"])

    @patch("opennetpulse.diagnostics.http.urlopen")
    def test_http_success(self, mock_urlopen):

        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.url = "https://example.com"

        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = check_http("https://example.com")

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["status_code"], 200)
        self.assertIsNone(result["error"])


class TestTCPDiagnostics(unittest.TestCase):

    @patch("opennetpulse.diagnostics.tcp.socket.create_connection")
    def test_tcp_success(self, mock_connection):

        mock_connection.return_value.__enter__.return_value = MagicMock()

        result = check_tcp("example.com", 443)

        self.assertEqual(result["status"], "success")
        self.assertIsNone(result["error"])

    @patch("opennetpulse.diagnostics.tcp.socket.create_connection")
    def test_tcp_failure(self, mock_connection):

        import socket

        mock_connection.side_effect = socket.timeout("Connection timed out")

        result = check_tcp("example.com", 443)

        self.assertEqual(result["status"], "failed")
        self.assertIsNotNone(result["error"])


if __name__ == "__main__":
    unittest.main()
