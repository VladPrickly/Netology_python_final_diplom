# backend/tests/test_throttling.py
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

User = get_user_model()


class AuthThrottlingTestCase(APITestCase):
    """
    Тесты троттлинга для эндпоинтов аутентификации.
    """

    def setUp(self):
        # self.client = APIClient()
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
                'anon': '3/minute', # 3 попытки входа в минуту для тестов
            }
        }
    )
    def test_register_account_throttling(self):
        """
        Тест: регистрация ограничена для анонимных пользователей. После 3 попыток должен вернуться 429.
        """
        url = '/api/v1/user/register'

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

        if isinstance(response.data, dict):
            self.assertTrue(
                'retry_after' in response.data or 'detail' in response.data,
                "Ответ 429 должен содержать информацию о повторной попытке"
            )


    @override_settings(
        REST_FRAMEWORK={
            'DEFAULT_THROTTLE_CLASSES': [
                'rest_framework.throttling.AnonRateThrottle',
            ],
            'DEFAULT_THROTTLE_RATES': {
                'anon': '3/minute',  # 3 попыток входа в минуту для тестов
            }
        }
    )
    def test_login_account_throttling(self):
        """
        Тест: вход ограничен для защиты от brute-force.
        """
        url = '/api/v1/user/login'

        # Создаём тестового пользователя для корректной проверки
        user, _ = User.objects.get_or_create(
            username='testuser',
            email='test@example.com',
            password='correct_password',
            type='buyer',
        )

        # Первые 3 попыток входа должны пройти
        for i in range(3):
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
        Авторизованный пользователь не ограничен лимитом.
        """
        user = User.objects.create_user(
            username='auth_user',
            email='auth@example.com',
            password='pass123',
            type='buyer'
        )
        self.client.force_authenticate(user=user)

        # Делаем 20 запросов (больше лимита anon)
        for i in range(20):
            response = self.client.get('/api/v1/products')
            self.assertNotEqual(
                response.status_code,
                status.HTTP_429_TOO_MANY_REQUESTS,
                f"Авторизованный пользователь не должен быть ограничен"
            )