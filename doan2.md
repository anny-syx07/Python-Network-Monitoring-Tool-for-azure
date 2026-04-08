BỘ GIÁO DỤC VÀ ĐÀO TẠO

**TRƯỜNG ĐẠI HỌC QUẢN LÝ & CÔNG NGHỆ TP. HCM**

**ĐỒ ÁN MÔN HỌC**

**XÂY DỰNG CÔNG CỤ GIÁM SÁT**

**MẠNG BẰNG PYTHON VÀ TRIỂN KHAI**

**TRÊN ĐÁM MÂY AZURE**

Ngành: **CÔNG NGHỆ THÔNG TIN**

Chuyên ngành: **MẠNG MÁY TÍNH VÀ ĐIỆN TOÁN ĐÁM MÂY**

Giảng viên hướng dẫn: Nguyễn Thanh Phong

Lớp: 1747

|Sinh viên thực hiện:|MSSV:|
| - | :- |
|1\.Ngô Đình Thông|2403700248|
|2\.Nguyễn Nhật Duy|2403700298|
|3\.Bùi Thị Anh Thư|2403700243|

TP. Hồ Chí Minh, 2026

---

## **DANH MỤC CHỮ VIẾT TẮT**

|**Viết tắt**|**Nghĩa đầy đủ**|
| :- | :- |
|API|Application Programming Interface|
|CSV|Comma-Separated Values|
|DNS|Domain Name System|
|GUI|Graphical User Interface|
|HTTP|HyperText Transfer Protocol|
|HTTPS|HTTP Secure|
|ICMP|Internet Control Message Protocol|
|IP|Internet Protocol|
|LAN|Local Area Network|
|NMS|Network Management System|
|REST|Representational State Transfer|
|SMB|Server Message Block|
|TCP|Transmission Control Protocol|
|TLS|Transport Layer Security|
|UI|User Interface|

---

**MỤC LỤC**

- Chương 1. MỞ ĐẦU
  - 1.1. Đặt vấn đề
  - 1.2. Mục tiêu đề tài
  - 1.3. Phạm vi và giới hạn
  - 1.4. Bố cục đồ án
- Chương 2. CƠ SỞ LÝ THUYẾT
  - 2.1. Tổng quan về giám sát mạng
  - 2.2. Giao thức mạng sử dụng trong đề tài
  - 2.3. Lập trình mạng với Python
  - 2.4. Giao diện đồ họa với Tkinter
  - 2.5. Trực quan hóa dữ liệu với Matplotlib
  - 2.6. Framework Flask và RESTful API
  - 2.7. Điện toán đám mây với Microsoft Azure
- Chương 3. KẾT QUẢ THỰC NGHIỆM
  - 3.1. Thiết kế hệ thống
  - 3.2. Cài đặt chi tiết – Ứng dụng Desktop (monitor.py)
  - 3.3. Cài đặt chi tiết – API Cloud (azure_app/app.py)
  - 3.4. Triển khai lên Azure
  - 3.5. Kết quả thu được
- Chương 4. KẾT LUẬN VÀ KIẾN NGHỊ
- TÀI LIỆU THAM KHẢO
- PHỤ LỤC

---

# **Chương 1. MỞ ĐẦU**

## **1.1. Đặt vấn đề**

Trong bối cảnh hạ tầng công nghệ thông tin ngày càng phức tạp và phân tán, việc giám sát liên tục trạng thái hoạt động của các thiết bị và dịch vụ mạng trở thành yêu cầu cấp thiết đối với mọi tổ chức. Sự cố mạng nếu không được phát hiện và xử lý kịp thời có thể gây ra gián đoạn dịch vụ, tổn thất kinh tế và mất uy tín đối với người dùng [1].

Các hệ thống quản lý mạng chuyên nghiệp hiện có như Nagios, Zabbix hay PRTG Network Monitor cung cấp khả năng giám sát toàn diện, nhưng đi kèm với chi phí triển khai cao, yêu cầu máy chủ chuyên dụng và độ phức tạp trong cấu hình. Điều này tạo ra rào cản đáng kể cho các tổ chức vừa và nhỏ hoặc các nhóm kỹ thuật có nguồn lực hạn chế.

