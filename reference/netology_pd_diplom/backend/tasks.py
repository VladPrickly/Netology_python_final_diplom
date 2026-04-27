import logging
import yaml
import requests
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from celery import shared_task
from django.db import transaction
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, User

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_registration(user_id: int, **kwargs):
    """
    Отправка письма на почту при регистрации пользователя
    """

    user = User.objects.get(id=user_id)
    subject = 'Подтверждение регистрации'
    recipient_list = [user.email, ]
    body = f'Регистрация прошла успешно. Ваш логин: {user.username}'
    try:
        msg = EmailMultiAlternatives(subject=subject, body=body, from_email=settings.EMAIL_HOST_USER, to=recipient_list)
        msg.send()
        logger.info(f"Email отправлен: {recipient_list}")
        return {'status': 'success', 'recipients': len(recipient_list)}

    except Exception as e:
        logger.error(f"Ошибка отправки email: {e}")
