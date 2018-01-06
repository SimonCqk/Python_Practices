import socket


def get_host_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))  # default port of HTTP.
        ip = s.getsockname()[0]
    return ip
