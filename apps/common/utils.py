import os
from uuid import uuid4
import requests
from django.apps import apps
from django.db.models import Q

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


SEARCHABLE_FIELDS = {
    'Industry': {
        'text': ['name_uz', 'name_en', 'name_ru'],
        'numeric': [],
    },
    'Company': {
        'text': ['name_uz', 'name_en', 'name_ru'],
        'numeric': [],
    },
    'ClubMember': {
        'text': ['name_uz', 'name_en', 'name_ru', 'bio_uz', 'bio_en', 'bio_ru', 'position_uz', 'position_en',
                 'position_ru'],
        'numeric': ['age', 'experience'],
    },
    'Autobiography': {
        'text': ['description_uz', 'description_en', 'description_ru', 'year'],
        'numeric': ['order'],
    },
    'SocialLink': {
        'text': ['name_uz', 'name_en', 'name_ru', 'url'],
        'numeric': [],
    },
    'Metric': {
        'text': ['title_uz', 'title_en', 'title_ru'],
        'numeric': ['revenue', 'employee_count', 'project_count'],
    },
    'ClubOffer': {
        'text': ['title_uz', 'title_en', 'title_ru', 'description_uz', 'description_en', 'description_ru'],
        'numeric': [],
    },
    'Banner': {
        'text': ['title_uz', 'title_en', 'title_ru', 'description_uz', 'description_en', 'description_ru'],
        'numeric': [],
    },
    'Speaker': {
        'text': ['name_uz', 'name_en', 'name_ru', 'bio_uz', 'bio_en', 'bio_ru'],
        'numeric': [],
    },
    'VideoAndAudio': {
        'text': ['title_uz', 'title_en', 'title_ru', 'description_uz', 'description_en', 'description_ru', 'duration'],
        'numeric': ['view_count'],
    },
    'TravelCountry': {
        'text': ['name_uz', 'name_en', 'name_ru'],
        'numeric': [],
    },
    'Travel': {
        'text': ['description_uz', 'description_en', 'description_ru', 'short_description_uz', 'short_description_en',
                 'short_description_ru'],
        'numeric': ['view_count'],
    },
    'Tag': {
        'text': ['name'],
        'numeric': [],
    },
    'News': {
        'text': ['title_uz', 'title_en', 'title_ru', 'description_uz', 'description_en', 'description_ru',
                 'short_description_uz', 'short_description_en', 'short_description_ru'],
        'numeric': ['view_count'],
    },
    'Images': {
        'text': [],
        'numeric': [],
    },
    'BusinessCourse': {
        'text': ['title_uz', 'title_en', 'title_ru', 'description_uz', 'description_en', 'description_ru'],
        'numeric': ['view_count'],
    },
    'CourseInfo': {
        'text': ['title_uz', 'title_en', 'title_ru', 'description_uz', 'description_en', 'description_ru'],
        'numeric': ['module_number'],
    },
    'NationalValue': {
        'text': ['title_uz', 'title_en', 'title_ru', 'description_uz', 'description_en', 'description_ru'],
        'numeric': [],
    },
    'Events': {
        'text': ['title_uz', 'title_en', 'title_ru', 'description_uz', 'description_en', 'description_ru',
                 'location_uz', 'location_en', 'location_ru', 'duration'],
        'numeric': [],
    },
    'EventAgenda': {
        'text': ['title_uz', 'title_en', 'title_ru', 'description_uz', 'description_en', 'description_ru', 'time'],
        'numeric': ['order'],
    },
    'Gallery': {
        'text': ['title_uz', 'title_en', 'title_ru', 'description_uz', 'description_en', 'description_ru'],
        'numeric': ['view_count'],
    },
    'Partners': {
        'text': ['name_uz', 'name_en', 'name_ru'],
        'numeric': [],
    },
    'FAQ': {
        'text': ['question_uz', 'question_en', 'question_ru', 'answer_uz', 'answer_en', 'answer_ru'],
        'numeric': [],
    },
}

MODEL_SECTION_MAPPING = {
    'Travel': 'travel',
    'BusinessCourse': 'business_course',
    'News': 'news',
    'ClubMember': 'club_member',
    'Events': 'events',
    'VideoAndAudio': 'podcasts',
    'Gallery': 'gallery',
}


def search_across_models(query):
    results = []
    query = str(query).strip()

    for model_name, fields in SEARCHABLE_FIELDS.items():
        model = apps.get_model(app_label='common', model_name=model_name)
        text_fields = fields['text']
        numeric_fields = fields['numeric']

        text_q = Q()
        for field in text_fields:
            text_q |= Q(**{f'{field}__icontains': query})

        numeric_q = Q()
        if query.isdigit():
            for field in numeric_fields:
                numeric_q |= Q(**{field: int(query)})

        combined_q = text_q | numeric_q

        if combined_q:
            queryset = model.objects.filter(combined_q, is_active=True)
            for obj in queryset:
                matched_fields = []
                for field in text_fields:
                    value = getattr(obj, field, None)
                    if value and query.lower() in str(value).lower():
                        matched_fields.append({'field': field, 'value': value})
                for field in numeric_fields:
                    value = getattr(obj, field, None)
                    if query.isdigit() and value == int(query):
                        matched_fields.append({'field': field, 'value': value})

                if matched_fields:
                    section = MODEL_SECTION_MAPPING.get(model_name, 'other')
                    results.append({
                        'section': section,
                        'model': model_name,
                        'object_id': obj.id,
                        'matched_fields': matched_fields,
                    })

    return results


t_errors = {
    'uz': {
        'degree': 'bu daraja bilan azo mavjud',
    },
    'ru': {
        'degree': 'bu daraja bilan azo mavjud',
    },
    'en': {
        'degree': 'bu daraja bilan azo mavjud'
    }
}


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
