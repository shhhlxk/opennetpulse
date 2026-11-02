
import json
import tempfile
import unittest

from pathlib import Path

from opennetpulse.reporting.json_report import (
    create_report,
    save_report
)


class TestJSONReporting(unittest.TestCase):

    def setUp(self):

        self.diagnostics = {
            "dns": {
                "status": "success",
                "resolution_time_ms": 25.5
            },
            "http": {
                "status": "success",
                "status_code": 200
            },
            "tcp": {
                "status": "success",
                "connection_time_ms": 32.1
            }
        }

        self.metrics = {
            "average_ms": 30.2,
            "p95_ms": 45.0
        }

    def test_report_creation(self):

        report = create_report(
            target="google.com",
            diagnostics=self.diagnostics,
            metrics=self.metrics
        )

        self.assertEqual(report["project"], "OpenNetPulse")
        self.assertEqual(report["target"], "google.com")
        self.assertIn("generated_at", report)
        self.assertEqual(report["diagnostics"], self.diagnostics)
        self.assertEqual(report["metrics"], self.metrics)

    def test_report_timestamp(self):

        report = create_report(
            target="example.com",
            diagnostics=self.diagnostics
        )

        timestamp = report["generated_at"]

        self.assertTrue(timestamp.endswith("+00:00"))

    def test_save_report(self):

        report = create_report(
            target="example.com",
            diagnostics=self.diagnostics
        )

        with tempfile.TemporaryDirectory() as directory:

            output_path = Path(directory) / "report.json"

            result = save_report(report, output_path)

            self.assertEqual(result["status"], "success")
            self.assertTrue(output_path.exists())

            with output_path.open(
                "r",
                encoding="utf-8"
            ) as file:

                saved_data = json.load(file)

            self.assertEqual(
                saved_data["target"],
                "example.com"
            )

    def test_create_missing_directories(self):

        report = create_report(
            target="example.com",
            diagnostics=self.diagnostics
        )

        with tempfile.TemporaryDirectory() as directory:

            output_path = (
                Path(directory)
                / "reports"
                / "network"
                / "report.json"
            )

            result = save_report(report, output_path)

            self.assertEqual(result["status"], "success")
            self.assertTrue(output_path.exists())

    def test_save_report_failure(self):

        report = create_report(
            target="example.com",
            diagnostics=self.diagnostics
        )

        with tempfile.TemporaryDirectory() as directory:

            # A directory cannot be opened as a normal file.
            result = save_report(report, directory)

            self.assertEqual(result["status"], "failed")
            self.assertIsNotNone(result["error"])


if __name__ == "__main__":
    unittest.main()
