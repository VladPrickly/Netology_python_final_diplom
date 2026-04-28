import logging
import yaml
import requests
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from celery import shared_task
from django.db import transaction
from django.http import JsonResponse

from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, User

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_confirm(user_id: int, subject: str, body: str, **kwargs):
    """
    Отправка письма на почту клиента
    """

    user = User.objects.get(id=user_id)
    recipient_list = [user.email,]

    try:
        msg = EmailMultiAlternatives(subject=subject, body=body, from_email=settings.EMAIL_HOST_USER, to=recipient_list)
        msg.send()
        logger.info(f"Email отправлен: {recipient_list}")
        return {'status': 'success', 'recipients': len(recipient_list)}

    except Exception as e:
        logger.error(f"Ошибка отправки email: {e}")


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def do_import(shop: int, user_id: int, url: str, data):
    """
    Асинхронный импорт товаров из YAML по ссылке.

    Выполняет полную синхронизацию прайс-листа:
    - создаёт/обновляет категории
    - удаляет старые товары магазина
    - загружает новые товары и параметры

    Args:
        shop: ID магазина (для привязки товаров)
        user_id: ID пользователя-владельца
        url: Ссылка на YAML-файл прайс-листа
    """

    for category in data['categories']:
        category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
        category_object.shops.add(shop.id)
        category_object.save()
    ProductInfo.objects.filter(shop_id=shop.id).delete()
    for item in data['goods']:
        product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

        product_info = ProductInfo.objects.create(product_id=product.id,
                                                  external_id=item['id'],
                                                  model=item['model'],
                                                  price=item['price'],
                                                  price_rrc=item['price_rrc'],
                                                  quantity=item['quantity'],
                                                  shop_id=shop.id)
        for name, value in item['parameters'].items():
            parameter_object, _ = Parameter.objects.get_or_create(name=name)
            ProductParameter.objects.create(product_info_id=product_info.id,
                                            parameter_id=parameter_object.id,
                                            value=value)

    logger.info(f"Импорт завершён: магазин {shop.name}, товаров: {len(data.get('goods', []))}")
    return JsonResponse({'Status': True})