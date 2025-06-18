from django.core.cache import cache
from django.db.models import Avg, Count
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


class IndustryDistributionSerializer(serializers.Serializer):
    industry = serializers.CharField()
    percentage = serializers.FloatField()

    @staticmethod
    def get_distribution(request):
        cache_key = "industry_distribution"
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return cached_data

        total = models.ClubMember.objects.filter(is_active=True).count()
        if total == 0:
            return []

        stats = (
            models.ClubMember.objects
            .filter(is_active=True)
            .values('industry')
            .annotate(count=Count('id'))
        )

        industry_map = {
            industry.id: industry for industry in models.Industry.objects.all()
        }

        result = []
        for item in stats:
            industry_obj = industry_map.get(item['industry'])
            if not industry_obj:
                continue
            industry_name = utils.get_translation(industry_obj, 'name', request)
            percentage = round((item['count'] / total) * 100)

            result.append({
                "industry": industry_name,
                "percentage": percentage
            })

        cache.set(cache_key, result, timeout=18000)
        return result


class ExclusiveVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VideoAndAudio
        fields = ('id', 'url')

    def create(self, validated_data):
        return models.VideoAndAudio.objects.create(**validated_data, type='exclusive')


class PartnersSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = models.Partners
        fields = ('id', 'name', 'logo')

    def get_name(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'name', request)


class PartnersSerializerCreate(serializers.ModelSerializer):
    name_uz = serializers.CharField(required=True)
    name_en = serializers.CharField(required=True)
    name_ru = serializers.CharField(required=True)

    class Meta:
        model = models.Partners
        fields = ('id', 'name_uz', 'name_ru', 'name_en', 'logo')

