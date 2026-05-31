# baton/autodiscover.py
from django.apps import apps
from importlib import import_module
from django.utils.module_loading import module_has_submodule


def autodiscover():
    """
    Автоматически находит и импортирует конфигурационные файлы
    для django-baton во всех установленных приложениях.

    Ищет модули: menus.py, dashboards.py, filters.py, config.py
    """
    for app_config in apps.get_app_configs():
        # Пропускаем системные приложения Django
        if app_config.name.startswith('django.'):
            continue

        # Список модулей, которые может использовать baton
        baton_modules = ('menus', 'dashboards', 'filters', 'config', 'baton')

        for module_name in baton_modules:
            if module_has_submodule(app_config.module, module_name):
                try:
                    import_module(f'{app_config.name}.{module_name}')
                except ImportError as e:
                    # Логируем ошибку, но не прерываем запуск
                    print(f"Warning: Could not import {app_config.name}.{module_name}: {e}")