from django.db import models

from apps.common.extra_models import BaseModel
from apps.common.utils import two_minutes_from_now


class User(BaseModel):
    class Regions(models.IntegerChoices):
        TASHKENT_CITY = 1, 'Toshkent shahri'
        ANDIJAN = 2, 'Andijon'
        BUKHARA = 3, 'Buxoro'
        FERGHANA = 4, 'Fargʻona'
        JIZZAKH = 5, 'Jizzax'
        KHOREZM = 6, 'Xorazm'
        NAMANGAN = 7, 'Namangan'
        NAVOI = 8, 'Navoiy'
        KASHKADARYA = 9, 'Qashqadaryo'
        KARAKALPAKSTAN = 10, 'Qoraqalpogʻiston Respublikasi'
        SYRDARYA = 12, 'Sirdaryo'
        SURKHANDARYA = 13, 'Surxondaryo'
        TASHKENT_REGION = 14, 'Toshkent viloyati'

    class UserTypes(models.IntegerChoices):
        DRIVER = 1, 'Haydovchi'
        PERSON = 2, 'Yuridik Shaxs'
        OTHER = 3, 'Boshqa'

    company = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    type = models.SmallIntegerField(
        choices=UserTypes.choices,
        default=UserTypes.DRIVER,
    )
    inn = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    country = models.SmallIntegerField(
        choices=Regions.choices,
        max_length=100,
        null=True,
        blank=True,
    )
    trans_count = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    rating = models.FloatField(
        default=0,
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=100,
    )
    full_name = models.CharField(
        max_length=100,
    )
    is_active = models.BooleanField(
        default=False,
    )


    def __str__(self):
        return str(self.full_name)

class UserVerificationCode(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='verification',
    )
    code = models.CharField(
        max_length=10,
    )
    expires_at = models.DateTimeField(
        default=two_minutes_from_now,
    )

    def __str__(self):
        return f"{self.user} - {self.code}"


class Service(BaseModel):
    class ServiceStaus(models.IntegerChoices):
        active = 1, 'Active'
        in_progress = 2, 'In-Progress'
        completed = 3, 'Completed'

    icon = models.ImageField(
        upload_to='icons',
        null=True,
        blank=True,
    )
    icon_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=100,
    )
    des = models.TextField(

    )
    status = models.SmallIntegerField(
        choices=ServiceStaus.choices,
        default=ServiceStaus.in_progress,
        max_length=100,
    )

class Docs(BaseModel):
    icon = models.FileField(
        upload_to='docs',
    )
    name = models.CharField(
        max_length=100,
    )
    size = models.CharField(
        default=0,
        max_length=100,
    )

    def save(self, *args, **kwargs):
        f = getattr(self, "icon", None)
        if f and hasattr(f, "size"):
            try:
                self.size = round(f.size / (1024 * 1024), 2)
            except Exception:
                pass
        super().save(*args, **kwargs)

class News(BaseModel):
    image = models.ImageField(
        upload_to='news',
    )
    name = models.CharField(
        max_length=100,
    )
    short_des = models.CharField(
        max_length=255,
    )
    description = models.TextField(
    )


class Application(BaseModel):
    full_name = models.CharField(
        max_length=100,
    )
    phone = models.CharField(
        max_length=100,
    )
    email = models.EmailField(
        max_length=100,
    )
    address = models.CharField(
        max_length=100,
    )
    text = models.TextField(
        null=True,
        blank=True,
    )
    file = models.FileField(
        upload_to='files',
        null=True,
        blank=True,
    )

class Employee(BaseModel):
    image = models.ImageField(
        upload_to='employee',
    )
    full_name = models.CharField(
        max_length=100,
    )
    degree = models.CharField(
        max_length=100,
    )
    email = models.EmailField(
        max_length=100,
    )
    work_time_from = models.TimeField()
    work_time_to = models.TimeField()
