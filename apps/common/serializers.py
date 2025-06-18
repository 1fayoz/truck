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
