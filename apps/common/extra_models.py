from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class NameTranslation(models.Model):
    name_uz = models.CharField(max_length=255, null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    name_ru = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class CompanyTranslation(models.Model):
    company_uz = models.CharField(max_length=255, null=True, blank=True)
    company_en = models.CharField(max_length=255, null=True, blank=True)
    company_ru = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class TitleTranslation(models.Model):
    title_uz = models.CharField(max_length=255, null=True, blank=True)
    title_en = models.CharField(max_length=255, null=True, blank=True)
    title_ru = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class DescriptionTranslation(models.Model):
    description_uz = models.CharField(max_length=255, null=True, blank=True)
    description_en = models.CharField(max_length=255, null=True, blank=True)
    description_ru = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class LocationTranslation(models.Model):
    location_uz = models.CharField(max_length=255, null=True, blank=True)
    location_en = models.CharField(max_length=255, null=True, blank=True)
    location_ru = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class BioTranslation(models.Model):
    bio_uz = models.CharField(max_length=255, null=True, blank=True)
    bio_en = models.CharField(max_length=255, null=True, blank=True)
    bio_ru = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class ShortDescriptionTranslation(models.Model):
    short_description_uz = models.CharField(max_length=255, null=True, blank=True)
    short_description_en = models.CharField(max_length=255, null=True, blank=True)
    short_description_ru = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class PositionTranslation(models.Model):
    position_uz = models.CharField(max_length=255, null=True, blank=True)
    position_en = models.CharField(max_length=255, null=True, blank=True)
    position_ru = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
