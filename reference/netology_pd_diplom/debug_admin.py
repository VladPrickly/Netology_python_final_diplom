#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netology_pd_diplom.settings')
django.setup()

print("🔍 Диагностика админ-панели")
print("=" * 50)

# 1. Проверка настроек
from django.conf import settings
print(f"\n📦 DEBUG: {settings.DEBUG}")
print(f"🔗 STATIC_URL: {settings.STATIC_URL}")
print(f"📁 MEDIA_URL: {settings.MEDIA_URL}")

# 2. Проверка AUTH_USER_MODEL
print(f"\n👤 AUTH_USER_MODEL: {getattr(settings, 'AUTH_USER_MODEL', 'Default User')}")

# 3. Проверка INSTALLED_APPS
apps = settings.INSTALLED_APPS
print(f"\n📋 Baton в INSTALLED_APPS: {'baton' in apps}")
print(f"📋 baton.autodiscover в INSTALLED_APPS: {'baton.autodiscover' in apps}")
if 'baton' in apps and 'django.contrib.admin' in apps:
    baton_idx = apps.index('baton')
    admin_idx = apps.index('django.contrib.admin')
    print(f"⚠️  Порядок: baton({'до' if baton_idx < admin_idx else 'ПОСЛЕ'}) django.contrib.admin")

# 4. Проверка URL
from django.urls import get_resolver
resolver = get_resolver()
admin_patterns = [str(p.pattern) for p in resolver.url_patterns if 'admin' in str(p.pattern).lower()]
print(f"\n🔗 Admin URL patterns: {admin_patterns}")

# 5. Проверка моделей в админке
from django.contrib import admin
registered = list(admin.site._registry.keys())
print(f"\n📊 Зарегистрировано моделей в админке: {len(registered)}")
if registered:
    print(f"   Примеры: {[m.__name__ for m in registered[:5]]}")

# 6. Проверка суперпользователя
from django.contrib.auth import get_user_model
User = get_user_model()
superusers = User.objects.filter(is_superuser=True)
print(f"\n🔑 Суперпользователи: {superusers.count()}")
for u in superusers:
    print(f"   - {u.username}: is_staff={u.is_staff}, is_active={u.is_active}")

print("\n" + "=" * 50)
print("✅ Диагностика завершена")