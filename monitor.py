import tkinter as tk
from tkinter import messagebox
from ping3 import ping
import time
import threading
import csv
import requests
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ===== AZURE (Flask Server API) =====
AZURE_API_URL = "https://network-monitor-pro-anna.azurewebsites.net/api/log"

# ===== GLOBAL VARIABLES =====
running = False
times = []
status_values = []
MAX_DATA_POINTS = 60  # Giới hạn 60 điểm để biểu đồ không bị rối
ani = None  # Biến lưu trữ Animation của biểu đồ để không bị lỗi

# ===== CHECK NETWORK =====
def check_network():
    global running, times, status_values
    while running:
        ip = entry_ip.get()
        # Thêm timeout=1 để không bị treo nếu mất mạng hoàn toàn
        result = ping(ip, timeout=1) 

        status = 1 if result else 0
        status_text = "Online" if result else "Offline"
        current_time = time.strftime("%H:%M:%S")

        # CẬP NHẬT UI AN TOÀN: Đẩy việc cập nhật chữ về luồng chính của Tkinter
        root.after(0, update_gui, status_text, current_time)

        # Lưu dữ liệu để vẽ đồ thị
        times.append(current_time)
        status_values.append(status)

        # Cắt bớt mảng nếu vượt quá giới hạn
        if len(times) > MAX_DATA_POINTS:
            times = times[-MAX_DATA_POINTS:]
            status_values = status_values[-MAX_DATA_POINTS:]

        # Ghi log dự phòng ra file CSV
        with open("log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([ip, status_text, current_time])

        # Gửi dữ liệu JSON lên Cloud Azure
        try:
            API_TOKEN = "Anna-Secret-Token-2026"
            headers = {"Authorization": f"Bearer {API_TOKEN}"}
            data = {"ip": ip, "status": status_text, "time": current_time}
            requests.post(AZURE_API_URL, json=data, headers=headers, timeout=2)
        except Exception as e:
            print(f"Lỗi kết nối Server Azure: {e}")

        # Tạm nghỉ 2 giây rồi ping tiếp
        time.sleep(2)

def update_gui(status_text, current_time):
    label_status.config(text=f"Status: {status_text}", fg="green" if status_text == "Online" else "red")
    label_time.config(text=f"Time: {current_time}")

# ===== START/STOP =====
def start():
    global running
    if not running:  
        running = True
        btn_start.config(state=tk.DISABLED)  # Khóa mờ nút Start lại để chống bấm đúp
        threading.Thread(target=check_network, daemon=True).start()

def stop():
    global running
    running = False
    btn_start.config(state=tk.NORMAL)  # Mở khóa lại nút Start
    label_status.config(text="Status: Stopped", fg="black")

# ===== REAL-TIME GRAPH =====
def show_graph():
    global times, status_values, ani
    
    if not times:
        messagebox.showinfo("Thông báo", "Chưa có dữ liệu! Hãy nhấn Start và đợi vài giây.")
        return

    # Khởi tạo cửa sổ biểu đồ
    fig, ax = plt.subplots(figsize=(8, 5))
    plt.subplots_adjust(bottom=0.25) # Nới rộng lề dưới để không bị cắt chữ

    def animate(i):
        if not times: return
        ax.clear() # Xóa nét vẽ cũ
        
        # Vẽ nét mới
        ax.plot(times, status_values, marker='o', linestyle='-', color='#1f77b4', linewidth=2)
        
        # Cấu hình thẩm mỹ cho biểu đồ
        ax.set_title("Biểu đồ giám sát mạng (Real-time)", fontsize=13, fontweight='bold')
        ax.set_ylim(-0.5, 1.5)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['Offline (0)', 'Online (1)'])
        ax.set_ylabel("Trạng thái")
        ax.grid(True, linestyle='--', alpha=0.6)

        # Tính toán để trục X không bị dính chữ vào nhau
        step = max(1, len(times) // 8)
        ax.set_xticks(range(0, len(times), step))
        ax.set_xticklabels(times[::step], rotation=45, ha='right')

    # Chạy Animation cập nhật tự động mỗi 1000ms (1 giây)
    ani = FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
    plt.show()

# ===== SCAN LAN =====
def scan_lan_thread():
    base_ip = entry_ip.get().rsplit('.', 1)[0]
    
    # Dọn dẹp Text box và khóa nút Scan an toàn
    root.after(0, lambda: result_text.delete(1.0, tk.END))
    root.after(0, lambda: btn_scan.config(state=tk.DISABLED))
    root.after(0, lambda: result_text.insert(tk.END, f"Đang quét IP từ {base_ip}.1 đến .10...\n"))

    for i in range(1, 11):
        ip = f"{base_ip}.{i}"
        result = ping(ip, timeout=0.5)
        if result:
            root.after(0, lambda current_ip=ip: result_text.insert(tk.END, f"[+] {current_ip} is ONLINE\n"))
            
    root.after(0, lambda: result_text.insert(tk.END, "Hoàn tất quét mạng!\n"))
    root.after(0, lambda: btn_scan.config(state=tk.NORMAL))

def scan_lan():
    threading.Thread(target=scan_lan_thread, daemon=True).start()

# ===== GUI SETUP =====
root = tk.Tk()
root.title("Network Monitor PRO")
root.geometry("350x510")

tk.Label(root, text="Enter Target IP:").pack(pady=(10,0))
entry_ip = tk.Entry(root, justify="center", font=("Arial", 11))
entry_ip.pack(pady=5)
entry_ip.insert(0, "8.8.8.8")

label_status = tk.Label(root, text="Status: Waiting...", font=("Arial", 12, "bold"))
label_status.pack(pady=5)

label_time = tk.Label(root, text="Time: --:--:--")
label_time.pack()

# Khung chứa nút Start và Stop nằm ngang
frame_btns = tk.Frame(root)
frame_btns.pack(pady=10)
btn_start = tk.Button(frame_btns, text="Start", command=start, width=10, bg="#90EE90", font=("Arial", 10, "bold"))
btn_start.grid(row=0, column=0, padx=5)
btn_stop = tk.Button(frame_btns, text="Stop", command=stop, width=10, bg="#FFB6C1", font=("Arial", 10, "bold"))
btn_stop.grid(row=0, column=1, padx=5)

tk.Button(root, text="Show Live Graph", command=show_graph, width=25, bg="#ADD8E6").pack(pady=5)
btn_scan = tk.Button(root, text="Scan Quick LAN (1-10)", command=scan_lan, width=25, bg="#FFFACD")
btn_scan.pack(pady=5)

result_text = tk.Text(root, height=10, width=35)
result_text.pack(pady=10)

root.mainloop()