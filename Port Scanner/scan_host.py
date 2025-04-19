import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_THREADS = 100


def scan_port(host, port):
    """Scans a single port and tries to grab a banner."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            if result == 0:
                try:
                    s.sendall(b"HEAD / HTTP/1.1\r\nHost: %s\r\n\r\n" % host.encode())
                    banner = s.recv(1024).decode(errors="ignore").strip()
                except Exception:
                    banner = "No banner"
                return port, banner
    except Exception:
        pass
    return None


def scan_host(host, ports):
    print(f"\nScanning host: {host}")
    open_ports = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(scan_port, host, port): port for port in ports}
        for future in as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
    return host, open_ports