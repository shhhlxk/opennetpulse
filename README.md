# \# OpenNetPulse

# 

# \*\*An open-source Python network diagnostics and monitoring toolkit.\*\*

# 

# OpenNetPulse is a command-line network diagnostics toolkit designed to help developers and network enthusiasts investigate connectivity, monitor network performance, trace network routes, and inspect TCP port availability.

# 

# The project combines Python networking libraries with command-line tools to provide practical network troubleshooting capabilities.

# 

# \## Features

# 

# \### 1. Network Diagnostics (`check`)

# \- DNS resolution checks

# \- HTTP/HTTPS response checks

# \- TCP connectivity tests

# \- Connection and response timing

# \- JSON diagnostic reports

# 

# \### 2. System Health Check (`doctor`)

# \- Python version verification

# \- Operating system information

# \- Package installation checks

# \- Internal module verification

# \- Required system utility checks

# 

# \### 3. Network Monitoring (`monitor`)

# \- Continuous TCP connectivity monitoring

# \- Configurable monitoring intervals

# \- Connection success and failure tracking

# \- Average, minimum and maximum latency

# \- Median, P95 and P99 latency metrics

# \- Jitter-like latency variation

# 

# \### 4. Route Tracing (`trace`)

# \- Traces the network path to a destination

# \- Displays intermediate network hops

# \- Shows responding IP addresses

# \- Measures probe response times

# \- Identifies non-responding hops

# 

# \*Note: The current implementation uses the native Windows `tracert` utility.\*

# 

# \### 5. TCP Port Scanner (`ports`) — New

# \- Scans individual TCP ports or custom port lists

# \- Checks common service ports

# \- Identifies open and closed ports

# \- Detects connection timeouts

# \- Measures connection latency

# \- Displays scan summaries

# \- Supports configurable connection timeouts

# 

# \## Technology Stack

# 

# | Technology | Purpose |

# |---|---|

# | Python | Core programming language |

# | Socket | TCP and DNS networking |

# | urllib | HTTP/HTTPS diagnostics |

# | Argparse | Command-line interface |

# | Subprocess | System traceroute integration |

# | Unittest | Automated testing |

# | Git \& GitHub | Version control |

# 

# \## Installation

# 

# \### Prerequisites

# 

# \- Python 3.10 or newer

# \- Git

# \- Windows, Linux or macOS (some system utilities are platform-dependent)

# 

# \### Clone the repository

# 

# ```bash

# git clone https://github.com/shhhlxk/opennetpulse.git

# ```

# 

# ```bash

# cd opennetpulse

# ```

# 

# \### Install the project

# 

# ```bash

# python -m pip install -e .

# ```

# 

# On Windows, if your Python launcher is configured differently, use your installed Python executable.

# 

# \### Verify installation

# 

# ```bash

# opennetpulse --help

# ```

# 

# \## Usage

# 

# \### 1. Network Diagnostics

# 

# Check a domain:

# 

# ```bash

# opennetpulse check google.com

# ```

# 

# Specify a TCP port:

# 

# ```bash

# opennetpulse check google.com --port 443

# ```

# 

# Change timeout:

# 

# ```bash

# opennetpulse check google.com --timeout 5

# ```

# 

# Choose JSON report destination:

# 

# ```bash

# opennetpulse check google.com --output network-report.json

# ```

# 

# \### 2. System Health Check

# 

# ```bash

# opennetpulse doctor

# ```

# 

# \### 3. Network Monitoring

# 

# Monitor a host:

# 

# ```bash

# opennetpulse monitor google.com

# ```

# 

# Customize monitoring:

# 

# ```bash

# opennetpulse monitor google.com --interval 2 --duration 30

# ```

# 

# Specify a TCP port:

# 

# ```bash

# opennetpulse monitor google.com --port 443

# ```

# 

# \### 4. Route Tracing

# 

# ```bash

# opennetpulse trace google.com

# ```

# 

# Customize maximum hops:

# 

# ```bash

# opennetpulse trace google.com --max-hops 20

# ```

# 

# Customize hop timeout:

# 

# ```bash

# opennetpulse trace google.com --hop-timeout 2000

# ```

# 

# \### 5. TCP Port Scanning

# 

# Scan the default common ports:

# 

# ```bash

# opennetpulse ports localhost

# ```

# 

# Scan selected ports:

# 

# ```bash

# opennetpulse ports localhost --ports 80,443,8080

