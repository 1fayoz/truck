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


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4()}.{ext}"
    if instance.type == Uploader.TypeChoices.IMAGE:
        return os.path.join('uploads/images/', filename)
    return os.path.join('uploads/videos/', filename)