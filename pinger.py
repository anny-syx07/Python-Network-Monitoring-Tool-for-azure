"""
pinger.py - Module thực hiện ping tới các host
Sử dụng subprocess để gọi lệnh ping hệ thống
"""

import subprocess
import platform
import socket
import time


def ping_host(host: str, timeout: int = 2, count: int = 1) -> dict:
    """
    Ping một host và trả về kết quả.

    Args:
        host: Địa chỉ IP hoặc hostname cần ping
        timeout: Thời gian chờ tối đa (giây)
        count: Số lần ping

    Returns:
        dict chứa: host, status, latency_ms, timestamp
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Xác định tham số lệnh ping theo hệ điều hành
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
    else:
        # Linux / macOS
        cmd = ["ping", "-c", str(count), "-W", str(timeout), host]

    try:
        start_time = time.time()
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout + 2
        )
        latency_ms = round((time.time() - start_time) * 1000, 2)

        if result.returncode == 0:
            return {
                "host": host,
                "status": "UP",
                "latency_ms": latency_ms,
                "timestamp": timestamp,
                "error": None
            }
        else:
            return {
                "host": host,
                "status": "DOWN",
                "latency_ms": None,
                "timestamp": timestamp,
                "error": "Host không phản hồi"
            }

    except subprocess.TimeoutExpired:
        return {
            "host": host,
            "status": "DOWN",
            "latency_ms": None,
            "timestamp": timestamp,
            "error": "Timeout"
        }
    except Exception as e:
        return {
            "host": host,
            "status": "ERROR",
            "latency_ms": None,
            "timestamp": timestamp,
            "error": str(e)
        }


def resolve_hostname(host: str) -> str:
    """
    Phân giải hostname thành IP address.

    Args:
        host: Hostname hoặc IP

    Returns:
        IP address hoặc hostname gốc nếu lỗi
    """
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return host