Python là ngôn ngữ lập trình mạnh mẽ, phổ biến và sở hữu hệ sinh thái thư viện phong phú, đặc biệt là các thư viện hỗ trợ lập trình mạng (ping3, requests), giao diện đồ họa (Tkinter) và trực quan hóa dữ liệu (Matplotlib) [2]. Kết hợp với nền tảng đám mây Microsoft Azure, hoàn toàn có thể xây dựng một công cụ giám sát mạng có giao diện trực quan, khả năng lưu trữ đám mây và hoạt động liên tục mà không cần đầu tư phần cứng.

Từ những phân tích trên, đề tài "Xây dựng công cụ giám sát mạng bằng Python và triển khai trên nền tảng đám mây Microsoft Azure" được đề xuất nhằm giải quyết bài toán giám sát mạng với chi phí thấp, giao diện thân thiện và khả năng lưu trữ dữ liệu tập trung trên Cloud.

## **1.2. Mục tiêu đề tài**

Đề tài hướng đến các mục tiêu cụ thể sau:

**Mục tiêu chính:**

- Xây dựng ứng dụng giám sát mạng bằng Python có giao diện đồ họa (GUI), có khả năng ping kiểm tra trạng thái host theo thời gian thực, hiển thị biểu đồ trực quan và quét mạng LAN.

**Mục tiêu phụ:**

- Xây dựng API trên nền tảng Flask để tiếp nhận và lưu trữ dữ liệu giám sát tập trung trên đám mây Azure.
- Áp dụng kỹ thuật lập trình đa luồng (multithreading) để ứng dụng không bị đóng băng khi ping.
- Triển khai biểu đồ thời gian thực (real-time chart) bằng Matplotlib Animation.
- Bảo mật API bằng cơ chế xác thực Bearer Token.
- Lưu trữ bền vững dữ liệu CSV trên Azure File Share thông qua Azure App Service.

## **1.3. Phạm vi và giới hạn**

**Phạm vi thực hiện:**

Bảng 1.1. Phạm vi đề tài

|**Khía cạnh**|**Chi tiết**|
| :-: | :-: |
|Ngôn ngữ lập trình|Python 3 (Tkinter, Flask, ping3, Matplotlib)|
|Nền tảng đám mây|Microsoft Azure (Azure for Students)|
|Dịch vụ Azure|App Service (B1), Storage Account, File Share|
|Giao thức giám sát|ICMP (ping)|
|Mục tiêu giám sát|Địa chỉ IP tùy chọn (mặc định 8.8.8.8) + quét LAN|
|Đầu ra|File CSV (local + cloud), biểu đồ thời gian thực|
|Tổng số bản ghi thu thập|14.765+ bản ghi log|

**Giới hạn:**

- Ứng dụng Desktop yêu cầu chạy trên máy tính có cài Python (chưa đóng gói thành file .exe/.app).
- Phạm vi giám sát giới hạn ở tầng mạng (Layer 3); chưa hỗ trợ giao thức ứng dụng (Layer 7).
- Quét LAN giới hạn ở dải IP .1 đến .10 để đảm bảo tốc độ nhanh.

## **1.4. Bố cục đồ án**

Ngoài phần mở đầu, tài liệu tham khảo và phụ lục, đồ án được tổ chức thành 4 chương:

- **Chương 1 – Mở đầu**: Trình bày bối cảnh, lý do chọn đề tài, mục tiêu và phạm vi nghiên cứu.
- **Chương 2 – Cơ sở lý thuyết**: Tổng quan các giao thức mạng, kỹ thuật lập trình Python, Tkinter, Matplotlib, Flask và nền tảng Azure.
- **Chương 3 – Kết quả thực nghiệm**: Trình bày thiết kế hệ thống, chi tiết cài đặt, quy trình triển khai lên Azure và kết quả thu được.
- **Chương 4 – Kết luận và kiến nghị**: Đánh giá kết quả, hạn chế và hướng phát triển tiếp theo.

---

# **Chương 2. CƠ SỞ LÝ THUYẾT**

## **2.1. Tổng quan về giám sát mạng**

### **2.1.1. Khái niệm giám sát mạng**

Giám sát mạng (Network Monitoring) là quá trình theo dõi liên tục trạng thái hoạt động của các thành phần hạ tầng mạng bao gồm: thiết bị đầu cuối (host), thiết bị mạng (router, switch), và các dịch vụ mạng (web server, database) [1]. Mục tiêu chính là phát hiện sớm các bất thường, đo lường hiệu suất và đảm bảo tính khả dụng (availability) của hệ thống.

Các chỉ số quan trọng trong giám sát mạng bao gồm:

