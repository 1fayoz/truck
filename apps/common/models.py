from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from apps.common.extra_models import BaseModel
from apps.common.utils import two_minutes_from_now, uz_phone_validator, inn_validator, passport_validator


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


class PersonProfile(BaseModel):
    class Region(models.IntegerChoices):
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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')


    birth_date = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=9, validators=[passport_validator], help_text="AA1234567", null=True, blank=True)
    passport_given_at = models.DateField(null=True, blank=True)
    passport_issuer = models.CharField(max_length=120, null=True, blank=True)


    region = models.SmallIntegerField(choices=Region.choices, null=True, blank=True)
    district = models.CharField(max_length=120, null=True, blank=True)
    street = models.CharField(max_length=120, null=True, blank=True)
    house = models.CharField(max_length=30, null=True, blank=True)


    workplace_name = models.CharField(max_length=150, null=True, blank=True)
    workplace_inn = models.CharField(max_length=12, null=True, blank=True, validators=[inn_validator])
    years_of_experience = models.PositiveIntegerField(default=0)
    has_international_visa = models.BooleanField(default=False)
    extra_phone = models.CharField(max_length=20, validators=[uz_phone_validator], null=True, blank=True)


    def __str__(self):
        return f"PersonProfile<{self.user.full_name}>"

class CompanyProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')


    name = models.CharField(max_length=200)
    registered_at = models.DateField(null=True, blank=True)
    inn = models.CharField(max_length=12, validators=[inn_validator])
    legal_address = models.CharField(max_length=255)


    director_full_name = models.CharField(max_length=150)
    responsible_full_name = models.CharField(max_length=150, null=True, blank=True)


    phone = models.CharField(max_length=20, validators=[uz_phone_validator])
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)


    employees_total = models.PositiveIntegerField(default=0)
    drivers_total = models.PositiveIntegerField(default=0)
    stability_rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])


    def __str__(self):
        return f"CompanyProfile<{self.name}>"



class Vehicle(BaseModel):
    class FuelType(models.IntegerChoices):
        PETROL = 1, 'Benzin'
        DIESEL = 2, 'Dizel'
        GAS = 3, 'Gaz'
        ELECTRIC = 4, 'Elektr'
        HYBRID = 5, 'Gibrid'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')

    brand = models.CharField(max_length=80)
    model = models.CharField(max_length=80)
    plate_number = models.CharField(max_length=20, db_index=True)
    manufactured_year = models.PositiveIntegerField(validators=[MinValueValidator(1970), MaxValueValidator(timezone.now().year + 1)])
    fuel = models.SmallIntegerField(choices=FuelType.choices)

    tech_passport_number = models.CharField(max_length=50)
    insurance_policy_number = models.CharField(max_length=50, null=True, blank=True)
    insurance_valid_until = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.plate_number} ({self.brand} {self.model})"


class Trailer(BaseModel):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='trailers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trailers')

    brand = models.CharField(max_length=80)
    model = models.CharField(max_length=80)
    plate_number = models.CharField(max_length=20, db_index=True)
    manufactured_year = models.PositiveIntegerField(validators=[MinValueValidator(1970), MaxValueValidator(timezone.now().year + 1)])
    capacity_tons = models.DecimalField(max_digits=6, decimal_places=2, help_text='tonnada')
    tech_passport_number = models.CharField(max_length=50)


    def __str__(self):
        return f"Trailer {self.plate_number} ({self.brand} {self.model})"


class CarrierPreference(BaseModel):
    class RouteScope(models.IntegerChoices):
        DOMESTIC = 1, 'Respublika bo\'yicha'
        INTERNATIONAL = 2, 'Xalqaro'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    scope = models.SmallIntegerField(choices=RouteScope.choices)

    primary_route_1 = models.CharField(max_length=150)
    primary_route_2 = models.CharField(max_length=150, null=True, blank=True)
    primary_route_3 = models.CharField(max_length=150, null=True, blank=True)

    international_routes = models.TextField(null=True, blank=True, help_text="Masalan: O'zbekiston–Qozog'iston; O'zbekiston–Rossiya ...")

    cargo_types = models.JSONField(default=list, help_text="CargoType qiymatlari ro'yxati (masalan: [1,2,3])")


    class Meta:
        verbose_name = "Yuk tashish preferensiyasi"
        verbose_name_plural = "Yuk tashish preferensiyalari"


    def __str__(self):
        return f"Preference<{self.user}>"

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

class UserDoc(models.Model):
    class DocumentType(models.IntegerChoices):
        PASSPORT = 1, 'Pasport nusxasi'
        DRIVER_LICENSE = 2, 'Haydovchilik guvohnomasi'
        VEHICLE_TECHPASSPORT = 3, 'Transport texnik pasporti'
        COMPANY_CERT = 4, 'Korxona guvohnomasi'
        PERMIT_DAZVOL = 5, 'Dazvol'
        LICENSE = 6, 'Litsenziya'
        INSURANCE = 7, 'Sug\'urta polis'
        OTHER = 8, 'Boshqa hujjat'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doc')
    file = models.FileField(upload_to='user_docs', null=True, blank=True)
    document_type = models.SmallIntegerField(choices=DocumentType.choices)

class Consent(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consent')
    charter_agreed = models.BooleanField(default=False, help_text="Uyushma Ustavini o'qib, rozilik")
    personal_data_processing = models.BooleanField(default=False, help_text="Shaxsiy ma'lumotlarni qayta ishlashga rozilik")
    agreed_at = models.DateTimeField(null=True, blank=True)


    def clean(self):
        if (self.charter_agreed or self.personal_data_processing) and not self.agreed_at:
            self.agreed_at = timezone.now()

    def __str__(self):
        return f"Consent<{self.user}>"


class MembershipApplication(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='membership_applications')


    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, validators=[uz_phone_validator])
    email = models.EmailField(null=True, blank=True)

    address = models.CharField(max_length=255)
    note = models.TextField(null=True, blank=True)
    attachment = models.FileField(upload_to='applications', null=True, blank=True)
    status = models.CharField(max_length=30, default='new')


    def __str__(self):
        return f"MembershipApplication<{self.full_name}>"


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
