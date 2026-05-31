# backend/validators.py

from django.conf import settings
from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError


def validate_image_upload(image):
    if image.size > settings.IMAGE_UPLOAD_MAX_SIZE:
        raise ValidationError(f'Image size must not exceed {settings.IMAGE_UPLOAD_MAX_SIZE} bytes.')

    try:
        image.seek(0)
        opened_image = Image.open(image)
        opened_image.verify()
        image_format = opened_image.format
        image.seek(0)
    except (UnidentifiedImageError, OSError) as exc:
        raise ValidationError('Upload a valid image file.') from exc

    if image_format and image_format.upper() not in settings.IMAGE_UPLOAD_ALLOWED_FORMATS:
        raise ValidationError('Unsupported image format.')