- **Uptime (%)**: Tỷ lệ thời gian host/dịch vụ hoạt động bình thường.
- **Latency (ms)**: Thời gian trễ từ điểm gửi đến điểm nhận, đo bằng millisecond.
- **Packet Loss (%)**: Tỷ lệ gói tin bị mất trên đường truyền.
- **Downtime**: Khoảng thời gian host/dịch vụ ngừng hoạt động.

### **2.1.2. Các công cụ giám sát mạng hiện có**

Bảng 2.1. So sánh các công cụ giám sát mạng phổ biến

|**Công cụ**|**Ưu điểm**|**Nhược điểm**|
| :-: | :-: | :-: |
|Nagios|Mạnh mẽ, plugin phong phú|Phức tạp, tốn tài nguyên|
|Zabbix|Dashboard trực quan|Yêu cầu cấu hình cao|
|PRTG|Giao diện thân thiện|Chi phí bản quyền cao|
|**Network Monitor PRO (đề tài này)**|Nhẹ, miễn phí, có GUI, tích hợp Cloud|Chưa hỗ trợ Layer 7|

## **2.2. Giao thức mạng sử dụng trong đề tài**

### **2.2.1. Giao thức ICMP**

ICMP (Internet Control Message Protocol) là giao thức tầng Network (Layer 3) trong mô hình OSI, được định nghĩa trong RFC 792 [3]. ICMP được thiết kế để truyền thông báo điều khiển và kiểm lỗi giữa các thiết bị mạng.

Lệnh ping hoạt động bằng cách:

1. Gửi gói tin **ICMP Echo Request** đến host đích.
2. Chờ nhận **ICMP Echo Reply** từ host đó.
3. Tính toán thời gian trễ (RTT – Round Trip Time).

Trong đề tài, thư viện `ping3` được sử dụng để gửi ICMP ping trực tiếp từ Python, thay vì gọi lệnh hệ điều hành qua subprocess. Điều này giúp code gọn hơn và hoạt động nhất quán trên mọi hệ điều hành.

### **2.2.2. Giao thức TCP và HTTP/HTTPS**

TCP (Transmission Control Protocol) là giao thức tầng Transport (Layer 4), cung cấp kết nối tin cậy thông qua cơ chế **3-way handshake** [4].

Đề tài sử dụng giao thức HTTP/HTTPS (dựa trên TCP) để giao tiếp giữa ứng dụng Desktop và API trên Azure Cloud:

- **POST /api/log**: Gửi dữ liệu giám sát lên Cloud dưới dạng JSON.
- **GET /api/csv**: Truy xuất dữ liệu log từ Cloud dưới dạng CSV.

### **2.2.3. Hệ thống phân giải tên miền DNS**

DNS (Domain Name System) là hệ thống phân cấp phân giải hostname (google.com) thành địa chỉ IP (172.217.x.x) [5]. Đề tài cho phép người dùng nhập cả hostname hoặc địa chỉ IP vào trường Target IP để kiểm tra.

## **2.3. Lập trình mạng với Python**

### **2.3.1. Thư viện ping3**

`ping3` là thư viện Python cho phép gửi ICMP Echo Request và nhận Echo Reply trực tiếp từ Python mà không cần gọi lệnh hệ điều hành [2]. Hàm `ping(ip, timeout)` trả về thời gian phản hồi (RTT) nếu host online, hoặc `None` nếu host offline/timeout.

### **2.3.2. Thư viện requests**

`requests` là thư viện HTTP phổ biến nhất trong Python, cung cấp giao diện đơn giản để gửi HTTP request [2]. Đề tài dùng `requests.post()` để gửi dữ liệu JSON lên Azure API với Bearer Token trong header Authorization.

### **2.3.3. Module threading và đa luồng**

Python cung cấp module `threading` để lập trình đa luồng. Đề tài sử dụng `threading.Thread(daemon=True)` để tạo luồng nền cho việc ping liên tục và quét LAN, đảm bảo giao diện GUI không bị đóng băng (freeze) trong quá trình xử lý mạng.

### **2.3.4. Module csv**

Module `csv` trong thư viện chuẩn Python hỗ trợ đọc và ghi file CSV (Comma-Separated Values). Đề tài ghi log dự phòng ra file `log.csv` local bằng `csv.writer()`, đảm bảo dữ liệu không bị mất nếu kết nối Cloud gặp sự cố.

## **2.4. Giao diện đồ họa với Tkinter**

