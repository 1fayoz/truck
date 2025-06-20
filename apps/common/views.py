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
    queryset = models.ClubMember.objects.filter(is_active=True, type__in=['member', 'expert'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.ClubMemberSerializerCreate
        return serializers.ClubMemberSerializer


class ClubMemberDetailRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.ClubMember.objects.filter(is_active=True, type='member')
    serializer_class = serializers.ClubMemberDetailSerializer


class TravelListAPIView(generics.ListCreateAPIView):
    queryset = models.Travel.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.TravelSerializerCreate
        return serializers.TravelSerializer


class MembersSpeechListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.VideoAndAudio.objects.filter(is_active=True, type='member_speech')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.MembersSpeechSerializerCreate
        return serializers.MembersSpeechSerializer


class NewsListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.News.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.NewsSerializerCreate
        return serializers.NewsSerializer


class NewsRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.News.objects.filter(is_active=True)
    serializer_class = serializers.NewsSerializerDetail


class BusinessCourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.BusinessCourse.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.BusinessCourseSerializer
        return serializers.BusinessCourseSerializer


class BusinessCourseRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.BusinessCourse.objects.filter(is_active=True)
    serializer_class = serializers.BusinessCourseSerializerDetail


class ClubPresidentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.ClubMember.objects.filter(is_active=True, degree='president')
    serializer_class = serializers.ClubPresidentDetailSerializer


class EventListAPIView(generics.ListCreateAPIView):
    queryset = models.Events.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'date']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.EventSerializer
        return serializers.EventSerializer


class EventRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.Events.objects.filter(is_active=True)
    serializer_class = serializers.EventDetailSerializer


class PodcastListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.VideoAndAudio.objects.filter(is_active=True, type__in=['video_podcast', 'audio_podcast'])
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.PodcastSerializer
        return serializers.PodcastSerializer


class PodcastRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.VideoAndAudio.objects.filter(is_active=True, type__in=['video_podcast', 'audio_podcast'])
    serializer_class = serializers.PodcastDetailSerializer


class GalleryListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Gallery.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.GallerySerializer
        return serializers.GallerySerializer


class GalleryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.Gallery.objects.filter(is_active=True, type='picture')
    serializer_class = serializers.GalleryDetailSerializer


class NationalValueListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.NationalValue.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.NationalValueSerializer
        return serializers.NationalValueSerializer


class FileUploadView(views.APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = serializers.UploaderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            return Response(serializers.UploaderSerializer(instance, context={'request': request}).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
