import ipaddress
import socket


def validate_target(target):
    try:
        # Try if it's a valid IP address
        ipaddress.ip_address(target)
        return True
    except ValueError:
        try:
            # Try resolving as a domain name
            socket.gethostbyname(target)
            print("IP address of given domain is " + socket.gethostbyname(target))
            return True
        except socket.gaierror:
            return False
