from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView

from apps.common import serializers
from apps.common.models import User, Service, Docs


class UserLogin(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('is_active',)


class ServiceView(ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = serializers.ServiceSerializer

class DocsView(ListCreateAPIView):
    queryset = Docs.objects.all()
    serializer_class = serializers.DocsSerializer


