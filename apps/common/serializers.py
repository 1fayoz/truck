from django.db.models import Avg
from rest_framework import serializers

from apps.common import models, utils


class BannerSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = models.Banner
        fields = (
            'id', 'url', 'title', 'description'
        )

    def get_title(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'title', request)

    def get_description(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'description', request)


class BannerSerializerCreate(serializers.ModelSerializer):
    title_uz = serializers.CharField(required=True)
    description_uz = serializers.CharField(required=True)
    title_en = serializers.CharField(required=True)
    description_en = serializers.CharField(required=True)
    title_ru = serializers.CharField(required=True)
    description_ru = serializers.CharField(required=True)

    class Meta:
        model = models.Banner
        fields = (
            'title_uz', 'title_en', 'title_ru', 'description_en', 'description_ru',
            'description_uz', 'url'
        )


class ClubOfferSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = models.ClubOffer
        fields = ('id', 'link', 'icon', 'title', 'description')

    def get_title(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'title', request)

    def get_description(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'description', request)


class ClubOfferSerializerCreate(serializers.ModelSerializer):
    title_uz = serializers.CharField(required=True)
    description_uz = serializers.CharField(required=True)
    title_en = serializers.CharField(required=True)
    description_en = serializers.CharField(required=True)
    title_ru = serializers.CharField(required=True)
    description_ru = serializers.CharField(required=True)

    class Meta:
        model = models.ClubOffer
        fields = (
            'title_uz', 'title_en', 'title_ru', 'description_en', 'description_ru',
            'description_uz', 'icon', 'link'
        )


class ClubStatisticsSerializer(serializers.Serializer):
    annual_revenue = serializers.SerializerMethodField()
    club_members = serializers.SerializerMethodField()
    business_fields = serializers.SerializerMethodField()
    export_scope = serializers.SerializerMethodField()
    experience_years = serializers.SerializerMethodField()

    @staticmethod
    def get_annual_revenue(obj):
        avg_revenue = models.Metric.objects.filter(is_active=True, type='after').aggregate(avg=Avg('revenue'))['avg']
        if avg_revenue:
            return round(avg_revenue / 1_000_000, 1)
        return 0

    @staticmethod
    def get_club_members(obj):
        return models.ClubMember.objects.filter(is_active=True, type='member').count() or 0

    @staticmethod
    def get_business_fields(obj):
        return models.Industry.objects.count() or 0

    @staticmethod
    def get_export_scope(obj):
        return models.ClubMember.objects.filter(is_active=True, type='expert').count() or 0

    @staticmethod
    def get_experience_years(obj):
        avg_exp = models.ClubMember.objects.aggregate(avg=Avg('experience'))['avg']
        return round(avg_exp) if avg_exp else 0
