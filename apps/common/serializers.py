import re
from uuid import uuid4

from django.core.cache import cache
from django.db.models import Avg, Count
from rest_framework import serializers
from datetime import datetime
from django.utils.timezone import now

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


class HomeStatIconsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HomeStatIcons
        fields = '__all__'


class ClubStatisticsSerializer(serializers.Serializer):
    annual_revenue = serializers.SerializerMethodField()
    club_members = serializers.SerializerMethodField()
    business_fields = serializers.SerializerMethodField()
    export_scope = serializers.SerializerMethodField()
    experience_years = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    @staticmethod
    def get_icon(obj):
        icon = models.HomeStatIcons.objects.last()
        return HomeStatIconsSerializer(icon).data if icon else None

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
        return utils.get_translation(obj.company, 'name', request) if obj.company else None

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
        return utils.get_translation(obj.company, 'name', request) if obj.company else None

    def get_position(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'position', request)


class ClubMemberSerializerCreate(serializers.ModelSerializer):
    name_uz = serializers.CharField(required=True)
    name_en = serializers.CharField(required=True)
    name_ru = serializers.CharField(required=True)

    company = serializers.PrimaryKeyRelatedField(
        queryset=models.Company.objects.filter(is_active=True),
        required=True
    )

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
        fields = ('name_uz', 'name_en', 'name_ru', 'company',
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


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Images
        fields = ('id', 'image', 'is_main')


class TravelSerializerCreate(serializers.ModelSerializer):
    images = ImageSerializer(many=True, write_only=True)

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


class MembersSpeechSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    class Meta:
        model = models.VideoAndAudio
        fields = (
            'id', 'url', 'full_name', 'position',
            'company',
        )

    def get_full_name(self, obj):
        request = self.context.get('request')
        return utils.get_translation(obj.members, 'name', request) if obj.members else None

    def get_position(self, obj):
        request = self.context.get('request')
        return utils.get_translation(obj.members, 'position', request) if obj.members else None

    def get_company(self, obj):
        request = self.context.get('request')
        return utils.get_translation(obj.members.company, 'name', request) if obj.members.company else None


class MembersSpeechSerializerCreate(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=models.ClubMember.objects.filter(is_active=True),
        required=True,
    )

    class Meta:
        model = models.VideoAndAudio
        fields = ('id', 'url', 'members')

    def create(self, validated_data):
        return models.VideoAndAudio.objects.create(type='member_speech', **validated_data)


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'name')


class NewsSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    tags = TagsSerializer(many=True, read_only=True)

    class Meta:
        model = models.News
        fields = ('id', 'title', 'short_description', 'image', 'view_count', 'tags', 'created_at')

    def get_title(self, obj):
        request = self.context.get('request')
        return utils.get_translation(obj, 'title', request) if obj else None

    def get_short_description(self, obj):
        request = self.context.get('request')
        return utils.get_translation(obj, 'short_description', request) if obj else None

    @staticmethod
    def get_image(obj):
        main_image = obj.images.filter(is_main=True, type='new', is_active=True).order_by('-created_at').first()
        return main_image.image if main_image else None


