# tests/test_caching_2.py

from django.core.cache import cache
from backend.models import Category
import time

cache.clear()

# Первый запрос — выполняется к БД
start = time.time()
cats = list(Category.objects.all())
print(f"1st query: {time.time() - start:.3f}s")

# Второй запрос — из кэша
start = time.time()
cats = list(Category.objects.all())
print(f"2nd query: {time.time() - start:.3f}s")
