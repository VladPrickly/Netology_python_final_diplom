from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill


class AvatarThumbnail64(ImageSpec):
    processors = [ResizeToFill(64, 64)]
    format = 'JPEG'
    options = {'quality': 85}


class AvatarThumbnail128(ImageSpec):
    processors = [ResizeToFill(128, 128)]
    format = 'JPEG'
    options = {'quality': 85}


class ProductThumbnail160(ImageSpec):
    processors = [ResizeToFill(160, 160)]
    format = 'JPEG'
    options = {'quality': 85}


class ProductThumbnail320(ImageSpec):
    processors = [ResizeToFill(320, 320)]
    format = 'JPEG'
    options = {'quality': 85}


class ProductThumbnail800(ImageSpec):
    processors = [ResizeToFill(800, 800)]
    format = 'JPEG'
    options = {'quality': 85}


AVATAR_THUMBNAIL_SPECS = {
    '64x64': 'backend:avatar_thumbnail_64',
    '128x128': 'backend:avatar_thumbnail_128',
}
PRODUCT_THUMBNAIL_SPECS = {
    '160x160': 'backend:product_thumbnail_160',
    '320x320': 'backend:product_thumbnail_320',
    '800x800': 'backend:product_thumbnail_800',
}

register.generator('backend:avatar_thumbnail_64', AvatarThumbnail64)
register.generator('backend:avatar_thumbnail_128', AvatarThumbnail128)
register.generator('backend:product_thumbnail_160', ProductThumbnail160)
register.generator('backend:product_thumbnail_320', ProductThumbnail320)
register.generator('backend:product_thumbnail_800', ProductThumbnail800)