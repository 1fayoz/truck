from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.extra_models import BaseModel
from apps.common.jwt import make_custom_jwt
from apps.common.utils import two_minutes_from_now, uz_phone_validator, inn_validator, passport_validator


class User(BaseModel):
    class Regions(models.IntegerChoices):
        TASHKENT_CITY = 1, _('Toshkent shahri')
        ANDIJAN = 2, _('Andijon')
        BUKHARA = 3, _('Buxoro')
        FERGHANA = 4, _('Fargʻona')
        JIZZAKH = 5, _('Jizzax')
        KHOREZM = 6, _('Xorazm')
        NAMANGAN = 7, _('Namangan')
        NAVOI = 8, _('Navoiy')
        KASHKADARYA = 9, _('Qashqadaryo')
        KARAKALPAKSTAN = 10, _('Qoraqalpogʻiston Respublikasi')
        SYRDARYA = 12, _('Sirdaryo')
        SURKHANDARYA = 13, _('Surxondaryo')
        TASHKENT_REGION = 14, _('Toshkent viloyati')

    class UserTypes(models.IntegerChoices):
        DRIVER = 1, _('Haydovchi')
        PERSON = 2, _('Yuridik shaxs')
        OTHER = 3, _('Boshqa')

    company = models.CharField(
        max_length=100, null=True, blank=True,
        verbose_name=_("Tashkilot nomi"),
    )
    type = models.SmallIntegerField(
        choices=UserTypes.choices, default=UserTypes.DRIVER,
        verbose_name=_("Foydalanuvchi turi"),
    )
    inn = models.CharField(
        max_length=100, null=True, blank=True,
        verbose_name=_("STIR"),
    )
    country = models.SmallIntegerField(
        choices=Regions.choices, null=True, blank=True,
        verbose_name=_("Hudud (viloyat)"),
    )
    trans_count = models.IntegerField(
        default=0, null=True, blank=True,
        verbose_name=_("Tashuvlar soni"),
    )
    rating = models.FloatField(
        default=0, null=True, blank=True,
        verbose_name=_("Reyting"),
    )
    phone = models.CharField(
        max_length=100,
        verbose_name=_("Telefon raqami"),
    )
    full_name = models.CharField(
        max_length=100,
        verbose_name=_("Toʻliq ism-sharif"),
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_("Faol"),
    )

    class Meta:
        verbose_name = _("Foydalanuvchi")
        verbose_name_plural = _("Foydalanuvchilar")

    @property
    def token(self):
        return make_custom_jwt(self.id)

    def __str__(self):
        return str(self.full_name)


class UserVerificationCode(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='verification',
        verbose_name=_("Foydalanuvchi"),
    )
    code = models.CharField(
        max_length=10,
        verbose_name=_("Tasdiqlash kodi"),
    )
    expires_at = models.DateTimeField(
        default=two_minutes_from_now,
        verbose_name=_("Amal qilish muddati"),
    )

    class Meta:
        verbose_name = _("Tasdiqlash kodi")
        verbose_name_plural = _("Tasdiqlash kodlari")

    def __str__(self):
        return f"{self.user} - {self.code}"


