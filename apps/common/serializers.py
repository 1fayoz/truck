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


class FAQSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()
    question = serializers.SerializerMethodField()

    class Meta:
        model = models.FAQ
        fields = ('id', 'question', 'answer')

    def get_answer(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'answer', request)

    def get_question(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'question', request)


class FAQSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = models.FAQ
        fields = ('id', 'question_uz', 'question_en', 'question_ru',
                  'answer_uz', 'answer_en', 'answer_ru', 'link'
                  )


class SocialLinkSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = models.SocialLink
        fields = ('id', 'url', 'name')

    def get_name(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'name', request)


class SocialLinkSerializerCreate(serializers.ModelSerializer):
    name_uz = serializers.CharField(required=True)
    name_en = serializers.CharField(required=True)
    name_ru = serializers.CharField(required=True)

    class Meta:
        model = models.SocialLink
        fields = ('id', 'url', 'name_uz', 'name_en', 'name_ru')


class MetricSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = models.Metric
        fields = ('id', 'type', 'title', 'revenue', 'employee_count',
                  'project_count'
                  )

    def get_title(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'title', request)


class MetricSerializerCreate(serializers.ModelSerializer):
    title_uz = serializers.CharField(required=True)
    title_en = serializers.CharField(required=True)
    title_ru = serializers.CharField(required=True)

    class Meta:
        model = models.Metric
        fields = ('id', 'type', 'title_uz', 'title_en', 'title_ru',
                  'revenue', 'employee_count', 'project_count'
                  )


class ClubMemberDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    social_links = SocialLinkSerializer(many=True, read_only=True)
    metric_before = serializers.SerializerMethodField()
    metric_after = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()

    class Meta:
        model = models.ClubMember
        fields = ('id', 'full_name', 'experience', 'company', 'position',
                  'image', 'social_links', 'metric_before', 'metric_after', 'bio', 'age', 'join_date')

    def get_metric_before(self, obj):
        metric = models.Metric.objects.filter(is_active=True, member=obj, type='before').last()
        if metric:
            return MetricSerializer(metric, context=self.context).data
        return None

    def get_metric_after(self, obj):
        metric = models.Metric.objects.filter(is_active=True, member=obj, type='after').last()
        if metric:
            return MetricSerializer(metric, context=self.context).data
        return None

    def get_bio(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'bio', request)

    def get_full_name(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'name', request)

    def get_company(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'company', request)

    def get_position(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'position', request)


class ClubMemberSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()
    project_count = serializers.SerializerMethodField()
    revenue = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    social_links = SocialLinkSerializer(many=True, read_only=True)

    class Meta:
        model = models.ClubMember
        fields = ('id', 'full_name', 'experience', 'employee_count',
                  'project_count', 'revenue', 'company', 'position',
                  'image', 'social_links'
                  )

    def get_full_name(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'name', request)

    @staticmethod
    def get_employee_count(obj):
        metric = obj.metric.filter(is_active=True, type='after').last()
        if not metric:
            return 0
        return metric.employee_count

    @staticmethod
    def get_project_count(obj):
        metric = obj.metric.filter(is_active=True, type='after').last()
        if not metric:
            return 0
        return metric.project_count or 0

    @staticmethod
    def get_revenue(obj):
        metric = obj.metric.filter(is_active=True, type='after').last()
        if not metric:
            return 0
        return metric.revenue or 0

    def get_company(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'company', request)

    def get_position(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'position', request)


class ClubMemberSerializerCreate(serializers.ModelSerializer):
    name_uz = serializers.CharField(required=True)
    name_en = serializers.CharField(required=True)
    name_ru = serializers.CharField(required=True)

    company_uz = serializers.CharField(required=True)
    company_en = serializers.CharField(required=True)
    company_ru = serializers.CharField(required=True)

    position_uz = serializers.CharField(required=True)
    position_en = serializers.CharField(required=True)
    position_ru = serializers.CharField(required=True)

    bio_uz = serializers.CharField(required=True)
    bio_ru = serializers.CharField(required=True)
    bio_en = serializers.CharField(required=True)

    age = serializers.IntegerField(required=True)
    image = serializers.URLField(required=True)
    join_date = serializers.DateField(required=True)
    experience = serializers.IntegerField(required=True)
    type = serializers.ChoiceField(models.ClubMember.TypeChoice)
    degree = serializers.ChoiceField(models.ClubMember.DegreeChoice)

    industry = serializers.PrimaryKeyRelatedField(
        queryset=models.Industry.objects.filter(is_active=True),
    )
    social_links = SocialLinkSerializerCreate(many=True, write_only=True)
    metric = MetricSerializerCreate(many=True, write_only=True)

    class Meta:
        model = models.ClubMember
        fields = ('name_uz', 'name_en', 'name_ru', 'company_uz', 'company_en', 'company_ru',
                  'position_uz', 'position_en', 'position_ru', 'bio_ru', 'bio_en', 'bio_uz',
                  'age', 'image', 'join_date', 'experience', 'type', 'degree', 'industry',
                  'social_links', 'metric'
                  )

    def create(self, validated_data):
        social_links_data = validated_data.pop('social_links', [])
        metric_data = validated_data.pop('metric', [])

        lang = utils.get_language(self.context['request'])

        if len(metric_data) > 2:
            raise serializers.ValidationError(
                utils.ERROR_MESSAGES['too_many_metrics'].get(lang, utils.ERROR_MESSAGES['too_many_metrics']['uz'])
            )

        types_seen = set()
        for metric in metric_data:
            metric_type = metric.get('type')
            if metric_type in types_seen:
                msg_template = utils.ERROR_MESSAGES['duplicate_type'].get(lang,
                                                                          utils.ERROR_MESSAGES['duplicate_type']['uz'])
                raise serializers.ValidationError(msg_template.format(type=metric_type))
            types_seen.add(metric_type)

        club_member = models.ClubMember.objects.create(**validated_data)

        social_links = [
            models.SocialLink(member=club_member, **link_data)
            for link_data in social_links_data
        ]
        models.SocialLink.objects.bulk_create(social_links)

        metrics = [
            models.Metric(member=club_member, **metric)
            for metric in metric_data
        ]
        models.Metric.objects.bulk_create(metrics)

        return club_member


class TravelSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = models.Travel
        fields = ('id', 'country', 'view_count', 'status', 'short_description', 'created_at', 'image')

    @staticmethod
    def get_image(obj):
        main_image = obj.images.filter(is_main=True, type='travel', is_active=True).order_by('-created_at').first()
        return main_image.image if main_image else None

    def get_country(self, obj):
        request = self.context.get('request')
        return utils.get_translation(obj.country, 'name', request) if obj.country else None

    def get_short_description(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'short_description', request)


class TravelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Images
        fields = ('image', 'is_main')


class TravelSerializerCreate(serializers.ModelSerializer):
    images = TravelImageSerializer(many=True, write_only=True)

    class Meta:
        model = models.Travel
        fields = (
            'id',
            'country',
            'description_uz', 'description_ru', 'description_en',
            'short_description_uz', 'short_description_ru', 'short_description_en',
            'status',
            'images'
        )

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        travel = models.Travel.objects.create(**validated_data)

        for image_data in images_data:
            models.Images.objects.create(travel=travel, type='travel', **image_data)

        return travel