Tkinter là thư viện GUI tiêu chuẩn đi kèm Python, không cần cài đặt thêm [2]. Tkinter cung cấp các widget cơ bản như Label, Entry, Button, Text, Frame để xây dựng giao diện ứng dụng desktop.

Đặc điểm quan trọng của Tkinter liên quan đến đề tài:

- **Vòng lặp sự kiện (Event Loop)**: `root.mainloop()` chạy vòng lặp chính, lắng nghe sự kiện người dùng.
- **Thread-safe update**: Tkinter không cho phép cập nhật UI từ luồng phụ. Phải dùng `root.after(0, callback)` để đẩy việc cập nhật về luồng chính.
- **Widget state**: Nút bấm có thể vô hiệu hóa (`state=tk.DISABLED`) để chống thao tác trùng lặp.

## **2.5. Trực quan hóa dữ liệu với Matplotlib**

Matplotlib là thư viện vẽ biểu đồ mạnh mẽ nhất trong Python [6]. Đề tài sử dụng `matplotlib.animation.FuncAnimation` để tạo biểu đồ cập nhật theo thời gian thực (real-time chart), hiển thị trạng thái Online/Offline của host theo thời gian.

FuncAnimation gọi hàm vẽ lại biểu đồ mỗi 1000ms (1 giây), cho phép người dùng quan sát xu hướng kết nối mạng một cách trực quan mà không cần tải lại trang.

## **2.6. Framework Flask và RESTful API**

Flask là micro web framework trong Python, nhẹ và linh hoạt, phù hợp để xây dựng REST API [7]. Đề tài sử dụng Flask để tạo 2 endpoint API trên Azure:

- `POST /api/log`: Nhận dữ liệu JSON từ ứng dụng Desktop, ghi vào file CSV trên Azure File Share.
- `GET /api/csv`: Trả về nội dung file CSV cho người dùng hoặc giảng viên xem trực online trên trình duyệt.

Cơ chế xác thực **Bearer Token** được áp dụng: mỗi request phải kèm header `Authorization: Bearer <token>` hoặc query parameter `?token=<token>` để được chấp nhận.

## **2.7. Điện toán đám mây với Microsoft Azure**

### **2.7.1. Azure App Service**

Azure App Service là dịch vụ PaaS (Platform as a Service) cho phép triển khai ứng dụng web mà không cần quản lý máy chủ vật lý [8]. Ứng dụng Flask được deploy trực tiếp bằng lệnh `az webapp deployment source config-zip`, Azure tự động nhận diện và chạy ứng dụng Python qua Gunicorn.

### **2.7.2. Azure Storage Account và File Share**

Azure File Share là dịch vụ lưu trữ file trên đám mây theo giao thức SMB (Server Message Block). Bằng cách **mount** (gắn kết) File Share vào Web App, tất cả file được ghi vào thư mục mount sẽ lưu trực tiếp trên đám mây, đảm bảo dữ liệu tồn tại độc lập với vòng đời ứng dụng [8].

### **2.7.3. Azure for Students**

Chương trình Azure for Students cung cấp $100 USD credit miễn phí cho sinh viên đại học có địa chỉ email trường. Credit được khấu trừ tự động vào chi phí sử dụng dịch vụ Azure, không yêu cầu thẻ tín dụng [9].

---

# **Chương 3. KẾT QUẢ THỰC NGHIỆM**

## **3.1. Thiết kế hệ thống**

### **3.1.1. Kiến trúc tổng quan**

Hệ thống được thiết kế theo mô hình **Client – Server**, gồm hai thành phần chính:

- **Client (Desktop App)**: `monitor.py` chạy trên máy tính người dùng, gửi dữ liệu giám sát lên Cloud.
- **Server (Cloud API)**: `azure_app/app.py` chạy trên Azure App Service, tiếp nhận và lưu trữ dữ liệu.

```
[Máy tính người dùng]                    [Microsoft Azure Cloud]
┌──────────────────────┐                  ┌──────────────────────────┐
│   monitor.py (GUI)   │  HTTP POST JSON  │  Azure App Service (B1)  │
│  - Ping (ping3)      │─────────────────>│  Flask API (app.py)      │
│  - LAN Scanner       │  Bearer Token    │  POST /api/log           │
│  - Live Graph        │                  │  GET  /api/csv           │
│  - CSV Backup        │                  │         │ mount           │
│  log.csv (local)     │                  │  Azure File Share        │
└──────────────────────┘                  │  csvreports/log.csv      │
                                          └──────────────────────────┘
```

