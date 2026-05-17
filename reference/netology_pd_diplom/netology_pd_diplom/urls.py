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
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from backend import views

urlpatterns = [
    path('', views.index, name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('api/v1/', include('backend.urls', namespace='backend')),
    path("__debug__/", include("debug_toolbar.urls")),

    # Схема OpenAPI в формате YAML
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI (интерактивная документация)
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ReDoc (альтернативный интерфейс документации)
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

admin.site.site_header = "Панель администрирования"

admin.site.index_title = "Администрирование базы данных"