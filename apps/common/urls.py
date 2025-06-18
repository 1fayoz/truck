from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.common import views

router = DefaultRouter()
router.register(r'banner', views.BannerViewSet, basename='banner')

urlpatterns = []
urlpatterns += router.urls
