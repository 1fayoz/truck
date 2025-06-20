import os
from uuid import uuid4
import requests

from apps.common import models


def get_translation(obj, attr, request):
    if request:
        language = request.headers.get(
            'Accept-Language', 'uz').split("-")[0][:2]
    else:
        language = 'uz'
    return getattr(obj, f"{attr}_{language}", None)


def get_language(request):
    if request:
        return request.headers.get('Accept-Language', 'uz').split("-")[0][:2]
    return 'uz'


ERROR_MESSAGES = {
    'too_many_metrics': {
        'uz': "Faqat ikkita 'metric' yuborishingiz mumkin (before va after).",
        'ru': "Вы можете отправить только два объекта 'metric' (before и after).",
        'en': "Only two 'metric' objects are allowed (before and after).",
    },
    'duplicate_type': {
        'uz': "'{type}' turi ikki marta takrorlandi.",
        'ru': "Тип '{type}' был повторён дважды.",
        'en': "The '{type}' type was duplicated.",
    }
}

messages = {
    'uz': {
        'attendee_required': "Ism va telefon raqami va boshqalar ishtirokchilar uchun majburiy.",
        'member_expert_required': "Ism, telefon raqami va kompaniya a'zolar va ekspertlar uchun majburiy.",
        'expert_revenue': "Ekspert uchun yillik daromad kamida $1,000,000 bo'lishi kerak."
    },
    'en': {
        'attendee_required': "Full name and phone and others are required for attendees.",
        'member_expert_required': "Full name, phone, and company are required for members and experts.",
        'expert_revenue': "Annual revenue must be at least $1,000,000 for experts."
    },
    'ru': {
        'attendee_required': "Имя и номер телефона обязательны для участников.",
        'member_expert_required': "Имя, номер телефона и компания обязательны для членов и экспертов.",
        'expert_revenue': "Годовой доход для эксперта должен быть не менее $1,000,000."
    }
}


def send_telegram_message(token: str, chat_id: str, message: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    return response


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4()}.{ext}"
    if instance.type == models.Uploader.TypeChoices.IMAGE:
        return os.path.join('uploads/images/', filename)
    return os.path.join('uploads/videos/', filename)
