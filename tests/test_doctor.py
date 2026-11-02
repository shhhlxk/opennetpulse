
import unittest
from unittest.mock import patch

from opennetpulse.diagnostics import doctor


class TestDoctor(unittest.TestCase):

    def test_healthy_environment(self):

        with patch.object(
            doctor.importlib.metadata,
            "version",
            return_value="0.1.0"
        ), patch.object(
            doctor.importlib,
            "import_module",
            return_value=None
        ), patch.object(
            doctor.shutil,
            "which",
            return_value="C:\\Windows\\system32\\tool.exe"
        ):

            result = doctor.run_doctor()

        self.assertEqual(result["status"], "healthy")

        for check in result["checks"]:
            self.assertEqual(check["status"], "pass")

    def test_missing_package(self):

        from importlib.metadata import PackageNotFoundError

        with patch.object(
            doctor.importlib.metadata,
            "version",
            side_effect=PackageNotFoundError
        ), patch.object(
            doctor.importlib,
            "import_module",
            return_value=None
        ), patch.object(
            doctor.shutil,
            "which",
            return_value="C:\\Windows\\system32\\tool.exe"
        ):

            result = doctor.run_doctor()

        self.assertEqual(result["status"], "unhealthy")

        package_check = next(
            check for check in result["checks"]
            if check["name"] == "Package Installation"
        )

        self.assertEqual(package_check["status"], "fail")

    def test_missing_system_tool(self):

        with patch.object(
            doctor.importlib.metadata,
            "version",
            return_value="0.1.0"
        ), patch.object(
            doctor.importlib,
            "import_module",
            return_value=None
        ), patch.object(
            doctor.shutil,
            "which",
            return_value=None
        ) as mock_which:

            result = doctor.run_doctor()

        self.assertEqual(result["status"], "warning")
        self.assertEqual(mock_which.call_count, 2)

        tool_checks = [
            check for check in result["checks"]
            if check["name"] in ("ping", "tracert", "traceroute")
        ]

        self.assertEqual(len(tool_checks), 2)

        for check in tool_checks:
            self.assertEqual(check["status"], "warning")


if __name__ == "__main__":
    unittest.main()
