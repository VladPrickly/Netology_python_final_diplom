## Why

User avatars and product images are a practical requirement for the shop API, and product images can quickly become a visible source of page-load and API response latency. Generating predictable thumbnail variants asynchronously keeps uploads responsive while making image delivery faster for common listing/detail use cases.

## What Changes

- Add image upload support for user avatars.
- Add image upload support for product images.
- Generate predefined thumbnail variants for avatars and product images in the background.
- Expose original image and thumbnail URLs through the API where user and product data are serialized.
- Validate uploaded images for supported formats and reasonable size limits.
- Use `django-imagekit` for image specs and the existing Celery infrastructure for asynchronous generation.

## Capabilities

### New Capabilities
- `image-media`: Uploading user/product images, validating them, exposing URLs, and asynchronously generating thumbnail variants.

### Modified Capabilities

## Impact

- Models: `User` and product-related models gain image fields.
- Serializers/views: relevant API responses and update endpoints handle image upload and thumbnail URLs.
- Tasks: Celery gains background thumbnail generation jobs.
- Dependencies: add `Pillow` and `django-imagekit`.
- Configuration: media settings and local development media routing may need to be configured.
- Database: model field additions require migrations.
