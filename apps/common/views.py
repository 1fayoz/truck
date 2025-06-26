from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, views, generics, status
from rest_framework.response import Response

from apps.common import models, utils
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
    queryset = models.ClubMember.objects.filter(is_active=True, type__in=['member', 'expert']).exclude(
        degree__in=['president', 'director', 'assistant_director'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.ClubMemberSerializerCreate
        return serializers.ClubMemberSerializer


class ClubMemberDetailRetrieveAPIView(generics.RetrieveUpdateAPIView):
    queryset = models.ClubMember.objects.filter(is_active=True, type='member')
    serializer_class = serializers.ClubMemberDetailSerializer

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return serializers.ClubMemberSerializerCreate
        return serializers.ClubMemberDetailSerializer


class TravelListAPIView(generics.ListCreateAPIView):
    queryset = models.Travel.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.TravelSerializerCreate
        return serializers.TravelSerializer


class TravelRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.Travel.objects.filter(is_active=True)
    serializer_class = serializers.TravelSerializerDetail

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        ip = utils.get_client_ip(request)
        key = f"travel_view:{instance.id}:{ip}"

        if not cache.get(key):
            cache.set(key, True, timeout=86400)
            instance.view_count += 1
            instance.save(update_fields=["view_count"])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        ip = utils.get_client_ip(request)
        key = f"news_view:{instance.id}:{ip}"

        if not cache.get(key):
            cache.set(key, True, timeout=86400)
            instance.view_count += 1
            instance.save(update_fields=["view_count"])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BusinessCourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.BusinessCourse.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.BusinessCourseCreateSerializer
        return serializers.BusinessCourseSerializer


class BusinessCourseRetrieveAPIView(generics.RetrieveUpdateAPIView):
    queryset = models.BusinessCourse.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return serializers.BusinessCourseCreateSerializer
        return serializers.BusinessCourseSerializerDetail

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        ip = utils.get_client_ip(request)
        key = f"course_view:{instance.id}:{ip}"

        if not cache.get(key):
            cache.set(key, True, timeout=86400)
            instance.view_count += 1
            instance.save(update_fields=["view_count"])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ClubPresidentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.ClubMember.objects.filter(is_active=True, degree='president')
    serializer_class = serializers.ClubPresidentDetailSerializer


class EventListAPIView(generics.ListCreateAPIView):
    queryset = models.Events.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'date']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.EventSerializerCreate
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        ip = utils.get_client_ip(request)
        key = f"podcast_view:{instance.id}:{ip}"

        if not cache.get(key):
            cache.set(key, True, timeout=86400)
            instance.view_count += 1
            instance.save(update_fields=["view_count"])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        ip = utils.get_client_ip(request)
        key = f"gallery_view:{instance.id}:{ip}"

        if not cache.get(key):
            cache.set(key, True, timeout=86400)
            instance.view_count += 1
            instance.save(update_fields=["view_count"])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class NationalValueListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.NationalValue.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.NationalValueSerializer
        return serializers.NationalValueSerializer


class FileUploadView(generics.CreateAPIView):
    queryset = models.Uploader.objects.filter(is_active=True)
    serializer_class = serializers.UploaderSerializer


class ContactFormView(generics.CreateAPIView):
    serializer_class = serializers.ContactFormSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"{serializer.validated_data['type']} form submitted successfully"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenericChoiceViewSet(viewsets.ModelViewSet):
    queryset = models.GenericChoice.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.GenericChoiceSerializerCreate
        elif self.request.method == 'PATCH':
            return serializers.GenericChoiceSerializerCreate
        return serializers.GenericChoiceSerializer


class TravelCountryViewSet(viewsets.ModelViewSet):
    queryset = models.TravelCountry.objects.filter(is_active=True)
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.TravelCountrySerializerCreate
        elif self.request.method == 'PATCH':
            return serializers.TravelCountrySerializerCreate
        return serializers.TravelCountrySerializer


class IndustryViewSet(viewsets.ModelViewSet):
    queryset = models.Industry.objects.filter(is_active=True)
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.IndustrySerializerCreate
        elif self.request.method == 'PATCH':
            return serializers.IndustrySerializerCreate
        return serializers.IndustrySerializer


class SpeakerViewSet(viewsets.ModelViewSet):
    queryset = models.Speaker.objects.filter(is_active=True)
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.SpeakerSerializerCreate
        elif self.request.method == 'PATCH':
            return serializers.SpeakerSerializerCreate
        return serializers.SpeakerSerializer


class SearchAPIView(views.APIView):

    @staticmethod
    def get(request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter "q" is required'}, status=status.HTTP_400_BAD_REQUEST)

        results = utils.search_across_models(query)
        return Response({
            'query': query,
            'results': results,
            'count': len(results),
        }, status=status.HTTP_200_OK)


class ClubPresidentListApiView(generics.ListAPIView):
    queryset = models.ClubMember.objects.filter(is_active=True, degree='president')
    serializer_class = serializers.ClubPresidentListSerializer


class HomeStatIconsViewSet(viewsets.ModelViewSet):
    queryset = models.HomeStatIcons.objects.all()
    serializer_class = serializers.HomeStatIconsSerializer
    http_method_names = ['get', 'post', 'patch']

    def create(self, request, *args, **kwargs):
        icon = models.HomeStatIcons.objects.exists()
        if icon:
            lang = utils.get_language(request)
            return Response(
                {'error': utils.t_errors[lang]['icon']},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)
