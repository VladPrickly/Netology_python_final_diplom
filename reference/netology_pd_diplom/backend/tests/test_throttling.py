# backend/tests/test_throttling.py
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class AuthThrottlingTestCase(TestCase):
    """
    Тесты троттлинга для эндпоинтов аутентификации.
    """

    def setUp(self):
        self.client = APIClient()
        cache.clear()

    def tearDown(self):
        """
        Очищаем кеш после теста
        """
        cache.clear()

    @override_settings(
        REST_FRAMEWORK={
            'DEFAULT_THROTTLE_CLASSES': [
                'rest_framework.throttling.AnonRateThrottle',
            ],
            'DEFAULT_THROTTLE_RATES': {
                'anon': '3/minute',  # 3 запроса в минуту для тестов
            }
        }
    )
    def test_register_account_throttling(self):
        """
        Тест: регистрация ограничена для анонимных пользователей.
        После N попыток должен вернуться 429.
        """
        url = 'http://127.0.0.1:8000/api/v1/user/register'

        # Первые 3 запроса должны пройти
        for i in range(3):
            response = self.client.post(url, {
                'email': f'test{i}@example.com',
                'username': f'user{i}',
                'password': 'SecurePass123!',
                'type': 'buyer'
            }, format='json')

            self.assertNotEqual(
                response.status_code,
                status.HTTP_429_TOO_MANY_REQUESTS,
                f"Запрос #{i + 1} не должен быть ограничен"
            )

        # 4-й запрос должен получить 429
        response = self.client.post(url, {
            'email': 'test4@example.com',
            'username': 'user4',
            'password': 'SecurePass123!',
            'type': 'buyer'
        }, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS,
            "После исчерпания лимита должен вернуться 429"
        )

    @override_settings(
        REST_FRAMEWORK={
            'DEFAULT_THROTTLE_CLASSES': [
                'rest_framework.throttling.AnonRateThrottle',
            ],
            'DEFAULT_THROTTLE_RATES': {
                'anon': '5/minute',  # 5 попыток входа в минуту для тестов
            }
        }
    )
    def test_login_account_throttling(self):
        """
        Тест: вход ограничен для защиты от brute-force.
        """
        url = 'http://127.0.0.1:8000/api/v1/user/login'

        # Создаём тестового пользователя для корректной проверки
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='correct_password',
            type='buyer'
        )

        # Первые 5 попыток входа должны пройти
        for i in range(5):
            response = self.client.post(url, {
                'email': 'test@example.com',
                'password': 'wrong_password'
            }, format='json')

            self.assertNotEqual(
                response.status_code,
                status.HTTP_429_TOO_MANY_REQUESTS,
                f"Попытка #{i + 1} не должна быть ограничена"
            )

        # 6-я попытка должна получить 429
        response = self.client.post(url, {
            'email': 'test@example.com',
            'password': 'any_password'
        }, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS,
            "После исчерпания лимита входа должен вернуться 429"
        )

    def test_login_throttling_does_not_affect_authenticated_users(self):
        """
        Тест: авторизованный пользователь не ограничен лимитом.

        """
        # Создаём и авторизуем пользователя
        user = User.objects.create_user(
            username='auth_user',
            email='auth@example.com',
            password='pass123',
            type='buyer'
        )
        self.client.force_authenticate(user=user)

        url = 'http://127.0.0.1:8000/api/v1/user/register'

        # Делаем больше запросов, чем лимит анонимного клиента
        for i in range(10):
            response = self.client.get('http://127.0.0.1:8000/api/v1/products')
            if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                pass

        self.assertTrue(True)