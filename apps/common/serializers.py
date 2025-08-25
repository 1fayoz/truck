from rest_framework import serializers

from apps.common.models import User, Service, Docs, News


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