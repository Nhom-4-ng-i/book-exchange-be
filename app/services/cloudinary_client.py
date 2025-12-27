from typing import Optional
from app.core.config import get_settings

try:
    import cloudinary
    import cloudinary.uploader
except Exception:
    cloudinary = None

def upload_image_to_cloudinary(file_obj) -> Optional[str]:
    settings = get_settings()

    # 1. Config Cloudinary
    try:
        cloudinary.config(
            cloud_name=getattr(settings, 'CLOUDINARY_CLOUD_NAME', None),
            api_key=getattr(settings, 'CLOUDINARY_API_KEY', None),
            api_secret=getattr(settings, 'CLOUDINARY_API_SECRET', None),
            secure=True,
        )
    except Exception:
        pass

    # 2. Đọc nội dung file từ UploadFile của FastAPI
    try:
        content = None
        # Nếu là đối tượng UploadFile (có thuộc tính .file là SpooledTemporaryFile)
        if hasattr(file_obj, 'file'):
            content = file_obj.file.read()
        # Nếu là file-like object thông thường
        elif hasattr(file_obj, 'read'):
            content = file_obj.read()
        else:
            return None
        
        # 3. Upload lên Cloudinary
        # Cloudinary tự động nhận diện binary stream
        result = cloudinary.uploader.upload(content)
        return result.get('secure_url') or result.get('url')
        
    except Exception as e:
        print(f"Cloudinary upload error: {e}")
        return None