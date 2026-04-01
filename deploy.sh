#!/bin/bash

# =================================================================
# SCRIPT TRIỂN KHAI NHANH (ONE-CLICK DEPLOY)
# Dự án: Python Network Monitoring Tool
# =================================================================

# 1. Cấu hình thông tin (Đã khớp với tài khoản của anh)
IMAGE_NAME="deflauthuman/network-monitor:latest"
RESOURCE_GROUP="pynetmon-rg"
CONTAINER_NAME="python-monitor-container"
STORAGE_ACCOUNT="pynetmonstorage999"
LOCATION="malaysiawest"

# Tự động nạp mã khóa từ file .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "❌ LỖI: Không tìm thấy file .env bí mật!"
  exit 1
fi

echo "🚀 BẮT ĐẦU QUÁ TRÌNH TRIỂN KHAI TỰ ĐỘNG..."

# 2. Build image chuẩn AMD64 cho Azure
echo "📦 Đang đóng gói ứng dụng (Build Docker)..."
docker build --platform linux/amd64 -t $IMAGE_NAME .

# 3. Đẩy lên Docker Hub
echo "☁️ Đang đẩy bản mới lên mạng (Push Docker)..."
docker push $IMAGE_NAME

# 4. Xóa bản cũ trên Azure (để nạp bản mới)
echo "🗑️ Đang dọn dẹp container cũ trên Azure..."
az container delete --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --yes

# 5. Khởi chạy bản mới nhất
echo "⚡ Đang kích hoạt máy chủ mới trên Azure (Malaysia West)..."
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $CONTAINER_NAME \
  --image $IMAGE_NAME \
  --cpu 1 \
  --memory 1 \
  --location $LOCATION \
  --os-type Linux \
  --azure-file-volume-account-name $STORAGE_ACCOUNT \
  --azure-file-volume-account-key $STORAGE_KEY \
  --azure-file-volume-share-name csvreports \
  --azure-file-volume-mount-path /app/reports \
  --environment-variables PYTHONUNBUFFERED=1 \
  --restart-policy Always

echo "✅ HOÀN TẤT! Hệ thống đã được cập nhật bản mới nhất."
echo "🌐 Anh có thể vào Azure Portal để xem Log và Báo cáo."
