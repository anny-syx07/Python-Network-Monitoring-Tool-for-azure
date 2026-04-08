"""
monitor.py - File chính của Network Monitoring Tool
Tích hợp ping, port check, logging và xuất CSV report
Sử dụng threading để giám sát song song
"""

import argparse
import threading
import time
import sys
import signal
import json
import os
from datetime import datetime

# Import các module tự tạo
from pinger import ping_host
from port_checker import check_port
from logger import setup_logger, DowntimeTracker
from reporter import (
    export_ping_report,
    export_port_report,
    export_downtime_report,
    export_summary_report
)


# ─── Biến toàn cục ────────────────────────────────────────────────────────────
ping_results_history = []       # Lưu toàn bộ lịch sử ping
port_results_history = []       # Lưu toàn bộ lịch sử port check
results_lock = threading.Lock() # Khoá để tránh race condition
stop_event = threading.Event()  # Sự kiện dừng tất cả thread
downtime_tracker = DowntimeTracker()
logger = None


# ─── Hàm giám sát từng host (chạy trong thread) ──────────────────────────────

def monitor_host(host: str, ports: list, interval: int, timeout: int):
    """
    Hàm chạy trong thread riêng, liên tục giám sát một host.

    Args:
        host: Địa chỉ IP hoặc hostname
        ports: Danh sách port cần check
        interval: Khoảng thời gian giữa các lần check (giây)
        timeout: Thời gian chờ (giây)
    """
    global logger, ping_results_history, port_results_history

    logger.info(f"[THREAD START] Bắt đầu giám sát host: {host}")

    while not stop_event.is_set():
        # Ping host
        ping_result = ping_host(host, timeout=timeout)

        with results_lock:
            ping_results_history.append(ping_result)
            downtime_tracker.update_host(ping_result)

        status_icon = "✅" if ping_result["status"] == "UP" else "❌"
        latency_str = f"{ping_result['latency_ms']}ms" if ping_result['latency_ms'] else "N/A"

        logger.info(
            f"{status_icon} PING | {host:<20} | {ping_result['status']:<6} | "
            f"Latency: {latency_str}"
        )

        # Check từng port
        for port in ports:
            if stop_event.is_set():
                break

            port_result = check_port(host, port, timeout=timeout)

            with results_lock:
                port_results_history.append(port_result)
                downtime_tracker.update_port(port_result)

            port_icon = "🟢" if port_result["status"] == "OPEN" else "🔴"
            port_latency = f"{port_result['latency_ms']}ms" if port_result['latency_ms'] else "N/A"

            logger.info(
                f"{port_icon} PORT | {host:<20} | Port {port:<5} "
                f"({port_result['service']:<12}) | {port_result['status']:<10} | "
                f"Latency: {port_latency}"
            )

        # Chờ đến chu kỳ tiếp theo
        if interval == 0:
            break
        stop_event.wait(timeout=interval)

    logger.info(f"[THREAD STOP] Dừng giám sát host: {host}")


# ─── Tạo báo cáo CSV ──────────────────────────────────────────────────────────

def generate_reports():
    """Xuất tất cả báo cáo ra file CSV."""
    global logger, ping_results_history, port_results_history

    logger.info("=" * 60)
    logger.info("Đang xuất báo cáo CSV...")

    # Báo cáo ping
    if ping_results_history:
        path = export_ping_report(ping_results_history)
        logger.info(f"✅ Đã xuất báo cáo ping: {path}")

    # Báo cáo port
    if port_results_history:
        path = export_port_report(port_results_history)
        logger.info(f"✅ Đã xuất báo cáo port: {path}")

    # Báo cáo downtime
    if downtime_tracker.downtime_events:
        path = export_downtime_report(downtime_tracker.downtime_events)
        logger.info(f"✅ Đã xuất báo cáo downtime: {path}")

    # Báo cáo tổng hợp
    path = export_summary_report(
        ping_results_history,
        port_results_history,
        downtime_tracker.downtime_events
    )
    logger.info(f"✅ Đã xuất báo cáo tổng hợp: {path}")
    logger.info("=" * 60)

    # In thống kê tóm tắt
    summary = downtime_tracker.get_summary()
    logger.info("📊 THỐNG KÊ DOWNTIME:")
    logger.info(f"   Tổng sự kiện downtime: {summary['total_downtime_events']}")
    logger.info(f"   Tổng thời gian down  : {summary['total_downtime_seconds']}s")
    logger.info(f"   Host down events     : {summary['host_downtime_events']}")
    logger.info(f"   Port down events     : {summary['port_downtime_events']}")