<!-- CHÈN HÌNH 3.1: Sơ đồ kiến trúc tổng quan hệ thống -->
*Hình 3.1. Kiến trúc tổng quan hệ thống giám sát mạng*

### **3.1.2. Cấu trúc thư mục dự án**

Bảng 3.1. Mô tả các file trong dự án

|**File / Thư mục**|**Vai trò**|
| :-: | :-: |
|`monitor.py`|Ứng dụng Desktop – GUI giám sát mạng (Tkinter + Matplotlib)|
|`azure_app/app.py`|Flask API – Tiếp nhận và lưu trữ log trên Cloud|
|`azure_app/requirements.txt`|Thư viện Python cần thiết cho Cloud API|
|`log.csv`|File log dự phòng local (14.765+ bản ghi thu thập)|
|`README.md`|Tài liệu hướng dẫn dự án|

### **3.1.3. Luồng xử lý chính**

Khi người dùng nhấn nút **Start**:

1. Ứng dụng tạo một **thread nền** (`daemon=True`) để ping liên tục mỗi 2 giây.
2. Mỗi lần ping, kết quả được xử lý đồng thời:
   - Cập nhật **giao diện GUI** qua `root.after(0, update_gui, ...)`.
   - Lưu dữ liệu vào mảng để vẽ **biểu đồ thời gian thực**.
   - Ghi vào **log.csv local** (bản sao dự phòng).
   - Gửi lên **Azure Cloud API** qua HTTP POST kèm Bearer Token.
3. Trên Cloud, Flask nhận JSON và append vào `log.csv` trên Azure File Share.

## **3.2. Cài đặt chi tiết – Ứng dụng Desktop (monitor.py)**

### **3.2.1. Giao diện người dùng (GUI)**

<!-- CHÈN HÌNH 3.2: Ảnh chụp giao diện ứng dụng monitor.py đang chạy -->
*Hình 3.2. Giao diện ứng dụng Network Monitor PRO*

Các thành phần GUI chính:

|**Widget**|**Chức năng**|
| :-: | :-: |
|Entry (ô nhập IP)|Nhập địa chỉ IP/hostname cần giám sát (mặc định: 8.8.8.8)|
|Label Status|Hiển thị Online (xanh) / Offline (đỏ) theo thời gian thực|
|Label Time|Hiển thị thời gian của lần kiểm tra gần nhất|
|Button Start|Bắt đầu giám sát, tự khóa khi đang chạy (chống bấm đúp)|
|Button Stop|Dừng giám sát, mở khóa lại nút Start|
|Button Show Live Graph|Mở cửa sổ biểu đồ Matplotlib thời gian thực|
|Button Scan Quick LAN|Quét nhanh 10 IP đầu tiên trong mạng LAN|
|Text Area|Hiển thị kết quả quét LAN|

### **3.2.2. Chức năng Ping và giám sát liên tục**

```python
def check_network():
    global running, times, status_values
    while running:
        ip = entry_ip.get()
        result = ping(ip, timeout=1)   # ping3 library – ICMP

        status = 1 if result else 0
        status_text = "Online" if result else "Offline"
        current_time = time.strftime("%H:%M:%S")

        # Thread-safe: cập nhật UI từ luồng chính
        root.after(0, update_gui, status_text, current_time)

        # Ghi log local dự phòng
        with open("log.csv", "a", newline="") as f:
            csv.writer(f).writerow([ip, status_text, current_time])

        # Gửi lên Cloud Azure (fail-safe: bắt exception)
        try:
            requests.post(AZURE_API_URL, json={
                "ip": ip, "status": status_text, "time": current_time
            }, headers={"Authorization": "Bearer Anna-Secret-Token-2026"}, timeout=2)
        except Exception as e:
            print(f"Lỗi kết nối Server Azure: {e}")

        time.sleep(2)
```

**Điểm kỹ thuật quan trọng:**
- `root.after(0, ...)`: Đẩy cập nhật UI về luồng chính, tránh crash do Tkinter không thread-safe.
- `daemon=True`: Thread tự hủy khi cửa sổ ứng dụng đóng.
- **Fail-safe**: Exception khi gửi Cloud được bắt và bỏ qua – ứng dụng tiếp tục chạy bình thường.

### **3.2.3. Biểu đồ thời gian thực**

