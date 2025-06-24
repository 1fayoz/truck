from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.common import views

router = DefaultRouter()
router.register(r'banner', views.BannerViewSet, basename='banner')
router.register(r'club/offers', views.ClubOfferViewSet, basename='club-offer')
router.register('exclusive-video', views.ExclusiveVideosListAPIView, basename='exclusive-video')
router.register('partner', views.PartnersModelViewSet, basename='partner')
router.register('faq', views.FAQViewSet, basename='faq')
router.register('form/choice', views.GenericChoiceViewSet, basename='form-choice')
router.register('country', views.TravelCountryViewSet, basename='country')
router.register('industry', views.IndustryViewSet, basename='industry')
router.register('speaker', views.SpeakerViewSet, basename='speaker')

urlpatterns = [
    path('club/stats/', views.ClubStatisticsAPIView.as_view()),
    path('industry-distribution/', views.IndustryDistributionAPIView.as_view()),

    path('club/members/', views.ClubMemberListAPIView.as_view()),
    path('club/members/<int:pk>/', views.ClubMemberDetailRetrieveAPIView.as_view()),

    path('travel/', views.TravelListAPIView.as_view()),
    path('travel/<int:pk>/', views.TravelRetrieveAPIView.as_view()),
    path('member-speech/', views.MembersSpeechListCreateAPIView.as_view()),

    path('news/', views.NewsListCreateAPIView.as_view()),
    path('news/<int:pk>/', views.NewsRetrieveAPIView.as_view()),

    path('business-course/', views.BusinessCourseListCreateAPIView.as_view()),
    path('business-course/<int:pk>/', views.BusinessCourseRetrieveAPIView.as_view()),

    path('club/president/', views.ClubPresidentListApiView.as_view()),
    path('club/president/<int:pk>/', views.ClubPresidentRetrieveAPIView.as_view()),

    path('events/', views.EventListAPIView.as_view()),
    path('events/<int:pk>/', views.EventRetrieveAPIView.as_view()),

    path('podcasts/', views.PodcastListCreateAPIView.as_view()),
    path('podcasts/<int:pk>/', views.PodcastRetrieveAPIView.as_view()),

    path('gallery/', views.GalleryListCreateAPIView.as_view()),
    path('gallery/<int:pk>/', views.GalleryRetrieveAPIView.as_view()),

    path('national-values/', views.NationalValueListCreateAPIView.as_view()),

    path('uploader/', views.FileUploadView.as_view()),

    path('contact-form/', views.ContactFormView.as_view()),

    path('search/', views.SearchAPIView.as_view())
]
urlpatterns += router.urls
