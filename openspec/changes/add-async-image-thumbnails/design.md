## Context

The project is a Django 5.2 API with a custom `backend.User` model, product catalog models, DRF serializers, token authentication, and Celery already used for email and partner import background work. Media settings and development media routing already exist, but image fields, validation, thumbnail specs, and asynchronous thumbnail generation are not implemented.

`django-imagekit` is the preferred image processing library for this change because it keeps Django's standard `ImageField` as the persisted field, provides simple generated image specs, has a current PyPI release, and can be driven from Celery tasks. This avoids replacing model fields with a library-specific field abstraction and keeps migrations straightforward.

## Goals / Non-Goals

**Goals:**
- Store user avatar uploads and product image uploads.
- Validate image uploads for supported formats and size limits.
- Generate predefined thumbnail variants asynchronously after image changes.
- Expose original and thumbnail URLs in API responses.
- Reuse the existing Celery worker path for background processing.

**Non-Goals:**
- Build a full image gallery, multiple images per product, or drag-and-drop media manager.
- Add external object storage or CDN integration.
- Add image editing features such as manual cropping, filters, watermarks, or focal-point selection.
- Backfill images from partner YAML imports unless image URLs are later added to the import contract.

## Decisions

1. Use `django-imagekit` with Django `ImageField` sources.
   - Rationale: It is simple, widely adopted, and lets the project keep ordinary model fields while defining generated thumbnail specs in Python.
   - Alternatives considered: `easy-thumbnails` is mature but less explicit for model-level variants; `django-versatileimagefield` has a convenient rendition API but is more opinionated and less aligned with the current Django version in its public docs.

2. Add `avatar` to `User` and `image` to `ProductInfo`.
   - Rationale: Avatar is naturally user-owned. Product images in this marketplace are likely shop-offer-specific because `ProductInfo` already represents a shop's concrete catalog item with external ID, model, price, and quantity.
   - Alternative considered: Add image to `Product`, but that would force all shops sharing a product name/category to share one image.

3. Trigger thumbnail generation from Celery after successful upload/update.
   - Rationale: Product owner explicitly requested asynchronous processing. It also prevents request latency spikes when large images are uploaded.
   - Alternative considered: rely only on lazy generation when thumbnail URLs are first accessed; this is simpler but shifts processing cost to the first API/browser consumer.

4. Expose thumbnail URLs as read-only serializer fields.
   - Rationale: Clients need stable URLs for fast loading, but should only upload the source image. Generated variants are implementation outputs.

5. Keep image variant set small and fixed for the first release.
   - Rationale: A few standard sizes cover common API needs and avoid uncontrolled media growth.
   - Proposed variants: avatars `64x64` and `128x128`; products `160x160`, `320x320`, and `800x800`.

## Risks / Trade-offs

- [Risk] Generated files may be missing if Celery is unavailable. → Mitigation: task should be retryable, and serializers should tolerate absent thumbnails without failing the whole response.
- [Risk] Media storage can grow over time as source images and thumbnails are replaced. → Mitigation: delete old source/generated files when images are replaced or records are deleted where practical.
- [Risk] Image validation gaps can allow oversized or unsupported uploads. → Mitigation: validate extension/content type and enforce a conservative file-size limit before saving.
- [Risk] New model fields require migrations, but migrations are currently ignored by `.gitignore`. → Mitigation: explicitly create and track the migration file for this change.
- [Risk] If product images later need multiple images per product, a single `ProductInfo.image` field may be insufficient. → Mitigation: this release covers the current single-primary-image requirement; a gallery model can be added later without breaking existing primary image behavior.

## Migration Plan

1. Add dependencies and app configuration.
2. Add nullable/blank image fields to avoid breaking existing users and products.
3. Generate and commit migrations explicitly.
4. Add serializers, validation, thumbnail specs, and Celery tasks.
5. Deploy with media volume persistence and a running Celery worker.
6. Rollback by removing API exposure and stopping thumbnail task dispatch; database fields can remain nullable until a follow-up cleanup migration.

## Open Questions

- Exact maximum upload size should be finalized; use 5 MB as the initial default unless product requirements say otherwise.
- Product image upload ownership rules should be enforced consistently with existing partner/shop permissions during implementation.
