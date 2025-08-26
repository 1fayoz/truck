from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.response import Response

from apps.common import serializers
from apps.common.models import User, Service, Docs, News, Application, Employee


class UserLogin(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('full_name', 'phone')
    filterset_fields = ('is_active', 'type')

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


