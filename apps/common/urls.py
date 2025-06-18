from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.common import views

router = DefaultRouter()
router.register(r'banner', views.BannerViewSet, basename='banner')
router.register(r'club/offers', views.ClubOfferViewSet, basename='club-offer')
router.register('exclusive-video', views.ExclusiveVideosListAPIView, basename='exclusive-video')

urlpatterns = [
    path('club/stats/', views.ClubStatisticsAPIView.as_view()),
    path('industry-distribution/', views.IndustryDistributionAPIView.as_view()),
]
urlpatterns += router.urls
