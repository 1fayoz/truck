from .extra_models import *


class Industry(BaseModel, NameTranslation):
    icon = models.URLField()


class Company(BaseModel, NameTranslation):
    pass


class ClubMember(BaseModel, NameTranslation, BioTranslation, PositionTranslation):
    class DegreeChoice(models.TextChoices):
        PRESIDENT = 'president', "President"
        DIRECTOR = 'director', "Director"
        ASSISTANT_DIRECTORY = 'assistant_director', "Assistant Director"

    class TypeChoice(models.TextChoices):
        MEMBER = 'member', "Member"
        EXPERT = 'expert', "Expert"

    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    age = models.IntegerField()
    image = models.URLField(null=True, blank=True)
    join_date = models.DateField()
    experience = models.IntegerField()
    type = models.CharField(max_length=255, choices=TypeChoice.choices, default=TypeChoice.MEMBER, null=True, blank=True)
    degree = models.CharField(max_length=255, choices=DegreeChoice.choices, default=DegreeChoice.PRESIDENT, null=True,
                              blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True)


class Autobiography(BaseModel, DescriptionTranslation):
    year = models.CharField(max_length=255)
    member = models.ForeignKey(ClubMember, on_delete=models.CASCADE, related_name='autobiographies')
    order = models.IntegerField(null=True, blank=True)


class SocialLink(BaseModel, NameTranslation):
    url = models.URLField()
    member = models.ForeignKey(ClubMember, on_delete=models.CASCADE, related_name='social_links')


class Metric(BaseModel, TitleTranslation):
    class MetricType(models.TextChoices):
        BEFORE = 'before', "Before"
        AFTER = 'after', "After"

    revenue = models.BigIntegerField()
    employee_count = models.IntegerField()
    project_count = models.IntegerField()
    member = models.ForeignKey(ClubMember, on_delete=models.CASCADE, related_name='metric')
    type = models.CharField(max_length=255, choices=MetricType.choices, default=MetricType.BEFORE)


class ClubOffer(BaseModel, TitleTranslation, DescriptionTranslation):
    icon = models.CharField(max_length=255)
    link = models.CharField(max_length=255)


class Banner(BaseModel, TitleTranslation, DescriptionTranslation):
    class BannerType(models.TextChoices):
        COURSE = 'course', "Course"
        HOME = 'home', "Home"
        EVENT = 'event', "Event"

    url = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=BannerType.choices, default=BannerType.HOME)


class Speaker(BaseModel, NameTranslation, BioTranslation):
    image = models.URLField()


class VideoAndAudio(BaseModel, TitleTranslation, DescriptionTranslation):
    class ContentType(models.TextChoices):
        EXCLUSIVE = 'exclusive', "Exclusive"
        VIDEO_PODCAST = 'video_podcast', "Video Podcast"
        AUDIO_PODCAST = 'audio_podcast', "Audio Podcast"
        MEMBER_SPEECH = 'member_speech', "Member Speech"

    url = models.URLField()
    extra_image = models.URLField(null=True, blank=True)
    type = models.CharField(max_length=255, choices=ContentType.choices, default=ContentType.VIDEO_PODCAST)
    members = models.ForeignKey(ClubMember, on_delete=models.SET_NULL, null=True, blank=True)
    view_count = models.BigIntegerField(null=True)
    duration = models.CharField(max_length=255, null=True)


class PodcastSpeaker(models.Model):
    podcast = models.ForeignKey(VideoAndAudio, on_delete=models.CASCADE, related_name='podcasts_speaker')
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE, related_name='podcasts_speaker')


class TravelCountry(BaseModel, NameTranslation):
    icon = models.URLField(null=True, blank=True)
    pass


class Travel(BaseModel, DescriptionTranslation, ShortDescriptionTranslation):
    class TravelStatus(models.TextChoices):
        WAITING = 'waiting', "Waiting"
        BEEN = 'been', "Been"

    country = models.ForeignKey(TravelCountry, on_delete=models.SET_NULL, null=True)
    view_count = models.BigIntegerField(default=0)
    status = models.CharField(max_length=20, choices=TravelStatus.choices, default=TravelStatus.WAITING)


class Tag(BaseModel):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.name)


class News(BaseModel, TitleTranslation, DescriptionTranslation, ShortDescriptionTranslation):
    view_count = models.BigIntegerField(default=0)
    tags = models.ManyToManyField(Tag)