# ```

# 

# Scan database and web service ports:

# 

# ```bash

# opennetpulse ports localhost --ports 3306,5432,80,443

# ```

# 

# Customize connection timeout:

# 

# ```bash

# opennetpulse ports localhost --ports 22,80,443 --timeout 2

# ```

# 

# \*\*Important:\*\* Only scan computers and networks that you own or have explicit permission to test.

# 

# \## Example Port Scanner Output

# 

# The following is an illustrative example, not a measured scan:

# 

# ```text

# OPENNETPULSE PORT SCANNER

# ==================================================

# Target: localhost

# Ports: 22, 80, 443, 3306, 5432

# Timeout: 1.0 seconds

# 

# PORT        STATUS         LATENCY

# \------------------------------------------

# 22          CLOSED         N/A

# 80          OPEN           2.5 ms

# 443         OPEN           3.1 ms

# 3306        CLOSED         N/A

# 5432        CLOSED         N/A

# 

# SCAN SUMMARY

# \------------------------------------------

# Total ports: 5

# Open ports: 2

# Closed ports: 3

# Timed out ports: 0

# Other errors: 0

# 

# PORT SCAN COMPLETED

# ```

# 

# Actual results depend on the target machine and its network configuration.

# 

# \## Project Structure

# 

# ```text

# opennetpulse/

# │

# ├── src/

# │   └── opennetpulse/

# │       │

# │       ├── \_\_init\_\_.py

# │       ├── cli.py

# │       │

# │       ├── diagnostics/

# │       │   ├── \_\_init\_\_.py

# │       │   ├── dns.py

# │       │   ├── http.py

# │       │   ├── tcp.py

# │       │   ├── doctor.py

# │       │   ├── trace.py

# │       │   └── ports.py

# │       │

# │       ├── monitoring/

# │       │   ├── \_\_init\_\_.py

# │       │   └── monitor.py

# │       │

# │       ├── analysis/

# │       │   └── metrics.py

# │       │

# │       └── reporting/

# │           └── json\_report.py

# │

# ├── tests/

# │   ├── test\_diagnostics.py

# │   ├── test\_metrics.py

# │   ├── test\_reporting.py

# │   ├── test\_doctor.py

# │   ├── test\_monitor.py

# │   ├── test\_trace.py

# │   └── test\_ports.py

# │

# ├── README.md

# ├── LICENSE

# ├── pyproject.toml

# └── .gitignore

# ```

# 

# \## Running Tests

# 

# Run the complete automated test suite:

# 

# ```bash

# python -m unittest discover -s tests -v

# ```

# 

# Run port scanner tests independently:

# 

# ```bash

# python -m unittest tests.test\_ports -v

# ```

# 

# \## Technical Notes and Limitations

# 

# \- DNS resolution time measures the operating system resolver operation and may be affected by caching.

# \- TCP connection time measures connection establishment, not application-level health.

# \- HTTP response timing measures the time until response headers are received, not the complete page download.

# \- Monitoring uses repeated TCP connection attempts rather than ICMP echo requests.

# \- Traceroute results depend on network routing and whether intermediate devices respond to probes.

# \- Port scanning reports TCP connection outcomes. A closed or filtered port may behave differently depending on firewall configuration.

# \- A successful TCP connection does not guarantee that the application running on that port is healthy.

# 

# \## Future Development

# 

# Potential areas for future development:

# 

# \- UDP diagnostics

# \- Cross-platform traceroute support

# \- Concurrent port scanning

# \- Network performance visualization

# \- Historical monitoring reports

# \- Advanced network analytics

# \- Real-time monitoring dashboard

# \- Network anomaly detection

# 

# \## Contributing

# 

# Contributions, suggestions, bug reports and feature requests are welcome.

# 

# 1\. Fork the repository.

# 2\. Create a feature branch.

# 3\. Implement your changes.

# 4\. Run the automated tests.

# 5\. Submit a pull request.

# 

# \## License

# 

# This project is licensed under the terms specified in the repository's `LICENSE` file.

# 

# \## Author

# 

# \*\*Shlok Bhendkar\*\*

# 

# GitHub: \[@shhhlxk](https://github.com/shhhlxk)

# 

# Project: \[OpenNetPulse](https://github.com/shhhlxk/opennetpulse)

# 

# \---

# 

# \*OpenNetPulse — Explore, Diagnose, Monitor.\*

