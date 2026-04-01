"""
logger.py - Module ghi log và theo dõi downtime
Sử dụng logging module của Python
"""

import logging
import os
import time
from datetime import datetime
from collections import defaultdict


# ─── Cấu hình logger ─────────────────────────────────────────────────────────

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "network_monitor.log")
DOWNTIME_FILE = os.path.join(LOG_DIR, "downtime.log")


def setup_logger(log_level: str = "INFO") -> logging.Logger:
    """
    Khởi tạo và cấu hình logger chính.

    Args:
        log_level: Mức độ log (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Logger đã được cấu hình
    """
    # Tạo thư mục logs nếu chưa tồn tại
    os.makedirs(LOG_DIR, exist_ok=True)

    level = getattr(logging, log_level.upper(), logging.INFO)

    # Định dạng log
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    logger = logging.getLogger("NetworkMonitor")
    logger.setLevel(level)

    # Tránh thêm handler trùng lặp
    if logger.handlers:
        return logger

    # Handler ghi ra file
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    # Handler hiển thị ra console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# ─── Theo dõi trạng thái downtime ────────────────────────────────────────────

class DowntimeTracker:
    """
    Theo dõi và ghi nhận thời gian downtime của từng host/port.
    """

    def __init__(self):
        # Lưu trạng thái trước đó: key -> "UP"/"DOWN"/"OPEN"/"CLOSED"
        self._prev_status: dict = {}
        # Lưu thời điểm bắt đầu down: key -> datetime
        self._down_since: dict = {}
        # Danh sách tất cả sự kiện downtime đã ghi nhận
        self.downtime_events: list = []
        # Logger downtime riêng
        self._setup_downtime_logger()

    def _setup_downtime_logger(self):
        """Tạo logger riêng để ghi file downtime."""
        os.makedirs(LOG_DIR, exist_ok=True)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self._dt_logger = logging.getLogger("DowntimeLogger")
        self._dt_logger.setLevel(logging.INFO)

        if not self._dt_logger.handlers:
            fh = logging.FileHandler(DOWNTIME_FILE, encoding="utf-8")
            fh.setFormatter(formatter)
            self._dt_logger.addHandler(fh)

    def update_host(self, result: dict):
        """
        Cập nhật trạng thái ping của host.
        Ghi nhận downtime khi host chuyển từ UP → DOWN.

        Args:
            result: Kết quả từ pinger.ping_host()
        """
        host = result["host"]
        status = result["status"]  # "UP" hoặc "DOWN"
        timestamp = result["timestamp"]
        key = f"HOST:{host}"

        prev = self._prev_status.get(key, "UP")  # Mặc định ban đầu là UP

        if prev == "UP" and status in ("DOWN", "ERROR"):
            # Bắt đầu downtime
            self._down_since[key] = datetime.now()
            self._dt_logger.info(
                f"[HOST DOWN] {host} | Bắt đầu down lúc {timestamp}"
            )

        elif prev in ("DOWN", "ERROR") and status == "UP":
            # Kết thúc downtime
            down_start = self._down_since.pop(key, datetime.now())
            duration_sec = round((datetime.now() - down_start).total_seconds(), 1)
            event = {
                "type": "HOST",
                "target": host,
                "port": None,
                "service": None,
                "down_start": str(down_start.strftime("%Y-%m-%d %H:%M:%S")),
                "down_end": timestamp,
                "duration_seconds": duration_sec
            }
            self.downtime_events.append(event)
            self._dt_logger.info(
                f"[HOST RECOVERED] {host} | Phục hồi lúc {timestamp} | "
                f"Downtime: {duration_sec}s"
            )

        self._prev_status[key] = status

    def update_port(self, result: dict):
        """
        Cập nhật trạng thái TCP port của host.
        Ghi nhận downtime khi port chuyển từ OPEN → CLOSED/FILTERED.

        Args:
            result: Kết quả từ port_checker.check_port()
        """
        host = result["host"]
        port = result["port"]
        service = result["service"]
        status = result["status"]
        timestamp = result["timestamp"]
        key = f"PORT:{host}:{port}"

        prev = self._prev_status.get(key, "OPEN")

        if prev == "OPEN" and status in ("CLOSED", "FILTERED", "ERROR"):
            self._down_since[key] = datetime.now()
            self._dt_logger.info(
                f"[PORT DOWN] {host}:{port} ({service}) | "
                f"Bắt đầu đóng lúc {timestamp}"
            )

        elif prev in ("CLOSED", "FILTERED", "ERROR") and status == "OPEN":
            down_start = self._down_since.pop(key, datetime.now())
            duration_sec = round((datetime.now() - down_start).total_seconds(), 1)
            event = {
                "type": "PORT",
                "target": host,
                "port": port,
                "service": service,
                "down_start": str(down_start.strftime("%Y-%m-%d %H:%M:%S")),
                "down_end": timestamp,
                "duration_seconds": duration_sec
            }
            self.downtime_events.append(event)
            self._dt_logger.info(
                f"[PORT RECOVERED] {host}:{port} ({service}) | "
                f"Phục hồi lúc {timestamp} | Downtime: {duration_sec}s"
            )

        self._prev_status[key] = status

    def get_currently_down(self) -> list:
        """
        Trả về danh sách host/port đang trong trạng thái down.
        """
        currently_down = []
        for key, status in self._prev_status.items():
            if status in ("DOWN", "ERROR", "CLOSED", "FILTERED"):
                down_since = self._down_since.get(key, datetime.now())
                duration = round((datetime.now() - down_since).total_seconds(), 1)
                currently_down.append({
                    "target": key,
                    "status": status,
                    "down_since": str(down_since.strftime("%Y-%m-%d %H:%M:%S")),
                    "duration_seconds": duration
                })
        return currently_down

    def get_summary(self) -> dict:
        """
        Trả về thống kê tổng hợp về downtime.
        """
        total_events = len(self.downtime_events)
        total_duration = sum(e["duration_seconds"] for e in self.downtime_events)
        host_events = [e for e in self.downtime_events if e["type"] == "HOST"]
        port_events = [e for e in self.downtime_events if e["type"] == "PORT"]

        return {
            "total_downtime_events": total_events,
            "total_downtime_seconds": total_duration,
            "host_downtime_events": len(host_events),
            "port_downtime_events": len(port_events),
            "currently_down_count": len(self.get_currently_down())
        }