class PersonProfile(BaseModel):
    class Region(models.IntegerChoices):
        TASHKENT_CITY = 1, _('Toshkent shahri')
        ANDIJAN = 2, _('Andijon')
        BUKHARA = 3, _('Buxoro')
        FERGHANA = 4, _('Fargʻona')
        JIZZAKH = 5, _('Jizzax')
        KHOREZM = 6, _('Xorazm')
        NAMANGAN = 7, _('Namangan')
        NAVOI = 8, _('Navoiy')
        KASHKADARYA = 9, _('Qashqadaryo')
        KARAKALPAKSTAN = 10, _('Qoraqalpogʻiston Respublikasi')
        SYRDARYA = 12, _('Sirdaryo')
        SURKHANDARYA = 13, _('Surxondaryo')
        TASHKENT_REGION = 14, _('Toshkent viloyati')

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='person',
        verbose_name=_("Foydalanuvchi"),
    )

    birth_date = models.DateField(null=True, blank=True, verbose_name=_("Tugʻilgan sana"))
    passport_number = models.CharField(
        max_length=9, validators=[passport_validator], help_text="AA1234567",
        null=True, blank=True, verbose_name=_("Pasport seriyasi va raqami"),
    )
    passport_given_at = models.DateField(null=True, blank=True, verbose_name=_("Pasport berilgan sana"))
    passport_issuer = models.CharField(max_length=120, null=True, blank=True, verbose_name=_("Beruvchi organ"))

    region = models.SmallIntegerField(choices=Region.choices, null=True, blank=True, verbose_name=_("Viloyat"))
    district = models.CharField(max_length=120, null=True, blank=True, verbose_name=_("Tuman"))
    street = models.CharField(max_length=120, null=True, blank=True, verbose_name=_("Koʻcha"))
    house = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("Uy"))

    workplace_name = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("Ish joyi (tashkilot nomi)"))
    workplace_inn = models.CharField(max_length=12, null=True, blank=True, validators=[inn_validator], verbose_name=_("Ish joyi STIR"))
    years_of_experience = models.PositiveIntegerField(default=0, verbose_name=_("Ish tajribasi (yil)"))
    has_international_visa = models.BooleanField(default=False, verbose_name=_("Xalqaro viza mavjud"))
    extra_phone = models.CharField(max_length=20, validators=[uz_phone_validator], null=True, blank=True, verbose_name=_("Qoʻshimcha telefon"))

    class Meta:
        verbose_name = _("Jismoniy shaxs profili")
        verbose_name_plural = _("Jismoniy shaxs profillari")

    def __str__(self):
        return f"PersonProfile<{self.user.full_name}>"


class CompanyProfile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='company_profile',
        verbose_name=_("Foydalanuvchi"),
    )

    name = models.CharField(max_length=200, verbose_name=_("Tashkilot nomi"))
    registered_at = models.DateField(null=True, blank=True, verbose_name=_("Roʻyxatdan oʻtgan sana"))
    inn = models.CharField(max_length=12, validators=[inn_validator], verbose_name=_("STIR"))
    legal_address = models.CharField(max_length=255, verbose_name=_("Yuridik manzil"))

    director_full_name = models.CharField(max_length=150, verbose_name=_("Rahbarning F.I.Sh."))
    responsible_full_name = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("Masʼul vakil F.I.Sh."))

    phone = models.CharField(max_length=20, validators=[uz_phone_validator], verbose_name=_("Telefon raqami"))
    email = models.EmailField(null=True, blank=True, verbose_name=_("Elektron pochta"))
    website = models.URLField(null=True, blank=True, verbose_name=_("Veb-sayt"))

    employees_total = models.PositiveIntegerField(default=0, verbose_name=_("Umumiy xodimlar soni"))
    drivers_total = models.PositiveIntegerField(default=0, verbose_name=_("Haydovchilar soni"))
    stability_rating = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name=_("Barqarorlik reytingi (0–5)"),
    )

    class Meta:
        verbose_name = _("Tashkilot profili")
        verbose_name_plural = _("Tashkilot profillari")

    def __str__(self):
        return f"CompanyProfile<{self.name}>"


class Vehicle(BaseModel):
    class FuelType(models.IntegerChoices):
        PETROL = 1, _('Benzin')
        DIESEL = 2, _('Dizel')
        GAS = 3, _('Gaz')
        ELECTRIC = 4, _('Elektr')
        HYBRID = 5, _('Gibrid')

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='vehicles',
        verbose_name=_("Ega (foydalanuvchi)"),
    )

    brand = models.CharField(max_length=80, verbose_name=_("Avtomobil markasi"))
    model = models.CharField(max_length=80, verbose_name=_("Modeli"))
    plate_number = models.CharField(max_length=20, db_index=True, verbose_name=_("Davlat raqami"))
    manufactured_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1970), MaxValueValidator(timezone.now().year + 1)],
        verbose_name=_("Ishlab chiqarilgan yili"),
    )
    fuel = models.SmallIntegerField(choices=FuelType.choices, verbose_name=_("Yoqilgʻi turi"))

    tech_passport_number = models.CharField(max_length=50, verbose_name=_("Texnik pasport raqami"))
    insurance_policy_number = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Sugʻurta polisi raqami"))
    insurance_valid_until = models.DateField(null=True, blank=True, verbose_name=_("Sugʻurta amal qilish sanasi"))

    class Meta:
        verbose_name = _("Transport vositasi")
        verbose_name_plural = _("Transport vositalari")

    def __str__(self):
        return f"{self.plate_number} ({self.brand} {self.model})"


