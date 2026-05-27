## ADDED Requirements

### Requirement: User avatar upload
The system SHALL allow an authenticated user to upload, replace, and retrieve a single avatar image for their account.

#### Scenario: Authenticated user uploads avatar
- **WHEN** an authenticated user submits a supported image file as their avatar
- **THEN** the system stores the image on the user's account and returns a successful response

#### Scenario: Anonymous user uploads avatar
- **WHEN** an anonymous user submits an avatar image
- **THEN** the system rejects the request with an authentication error

### Requirement: Product image upload
The system SHALL allow an authorized shop user to upload, replace, and retrieve a single primary image for a product offer.

#### Scenario: Shop user uploads product image
- **WHEN** an authenticated shop user submits a supported image file for one of their product offers
- **THEN** the system stores the image on that product offer and returns a successful response

#### Scenario: User uploads image for another shop's product offer
- **WHEN** an authenticated user submits a product image for a product offer they do not own
- **THEN** the system rejects the request with a permission error

### Requirement: Image validation
The system SHALL validate uploaded avatar and product images before saving them.

#### Scenario: Unsupported image upload
- **WHEN** a user submits a file that is not a supported image format
- **THEN** the system rejects the upload with validation errors and does not save the file

#### Scenario: Oversized image upload
- **WHEN** a user submits an image larger than the configured maximum upload size
- **THEN** the system rejects the upload with validation errors and does not save the file

### Requirement: Asynchronous thumbnail generation
The system SHALL enqueue background thumbnail generation after a user avatar or product image is successfully saved.

#### Scenario: Avatar thumbnail task is queued
- **WHEN** a user avatar image is saved successfully
- **THEN** the system queues a background task to generate all configured avatar thumbnail variants

#### Scenario: Product thumbnail task is queued
- **WHEN** a product image is saved successfully
- **THEN** the system queues a background task to generate all configured product thumbnail variants

### Requirement: Thumbnail URL exposure
The system SHALL expose original image URLs and configured thumbnail URLs in relevant API responses.

#### Scenario: Account details include avatar URLs
- **WHEN** an authenticated user retrieves their account details
- **THEN** the response includes the original avatar URL and available avatar thumbnail URLs

#### Scenario: Product listing includes image URLs
- **WHEN** a client retrieves product offer data
- **THEN** the response includes the original product image URL and available product thumbnail URLs

### Requirement: Missing thumbnail tolerance
The system SHALL keep API responses available while thumbnail generation is pending or failed.

#### Scenario: Thumbnail not generated yet
- **WHEN** an API response includes an image whose thumbnail file has not been generated yet
- **THEN** the system returns the response without a server error and represents the missing thumbnail predictably
