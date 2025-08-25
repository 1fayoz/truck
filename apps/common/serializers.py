from rest_framework import serializers

from apps.common.models import User, Service, Docs


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
            'name',
            'short_des',
            'description'
        )