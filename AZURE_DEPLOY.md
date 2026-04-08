# Triển khai Python Network Monitor lên Azure (ACI)

Tài liệu này hướng dẫn anh từng bước đưa ứng dụng Python (mini-NMS) lên hệ thống đám mây Azure sao cho script có thể theo dõi 24/7 và hoàn toàn "serverless".

> ⚠️ Cần phải cài đặt công cụ **Azure CLI** (`az`) trên máy tính để thực thi các lệnh phía dưới, hoặc anh có thể mở **Azure Cloud Shell** trực tiếp trên www.portal.azure.com.

---

## 1. Đăng nhập vào Azure
Mở terminal và gõ:
```bash
az login
```
*Trình duyệt sẽ mở ra yêu cầu anh điền email và mật khẩu Azure. Sau khi thành công, terminal sẽ liên kết với tài khoản của anh.*

---

## 2. Tạo Không gian tài nguyên (Resource Group)
Resource Group là thư mục chứa mọi phần cứng/dịch vụ của dự án này. Đặt ở khu vực Singapore (Đông Nam Á) để tốc độ ping qua VN nhanh:

```bash
az group create --name "network-monitor-rg" --location "southeastasia"
```

---

## 3. Upload Image lên Azure Container Registry (ACR)
Tạo kho bí mật chứa mã nguồn (giống DockerHub nhưng riêng tư đắt đỏ của Azure):
```bash
# Thay đổi đuôi random999 thành một cụm tuỳ ý (vì tên này phải là ĐỘC NHẤT trên toàn thế giới Azure)
az acr create --resource-group network-monitor-rg \
              --name pythontoolregistry999 \
              --sku Basic
```

Sau khi kho chứa được tạo, mình sẽ biên dịch Docker từ máy tính và đẩy (push) lên kho Azure:
```bash
# Lưu ý đứng ở thư mục đang chứa file Dockerfile
az acr build --registry pythontoolregistry999 --image network-monitor:latest .
```

---

## 4. Thiết lập File Share (Tránh mất file Log & Báo Cáo)
Vì container sẽ tắt bật hoặc di dời ảo trên Azure, mình phải tạo một ổ đĩa USB ảo (Azure Files) thì các file `.csv` mới được bảo toàn vĩnh viễn.

```bash
# Tạo Storage Account để cắm USB ảo
az storage account create --resource-group network-monitor-rg \
                          --name pynetmonstorage999 \
                          --location southeastasia \
                          --sku Standard_LRS

# Tạo thư mục con csvreports bên trong Storage đó
az storage share create --name csvreports \
                        --account-name pynetmonstorage999
```
*Lưu ý: Lệnh sau đó có thể cần anh Export biến môi trường (Connection String). Mình lấy trong Azure Portal ở mục Storage account -> Access keys sẽ dễ nhất.*

---

## 5. Dựng Máy Chủ Monitor Chạy 24/7 (Deploy Container)
Sau khi setup xong, 1 dòng lệnh duy nhất để kick-start toàn bộ dự án:

```bash
az container create \
  --resource-group network-monitor-rg \
  --name python-monitor-container \
  --image pythontoolregistry999.azurecr.io/network-monitor:latest \
  --assign-identity \
  --azure-file-volume-account-name pynetmonstorage999 \
  --azure-file-volume-account-key "<ĐIỀN PASSWORD ACCESS KEY TỪ BƯỚC 4 VÀO ĐÂY>" \
  --azure-file-volume-share-name csvreports \
  --azure-file-volume-mount-path /app/reports \
  --os-type Linux
```

**Thế là xong!** Tool Mini-NMS của anh hiện đã trở thành một *Thực thể Đám Mây Mông Lung*. 
Từ bây giờ, cứ mỗi 60 giây, cỗ máy ảo này của Azure sẽ tự động quét trạng thái các host, ghi file logs, và nhét file báo cáo `.csv` siêu giá trị vào trong thư mục Storage Account an toàn của anh. Khỏi cần lo lắng sập máy tính sập nguồn gì hết á nha!