class Trailer(BaseModel):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name='trailers',
        verbose_name=_("Asosiy transport vositasi"),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='trailers',
        verbose_name=_("Ega (foydalanuvchi)"),
    )

    brand = models.CharField(max_length=80, verbose_name=_("Tirkama markasi"))
    model = models.CharField(max_length=80, verbose_name=_("Modeli"))
    plate_number = models.CharField(max_length=20, db_index=True, verbose_name=_("Davlat raqami"))
    manufactured_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1970), MaxValueValidator(timezone.now().year + 1)],
        verbose_name=_("Ishlab chiqarilgan yili"),
    )
    capacity_tons = models.DecimalField(
        max_digits=6, decimal_places=2, help_text='tonnada',
        verbose_name=_("Yuk ko‘tarish sig‘imi (t)"),
    )
    tech_passport_number = models.CharField(max_length=50, verbose_name=_("Texnik pasport raqami"))

    class Meta:
        verbose_name = _("Tirkama")
        verbose_name_plural = _("Tirkamalar")

    def __str__(self):
        return f"Trailer {self.plate_number} ({self.brand} {self.model})"


class CarrierPreference(BaseModel):
    class RouteScope(models.IntegerChoices):
        DOMESTIC = 1, _("Respublika bo‘yicha")
        INTERNATIONAL = 2, _("Xalqaro")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='preferences',
        verbose_name=_("Foydalanuvchi"),
    )
    scope = models.SmallIntegerField(choices=RouteScope.choices, verbose_name=_("Yo‘nalish turi"))

    primary_route_1 = models.CharField(max_length=150, verbose_name=_("Asosiy yo‘nalish 1"))
    primary_route_2 = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("Asosiy yo‘nalish 2"))
    primary_route_3 = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("Asosiy yo‘nalish 3"))

    international_routes = models.TextField(
        null=True, blank=True,
        help_text="Masalan: O'zbekiston–Qozog'iston; O'zbekiston–Rossiya ...",
        verbose_name=_("Xalqaro yo‘nalishlar"),
    )

    cargo_types = models.JSONField(
        default=list,
        help_text="CargoType qiymatlari ro‘yxati (masalan: [1,2,3])",
        verbose_name=_("Asosiy yuk turlari (ID ro‘yxati)"),
    )

    class Meta:
        verbose_name = _("Yuk tashish preferensiyasi")
        verbose_name_plural = _("Yuk tashish preferensiyalari")

    def __str__(self):
        return f"Preference<{self.user}>"


class Service(BaseModel):
    class ServiceStaus(models.IntegerChoices):  # yozilish saqlab qolindi
        active = 1, _('Faol')
        in_progress = 2, _('Jarayonda')
        completed = 3, _('Yakunlangan')

    icon = models.FileField(
        upload_to='icons', null=True, blank=True,
        verbose_name=_("Piktogramma"),
    )
    icon_name = models.CharField(
        max_length=100, null=True, blank=True,
        verbose_name=_("Piktogramma nomi"),
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("Xizmat nomi"),
    )
    des = models.TextField(
        verbose_name=_("Tavsif"),
    )
    status = models.SmallIntegerField(
        choices=ServiceStaus.choices,
        default=ServiceStaus.in_progress,
        max_length=100,  # mavjud kodga tegmadi
        verbose_name=_("Holat"),
    )

    class Meta:
        verbose_name = _("Xizmat")
        verbose_name_plural = _("Xizmatlar")


class UserDoc(models.Model):
    class DocumentType(models.IntegerChoices):
        PASSPORT = 1, _("Pasport nusxasi")
        DRIVER_LICENSE = 2, _("Haydovchilik guvohnomasi")
        VEHICLE_TECHPASSPORT = 3, _("Transport texnik pasporti")
        COMPANY_CERT = 4, _("Korxona guvohnomasi")
        PERMIT_DAZVOL = 5, _("Dazvol")
        LICENSE = 6, _("Litsenziya")
        INSURANCE = 7, _("Sug‘urta polis")
        OTHER = 8, _("Boshqa hujjat")

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='doc',
        verbose_name=_("Foydalanuvchi"),
    )
    file = models.FileField(upload_to='user_docs', null=True, blank=True, verbose_name=_("Fayl"))
    document_type = models.SmallIntegerField(choices=DocumentType.choices, verbose_name=_("Hujjat turi"))

    class Meta:
        verbose_name = _("Foydalanuvchi hujjati")
        verbose_name_plural = _("Foydalanuvchi hujjatlari")