# ─── Xử lý tín hiệu dừng (Ctrl+C) ────────────────────────────────────────────

def signal_handler(sig, frame):
    """Xử lý khi người dùng nhấn Ctrl+C."""
    global logger
    print()  # Xuống dòng sau ^C
    logger.warning("Nhận tín hiệu dừng (Ctrl+C). Đang dừng chương trình...")
    stop_event.set()


# ─── Đọc danh sách host từ file ──────────────────────────────────────────────

def load_hosts_from_file(filepath: str) -> list:
    """
    Đọc danh sách host từ file text (mỗi dòng một host).

    Args:
        filepath: Đường dẫn tới file hosts

    Returns:
        Danh sách hostname/IP
    """
    hosts = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Bỏ qua dòng trống và comment (bắt đầu bằng #)
                if line and not line.startswith("#"):
                    hosts.append(line)
    except FileNotFoundError:
        print(f"[LỖI] Không tìm thấy file: {filepath}")
        sys.exit(1)
    return hosts


# ─── Cấu hình argparse ────────────────────────────────────────────────────────

def parse_arguments() -> argparse.Namespace:
    """
    Phân tích các tham số dòng lệnh với argparse.

    Returns:
        Namespace chứa tất cả tham số đã parse
    """
    parser = argparse.ArgumentParser(
        prog="monitor.py",
        description=(
            "🌐 Python Network Monitoring Tool (mini-NMS)\n"
            "Giám sát trạng thái mạng: ping host, kiểm tra TCP port,\n"
            "ghi log downtime và xuất báo cáo CSV."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  python monitor.py --hosts 8.8.8.8 1.1.1.1
  python monitor.py --hosts 192.168.1.1 --ports 80 443 22
  python monitor.py --file hosts.txt --ports 80 443 --interval 10
  python monitor.py --file hosts.txt --interval 5 --timeout 3 --log-level DEBUG
  python monitor.py --hosts google.com --once
        """
    )

    # Nhóm: Nguồn host
    host_group = parser.add_mutually_exclusive_group(required=True)
    host_group.add_argument(
        "--hosts", "-H",
        nargs="+",
        metavar="HOST",
        help="Danh sách host/IP cần giám sát (ví dụ: 8.8.8.8 google.com)"
    )
    host_group.add_argument(
        "--file", "-f",
        metavar="FILE",
        help="File chứa danh sách host (mỗi dòng một host)"
    )

    # Cấu hình giám sát
    parser.add_argument(
        "--ports", "-p",
        nargs="+",
        type=int,
        default=[80, 443],
        metavar="PORT",
        help="Danh sách TCP port cần check (mặc định: 80 443)"
    )
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=30,
        metavar="SECONDS",
        help="Khoảng thời gian giữa mỗi lần ping/check (giây, mặc định: 30)"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=3,
        metavar="SECONDS",
        help="Thời gian chờ phản hồi tối đa (giây, mặc định: 3)"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Chỉ chạy một lần rồi thoát (không lặp liên tục)"
    )

    # Cấu hình log
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Mức độ log (mặc định: INFO)"
    )

    # Cấu hình report
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Không xuất báo cáo CSV khi kết thúc"
    )

    return parser.parse_args()


# ─── Hàm chính ────────────────────────────────────────────────────────────────

def main():
    global logger

    # Parse tham số dòng lệnh
    args = parse_arguments()

    # Khởi tạo logger
    logger = setup_logger(args.log_level)

    # ── Banner ──────────────────────────────────────────────────────────────
    banner = """
╔══════════════════════════════════════════════════════════╗
║      🌐  Python Network Monitoring Tool (mini-NMS)       ║
║         Giám sát mạng bằng Python | socket + threading   ║
╚══════════════════════════════════════════════════════════╝"""
    print(banner)

    # Xác định danh sách host
    if args.hosts:
        hosts = args.hosts
    else:
        hosts = load_hosts_from_file(args.file)

    if not hosts:
        logger.error("Không có host nào để giám sát!")
        sys.exit(1)

    # Validate port range
    for port in args.ports:
        if not (1 <= port <= 65535):
            logger.error(f"Port không hợp lệ: {port}. Port phải từ 1-65535.")
            sys.exit(1)

    # ── Hiển thị cấu hình ───────────────────────────────────────────────────
    logger.info("=" * 60)
    logger.info(f"📋 CẤU HÌNH GIÁM SÁT:")
    logger.info(f"   Hosts       : {', '.join(hosts)}")
    logger.info(f"   Ports       : {', '.join(map(str, args.ports))}")
    logger.info(f"   Interval    : {args.interval}s")
    logger.info(f"   Timeout     : {args.timeout}s")
    logger.info(f"   Log level   : {args.log_level}")
    logger.info(f"   Mode        : {'Một lần' if args.once else 'Liên tục'}")
    logger.info("=" * 60)

    # Đăng ký handler Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # ── Chế độ chỉ chạy một lần ─────────────────────────────────────────────
    if args.once:
        logger.info("🔍 Đang thực hiện kiểm tra một lần...")

        threads = []
        for host in hosts:
            t = threading.Thread(
                target=monitor_host,
                args=(host, args.ports, 0, args.timeout),
                name=f"Monitor-{host}",
                daemon=True
            )
            threads.append(t)
            t.start()

        # Đợi tất cả thread hoàn thành
        for t in threads:
            t.join(timeout=args.timeout * len(args.ports) + 5)

        stop_event.set()

    # ── Chế độ giám sát liên tục ─────────────────────────────────────────────
    else:
        logger.info("🚀 Bắt đầu giám sát liên tục (Ctrl+C để dừng)...")
        logger.info("📢 Báo cáo sẽ được lưu tự động mỗi 5 phút.")

        threads = []
        for host in hosts:
            t = threading.Thread(
                target=monitor_host,
                args=(host, args.ports, args.interval, args.timeout),
                name=f"Monitor-{host}",
                daemon=True
            )
            threads.append(t)
            t.start()
            logger.debug(f"Thread created: {t.name}")

        logger.info(f"✅ Đã khởi động {len(threads)} thread giám sát")

        # Chế độ lưu báo cáo định kỳ (300 giây = 5 phút)
        REPORT_INTERVAL = 300
        last_report_time = time.time()

        # Chờ tín hiệu dừng
        try:
            while not stop_event.is_set():
                # Kiểm tra xem đã đến lúc lưu báo cáo chưa
                current_time = time.time()
                if current_time - last_report_time >= REPORT_INTERVAL:
                    generate_reports()
                    last_report_time = current_time
                
                time.sleep(1)
        except KeyboardInterrupt:
            stop_event.set()

        # Đợi tất cả thread kết thúc
        for t in threads:
            t.join(timeout=5)

    # ── Xuất báo cáo ────────────────────────────────────────────────────────
    if not args.no_report:
        generate_reports()
    else:
        logger.info("Bỏ qua xuất báo cáo (--no-report).")

    logger.info("👋 Chương trình kết thúc.")


if __name__ == "__main__":
    main()
