### 🔧 Exchange Old Books — Backend

## Giới thiệu
Đây là mã nguồn backend cho hệ thống Exchange Old Books, được xây dựng bằng FastAPI.

## Cấu trúc thư mục
```
app/
├─ core/
│  └─ config.py         # Cấu hình ứng dụng, đọc biến môi trường (.env)
├─ models/              # Khai báo các bảng (ORM models)
├─ crud/                # Thao tác dữ liệu với DB (CRUD logic)
├─ schemas/             # Định nghĩa cấu trúc dữ liệu vào/ra API
├─ api/                 # Định nghĩa các route (endpoint HTTP)
│  ├─ routes/           
│  └─ router.py         
├─ services/            # Tích hợp các dịch vụ ngoài (AI, Supabase Storage, ...)
├─ utils/               # Các hàm hỗ trợ
└─ main.py              # Chạy ứng dụng
README.md
.env
requirements.txt
```

## Yêu cầu hệ thống
- Python 3.13

## Cài đặt
### Cài các thư viện cần thiết
```powershell
pip install -r requirements.txt
```

### Cấu hình file .env
Tạo file .env tương tự như .env.example

### Chạy ứng dụng

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

