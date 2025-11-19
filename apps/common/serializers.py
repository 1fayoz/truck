from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.common.jwt import make_custom_jwt
from apps.common.models import User, Service, Docs, News, Application, Employee, UserVerificationCode
from apps.common.utils import get_code, send_sms

VERIFICATION_MSG = "Kodni hech kimga bermang! O'zbekiston yuk tashuvchilar uyushmasi platformasiga kirish uchun tasdiqlash kodi: {code}"

class UserSerializer(serializers.ModelSerializer):
    country_display = serializers.CharField(source="get_country_display", read_only=True)

    class Meta:
        model = User
        fields = "__all__"

    @staticmethod
    def validate_phone(value):
        value = value.strip()
        if not value:
            raise ValidationError("Telefon raqami majburiy.")
        return value

    def create(self, validated_data):
        phone = self.validated_data["phone"].strip()

        user, created = User.objects.get_or_create(
            phone=phone,
            defaults=validated_data,
        )

        # ver, _ = UserVerificationCode.objects.get_or_create(user=user)
        # ver.code = get_code()
        # ver.save(update_fields=["code"])
        # send_sms(VERIFICATION_MSG.format(code=ver.code), phone)
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['country'] = instance.get_country_display()
        representation['access'] = instance.token
        return representation


class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=100)
    code = serializers.CharField(max_length=10)

    def validate(self, attrs):
        phone = attrs.get("phone", "").strip()
        code = attrs.get("code", "").strip()
        if not phone or not code:
            raise ValidationError("Telefon va kod majburiy.")
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise ValidationError({"phone": "Foydalanuvchi topilmadi."})

        try:
            ver = user.verification
        except UserVerificationCode.DoesNotExist:
            raise ValidationError({"code": "Kod xato yoki qaytadan yuboring"})

        if ver.code != code:
            raise ValidationError({"code": "Kod noto‘g‘ri."})

        if timezone.now() > ver.expires_at:
            raise ValidationError({"code": "Kodning muddati o‘tgan."})

        attrs["user"] = user
        attrs["verification"] = ver
        return attrs

    def create(self, validated_data):
        user = self.validated_data["user"]
        ver = self.validated_data["verification"]
        ver.delete()
        token = make_custom_jwt(user.id)

        return {
            "access": str(token),
        }



class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class DocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docs
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class UserStats(serializers.Serializer):
    driver_count = serializers.IntegerField(default=0)
    person_count = serializers.IntegerField(default=0)
    other_count = serializers.IntegerField(default=0)

