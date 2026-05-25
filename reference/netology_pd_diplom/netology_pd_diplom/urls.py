"""netology_pd_diplom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Импортируем admin из baton.autodiscover
from baton.autodiscover import admin

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from backend import views

urlpatterns = [
    path('', views.index, name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('baton/', include('baton.urls'), name='baton'),
    path('api/v1/', include('backend.urls', namespace='backend')),
    path('__debug__/', include("debug_toolbar.urls")),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), # Swagger UI (интерактивная документация)
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), # ReDoc (альтернативный интерфейс документации)
    path('schema', SpectacularAPIView.as_view(), name='schema'),  # Схема OpenAPI в формате YAML
    path('social-oauth/', include('social_django.urls', namespace='social')),  # Авторизация через социальные сети

] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обслуживание медиа-файлов в разработке
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.site.site_header = "Панель администрирования"

admin.site.index_title = "Администрирование базы данных"