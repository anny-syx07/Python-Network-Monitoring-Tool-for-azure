# Python Network Monitoring Tool

> **mini-NMS** – Công cụ giám sát mạng bằng Python  
> Môn học: Lập trình mạng và hệ thống | Đồ án cá nhân

---

## 📋 Mô tả

Đây là một công cụ giám sát mạng đơn giản (mini-NMS) được xây dựng bằng Python thuần.  
Công cụ có thể:
- **Ping nhiều host** đồng thời
- **Kiểm tra TCP port** (HTTP, HTTPS, SSH, MySQL,...)
- **Ghi log downtime** tự động
- **Xuất báo cáo CSV** chi tiết

---

## 🗂️ Cấu trúc dự án

```
Python Network Monitoring Tool/
│
├── monitor.py          # File chính – khởi động, argparse, threading
├── pinger.py           # Module ping host (subprocess + socket)
├── port_checker.py     # Module kiểm tra TCP port (socket)
├── logger.py           # Module logging + theo dõi downtime
├── reporter.py         # Module xuất báo cáo CSV
│
├── hosts.txt           # Danh sách host cần giám sát
│
├── logs/               # (Tự tạo khi chạy)
│   ├── network_monitor.log
│   └── downtime.log
│
└── reports/            # (Tự tạo khi chạy)
    ├── ping_report_YYYYMMDD_HHMMSS.csv
    ├── port_report_YYYYMMDD_HHMMSS.csv
    ├── downtime_report_YYYYMMDD_HHMMSS.csv
    └── summary_report_YYYYMMDD_HHMMSS.csv
```

---

## 🛠️ Công nghệ sử dụng

| Module      | Mục đích                                      |
|-------------|-----------------------------------------------|
| `socket`    | Kết nối TCP để kiểm tra port, phân giải DNS   |
| `threading` | Chạy song song nhiều host cùng lúc            |
| `logging`   | Ghi log ra file và console                    |
| `argparse`  | Xử lý tham số dòng lệnh                       |
| `subprocess`| Gọi lệnh ping của hệ điều hành                |
| `csv`       | Xuất báo cáo dạng bảng                        |
| `signal`    | Xử lý Ctrl+C an toàn                          |

> **Không cần cài thêm thư viện ngoài** – chỉ dùng Python standard library!

---

## 🚀 Hướng dẫn sử dụng

### Yêu cầu hệ thống
- Python 3.7 trở lên
- macOS / Linux / Windows

### Cài đặt

Không cần cài đặt gì thêm. Clone hoặc tải project về và chạy ngay.

### Các lệnh cơ bản

#### 1. Ping một hoặc nhiều host (chạy một lần)
```bash
python monitor.py --hosts 8.8.8.8 google.com --once
```

#### 2. Ping + kiểm tra port cụ thể
```bash
python monitor.py --hosts 8.8.8.8 --ports 80 443 22 --once
```

#### 3. Đọc host từ file, giám sát liên tục
```bash
python monitor.py --file hosts.txt --ports 80 443 --interval 30
```

#### 4. Giám sát liên tục mỗi 10 giây, timeout 5 giây
```bash
python monitor.py --file hosts.txt --interval 10 --timeout 5
```

#### 5. Bật chế độ DEBUG chi tiết
```bash
python monitor.py --hosts google.com --log-level DEBUG --once
```

#### 6. Không xuất báo cáo CSV
```bash
python monitor.py --file hosts.txt --no-report
```

### Xem tất cả tùy chọn
```bash
python monitor.py --help
```

---

## 📊 Giải thích tham số (argparse)

| Tham số       | Viết tắt | Mặc định | Mô tả                                   |
|---------------|----------|----------|-----------------------------------------|
| `--hosts`     | `-H`     | -        | Danh sách host/IP (bắt buộc hoặc --file)|
| `--file`      | `-f`     | -        | File danh sách host                     |
| `--ports`     | `-p`     | 80 443   | Danh sách TCP port kiểm tra             |
| `--interval`  | `-i`     | 30       | Chu kỳ kiểm tra (giây)                 |
| `--timeout`   | `-t`     | 3        | Thời gian chờ tối đa (giây)             |
| `--once`      | -        | False    | Chỉ chạy một lần rồi thoát             |
| `--log-level` | -        | INFO     | Mức độ log: DEBUG/INFO/WARNING/ERROR    |
| `--no-report` | -        | False    | Không xuất file CSV                     |

---

## 📁 Định dạng file báo cáo CSV

### `ping_report_*.csv`
```
timestamp,host,status,latency_ms,error
2024-01-15 10:30:00,8.8.8.8,UP,12.5,
2024-01-15 10:30:00,google.com,DOWN,,Host không phản hồi
```

### `port_report_*.csv`
```
timestamp,host,port,service,status,latency_ms,error
2024-01-15 10:30:00,google.com,80,HTTP,OPEN,45.2,
2024-01-15 10:30:00,google.com,22,SSH,CLOSED,,Connection refused
```

### `downtime_report_*.csv`
```
type,target,port,service,down_start,down_end,duration_seconds
HOST,8.8.8.8,,,2024-01-15 10:30:00,2024-01-15 10:35:00,300.0
PORT,192.168.1.1,80,HTTP,2024-01-15 10:00:00,2024-01-15 10:05:00,300.0
```

### `summary_report_*.csv`
Báo cáo tổng hợp bao gồm:
- Thống kê ping theo host (uptime %, latency trung bình)
- Thống kê port check theo host:port
- Danh sách tất cả sự kiện downtime

---

## 🔄 Luồng xử lý

```
main()
  ├── parse_arguments()          ← argparse
  ├── setup_logger()             ← logging
  ├── load_hosts_from_file()     ← (nếu dùng --file)
  │
  └── threading: mỗi host chạy 1 thread
        └── monitor_host()
              ├── ping_host()         ← pinger.py / subprocess
              ├── check_port() x N    ← port_checker.py / socket
              └── downtime_tracker.update_*()  ← logger.py
  
  [Ctrl+C / --once]
  └── generate_reports()
        ├── export_ping_report()
        ├── export_port_report()
        ├── export_downtime_report()
        └── export_summary_report()   ← reporter.py / csv
```

---

## 📝 Ví dụ output

```
╔══════════════════════════════════════════════════════════╗
║      🌐  Python Network Monitoring Tool (mini-NMS)       ║
║         Giám sát mạng bằng Python | socket + threading   ║
╚══════════════════════════════════════════════════════════╝

2024-01-15 10:30:00 | INFO     | ============================================================
2024-01-15 10:30:00 | INFO     | 📋 CẤU HÌNH GIÁM SÁT:
2024-01-15 10:30:00 | INFO     |    Hosts       : 8.8.8.8, google.com
2024-01-15 10:30:00 | INFO     |    Ports       : 80, 443
2024-01-15 10:30:00 | INFO     |    Interval    : 30s
...
2024-01-15 10:30:01 | INFO     | ✅ PING | 8.8.8.8             | UP     | Latency: 15.3ms
2024-01-15 10:30:01 | INFO     | 🟢 PORT | 8.8.8.8             | Port 80    (HTTP        ) | OPEN       | Latency: 25.1ms
2024-01-15 10:30:01 | INFO     | 🔴 PORT | 8.8.8.8             | Port 443   (HTTPS       ) | CLOSED     | Latency: N/A
```

---

## 👤 Tác giả

- **Họ tên:** [Tên sinh viên]
- **MSSV:** [Mã số sinh viên]
- **Lớp:** [Tên lớp]
- **GVHD:** [Tên giảng viên]
