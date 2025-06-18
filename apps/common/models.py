from .extra_models import *


class Industry(BaseModel, NameTranslation):
    icon = models.CharField(max_length=255)


class ClubMember(BaseModel, NameTranslation, CompanyTranslation, BioTranslation, PositionTranslation):
    class DegreeChoice(models.TextChoices):
        PRESIDENT = 'president', "President"
        DIRECTOR = 'director', "Director"
        ASSISTANT_DIRECTORY = 'assistant_director', "Assistant Director"

    class TypeChoice(models.TextChoices):
        MEMBER = 'member', "Member"
        EXPERT = 'expert', "Expert"

    age = models.IntegerField()

    join_date = models.DateField()
    experience = models.IntegerField()
    type = models.CharField(max_length=255, choices=TypeChoice.choices, default=TypeChoice.MEMBER)
    degree = models.CharField(max_length=255, choices=DegreeChoice.choices, default=DegreeChoice.PRESIDENT, null=True,
                              blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True)


class Autobiography(BaseModel, DescriptionTranslation):
    year = models.CharField(max_length=255)
    member = models.ForeignKey(ClubMember, on_delete=models.CASCADE)


class SocialLink(BaseModel, NameTranslation):
    url = models.CharField(max_length=255)
    member = models.ForeignKey(ClubMember, on_delete=models.CASCADE)


class Metric(BaseModel, TitleTranslation):
    class MetricType(models.TextChoices):
        BEFORE = 'before', "Before"
        AFTER = 'after', "After"

    revenue = models.BigIntegerField()
    employee_count = models.IntegerField()
    project_count = models.IntegerField()
    member = models.ForeignKey(ClubMember, on_delete=models.CASCADE)
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

    url = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=ContentType.choices, default=ContentType.VIDEO_PODCAST)
    speakers = models.CharField(max_length=255, null=True)
    view_count = models.BigIntegerField(null=True)
    duration = models.CharField(max_length=255, null=True)


class TravelCountry(BaseModel, NameTranslation):
    pass


class Travel(BaseModel, TitleTranslation, DescriptionTranslation, ShortDescriptionTranslation):
    class TravelStatus(models.TextChoices):
        PENDING = 'pending', "Pending"
        WAITING = 'waiting', "Waiting"
        BEEN = 'been', "Been"

    country = models.ForeignKey(TravelCountry, on_delete=models.SET_NULL, null=True)
    view_count = models.BigIntegerField(default=0)
    status = models.CharField(max_length=20, choices=TravelStatus.choices, default=TravelStatus.PENDING)


class Tag(BaseModel, NameTranslation):
    pass


class News(BaseModel, TitleTranslation, DescriptionTranslation, ShortDescriptionTranslation):
    view_count = models.BigIntegerField()
    tags = models.ManyToManyField(Tag)


class Images(BaseModel):
    class ImageType(models.TextChoices):
        NEW = 'new', "New"
        TRAVEL = 'travel', "Travel"
        GALLERY = 'gallery', "Gallery"

    type = models.CharField(max_length=255, choices=ImageType.choices, default=ImageType.NEW)
    image = models.URLField()

    travel = models.ForeignKey(Travel, on_delete=models.SET_NULL, null=True)
    news = models.ForeignKey(News, on_delete=models.SET_NULL, null=True)
    gallery = models.ForeignKey("Gallery", on_delete=models.SET_NULL, null=True)

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
    business_course = models.ForeignKey(BusinessCourse, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=ModuleType.choices, default=ModuleType.MODULE)
    icon = models.CharField(max_length=255, null=True, blank=True)


class NationalValue(BaseModel, TitleTranslation, DescriptionTranslation):
    icon = models.CharField(max_length=255)


class Events(BaseModel, TitleTranslation, DescriptionTranslation, LocationTranslation):
    class EventType(models.TextChoices):
        PENDING = 'pending', "Pending"
        COMPLETED = 'completed', "Completed"

    banner = models.ForeignKey(Banner, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
    duration = models.CharField(max_length=255)


class EventAgenda(BaseModel, TitleTranslation, DescriptionTranslation):
    time = models.CharField(max_length=255)
    order = models.IntegerField()


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
        return f"{self.name} ({self.get_type_display()})"


class ContactForm(BaseModel):
    class ContactType(models.TextChoices):
        ATTENDEE = 'attendee', "Attendee"
        MEMBER = 'member', "Member"
        EXPERT = 'expert', "Expert"

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    annual_revenue = models.BigIntegerField()

    business_type = models.ForeignKey(
        GenericChoice,
        on_delete=models.SET_NULL,
        null=True,
        related_name='business_type_choices'
    )
    business_experience = models.ForeignKey(
        GenericChoice,
        on_delete=models.SET_NULL,
        null=True,
        related_name='experience_choices'
    )
    project_count = models.ForeignKey(
        GenericChoice,
        on_delete=models.SET_NULL,
        null=True,
        related_name='project_count_choices'
    )
    employee_count = models.ForeignKey(
        GenericChoice,
        on_delete=models.SET_NULL,
        null=True,
        related_name='employee_count_choices'
    )

    telegram = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255)
    instagram = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)


class Partners(BaseModel, NameTranslation):
    logo = models.URLField()


class FAQ(BaseModel):
    question_uz = models.CharField(max_length=255)
    question_en = models.CharField(max_length=255)
    question_ru = models.CharField(max_length=255)

    answer_uz = models.TextField()
    answer_en = models.TextField()
    answer_ru = models.TextField()

    link = models.URLField()

    def __str__(self):
        return self.question_uz or " "
