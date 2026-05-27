## 1. Dependencies And Configuration

- [x] 1.1 Add `Pillow` and `django-imagekit` to `requirements.txt`.
- [x] 1.2 Add `imagekit` to `INSTALLED_APPS`.
- [x] 1.3 Add configurable image upload limits and allowed formats to settings.
- [x] 1.4 Confirm media settings and development media URL routing work for uploaded files.

## 2. Data Model And Migrations

- [x] 2.1 Add nullable/blank avatar image field to `User` with a stable upload path.
- [x] 2.2 Add nullable/blank product image field to `ProductInfo` with a stable upload path.
- [x] 2.3 Generate migration for the new image fields.
- [x] 2.4 Ensure the migration file is tracked despite the repository migration ignore pattern.

## 3. Image Specs And Validation

- [x] 3.1 Define `django-imagekit` specs for avatar thumbnails at `64x64` and `128x128`.
- [x] 3.2 Define `django-imagekit` specs for product thumbnails at `160x160`, `320x320`, and `800x800`.
- [x] 3.3 Implement shared upload validation for image format and maximum file size.
- [x] 3.4 Apply validation to avatar and product image upload paths.

## 4. API Integration

- [x] 4.1 Update `UserSerializer` to accept avatar upload and expose avatar original/thumbnail URLs.
- [x] 4.2 Update product offer serialization to accept product image upload where authorized and expose original/thumbnail URLs.
- [x] 4.3 Ensure anonymous users cannot upload avatars.
- [x] 4.4 Ensure product image upload is restricted to the owning shop user.
- [x] 4.5 Ensure missing or pending thumbnails do not cause API serialization errors.

## 5. Asynchronous Processing

- [x] 5.1 Add Celery task to generate avatar thumbnails for a saved user image.
- [x] 5.2 Add Celery task to generate product thumbnails for a saved product image.
- [x] 5.3 Dispatch the avatar thumbnail task after successful avatar save.
- [x] 5.4 Dispatch the product thumbnail task after successful product image save.
- [x] 5.5 Add retries/logging for thumbnail generation failures.

## 6. Cleanup And Admin

- [x] 6.1 Remove old source/generated files when avatar or product images are replaced where practical.
- [x] 6.2 Add image fields or previews to relevant admin configuration if admin classes exist for these models.

## 7. Verification

- [x] 7.1 Add or update tests for avatar upload success, authentication failure, validation failure, and thumbnail URL exposure.
- [x] 7.2 Add or update tests for product image upload success, ownership failure, validation failure, and thumbnail URL exposure.
- [x] 7.3 Add or update tests for thumbnail task generation behavior.
- [x] 7.4 Run `python3 manage.py check`.
- [x] 7.5 Run `python3 manage.py test backend`.
