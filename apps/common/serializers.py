from rest_framework import serializers

from apps.common.models import User, Service, Docs, News, Application, Employee


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'phone',
            'full_name',
        )


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            'id',
            'name',
            'icon',
            'des',
            'status'
        )


class DocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docs
        fields = (
            'id',
            'icon',
            'name',
            'size'
        )

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = (
            'id',
            'name',
            'image',
            'short_des',
            'description'
        )

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            'id',
            'full_name',
            'phone',
            'email',
            'address',
            'text',
            'file'
        )

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'image',
            'full_name',
            'email',
            'degree',
            'work_time_from',
            'work_time_to',
        )
