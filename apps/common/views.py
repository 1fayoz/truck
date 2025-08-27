import jwt
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from jwt import ExpiredSignatureError, InvalidSignatureError, ImmatureSignatureError, InvalidAlgorithmError, \
    DecodeError, InvalidTokenError
from rest_framework.exceptions import NotAuthenticated, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response

from apps.common import serializers
from apps.common.models import User, Service, Docs, News, Application, Employee
from apps.common.pagination import UserPagination
from core.settings import base


class UserLogin(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('full_name', 'phone')
    filterset_fields = ('is_active', 'type')
    pagination_class = UserPagination

class VerifyLoginCodeView(GenericAPIView):
    serializer_class = serializers.VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.save()
        return Response(data, status=200)


class ServiceView(ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = serializers.ServiceSerializer

class DocsView(ListCreateAPIView):
    queryset = Docs.objects.all()
    serializer_class = serializers.DocsSerializer

class NewsListView(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = serializers.NewsSerializer

class ApplicationListView(ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = serializers.ApplicationSerializer

class EmployeeCreateList(ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer


class MeFromSubView(RetrieveAPIView):
    serializer_class = serializers.UserSerializer

    def get_bearer_token(self):
        auth_header = self.request.headers.get("Authorization") or ""
        if not auth_header.startswith("Bearer "):
            raise NotAuthenticated("Authorization header topilmadi yoki noto‘g‘ri.")
        return auth_header.split(" ", 1)[1].strip()

    def get_object(self):
        token = self.get_bearer_token()

        try:
            unverified_header = jwt.get_unverified_header(token)
        except DecodeError:
            raise ValidationError("Token formati noto‘g‘ri (header o‘qilmadi).")

        expected_alg = getattr(base, "JWT_ALG", "HS256")
        if unverified_header.get("alg") != expected_alg:
            raise ValidationError(
                f"Token algoritmi mos emas: {unverified_header.get('alg')} ≠ {expected_alg}"
            )

        try:
            payload = jwt.decode(
                token,
                getattr(base, "JWT_SECRET"),
                algorithms=[expected_alg],
                options={"require": ["exp", "sub"]},
                leeway=10,
            )
        except ExpiredSignatureError:
            raise ValidationError("Token muddati tugagan.")
        except InvalidSignatureError:
            raise ValidationError("Imzo noto‘g‘ri (secret mos emas).")
        except ImmatureSignatureError:
            raise ValidationError("Token hali kuchga kirmagan (nbf/iat muammosi).")
        except InvalidAlgorithmError:
            raise ValidationError("Algoritm ruxsat etilmagan.")
        except DecodeError:
            raise ValidationError("Tokenni o‘qib bo‘lmadi (format/base64).")
        except InvalidTokenError as e:
            raise ValidationError(f"Token noto‘g‘ri: {str(e) or 'sababsiz'}")

        sub = payload.get("sub")
        if sub is None:
            raise ValidationError("Tokenda 'sub' claim yo‘q.")

        return get_object_or_404(User, pk=sub)

class NewsDetailView(RetrieveAPIView):
    serializer_class = serializers.UserStats

    def get_object(self):
        stats = User.objects.aggregate(
            driver_count=Count('id', filter=Q(type=1)),
            person_count=Count('id', filter=Q(type=2)),
            other_count=Count('id', filter=Q(type=3)),
        )
        return stats
