import socket
import scan_host
from validate_target import validate_target
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_THREADS = 100


def parse_port_range(port_range_str):
    """Parses a string like '20-25,80,443' into a list of ports."""
    ports = set()
    parts = port_range_str.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part))
    print(sorted(ports))
    return sorted(ports)


def main():
    # User input
    targets = input("Enter target IPs (comma-separated): ").split(",")
    targets = [ip.strip() for ip in targets if ip.strip()]

    valid_targets = []
    for t in targets:
        if validate_target(t):
            valid_targets.append(t)
        else:
            print(f"[!] Invalid target: {t}")

    if not valid_targets:
        print("No valid targets to scan. Exiting.")
        return

    port_range_input = input("Enter port range (e.g. 20-25,80,443): ").strip()
    ports = parse_port_range(port_range_input)

    for target in valid_targets:
        host, open_ports = scan_host.scan_host(target, ports)
        if open_ports:
            print(f"\n[+] Open ports on {host}:")
            for port, banner in open_ports:
                print(f"  Port {port} open - Banner: {banner}")
        else:
            print(f"\n[-] No open ports found on {host}.")


if __name__ == "__main__":
    main()
