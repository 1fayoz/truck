import random
from datetime import timedelta

import requests
from django.core.cache import cache
from django.core.validators import RegexValidator
from django.utils import timezone

from core.settings.base import SMS_TOKEN_URL, SMS_EMAIL, SMS_PASSWORD, SMS_SEND_URL


def sms_access_token():
    payload = {
        'email': SMS_EMAIL,
        'password': SMS_PASSWORD,
    }

    response = requests.post(
        SMS_TOKEN_URL,
        data=payload,
    )
    if response.status_code == 200:
        data = response.json()
        return data['data']['token']
    else:
        return None


def send_sms(message: str, phone: str):
    if not (token := cache.get('sms_sender_token')):
        token = sms_access_token()
        cache.set('sms_sender_token', token, timeout=int(29.5 * 24 * 60 * 60))

    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'mobile_phone': phone,
        'message': message,
        'from': 'Lorry.uz'
    }

    response = requests.post(
        SMS_SEND_URL,
        data=payload,
        headers=headers,
    )
    if response.status_code == 200:
        return response.json()
    else:
        return None


def two_minutes_from_now():
    return timezone.now() + timedelta(minutes=2)


def get_code(length: int = 4) -> str:
    return f"{random.randint(10 ** (length - 1), 10 ** length - 1)}"


digits_only_validator = RegexValidator(r"^\d+$", "Faqat raqam kiriting.")
uz_phone_validator = RegexValidator(
    r"^(\+?998|998)?\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}$",
    "Telefon raqamini +998 ** ** ** ** ko'rinishida kiriting.",
)

passport_validator = RegexValidator(
    r"^[A-Z]{2}\d{7}$",
    "Pasport seriya va raqami (masalan, AA1234567) ko'rinishida bo'lishi kerak.",
)
inn_validator = RegexValidator(r"^\d{9,12}$", "STIR/INN 9–12 xonali bo'lishi kerak.")
