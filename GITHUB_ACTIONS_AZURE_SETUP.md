# Cẩm nang Thiết lập Chìa khóa tự động hóa (GitHub Actions x Azure)

Kịch bản Deploy (`.github/workflows/azure-deploy.yml`) đã được em viết hoàn chỉnh nhưng để kịch bản này chạy trên Github của anh, anh cần thao tác 5 phút cực dễ sau đây.

## Mở đường cho GitHub sang Azure:
Mặc định Github và Azure là 2 nền tảng "xa lạ", anh phải tạo 1 thẻ công vụ tên là **Service Principal** trên Azure thì Github mới truy cập được:

### BƯỚC 1: Dán 1 Lệnh duy nhất để lấy thẻ từ Azure Cloud Shell
Anh đăng nhập [Azure Cloud Shell (portal.azure.com)](https://shell.azure.com/) rồi Paste lệnh này vào:
```bash
# Tự thiết lập thẻ công vụ lấy mã đăng nhập
az ad sp create-for-rbac --name "PythonDeployerBot" \
                         --role contributor \
                         --scopes /subscriptions/$(az account show --query id --output tsv) \
                         --sdk-auth
```

Kết quả nó sẽ in ra màn hình một cục Code dạng JSON (có clientId, clientSecret, subscriptionId, tenantId).
Anh **Bôi Đen và Copy** đoạn JSON này lại.

---

### BƯỚC 2: Nhập "Chìa khóa" vào cài đặt của GitHub
1. Vào Repo Github chứa Mini-NMS của anh.
2. Ấn vào Tab **Settings**, nhìn cột cúp bên trái, chọn kéo xuống nhón chuột vào: **Secrets and variables** -> **Actions**
3. Bấm nháy nút xanh lá: **New repository secret**
4. Anh Add tên biến đúng y chang như dưới đây:
   - **Tên (Name)**: `AZURE_CREDENTIALS`
   - **Nội dung (Value)**: *(Cứ rà chuột dán nguyên cái cụm JSON anh vừa Copy ở BƯỚC 1 vào)*
   Mở Settings, click **Add secret**.

---

### BƯỚC 3: Thêm các Biến của Ổ Cứng Mây (Azure Storage Accounts)
Nếu anh muốn gắn USB Ảo bảo tồn File CSV (như phương án 3 đợt trước em bảo nắn thêm file Storage), thì anh tạo thêm 2 Secrets (Chìa khóa Repository thứ 2 và 3) tương tự BƯỚC 2:

- Khóa số 2:
   - Name: `AZURE_STORAGE_ACCOUNT`
   - Value: `pynetmonstorage999` *(Tên tài khoản storage lúc anh tạo Azure Cũ)*
- Khóa số 3:
   - Name: `AZURE_STORAGE_KEY` 
   - Value: *(Điền cái Key Password anh lấy trong menu Storage -> Access Keys ở giao diện Portal)*

> ⚠️ LƯU Ý LỚN: Anh có thể đổi tên Resource ở file `./github/workflows/azure-deploy.yml` tự động sao cho trùng với cấu hình tên của anh trên Azure trước (Ví dụ: tên Azure Container Registry (ACR), tên Resource Group) nhé!
 
---

## Chúc Mừng 🎊 
Chỉ cần hoàn thiện 3 bước khóa móc, anh có thể sửa 1 chữ ở source gốc `monitor.py` và Push thử lên `main` Github -> Chạy đà ngay qua tab "Actions" trên Repo Github để thưởng lãm công sức của tụi nó! 🚀
