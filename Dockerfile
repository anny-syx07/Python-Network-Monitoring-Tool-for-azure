# Sử dụng phiên bản Python siêu nhẹ 
FROM python:3.10-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Cài đặt công cụ ping (iputils-ping) do bản slim-linux mặc định không có
RUN apt-get update && \
    apt-get install -y iputils-ping && \
    rm -rf /var/lib/apt/lists/*
    
# Copy toàn bộ file dự án vào /app của Docker
COPY . /app/

# Khởi tạo thư mục logs và reports để script không bị lỗi permission vặt
RUN mkdir -p /app/logs /app/reports

# (Tuỳ chọn) Cài thêm package (hiện tại mình dùng toàn standard lib nên requirements rỗng)
# RUN pip install --no-cache-dir -r requirements.txt

# Khởi chạy script Python khi Docker nổ máy
# (Lệnh này sẽ quét danh sách host 60 giây 1 lần và chạy liên tục 24/7)
CMD ["python", "monitor.py", "--file", "hosts.txt", "--interval", "60"]
