
from diagnostics.dns import check_dns

result = check_dns("google.com")

print("\nOPENNETPULSE DNS DIAGNOSTICS")
print("----------------------------")

print("Domain:", result["domain"])
print("Status:", result["status"])
print("IP Addresses:", result["ip_addresses"])
print("Resolution Time:", result["resolution_time_ms"], "ms")
print("Error:", result["error"])
