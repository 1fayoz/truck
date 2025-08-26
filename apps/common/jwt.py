import jwt, time
from django.conf import settings

def make_custom_jwt(profile_id: int):
    now = int(time.time())
    payload = {
        "sub": str(profile_id),
        "iat": now,
        "exp": now + settings.JWT_EXPIRE_MIN,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)