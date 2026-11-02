
import unittest

from opennetpulse.diagnostics.trace import (
    parse_trace_output,
    trace_route
)


class TestTraceroute(unittest.TestCase):

    def test_successful_hop(self):
        output = "  1    2 ms    3 ms    4 ms  192.168.1.1"

        hops = parse_trace_output(output)

        self.assertEqual(len(hops), 1)
        self.assertEqual(hops[0]["address"], "192.168.1.1")
        self.assertEqual(hops[0]["average_ms"], 3.0)
        self.assertEqual(hops[0]["status"], "success")

    def test_partial_timeout(self):
        output = "  2    5 ms    *    7 ms  10.0.0.1"

        hops = parse_trace_output(output)

        self.assertEqual(hops[0]["response_times_ms"], [5.0, None, 7.0])
        self.assertEqual(hops[0]["average_ms"], 6.0)
        self.assertEqual(hops[0]["status"], "success")

    def test_complete_timeout(self):
        output = "  3    *    *    *  Request timed out."

        hops = parse_trace_output(output)

        self.assertEqual(hops[0]["address"], None)
        self.assertEqual(hops[0]["average_ms"], None)
        self.assertEqual(hops[0]["status"], "timeout")

    def test_invalid_max_hops(self):
        with self.assertRaises(ValueError):
            trace_route("google.com", max_hops=100)

    def test_invalid_timeout(self):
        with self.assertRaises(ValueError):
            trace_route("google.com", timeout_ms=0)

    def test_empty_output(self):
        hops = parse_trace_output("")

        self.assertEqual(hops, [])

    def test_non_string_output(self):
        with self.assertRaises(ValueError):
            parse_trace_output(None)

    def test_unrelated_lines_are_ignored(self):
        output = """
        Tracing route to google.com
        over a maximum of 30 hops:

          1    2 ms    3 ms    4 ms  192.168.1.1

        Trace complete.
        """

        hops = parse_trace_output(output)

        self.assertEqual(len(hops), 1)
        self.assertEqual(hops[0]["hop"], 1)


if __name__ == "__main__":
    unittest.main()
