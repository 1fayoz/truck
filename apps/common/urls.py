from django.urls import path

from apps.common import views

urlpatterns = [
    path('user', views.UserLogin.as_view()),
    path('service', views.ServiceView.as_view()),

    path('docs', views.DocsView.as_view()),
    path('news', views.NewsListView.as_view()),

]