from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, views, generics
from rest_framework.response import Response

from apps.common import models
from apps.common import serializers


class BannerViewSet(viewsets.ModelViewSet):
    queryset = models.Banner.objects.filter(is_active=True, type='home')
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.BannerSerializerCreate
        return serializers.BannerSerializer


class ClubOfferViewSet(viewsets.ModelViewSet):
    queryset = models.ClubOffer.objects.filter(is_active=True)
    serializer_class = serializers.ClubOfferSerializer
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.ClubOfferSerializerCreate
        return serializers.ClubOfferSerializer


class ClubStatisticsAPIView(views.APIView):

    @staticmethod
    def get(request):
        serializer = serializers.ClubStatisticsSerializer(instance={})
        return Response(serializer.data)


class IndustryDistributionAPIView(views.APIView):

    @staticmethod
    def get(request):
        data = serializers.IndustryDistributionSerializer.get_distribution(request)
        return Response(data)


class ExclusiveVideosListAPIView(viewsets.ModelViewSet):
    queryset = models.VideoAndAudio.objects.filter(is_active=True, type='exclusive')
    serializer_class = serializers.ExclusiveVideosSerializer
    http_method_names = ['get', 'post', 'patch']


class PartnersModelViewSet(viewsets.ModelViewSet):
    queryset = models.Partners.objects.filter(is_active=True)
    serializer_class = serializers.PartnersSerializer
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.PartnersSerializerCreate
        return serializers.PartnersSerializer


class FAQViewSet(viewsets.ModelViewSet):
    queryset = models.FAQ.objects.filter(is_active=True)
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.FAQSerializerCreate
        return serializers.FAQSerializer


class ClubMemberListAPIView(generics.ListCreateAPIView):
    queryset = models.ClubMember.objects.filter(is_active=True, type='member')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.ClubMemberSerializerCreate
        return serializers.ClubMemberSerializer


class ClubMemberDetailRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ClubMember.objects.filter(is_active=True, type='member')
    serializer_class = serializers.ClubMemberDetailSerializer


class TravelListAPIView(generics.ListCreateAPIView):
    queryset = models.Travel.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.TravelSerializer
        return serializers.TravelSerializer
