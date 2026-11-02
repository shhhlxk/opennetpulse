
import unittest
from unittest.mock import patch, MagicMock

from opennetpulse.monitoring.monitor import monitor_host


class TestNetworkMonitoring(unittest.TestCase):

    @patch("opennetpulse.monitoring.monitor.socket.create_connection")
    def test_successful_monitoring(self, mock_connection):

        mock_connection.return_value = MagicMock()

        result = monitor_host(
            host="example.com",
            port=443,
            interval=0.01,
            duration=0.025,
            timeout=1
        )

        self.assertGreater(result["total_measurements"], 0)
        self.assertEqual(result["failed_measurements"], 0)
        self.assertEqual(result["packet_loss_percent"], 0)

        for measurement in result["measurements"]:
            self.assertEqual(measurement["status"], "success")
            self.assertIsNotNone(measurement["latency_ms"])

    @patch("opennetpulse.monitoring.monitor.socket.create_connection")
    def test_failed_monitoring(self, mock_connection):

        mock_connection.side_effect = OSError("Connection refused")

        result = monitor_host(
            host="example.com",
            port=443,
            interval=0.01,
            duration=0.025,
            timeout=1
        )

        self.assertGreater(result["total_measurements"], 0)
        self.assertEqual(result["successful_measurements"], 0)
        self.assertEqual(result["packet_loss_percent"], 100)

        for measurement in result["measurements"]:
            self.assertEqual(measurement["status"], "failed")
            self.assertIsNone(measurement["latency_ms"])

    def test_invalid_host(self):

        with self.assertRaises(ValueError):
            monitor_host("")

    def test_invalid_port(self):

        with self.assertRaises(ValueError):
            monitor_host("example.com", port=70000)

    def test_invalid_duration(self):

        with self.assertRaises(ValueError):
            monitor_host("example.com", duration=0)


if __name__ == "__main__":
    unittest.main()
