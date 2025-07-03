from django.contrib import admin
from .models import (
    Industry, ClubMember, Autobiography, SocialLink, Metric, ClubOffer, Banner, Speaker, VideoAndAudio,
    Travel, Tag, News, Images, BusinessCourse, CourseInfo, NationalValue, Events, EventAgenda,
    Gallery, GenericChoice, ContactForm, TravelCountry, Company, EventSpeaker, PodcastSpeaker, HomeStatIcons, Uploader
)

# 🔹 Helper for image/icon preview
from django.utils.html import format_html


def image_preview(obj):
    if obj.image:
        return format_html('<img src="{}" width="60" style="object-fit:contain;" />', obj.image)
    return "-"


image_preview.short_description = 'Preview'


def icon_preview(obj):
    if obj.icon:
        return format_html('<img src="{}" width="40" style="object-fit:contain;" />', obj.icon)
    return "-"


icon_preview.short_description = 'Icon'


# 🔹 Inline classes
class AutobiographyInline(admin.TabularInline):
    model = Autobiography
    extra = 0


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 0


class MetricInline(admin.TabularInline):
    model = Metric
    extra = 0


# 🔹 Main Admins
@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ['name_en', icon_preview]
    search_fields = ['name_en', 'name_uz', 'name_ru']


@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'age', 'experience', 'type', 'degree', 'industry']
    list_filter = ['type', 'degree', 'industry']
    search_fields = ['name_en', 'name_uz', 'name_ru', 'company_en']
    inlines = [AutobiographyInline, SocialLinkInline, MetricInline]


@admin.register(Autobiography)
class AutobiographyAdmin(admin.ModelAdmin):
    list_display = ['year', 'member']
    search_fields = ['year', 'member__name_en']


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'url', 'member']
    search_fields = ['name_en', 'url']


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ['member', 'type', 'revenue', 'employee_count', 'project_count']
    list_filter = ['type']
    search_fields = ['member__name_en']


@admin.register(ClubOffer)
class ClubOfferAdmin(admin.ModelAdmin):
    list_display = ['title_en', icon_preview, 'link']
    search_fields = ['title_en']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'type', 'url']
    list_filter = ['type']
    search_fields = ['title_en']


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['name_en', image_preview]
    search_fields = ['name_en']


@admin.register(VideoAndAudio)
class VideoAndAudioAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_en', 'type', 'view_count', 'duration']
    list_filter = ['type']
    search_fields = ['title_en']


@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    list_display = ['country', 'status', 'view_count']
    list_filter = ['status']
    search_fields = ['title_en']


@admin.register(TravelCountry)
class TravelCountryAdmin(admin.ModelAdmin):
    list_display = ['name_uz']


@admin.register(EventSpeaker)
class TravelCountryAdmin(admin.ModelAdmin):
    list_display = ['speaker']


@admin.register(PodcastSpeaker)
class TravelCountryAdmin(admin.ModelAdmin):
    list_display = ['speaker']


@admin.register(Company)
class TravelCountryAdmin(admin.ModelAdmin):
    list_display = ['name_uz']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'view_count']
    search_fields = ['title_en']
    filter_horizontal = ['tags']


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['type', image_preview, 'is_main', 'travel', 'news', 'gallery']
    list_filter = ['type', 'is_main']


@admin.register(BusinessCourse)
class BusinessCourseAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'view_count', 'speaker', image_preview]
    search_fields = ['title_en']
    autocomplete_fields = ['speaker']


@admin.register(CourseInfo)
class CourseInfoAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'type', 'module_number', icon_preview]
    list_filter = ['type']
    search_fields = ['title_en']
    autocomplete_fields = ['business_course']


@admin.register(NationalValue)
class NationalValueAdmin(admin.ModelAdmin):
    list_display = ['title_en', icon_preview]
    search_fields = ['title_en']


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'date', 'duration', 'banner']
    search_fields = ['title_en']
    autocomplete_fields = ['banner']


@admin.register(EventAgenda)
class EventAgendaAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'time', 'order']
    search_fields = ['title_en']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'type', 'view_count', 'url']
    list_filter = ['type']
    search_fields = ['title_en']


@admin.register(Uploader)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['file', 'type']
    list_filter = ['type']


@admin.register(GenericChoice)
class GenericChoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_en', 'type']
    list_filter = ['type']
    search_fields = ['name_en']


@admin.register(HomeStatIcons)
class HomeStatIconsAdmin(admin.ModelAdmin):
    list_display = ['id', 'annual_revenue']


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'company', 'phone', 'annual_revenue']
    search_fields = ['full_name', 'company', 'phone']
    list_filter = ['business_type', 'business_experience']
    autocomplete_fields = ['business_type', 'business_experience', 'project_count', 'employee_count']
