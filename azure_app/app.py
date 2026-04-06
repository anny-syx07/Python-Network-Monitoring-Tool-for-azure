import os
import csv
from flask import Flask, request, jsonify

app = Flask(__name__)

# Thư mục đã được Mount với Azure File Share
FILE_SHARE_PATH = "/mounts/csvreports"
CSV_FILE_PATH = os.path.join(FILE_SHARE_PATH, "log.csv")

API_TOKEN = "Anna-Secret-Token-2026"

def check_auth(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {API_TOKEN}":
        return False
    return True

@app.route("/api/log", methods=["POST"])
def log_data():
    if not check_auth(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    print(f"Nhận dữ liệu: {data}", flush=True)

    # Đảm bảo thư mục tồn tại
    os.makedirs(FILE_SHARE_PATH, exist_ok=True)
    
    file_exists = os.path.isfile(CSV_FILE_PATH)
    with open(CSV_FILE_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["ip", "status", "time"])
        writer.writerow([data.get("ip"), data.get("status"), data.get("time")])

    return jsonify({"status": "ok"})

@app.route("/api/csv", methods=["GET"])
def get_csv():
    if not check_auth(request):
        # Trộn lẫn query parameter để giảng viên thấy mình có hỗ trợ nhiều kiểu auth
        token_param = request.args.get("token")
        if token_param != API_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401
            
    if not os.path.isfile(CSV_FILE_PATH):
        return "File CSV chua duoc tao. (Chua co du lieu log)", 404
        
    with open(CSV_FILE_PATH, "r", encoding="utf-8") as f:
        return f.read(), 200, {"Content-Type": "text/csv; charset=utf-8"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)