class NewsSerializerCreate(serializers.ModelSerializer):
    title_uz = serializers.CharField(required=True)
    title_en = serializers.CharField(required=True)
    title_ru = serializers.CharField(required=True)

    description_uz = serializers.CharField(required=True)
    description_ru = serializers.CharField(required=True)
    description_en = serializers.CharField(required=True)

    short_description_uz = serializers.CharField(required=True)
    short_description_ru = serializers.CharField(required=True)
    short_description_en = serializers.CharField(required=True)

    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.Tag.objects.filter(is_active=True), required=True
    )

    images = ImageSerializer(many=True, required=True)

    class Meta:
        model = models.News
        fields = (
            'id', 'title_ru', 'title_en', 'title_uz',
            'description_ru', 'description_en', 'description_uz',
            'short_description_ru', 'short_description_en', 'short_description_uz',
            'tags', 'images'
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        images_data = validated_data.pop('images', [])

        news = models.News.objects.create(**validated_data)
        news.tags.set(tags)

        images = [
            models.Images(
                news=news,
                type='new',
                **image_data
            )
            for image_data in images_data
        ]
        if images:
            models.Images.objects.bulk_create(images)

        return news


class NewsSerializerDetail(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = models.News
        fields = ('id', 'title', 'description', 'images', 'view_count', 'created_at')

    @staticmethod
    def get_images(obj):
        queryset = obj.images.filter(type='new', is_active=True).order_by('-created_at')
        return ImageSerializer(queryset, many=True).data

    def get_title(self, obj):
        request = self.context.get('request')
        return utils.get_translation(obj, 'title', request) if obj else None

    def get_description(self, obj):
        request = self.context.get('request')
        return utils.get_translation(obj, 'description', request) if obj else None


class SpeakerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = models.Speaker
        fields = ('id', 'name', 'image')

    def get_name(self, obj):
        request = self.context.get('request')
        return utils.get_translation(obj, 'name', request) if obj else None


class BusinessCourseSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    speaker = SpeakerSerializer()

    class Meta:
        model = models.BusinessCourse
        fields = ('id', 'title', 'view_count', 'image', 'speaker')

    def get_title(self, obj):
        request = self.context.get('request')
        return utils.get_translation(obj, 'title', request) if obj else None


class CourseInfoSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = models.CourseInfo
        fields = ('id', 'title', 'description', 'module_number', 'icon')

    def get_title(self, obj):
        request = self.context.get('request')
        return utils.get_translation(obj, 'title', request) if obj else None

    def get_description(self, obj):
        request = self.context.get('request')
        return utils.get_translation(obj, 'description', request) if obj else None


class BusinessCourseSerializerDetail(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    banner = BannerSerializer()
    course_format = serializers.SerializerMethodField()
    course_modules = serializers.SerializerMethodField()

    class Meta:
        model = models.BusinessCourse
        fields = (
            'id', 'description', 'banner', 'course_format', 'course_modules'
        )

    @staticmethod
    def get_course_modules(obj):
        queryset = obj.course_info.filter(type='module', is_active=True).order_by('module_number')
        return CourseInfoSerializer(queryset, many=True).data

    @staticmethod
    def get_course_format(obj):
        queryset = obj.course_info.filter(type='format', is_active=True)
        return CourseInfoSerializer(queryset, many=True).data

    def get_description(self, obj):
        request = self.context.get('request')
        return utils.get_translation(obj, 'description', request) if obj else None


class BusinessCourseSerializerCreate(serializers.ModelSerializer):
    title_uz = serializers.CharField(required=True)
    title_en = serializers.CharField(required=True)
    title_ru = serializers.CharField(required=True)

    description_uz = serializers.CharField(required=True)
    description_ru = serializers.CharField(required=True)
    description_en = serializers.CharField(required=True)

    banner = BannerSerializer(required=True)

    class Meta:
        model = models.BusinessCourse
        fields = ('id', 'title_uz', 'title_en', 'title_ru',
                  'description_uz', 'description_ru', 'description_en',
                  'banner'
                  )


class AutobiographySerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = models.Autobiography
        fields = ('id', 'year', 'description')

    def get_description(self, obj):
        request = self.context.get('request')
        return utils.get_translation(obj, 'description', request) if obj else None


class ClubPresidentDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    social_links = SocialLinkSerializer(many=True, read_only=True)
    bio = serializers.SerializerMethodField()
    autobiographies = serializers.SerializerMethodField()

    class Meta:
        model = models.ClubMember
        fields = ('id', 'full_name', 'experience', 'company', 'position',
                  'image', 'social_links', 'bio', 'age', 'autobiographies')

    @staticmethod
    def get_autobiographies(obj):
        queryset = obj.autobiographies.filter(is_active=True).order_by('order')
        return AutobiographySerializer(queryset, many=True).data

    def get_bio(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'bio', request)

    def get_full_name(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'name', request)

    def get_company(self, obj):
        request = self.context['request']
        return utils.get_translation(obj.company, 'name', request) if obj.company else None

    def get_position(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'position', request)


class EventSpeakersSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = models.EventSpeaker
        fields = ('id', 'name', 'image')

    def get_name(self, obj):
        request = self.context['request']
        return utils.get_translation(obj.speaker, 'name', request)

    @staticmethod
    def get_image(obj):
        return obj.speaker.image


class EventSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    event_speakers = EventSpeakersSerializer(many=True, read_only=True)

    class Meta:
        model = models.Events
        fields = ('id', 'image', 'title', 'status',
                  'location', 'date', 'duration', 'event_speakers'
                  )

    def get_title(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'title', request)

    def get_location(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'location', request)


class EventAgendaSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = models.EventAgenda
        fields = ('id', 'title', 'description', 'time')

    def get_title(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'title', request)

    def get_description(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'description', request)


class EventDetailSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    banner = BannerSerializer(read_only=True)
    title = serializers.SerializerMethodField()
    agendas = serializers.SerializerMethodField()
    remaining_seconds = serializers.SerializerMethodField()

    class Meta:
        model = models.Events
        fields = ('id', 'title', 'description', 'location',
                  'date', 'duration', 'banner', 'agendas', 'remaining_seconds'
                  )

    def get_agendas(self, obj):
        queryset = obj.agendas.filter(is_active=True).order_by('order')
        return EventAgendaSerializer(queryset, many=True, context=self.context).data

    def get_title(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'title', request)

    def get_description(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'description', request) if obj else None

    def get_location(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'location', request)

    @staticmethod
    def get_remaining_seconds(obj):
        if obj.date:
            now_time = now()
            delta = obj.date - now_time
            remaining_seconds = int(delta.total_seconds())
            return max(0, remaining_seconds)
        return None


class PodcastSpeakerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = models.PodcastSpeaker
        fields = ('id', 'name', 'image')

    def get_name(self, obj):
        request = self.context['request']
        return utils.get_translation(obj.speaker, 'name', request)

    @staticmethod
    def get_image(obj):
        return obj.speaker.image if obj.speaker else None


class PodcastSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    podcasts_speaker = PodcastSpeakerSerializer(many=True, read_only=True)

    class Meta:
        model = models.VideoAndAudio
        fields = ('id', 'title', 'url', 'duration', 'view_count', 'podcasts_speaker', 'type')

    def get_title(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'title', request)


class PodcastDetailSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    podcasts_speaker = PodcastSpeakerSerializer(many=True, read_only=True)
    description = serializers.SerializerMethodField()

    class Meta:
        model = models.VideoAndAudio
        fields = ('id', 'title', 'url', 'duration', 'view_count',
                  'podcasts_speaker', 'type', 'extra_image', 'description',
                  'created_at'
                  )

    def get_title(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'title', request)

    def get_description(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'description', request)


class GallerySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    image_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Gallery
        fields = ('id', 'title', 'url', 'view_count', 'created_at', 'image_count')

    def get_title(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'title', request)

    @staticmethod
    def get_image_count(obj):
        main_image = obj.images.filter(type='gallery', is_active=True).count()
        return main_image if main_image else None


class GalleryDetailSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Gallery
        fields = ('id', 'title', 'description', 'images')

    def get_title(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'title', request)

    def get_description(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'description', request)


class NationalValueSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = models.NationalValue
        fields = ('id', 'title', 'description', 'icon')

    def get_title(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'title', request)

    def get_description(self, obj):
        request = self.context['request']
        return utils.get_translation(obj, 'description', request)


class UploaderSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    file = serializers.FileField(required=True, write_only=True)

    class Meta:
        model = models.Uploader
        fields = ['id', 'type', 'file', 'file_url']

    @staticmethod
    def validate_type(value):
        if value not in models.Uploader.TypeChoices.values:
            raise serializers.ValidationError("Type must be 'image' or 'video'.")
        return value

    def validate_file(self, file):
        allowed_image_ext = ['jpg', 'jpeg', 'png']
        allowed_video_ext = ['mp4', 'mov']
        ext = file.name.split('.')[-1].lower()

        _type = self.initial_data.get('type')
        if _type == models.Uploader.TypeChoices.IMAGE and ext not in allowed_image_ext:
            raise serializers.ValidationError("Only JPG, JPEG, PNG files are allowed for images.")
        elif _type == models.Uploader.TypeChoices.VIDEO and ext not in allowed_video_ext:
            raise serializers.ValidationError("Only MP4, MOV files are allowed for videos.")

        return file

    def create(self, validated_data):
        file = validated_data.get('file')
        ext = file.name.split('.')[-1]
        file.name = f"{uuid4()}.{ext}"
        return super().create(validated_data)

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


PHONE_REGEX = re.compile(r'^\+?1?\d{9,15}$')


class ContactFormSerializer(serializers.ModelSerializer):
    business_type = serializers.PrimaryKeyRelatedField(
        queryset=models.GenericChoice.objects.filter(type='business_type'),
        required=False
    )
    business_experience = serializers.PrimaryKeyRelatedField(
        queryset=models.GenericChoice.objects.filter(type='experience'),
        required=False
    )
    project_count = serializers.PrimaryKeyRelatedField(
        queryset=models.GenericChoice.objects.filter(type='project_count'),
        required=False
    )
    employee_count = serializers.PrimaryKeyRelatedField(
        queryset=models.GenericChoice.objects.filter(type='employee_count'),
        required=False
    )

    phone = serializers.CharField()

    class Meta:
        model = models.ContactForm
        fields = [
            'type', 'full_name', 'phone', 'company', 'annual_revenue',
            'business_type', 'business_experience', 'project_count',
            'employee_count', 'telegram', 'linkedin', 'instagram', 'facebook'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'] = serializers.ChoiceField(
            choices=models.ContactForm.ContactType.choices,
            required=True
        )

    @staticmethod
    def validate_phone(value):
        if not PHONE_REGEX.match(value):
            raise serializers.ValidationError("Telefon raqami noto‘g‘ri formatda. Masalan: +998901234567")
        return value

    def validate(self, data):
        contact_type = data.get('type')
        lang = utils.get_language(self.context.get('request'))

        if contact_type == 'attendee':
            if not data.get('full_name') or not data.get('phone'):
                raise serializers.ValidationError(utils.messages[lang]['attendee_required'])

        elif contact_type in ['member', 'expert']:
            required_fields = ['full_name', 'phone', 'company', 'annual_revenue', 'business_type',
                               'business_experience', 'project_count', 'employee_count']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError(utils.messages[lang]['member_expert_required'])

            if contact_type == 'expert':
                revenue = data.get('annual_revenue')
                if not revenue or revenue < 1_000_000:
                    raise serializers.ValidationError(utils.messages[lang]['expert_revenue'])

        return data
