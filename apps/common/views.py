from rest_framework import viewsets

from apps.common import models
from apps.common import serializers


class BannerViewSet(viewsets.ModelViewSet):
    queryset = models.Banner.objects.filter(is_active=True, type='home')
    serializer_class = serializers.BannerSerializer
    http_method_names = ['get', 'post', 'patch']


