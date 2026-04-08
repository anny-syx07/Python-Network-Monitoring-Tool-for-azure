"""
pinger.py - Module thực hiện ping tới các host
Ưu tiên ICMP ping; tự động fallback sang TCP ping nếu ICMP bị block (ví dụ: Azure ACI).
"""

import subprocess
import platform
import socket
import time

# Port thử khi dùng TCP ping (thử theo thứ tự)
TCP_FALLBACK_PORTS = [80, 443, 53]


def tcp_ping_host(host: str, timeout: int = 2) -> dict:
    """
    Kiểm tra host còn sống bằng cách thử kết nối TCP (thay thế ICMP).
    Phù hợp cho môi trường chặn ICMP như Azure Container Instances.

    Cơ chế:
      - Thử kết nối TCP đến các port phổ biến (80, 443, 53).
      - Nếu kết nối thành công HOẶC bị từ chối (Connection refused)
        → host ĐANG HOẠT ĐỘNG (chỉ là port đó đóng, nhưng máy còn sống).
      - Nếu timeout → host DOWN hoặc bị tường lửa chặn hoàn toàn.

    Args:
        host: Địa chỉ IP hoặc hostname cần kiểm tra
        timeout: Thời gian chờ kết nối TCP (giây)

    Returns:
        dict chứa: host, status, latency_ms, timestamp, method, error
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Mã lỗi "Connection refused" trên từng OS — nghĩa là host còn sống
    # Windows: 10061, Linux: 111, macOS: 61
    CONNECTION_REFUSED_CODES = {10061, 111, 61}

    for port in TCP_FALLBACK_PORTS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)

            start_time = time.time()
            err_code = sock.connect_ex((host, port))
            latency_ms = round((time.time() - start_time) * 1000, 2)
            sock.close()

            # Kết nối thành công (port mở) hoặc bị từ chối (port đóng nhưng máy sống)
            if err_code == 0 or err_code in CONNECTION_REFUSED_CODES:
                return {
                    "host": host,
                    "status": "UP",
                    "latency_ms": latency_ms,
                    "timestamp": timestamp,
                    "method": f"TCP:{port}",
                    "error": None
                }
            # Tiếp tục thử port tiếp theo nếu port này bị filter

        except socket.timeout:
            continue  # Thử port tiếp theo
        except socket.gaierror as e:
            # Lỗi DNS — không cần thử port khác
            return {
                "host": host,
                "status": "ERROR",
                "latency_ms": None,
                "timestamp": timestamp,
                "method": "TCP",
                "error": f"DNS error: {e}"
            }
        except Exception:
            continue

    # Tất cả port đều timeout → host DOWN
    return {
        "host": host,
        "status": "DOWN",
        "latency_ms": None,
        "timestamp": timestamp,
        "method": "TCP",
        "error": "Không phản hồi trên TCP (80, 443, 53)"
    }


def ping_host(host: str, timeout: int = 2, count: int = 1) -> dict:
    """
    Ping một host và trả về kết quả.
    Ưu tiên ICMP ping; tự động fallback sang TCP nếu ICMP bị block.

    Args:
        host: Địa chỉ IP hoặc hostname cần ping
        timeout: Thời gian chờ tối đa (giây)
        count: Số lần ping

    Returns:
        dict chứa: host, status, latency_ms, timestamp, method, error
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Xác định tham số lệnh ping theo hệ điều hành
    system = platform.system().lower()
    if system == "windows":
        # Windows: -w tính bằng millisecond
        cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
    elif system == "darwin":
        # macOS: -W tính bằng millisecond (khác Linux!)
        cmd = ["ping", "-c", str(count), "-W", str(timeout * 1000), host]
    else:
        # Linux: -W tính bằng giây
        cmd = ["ping", "-c", str(count), "-W", str(timeout), host]

    # ── Bước 1: Thử ICMP ping ────────────────────────────────────────────────
    icmp_blocked = False
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
                "method": "ICMP",
                "error": None
            }
        else:
            # ICMP thất bại — có thể bị block hoặc host thực sự down
            icmp_blocked = True

    except subprocess.TimeoutExpired:
        icmp_blocked = True
    except Exception:
        icmp_blocked = True

    # ── Bước 2: Fallback sang TCP ping nếu ICMP không thành công ─────────────
    if icmp_blocked:
        tcp_result = tcp_ping_host(host, timeout=timeout)
        # Ghi lại rằng kết quả này đến từ TCP fallback
        if tcp_result["status"] == "UP":
            tcp_result["method"] = f"TCP-fallback:{tcp_result.get('method', 'TCP')}"
        return tcp_result

    # ICMP thất bại và TCP cũng không thử được (không nên xảy ra)
    return {
        "host": host,
        "status": "DOWN",
        "latency_ms": None,
        "timestamp": timestamp,
        "method": "ICMP",
        "error": "Host không phản hồi"
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
