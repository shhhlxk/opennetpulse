
import unittest

from opennetpulse.analysis.metrics import calculate_metrics


class TestNetworkMetrics(unittest.TestCase):

    def test_empty_measurements(self):
        result = calculate_metrics([])

        self.assertEqual(result["sample_count"], 0)
        self.assertIsNone(result["average_ms"])
        self.assertIsNone(result["p95_ms"])

    def test_basic_statistics(self):
        result = calculate_metrics([10, 20, 30, 40, 50])

        self.assertEqual(result["sample_count"], 5)
        self.assertEqual(result["minimum_ms"], 10)
        self.assertEqual(result["maximum_ms"], 50)
        self.assertEqual(result["average_ms"], 30)
        self.assertEqual(result["median_ms"], 30)

    def test_percentiles(self):
        measurements = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        result = calculate_metrics(measurements)

        self.assertEqual(result["p95_ms"], 100)
        self.assertEqual(result["p99_ms"], 100)

    def test_single_measurement(self):
        result = calculate_metrics([25])

        self.assertEqual(result["sample_count"], 1)
        self.assertEqual(result["average_ms"], 25)
        self.assertEqual(result["median_ms"], 25)
        self.assertEqual(result["jitter_ms"], 0)

    def test_invalid_measurements(self):
        result = calculate_metrics([
            10,
            20,
            -5,
            "invalid",
            True,
            30
        ])

        self.assertEqual(result["sample_count"], 3)
        self.assertEqual(result["average_ms"], 20)


if __name__ == "__main__":
    unittest.main()