class Consent(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='consent',
        verbose_name=_("Foydalanuvchi"),
    )
    charter_agreed = models.BooleanField(
        default=False,
        help_text="Uyushma Ustavini o‘qib, rozilik",
        verbose_name=_("«Uyushma Ustavini o‘qidim va roziman»"),
    )
    personal_data_processing = models.BooleanField(
        default=False,
        help_text="Shaxsiy maʼlumotlarni qayta ishlashga rozilik",
        verbose_name=_("«Shaxsiy maʼlumotlarimni qayta ishlashga roziman»"),
    )
    agreed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Tasdiqlangan vaqti"))

    class Meta:
        verbose_name = _("Rozilik")
        verbose_name_plural = _("Roziliklar")

    def clean(self):
        if (self.charter_agreed or self.personal_data_processing) and not self.agreed_at:
            self.agreed_at = timezone.now()

    def __str__(self):
        return f"Consent<{self.user}>"


class MembershipApplication(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='membership_applications',
        verbose_name=_("Foydalanuvchi"),
    )

    full_name = models.CharField(max_length=150, verbose_name=_("To‘liq ism-sharif"))
    phone = models.CharField(max_length=20, validators=[uz_phone_validator], verbose_name=_("Telefon raqami"))
    email = models.EmailField(null=True, blank=True, verbose_name=_("Elektron pochta"))

    address = models.CharField(max_length=255, verbose_name=_("Manzil"))
    note = models.TextField(null=True, blank=True, verbose_name=_("Izoh"))
    attachment = models.FileField(upload_to='applications', null=True, blank=True, verbose_name=_("Biriktirilgan fayl"))
    status = models.CharField(max_length=30, default='new', verbose_name=_("Holat"))

    class Meta:
        verbose_name = _("Aʼzolik arizasi")
        verbose_name_plural = _("Aʼzolik arizalari")

    def __str__(self):
        return f"MembershipApplication<{self.full_name}>"


class Docs(BaseModel):
    icon = models.FileField(upload_to='docs', verbose_name=_("Fayl"))
    name = models.CharField(max_length=555, verbose_name=_("Nom"))
    size = models.CharField(default=0, max_length=100, verbose_name=_("Hajm (MB)"))

    class Meta:
        verbose_name = _("Hujjat")
        verbose_name_plural = _("Hujjatlar")

    def save(self, *args, **kwargs):
        f = getattr(self, "icon", None)
        if f and hasattr(f, "size"):
            try:
                self.size = round(f.size / (1024 * 1024), 2)
            except Exception:
                pass
        super().save(*args, **kwargs)


class News(BaseModel):
    image = models.ImageField(upload_to='news', verbose_name=_("Rasm"))
    name = models.CharField(max_length=555, verbose_name=_("Sarlavha"))
    short_des = models.CharField(max_length=255, verbose_name=_("Qisqa taʼrif"))
    description = models.TextField(verbose_name=_("Matn"))

    class Meta:
        verbose_name = _("Yangilik")
        verbose_name_plural = _("Yangiliklar")


class Application(BaseModel):
    full_name = models.CharField(max_length=100, verbose_name=_("To‘liq ism-sharif"))
    phone = models.CharField(max_length=100, verbose_name=_("Telefon raqami"))
    email = models.EmailField(max_length=100, verbose_name=_("Elektron pochta"))
    address = models.CharField(max_length=100, verbose_name=_("Manzil"))
    text = models.TextField(null=True, blank=True, verbose_name=_("Matn"))
    file = models.FileField(upload_to='files', null=True, blank=True, verbose_name=_("Biriktirilgan fayl"))

    class Meta:
        verbose_name = _("Murojaat")
        verbose_name_plural = _("Murojaatlar")


class Employee(BaseModel):
    image = models.ImageField(upload_to='employee', verbose_name=_("Rasm"))
    full_name = models.CharField(max_length=100, verbose_name=_("F.I.Sh."))
    degree = models.CharField(max_length=100, verbose_name=_("Lavozim / daraja"))
    email = models.EmailField(max_length=100, verbose_name=_("Elektron pochta"))
    work_time_from = models.TimeField(verbose_name=_("Ish vaqti (dan)"))
    work_time_to = models.TimeField(verbose_name=_("Ish vaqti (gacha)"))

    class Meta:
        verbose_name = _("Xodim")
        verbose_name_plural = _("Xodimlar")
