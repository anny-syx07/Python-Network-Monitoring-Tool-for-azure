"""
reporter.py - Module xuất báo cáo dạng CSV
Tổng hợp kết quả giám sát và xuất ra file CSV
"""

import csv
import os
import time
from datetime import datetime
from collections import defaultdict


REPORTS_DIR = "reports"


def export_ping_report(results: list, filename: str = None) -> str:
    """
    Xuất kết quả ping ra file CSV.

    Args:
        results: Danh sách kết quả từ pinger.ping_host()
        filename: Tên file xuất (tự động tạo nếu không truyền)

    Returns:
        Đường dẫn tới file CSV đã xuất
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ping_report_{timestamp}.csv"

    filepath = os.path.join(REPORTS_DIR, filename)

    fieldnames = ["timestamp", "host", "status", "latency_ms", "error"]

    with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for r in results:
            writer.writerow({
                "timestamp": r.get("timestamp", ""),
                "host": r.get("host", ""),
                "status": r.get("status", ""),
                "latency_ms": r.get("latency_ms", ""),
                "error": r.get("error", "")
            })

    return filepath


def export_port_report(results: list, filename: str = None) -> str:
    """
    Xuất kết quả kiểm tra port ra file CSV.

    Args:
        results: Danh sách kết quả từ port_checker.check_port()
        filename: Tên file xuất (tự động tạo nếu không truyền)

    Returns:
        Đường dẫn tới file CSV đã xuất
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"port_report_{timestamp}.csv"

    filepath = os.path.join(REPORTS_DIR, filename)

    fieldnames = ["timestamp", "host", "port", "service", "status", "latency_ms", "error"]

    with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for r in results:
            writer.writerow({
                "timestamp": r.get("timestamp", ""),
                "host": r.get("host", ""),
                "port": r.get("port", ""),
                "service": r.get("service", ""),
                "status": r.get("status", ""),
                "latency_ms": r.get("latency_ms", ""),
                "error": r.get("error", "")
            })

    return filepath


def export_downtime_report(downtime_events: list, filename: str = None) -> str:
    """
    Xuất báo cáo downtime ra file CSV.

    Args:
        downtime_events: Danh sách sự kiện downtime từ DowntimeTracker
        filename: Tên file xuất (tự động tạo nếu không truyền)

    Returns:
        Đường dẫn tới file CSV đã xuất
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"downtime_report_{timestamp}.csv"

    filepath = os.path.join(REPORTS_DIR, filename)

    fieldnames = [
        "type", "target", "port", "service",
        "down_start", "down_end", "duration_seconds"
    ]

    with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for event in downtime_events:
            writer.writerow({
                "type": event.get("type", ""),
                "target": event.get("target", ""),
                "port": event.get("port", ""),
                "service": event.get("service", ""),
                "down_start": event.get("down_start", ""),
                "down_end": event.get("down_end", ""),
                "duration_seconds": event.get("duration_seconds", "")
            })

    return filepath


def export_summary_report(
    ping_results: list,
    port_results: list,
    downtime_events: list,
    filename: str = None
) -> str:
    """
    Xuất báo cáo tổng hợp bao gồm ping, port và downtime.

    Args:
        ping_results: Toàn bộ lịch sử kết quả ping
        port_results: Toàn bộ lịch sử kết quả port check
        downtime_events: Danh sách sự kiện downtime
        filename: Tên file xuất

    Returns:
        Đường dẫn tới file CSV đã xuất
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_report_{timestamp}.csv"

    filepath = os.path.join(REPORTS_DIR, filename)

    with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # ── Section 1: Thống kê Ping ──────────────────────────────────────
        writer.writerow(["=== PING STATISTICS ==="])
        writer.writerow(["Host", "Total Checks", "UP", "DOWN", "Avg Latency (ms)",
                         "Max Latency (ms)", "Min Latency (ms)", "Uptime %"])

        ping_stats = defaultdict(lambda: {
            "total": 0, "up": 0, "down": 0, "latencies": []
        })
        for r in ping_results:
            host = r["host"]
            ping_stats[host]["total"] += 1
            if r["status"] == "UP":
                ping_stats[host]["up"] += 1
                if r["latency_ms"] is not None:
                    ping_stats[host]["latencies"].append(r["latency_ms"])
            else:
                ping_stats[host]["down"] += 1

        for host, s in ping_stats.items():
            latencies = s["latencies"]
            avg_lat = round(sum(latencies) / len(latencies), 2) if latencies else ""
            max_lat = max(latencies) if latencies else ""
            min_lat = min(latencies) if latencies else ""
            uptime_pct = round((s["up"] / s["total"]) * 100, 2) if s["total"] > 0 else 0
            writer.writerow([
                host, s["total"], s["up"], s["down"],
                avg_lat, max_lat, min_lat, f"{uptime_pct}%"
            ])

        writer.writerow([])  # Dòng trống phân cách

        # ── Section 2: Thống kê Port ──────────────────────────────────────
        writer.writerow(["=== PORT CHECK STATISTICS ==="])
        writer.writerow(["Host", "Port", "Service", "Total Checks",
                         "OPEN", "CLOSED/FILTERED", "Availability %"])

        port_stats = defaultdict(lambda: {"total": 0, "open": 0, "closed": 0})
        port_info = {}
        for r in port_results:
            key = (r["host"], r["port"])
            port_stats[key]["total"] += 1
            port_info[key] = r.get("service", "")
            if r["status"] == "OPEN":
                port_stats[key]["open"] += 1
            else:
                port_stats[key]["closed"] += 1

        for (host, port), s in port_stats.items():
            avail_pct = round((s["open"] / s["total"]) * 100, 2) if s["total"] > 0 else 0
            writer.writerow([
                host, port, port_info.get((host, port), ""),
                s["total"], s["open"], s["closed"], f"{avail_pct}%"
            ])

        writer.writerow([])

        # ── Section 3: Downtime Events ────────────────────────────────────
        writer.writerow(["=== DOWNTIME EVENTS ==="])
        writer.writerow([
            "Type", "Target", "Port", "Service",
            "Down Start", "Down End", "Duration (s)"
        ])
        for event in downtime_events:
            writer.writerow([
                event.get("type", ""),
                event.get("target", ""),
                event.get("port", ""),
                event.get("service", ""),
                event.get("down_start", ""),
                event.get("down_end", ""),
                event.get("duration_seconds", "")
            ])

    return filepath