<!-- CHÈN HÌNH 3.3: Ảnh chụp biểu đồ Matplotlib đang hiển thị -->
*Hình 3.3. Biểu đồ giám sát mạng thời gian thực (FuncAnimation)*

```python
ani = FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
```

Biểu đồ cập nhật mỗi 1 giây, giới hạn **60 điểm dữ liệu** gần nhất, trục Y chỉ 2 giá trị: `Offline (0)` và `Online (1)`.

### **3.2.4. Quét mạng LAN**

<!-- CHÈN HÌNH 3.4: Ảnh chụp kết quả quét LAN trong Text Area -->
*Hình 3.4. Kết quả quét nhanh mạng LAN*

```python
def scan_lan_thread():
    base_ip = entry_ip.get().rsplit('.', 1)[0]   # Lấy 3 octet đầu
    for i in range(1, 11):
        ip = f"{base_ip}.{i}"
        result = ping(ip, timeout=0.5)
        if result:
            # Dùng biến mặc định lambda tránh lỗi closure
            root.after(0, lambda cur=ip:
                result_text.insert(tk.END, f"[+] {cur} is ONLINE\n"))
```

## **3.3. Cài đặt chi tiết – API Cloud (azure_app/app.py)**

### **3.3.1. Endpoint POST /api/log – Nhận và lưu dữ liệu**

```python
@app.route("/api/log", methods=["POST"])
def log_data():
    if not check_auth(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    os.makedirs(FILE_SHARE_PATH, exist_ok=True)

    file_exists = os.path.isfile(CSV_FILE_PATH)
    with open(CSV_FILE_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["ip", "status", "time"])  # Tự tạo header
        writer.writerow([data.get("ip"), data.get("status"), data.get("time")])

    return jsonify({"status": "ok"})
```

### **3.3.2. Endpoint GET /api/csv – Xem dữ liệu trên trình duyệt**

<!-- CHÈN HÌNH 3.5: Ảnh chụp trình duyệt truy cập /api/csv có dữ liệu CSV -->
*Hình 3.5. Dữ liệu CSV trả về qua trình duyệt*

API hỗ trợ 2 kiểu xác thực linh hoạt:
1. **Header**: `Authorization: Bearer Anna-Secret-Token-2026`
2. **Query param**: `?token=Anna-Secret-Token-2026` (mở thẳng trên trình duyệt)

```bash
# Kiểm tra qua curl
curl -H "Authorization: Bearer Anna-Secret-Token-2026" \
  https://network-monitor-pro-anna.azurewebsites.net/api/csv

# Kết quả
ip,status,time
8.8.8.8,Online,20:47:16
8.8.8.8,Online,20:47:18
...

# Truy cập không có token → 401
curl https://network-monitor-pro-anna.azurewebsites.net/api/csv
{"error":"Unauthorized"}
```

## **3.4. Triển khai lên Azure**

### **3.4.1. Cấu hình tài nguyên Azure**

Bảng 3.5. Cấu hình tài nguyên Azure đã triển khai

|**Tài nguyên**|**Giá trị**|**Lý do chọn**|
| :-: | :-: | :-: |
|Resource Group|RG_Network_Monitor|Nhóm quản lý toàn bộ tài nguyên|
|Location|Malaysia West|Gần Việt Nam, phù hợp tài khoản sinh viên|
|Storage Account|stloganna2026 (Standard_LRS)|Lưu trữ file CSV bền vững chi phí thấp|
|File Share|csvreports|Giao thức SMB mount vào Web App|
|App Service Plan|ASP-NetworkMonitor (B1, Linux)|Gói Basic – đủ cho API nhẹ|
|Web App|network-monitor-pro-anna|Python 3.12 runtime|
|Mount Path|/mounts/csvreports|Đường dẫn mount File Share trong app|

### **3.4.2. Lưu trữ bền vững với Azure File Share**

<!-- CHÈN HÌNH 3.6: Ảnh chụp Azure Portal → Storage Account → File Share csvreports -->
*Hình 3.6. File Share csvreports trên Azure Portal*

Khi Flask ghi vào `/mounts/csvreports/log.csv`, dữ liệu được lưu **trực tiếp trên Azure File Share**, độc lập với vòng đời Web App. Redeploy hay restart không làm mất dữ liệu.

## **3.5. Kết quả thu được**

### **3.5.1. Thống kê dữ liệu thu thập**

Bảng 3.7. Thống kê dữ liệu thực nghiệm

