import gzip
import io
import os
import random
from datetime import datetime
from datetime import timedelta

import requests
from django.core.cache import cache
from django.core.validators import RegexValidator
from django.utils import timezone

from core.settings.base import SMS_TOKEN_URL, SMS_EMAIL, SMS_PASSWORD, SMS_SEND_URL


def compress_in_memory(data):
    compressed_stream = io.BytesIO()
    with gzip.GzipFile(fileobj=compressed_stream, mode='wb') as f_out:
        f_out.write(data)
    return compressed_stream.getvalue()


def dump_pg_data(project_name, db_name, db_user, db_password, db_host, db_port, chat_id, bot_token):
    try:
        command = f'PGPASSWORD={db_password} pg_dump -U {db_user} -h {db_host} -p {db_port} {db_name}'
        dump_data = os.popen(command).read().encode()

        if not dump_data:
            raise Exception("Database dump failed or empty.")

        compressed_data = compress_in_memory(dump_data)

        return send_to_telegram(compressed_data, project_name, chat_id, bot_token)
    except Exception as e:
        return False, f'Error: {e}'


def send_to_telegram(compressed_data, project_name: str, chat_id, bot_token):
    now = datetime.now()
    caption = (
        f'Proyekt: {project_name}\n'
        f'📂 **Yangi ma\'lumotlar bazasi dump fayli** \n'
        f'🕒 **Yaratilgan vaqt:** {now.strftime("%d/%m/%Y %H:%M:%S")}\n'
        f'#{project_name}\n'
    )
    files = {
        'document': ('dump.sql.gz', io.BytesIO(compressed_data), 'application/gzip')
    }
    data = {'chat_id': chat_id, 'caption': caption, 'parse_mode': 'Markdown'}

    res = requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendDocument',
        data=data,
        files=files
    )
    if res.status_code != 200:
        return False, f'text: {res.text}, status_code: {res.status_code}'
    return True, 'success'


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
