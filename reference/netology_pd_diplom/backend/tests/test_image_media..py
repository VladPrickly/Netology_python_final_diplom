import shutil
import tempfile
from io import BytesIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework.test import APITestCase

from backend.models import Category, Product, ProductInfo, Shop
from backend.tasks import generate_avatar_thumbnails, generate_product_thumbnails


User = get_user_model()
TEST_MEDIA_ROOT = tempfile.mkdtemp()


def make_image(name='image.jpg', size=(32, 32), image_format='JPEG'):
    image = BytesIO()
    Image.new('RGB', size, color='red').save(image, format=image_format)
    image.seek(0)
    return SimpleUploadedFile(name, image.read(), content_type=f'image/{image_format.lower()}')


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT, IMAGE_UPLOAD_MAX_SIZE=1024 * 1024)
class ImageMediaTestCase(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user = User.objects.create_user(
            email='buyer@example.com',
            username='buyer',
            password='password',
            type='buyer',
            is_active=True,
        )
        self.shop_user = User.objects.create_user(
            email='shop@example.com',
            username='shop',
            password='password',
            type='shop',
            is_active=True,
        )
        self.other_shop_user = User.objects.create_user(
            email='other-shop@example.com',
            username='other-shop',
            password='password',
            type='shop',
            is_active=True,
        )
        self.shop = Shop.objects.create(name='Shop', user=self.shop_user)
        self.other_shop = Shop.objects.create(name='Other shop', user=self.other_shop_user)
        self.category = Category.objects.create(name='Category')
        self.product = Product.objects.create(name='Product', category=self.category)
        self.product_info = ProductInfo.objects.create(
            product=self.product,
            shop=self.shop,
            external_id=1,
            model='Model',
            quantity=10,
            price=100,
            price_rrc=120,
        )

    @patch('backend.views.generate_avatar_thumbnails.delay')
    def test_avatar_upload_success_and_urls(self, delay_mock):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/v1/user/details', {'avatar': make_image('avatar.jpg')}, format='multipart')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Status'], True)
        self.user.refresh_from_db()
        self.assertTrue(self.user.avatar)
        delay_mock.assert_called_once_with(self.user.id)

        details_response = self.client.get('/api/v1/user/details')
        self.assertEqual(details_response.status_code, 200)
        self.assertIn('avatar_url', details_response.data)
        self.assertEqual(set(details_response.data['avatar_thumbnails']), {'64x64', '128x128'})

    def test_anonymous_user_cannot_upload_avatar(self):
        response = self.client.post('/api/v1/user/details', {'avatar': make_image('avatar.jpg')}, format='multipart')

        self.assertEqual(response.status_code, 403)

    def test_avatar_upload_validation_failure(self):
        self.client.force_authenticate(user=self.user)
        upload = SimpleUploadedFile('avatar.txt', b'not an image', content_type='text/plain')

        response = self.client.post('/api/v1/user/details', {'avatar': upload}, format='multipart')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Status'], False)
        self.assertIn('avatar', response.json()['Errors'])

    @patch('backend.views.generate_product_thumbnails.delay')
    def test_product_image_upload_success_and_urls(self, delay_mock):
        self.client.force_authenticate(user=self.shop_user)

        response = self.client.post(
            '/api/v1/products',
            {'id': self.product_info.id, 'image': make_image('product.jpg')},
            format='multipart',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Status'], True)
        self.product_info.refresh_from_db()
        self.assertTrue(self.product_info.image)
        delay_mock.assert_called_once_with(self.product_info.id)

        list_response = self.client.get('/api/v1/products')
        self.assertEqual(list_response.status_code, 200)
        self.assertIn('image_url', list_response.data[0])
        self.assertEqual(set(list_response.data[0]['image_thumbnails']), {'160x160', '320x320', '800x800'})

    def test_product_image_upload_requires_owner_shop(self):
        self.client.force_authenticate(user=self.other_shop_user)

        response = self.client.post(
            '/api/v1/products',
            {'id': self.product_info.id, 'image': make_image('product.jpg')},
            format='multipart',
        )

        self.assertEqual(response.status_code, 403)

    def test_product_image_upload_validation_failure(self):
        self.client.force_authenticate(user=self.shop_user)
        upload = SimpleUploadedFile('product.txt', b'not an image', content_type='text/plain')

        response = self.client.post('/api/v1/products', {'id': self.product_info.id, 'image': upload}, format='multipart')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Status'], False)
        self.assertIn('image', response.json()['Errors'])

    @patch('backend.tasks.generate_thumbnails')
    def test_avatar_thumbnail_task_generates_variants(self, generate_mock):
        self.user.avatar.save('avatar.jpg', make_image('avatar.jpg'), save=True)

        generate_avatar_thumbnails(self.user.id)

        generate_mock.assert_called_once()

    @patch('backend.tasks.generate_thumbnails')
    def test_product_thumbnail_task_generates_variants(self, generate_mock):
        self.product_info.image.save('product.jpg', make_image('product.jpg'), save=True)

        generate_product_thumbnails(self.product_info.id)

        generate_mock.assert_called_once()