
def get_translation(obj, attr, request):
    if request:
        language = request.headers.get(
            'Accept-Language', 'uz').split("-")[0][:2]
    else:
        language = 'uz'
    return getattr(obj, f"{attr}_{language}", None)