|**Thông số**|**Giá trị**|
| :-: | :-: |
|Cloud API URL|https://network-monitor-pro-anna.azurewebsites.net|
|Tổng bản ghi thu thập (log.csv local)|14.765 bản ghi|
|Các IP đã giám sát|8.8.8.8, 1.1.1.1, 192.168.1.90, 10.12.3.221, ...|
|Chu kỳ ping|2 giây/lần|
|Gói Azure|Azure for Students ($100 credit)|

### **3.5.2. Mẫu dữ liệu CSV**

**Local log.csv (14.765+ bản ghi):**
```
8.8.8.8,Online,02:05:00
8.8.8.8,Online,02:05:02
192.168.1.90,Online,04:43:10
1.1.1.1,Online,04:52:02
10.12.3.221,Online,10:03:06
8.8.8.8,Offline,10:59:20   ← phát hiện mất kết nối
8.8.8.8,Online,10:59:23    ← kết nối phục hồi
```

**Cloud log.csv (Azure File Share):**
```
ip,status,time
8.8.8.8,Online,20:47:16
8.8.8.8,Online,20:47:18
8.8.8.8,Online,20:47:20
```

### **3.5.3. Kết quả demo**

<!-- CHÈN HÌNH 3.7: Ảnh chụp ứng dụng đang chạy – Status: Online màu xanh -->
*Hình 3.7. Ứng dụng Network Monitor PRO đang giám sát 8.8.8.8*

<!-- CHÈN VIDEO 3.1: Video demo toàn bộ chức năng (Ping, Graph, Scan LAN, Cloud API) -->
*Video 3.1. Demo toàn bộ chức năng hệ thống*

### **3.5.4. Đánh giá kết quả tổng thể**

Bảng 3.10. Tổng kết đánh giá các chỉ tiêu

|**Chỉ tiêu**|**Kết quả**|**Đánh giá**|
| :-: | :-: | :-: |
|GUI hoạt động ổn định, không freeze|✅ Đạt|Thread nền + root.after()|
|Biểu đồ real-time cập nhật đúng|✅ Đạt|FuncAnimation 1s/lần|
|Quét LAN phát hiện thiết bị|✅ Đạt|Phát hiện đúng Online/Offline|
|Ghi log local 14.765+ bản ghi|✅ Đạt|CSV append mode hoạt động|
|API Cloud nhận và lưu dữ liệu|✅ Đạt|Azure File Share mount OK|
|Bảo mật Bearer Token|✅ Đạt|401 khi không có token|
|File Share bền vững qua redeploy|✅ Đạt|Dữ liệu không mất sau restart|
|Fail-safe khi mất kết nối Cloud|✅ Đạt|App tiếp tục chạy bình thường|

---

# **Chương 4. KẾT LUẬN VÀ KIẾN NGHỊ**

## **4.1. Kết luận**

Đề tài đã hoàn thành xây dựng hệ thống giám sát mạng hoàn chỉnh gồm ứng dụng Desktop có GUI và API Cloud trên Azure.

**Các kết quả đạt được:**

1. **Giao diện người dùng**: Ứng dụng Tkinter với đầy đủ chức năng: giám sát real-time, biểu đồ trực quan, quét LAN, cập nhật màu sắc trạng thái.

2. **Kỹ thuật lập trình**: Áp dụng đa luồng (`threading`) bảo đảm UI không freeze. Xử lý đúng thread-safe với `root.after()`. Fail-safe exception handling cho kết nối Cloud.

3. **Tích hợp Cloud**: REST API Flask trên Azure App Service nhận dữ liệu liên tục và lưu bền vững lên Azure File Share. Hệ thống thu thập 14.765+ bản ghi log.

4. **Bảo mật**: Bearer Token Authentication ngăn truy cập trái phép. Hỗ trợ 2 kiểu xác thực (Header + Query Param).

5. **Chi phí**: Toàn bộ vận hành trong phạm vi Azure for Students ($100 credit).

## **4.2. Kiến nghị và hướng phát triển**

**Hạn chế hiện tại:**

|**Hạn chế**|**Nguyên nhân**|**Mức độ ảnh hưởng**|
| :-: | :-: | :-: |
|Chưa đóng gói .exe/.app|Chưa dùng PyInstaller|Trung bình – cần cài Python|
|Chưa có cảnh báo realtime|Chưa tích hợp Telegram/Slack|Cao – ảnh hưởng thực tiễn|
|Quét LAN giới hạn 10 IP|Thiết kế ban đầu đơn giản|Thấp|
|Cloud CSV chưa có giao diện web|Chỉ trả raw CSV|Trung bình|