class Images(BaseModel):
    class ImageType(models.TextChoices):
        NEW = 'new', "New"
        TRAVEL = 'travel', "Travel"
        GALLERY = 'gallery', "Gallery"

    type = models.CharField(max_length=255, choices=ImageType.choices, default=ImageType.NEW)
    image = models.URLField()

    travel = models.ForeignKey(Travel, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')
    news = models.ForeignKey(News, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')
    gallery = models.ForeignKey("Gallery", on_delete=models.SET_NULL, null=True, blank=True, related_name='images')

    is_main = models.BooleanField(default=False)


class BusinessCourse(BaseModel, TitleTranslation, DescriptionTranslation):
    view_count = models.BigIntegerField()
    image = models.URLField()
    speaker = models.ForeignKey(Speaker, on_delete=models.SET_NULL, null=True)
    banner = models.ForeignKey(Banner, on_delete=models.SET_NULL, null=True)


class CourseInfo(BaseModel, TitleTranslation, DescriptionTranslation):
    class ModuleType(models.TextChoices):
        MODULE = 'module', "Module"
        FORMAT = 'format', "Format"

    module_number = models.BigIntegerField(null=True, blank=True)
    business_course = models.ForeignKey(BusinessCourse, on_delete=models.CASCADE, related_name='course_info')
    type = models.CharField(max_length=255, choices=ModuleType.choices, default=ModuleType.MODULE)
    icon = models.CharField(max_length=255, null=True, blank=True)


class NationalValue(BaseModel, TitleTranslation, DescriptionTranslation):
    icon = models.CharField(max_length=255)


class Events(BaseModel, TitleTranslation, DescriptionTranslation, LocationTranslation):
    class EventType(models.TextChoices):
        PENDING = 'pending', "Pending"
        COMPLETED = 'completed', "Completed"

    status = models.CharField(max_length=20, choices=EventType.choices, default=EventType.PENDING)
    image = models.URLField(null=True)
    banner = models.ForeignKey(Banner, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
    duration = models.CharField(max_length=255)
    is_zoom = models.BooleanField(default=False)


class EventSpeaker(models.Model):
    events = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='event_speakers')
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)


class EventAgenda(BaseModel, TitleTranslation, DescriptionTranslation):
    time = models.CharField(max_length=255)
    order = models.IntegerField()
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=True, related_name='agendas')


class Gallery(BaseModel, TitleTranslation, DescriptionTranslation):
    class GalleryType(models.TextChoices):
        PICTURE = 'picture', "Picture"
        VIDEO = 'video', "Video"

    type = models.CharField(max_length=50, choices=GalleryType.choices, default=GalleryType.PICTURE)
    url = models.URLField()
    view_count = models.BigIntegerField(default=0)


class ChoiceType(models.TextChoices):
    BUSINESS_TYPE = "business_type", "Biznes turi"
    EXPERIENCE = "experience", "Biznes tajribasi"
    PROJECT_COUNT = "project_count", "Loyihalar soni"
    EMPLOYEE_COUNT = "employee_count", "Xodimlar soni"


class GenericChoice(BaseModel, NameTranslation):
    type = models.CharField(max_length=50, choices=ChoiceType.choices)

    def __str__(self):
        return f"({self.get_type_display()})"


class ContactForm(BaseModel):
    class ContactType(models.TextChoices):
        ATTENDEE = 'attendee', "Attendee"
        MEMBER = 'member', "Member"
        EXPERT = 'expert', "Expert"

    type = models.CharField(max_length=50, choices=ContactType.choices, default='attendee')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    company = models.CharField(max_length=255, null=True, blank=True)
    annual_revenue = models.BigIntegerField(null=True, blank=True)

    business_type = models.ForeignKey(
        GenericChoice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='business_type_choices'
    )
    business_experience = models.ForeignKey(
        GenericChoice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='experience_choices'
    )
    project_count = models.ForeignKey(
        GenericChoice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='project_count_choices'
    )
    employee_count = models.ForeignKey(
        GenericChoice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employee_count_choices'
    )

    telegram = models.CharField(max_length=255, null=True, blank=True)
    linkedin = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)


class Partners(BaseModel, NameTranslation):
    logo = models.URLField()


class FAQ(BaseModel):
    question_uz = models.CharField(max_length=255)
    question_en = models.CharField(max_length=255)
    question_ru = models.CharField(max_length=255)

    answer_uz = models.TextField()
    answer_en = models.TextField()
    answer_ru = models.TextField()

    def __str__(self):
        return self.question_uz or " "


class Uploader(BaseModel):
    from .utils import upload_to

    class TypeChoices(models.TextChoices):
        IMAGE = 'image', "Image"
        VIDEO = 'video', "Video"

    type = models.CharField(max_length=10, choices=TypeChoices.choices)
    file = models.FileField(upload_to=upload_to)

    def __str__(self):
        return f"{self.file.name}"


class HomeStatIcons(models.Model):
    annual_revenue = models.URLField()
    club_members = models.URLField()
    business_fields = models.URLField()
    export_scope = models.URLField()
    experience_years = models.URLField()

