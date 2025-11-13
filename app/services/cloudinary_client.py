from typing import Optional
from app.core.config import get_settings

try:
    import cloudinary
    import cloudinary.uploader
except Exception:
    cloudinary = None


def upload_image_to_cloudinary(file_obj) -> Optional[str]:

    settings = get_settings()
    # if cloudinary is None:
    #     return None

    # configure
    try:
        # try CLOUDINARY_URL or individual vars
        cloudinary.config(
            cloud_name=getattr(settings, 'CLOUDINARY_CLOUD_NAME', None),
            api_key=getattr(settings, 'CLOUDINARY_API_KEY', None),
            api_secret=getattr(settings, 'CLOUDINARY_API_SECRET', None),
            secure=True,
        )
    except Exception:
        pass

    # read
    try:
        if hasattr(file_obj, 'read'):
            content = file_obj.read()
        elif isinstance(file_obj, bytes):
            content = file_obj
        else:
            return None
    except Exception:
        return None

    try:
        result = cloudinary.uploader.upload(content)
        return result.get('secure_url') or result.get('url')
    except Exception:
        return None
