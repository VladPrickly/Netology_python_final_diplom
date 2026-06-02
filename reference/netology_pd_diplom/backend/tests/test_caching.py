# tests/test_caching.py

from django.test import TestCase
from django.core.cache import cache
from backend.models import Category


class CachalotTest(TestCase):
    def test_category_query_cached(self):
        # Первый запрос — выполняется к БД
        list(Category.objects.all())

        # Второй запрос — из кэша
        with self.assertNumQueries(0):
            list(Category.objects.all())