**Hướng phát triển:**

1. **Alert System**: Tích hợp Telegram Bot gửi cảnh báo khi host down.
2. **Dashboard Web**: Flask + Chart.js hiển thị biểu đồ latency online.
3. **Đóng gói ứng dụng**: PyInstaller → file .exe/.app cho người dùng phổ thông.
4. **Mở rộng LAN Scanner**: Quét toàn bộ /24 subnet với ThreadPoolExecutor.
5. **Database**: Thay CSV bằng SQLite hoặc Azure Cosmos DB cho truy vấn phức tạp.

---

# **TÀI LIỆU THAM KHẢO**

[1] Subramanian, M. (2000). *Network Management: Principles and Practice*. Addison-Wesley.

[2] Python Software Foundation (2023). *Python 3 Standard Library Documentation*. https://docs.python.org/3/library/

[3] Postel, J. (1981). *Internet Control Message Protocol (RFC 792)*. IETF. https://www.rfc-editor.org/rfc/rfc792

[4] Postel, J. (1981). *Transmission Control Protocol (RFC 793)*. IETF. https://www.rfc-editor.org/rfc/rfc793

[5] Mockapetris, P. (1987). *Domain Names – Specification (RFC 1035)*. IETF. https://www.rfc-editor.org/rfc/rfc1035

[6] Hunter, J.D. (2007). Matplotlib: A 2D Graphics Environment. *Computing in Science & Engineering*, 9(3), 90–95.

[7] Grinberg, M. (2018). *Flask Web Development*. O'Reilly Media.

[8] Microsoft Corporation (2024). *Azure App Service Documentation*. https://learn.microsoft.com/en-us/azure/app-service/

[9] Microsoft Corporation (2024). *Azure for Students*. https://azure.microsoft.com/en-us/free/students/

---

# **PHỤ LỤC**

## **Phụ lục A. Mã nguồn monitor.py**

Xem file: `monitor.py` trong thư mục gốc dự án.

Các hàm chính:
- `check_network()` – Vòng lặp ping + ghi log + gửi Cloud
- `update_gui()` – Cập nhật Label Status/Time an toàn từ thread chính
- `show_graph()` – Khởi tạo Matplotlib FuncAnimation
- `scan_lan_thread()` – Quét dải IP LAN
- `start()` / `stop()` – Điều khiển trạng thái giám sát

## **Phụ lục B. Mã nguồn azure_app/app.py**

Xem file: `azure_app/app.py` trong thư mục dự án.

Các route chính:
- `POST /api/log` – Nhận JSON, append vào CSV trên File Share
- `GET /api/csv` – Trả nội dung CSV cho trình duyệt/curl

## **Phụ lục C. Mẫu dữ liệu log.csv**

```
ip,status,time
8.8.8.8,Online,02:05:00
8.8.8.8,Online,02:05:02
192.168.1.90,Online,04:43:10
1.1.1.1,Online,04:52:02
10.12.3.221,Online,10:03:06
8.8.8.8,Offline,10:59:20
8.8.8.8,Online,10:59:23
```

## **Phụ lục D. Lệnh Azure CLI triển khai**

```bash
# Tạo Resource Group
az group create --name RG_Network_Monitor --location malaysiawest

# Tạo Storage + File Share
az storage account create --name stloganna2026 \
  --resource-group RG_Network_Monitor --location malaysiawest --sku Standard_LRS
az storage share create --name csvreports --account-name stloganna2026

# Tạo App Service + Web App
az appservice plan create --name ASP-NetworkMonitor \
  --resource-group RG_Network_Monitor --location malaysiawest --sku B1 --is-linux
az webapp create --resource-group RG_Network_Monitor \
  --plan ASP-NetworkMonitor --name network-monitor-pro-anna --runtime "PYTHON:3.12"

# Mount File Share
az webapp config storage-account add \
  --resource-group RG_Network_Monitor --name network-monitor-pro-anna \
  --custom-id csvmount --storage-type AzureFiles \
  --share-name csvreports --account-name stloganna2026 \
  --access-key <KEY> --mount-path /mounts/csvreports

# Deploy code
cd azure_app && zip -r ../deploy.zip .
az webapp deployment source config-zip \
  --resource-group RG_Network_Monitor \
  --name network-monitor-pro-anna --src deploy.zip
```
