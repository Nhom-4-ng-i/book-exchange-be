from typing import Optional
from app.core.config import get_settings

# 1. Kiểm tra import thư viện
try:
    import cloudinary
    import cloudinary.uploader
except ImportError:
    cloudinary = None
    print("WARNING: Thư viện 'cloudinary' chưa được cài đặt. Hãy chạy: pip install cloudinary")

def upload_image_to_cloudinary(file_obj) -> Optional[str]:
    settings = get_settings()

    # Nếu thư viện chưa cài thì dừng luôn
    if cloudinary is None:
        print("Error: Cloudinary library not found.")
        return None

    # 2. Cấu hình Cloudinary (Thêm log lỗi nếu thiếu config)
    try:
        # Kiểm tra xem các biến môi trường có giá trị không
        if not getattr(settings, 'CLOUDINARY_CLOUD_NAME', None):
            print("Error: Missing CLOUDINARY_CLOUD_NAME in .env")
            return None

        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )
    except Exception as e:
        print(f"Cloudinary config error: {e}")
        return None

    # 3. Đọc nội dung file và Upload
    try:
        content = None
        
        # Trường hợp 1: UploadFile từ FastAPI (có thuộc tính .file)
        if hasattr(file_obj, 'file'):
            # QUAN TRỌNG: Đưa con trỏ về đầu file trước khi đọc
            file_obj.file.seek(0)
            content = file_obj.file.read()
            
        # Trường hợp 2: File-like object thông thường
        elif hasattr(file_obj, 'read'):
            if hasattr(file_obj, 'seek'):
                file_obj.seek(0)
            content = file_obj.read()
            
        # Trường hợp 3: Dữ liệu dạng bytes
        elif isinstance(file_obj, bytes):
            content = file_obj
            
        else:
            print("Error: Invalid file object type for upload")
            return None
        
        # Thực hiện upload
        if not content:
            print("Error: File content is empty")
            return None

        result = cloudinary.uploader.upload(content)
        return result.get('secure_url') or result.get('url')
        
    except Exception as e:
        # In lỗi chi tiết ra terminal để bạn debug
        print(f"Cloudinary upload Exception: {e}")
        return None