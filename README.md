# 🌐 Python Network Monitoring Tool (mini-NMS)

> **Đồ án môn học: Lập trình mạng và hệ thống**  
> Dự án giám sát trạng thái mạng 24/7 và xuất báo cáo CSV tự động.

---

## 📋 Giới thiệu
Đây là công cụ giám sát mạng được viết bằng **Python thuần**, không phụ thuộc thư viện ngoài. Hệ thống có khả năng giám sát hàng loạt Host và Port cùng lúc thông qua cơ chế đa luồng (Threading).

### Các tính năng chính:
- **Ping Monitoring**: Kiểm tra độ trễ (latency) và trạng thái sống/chết của Host.
- **Port Monitoring**: Kiểm tra các dịch vụ ứng dụng (HTTP, SSH, MySQL...) qua TCP Port.
- **Downtime Tracking**: Tự động tính toán thời gian chết (Downtime) của từng dịch vụ.
- **Cloud Deployment**: Chạy 24/7 trên **Azure Container Instances (ACI)**.
- **Auto Reports**: Tự động xuất file báo cáo CSV vào **Azure Storage** mỗi 60 giây.

---

## 🗂️ Cấu trúc dự án
- `monitor.py`: Luồng xử lý chính, quản lý các Thread giám sát.
- `pinger.py` & `port_checker.py`: Module thực hiện ping và quét port.
- `logger.py` & `reporter.py`: Ghi nhật ký hệ thống và xuất báo cáo CSV.
- `deploy.sh`: **Script 1-Click** để cập nhật code lên Azure.
- `hosts.txt`: File cấu hình danh sách IP/Domain cần giám sát.

---

## 🚀 Hướng dẫn vận hành

### 1. Cách chạy trên máy cá nhân (Local)
Dùng để kiểm tra code hoặc giám sát nhanh:
```bash
python monitor.py --file hosts.txt --interval 30
```

### 2. Cách triển khai lên Azure (Dành cho Trưởng nhóm)
Mỗi khi sửa code, anh chỉ cần chạy lệnh sau để hệ thống tự động cập nhật lên đám mây:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## 📂 Cách lấy báo cáo (Dành cho cả nhóm)
Nhóm có thể lấy báo cáo 24/7 mà không cần máy tính của trưởng nhóm phải bật:
1. Đăng nhập **Azure Portal**.
2. Tìm Storage Account: `pynetmonstorage999`.
3. Vào **File shares** -> `csvreports`.
4. Tại mục **Browse** (Parcourir), các file CSV mới nhất sẽ xuất hiện tại đây.

---

## 👤 Thông tin thực hiện
- **Lớp**: [Điền tên lớp]
- **Nhóm thực hiện**: [Điền tên các thành viên]
- **Trưởng nhóm**: buianna1999
- **Link GitHub**: [Link của anh]
