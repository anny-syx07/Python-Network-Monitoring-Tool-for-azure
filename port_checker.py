"""
port_checker.py - Module kiểm tra kết nối TCP tới các port
Sử dụng socket để kết nối và kiểm tra trạng thái port
"""

import socket
import time


# Danh sách tên dịch vụ phổ biến theo port
KNOWN_SERVICES = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    143:  "IMAP",
    443:  "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017: "MongoDB",
}


def check_port(host: str, port: int, timeout: int = 3) -> dict:
    """
    Kiểm tra một TCP port trên host có mở hay không.

    Args:
        host: Địa chỉ IP hoặc hostname
        port: Số port cần kiểm tra (0-65535)
        timeout: Thời gian chờ kết nối (giây)

    Returns:
        dict chứa: host, port, service, status, latency_ms, timestamp, error
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    service = KNOWN_SERVICES.get(port, f"Port-{port}")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        start_time = time.time()
        result = sock.connect_ex((host, port))
        latency_ms = round((time.time() - start_time) * 1000, 2)
        sock.close()

        if result == 0:
            return {
                "host": host,
                "port": port,
                "service": service,
                "status": "OPEN",
                "latency_ms": latency_ms,
                "timestamp": timestamp,
                "error": None
            }
        else:
            return {
                "host": host,
                "port": port,
                "service": service,
                "status": "CLOSED",
                "latency_ms": None,
                "timestamp": timestamp,
                "error": f"Connection refused (code: {result})"
            }

    except socket.timeout:
        return {
            "host": host,
            "port": port,
            "service": service,
            "status": "FILTERED",
            "latency_ms": None,
            "timestamp": timestamp,
            "error": "Connection timed out"
        }
    except socket.gaierror as e:
        return {
            "host": host,
            "port": port,
            "service": service,
            "status": "ERROR",
            "latency_ms": None,
            "timestamp": timestamp,
            "error": f"DNS error: {e}"
        }
    except Exception as e:
        return {
            "host": host,
            "port": port,
            "service": service,
            "status": "ERROR",
            "latency_ms": None,
            "timestamp": timestamp,
            "error": str(e)
        }


def check_ports_for_host(host: str, ports: list, timeout: int = 3) -> list:
    """
    Kiểm tra nhiều port cho một host.

    Args:
        host: Địa chỉ IP hoặc hostname
        ports: Danh sách port cần kiểm tra
        timeout: Thời gian chờ mỗi port

    Returns:
        Danh sách kết quả check_port
    """
    results = []
    for port in ports:
        result = check_port(host, port, timeout)
        results.append(result)
    return results
