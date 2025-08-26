import datetime

from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.forms.widgets import Textarea
from packaging.utils import _

from .models import User, Service, Docs, News, Application, Employee, Consent

# ---------- Umumiy qulayliklar ----------
admin.site.site_header = "Admin Panel"
admin.site.site_title = "Admin"
admin.site.index_title = "Boshqaruv"
admin.site.enable_nav_sidebar = True  # chapdagi filter paneli

TEXTAREA_OVERRIDES = {
    models.TextField: {'widget': Textarea(attrs={'rows': 4, 'style': 'width: 95%;'})}
}


# ---------- Custom ListFilterlar ----------
class RatingRangeFilter(admin.SimpleListFilter):
    title = "Reyting (oralig‘i)"
    parameter_name = "rating_range"

    def lookups(self, request, model_admin):
        return [
            ("lt2", "0 — 2"),
            ("2to4", "2 — 4"),
            ("gte4", "4 — 5"),
        ]

    def queryset(self, request, queryset):
        val = self.value()
        if val == "lt2":
            return queryset.filter(rating__lt=2)
        if val == "2to4":
            return queryset.filter(rating__gte=2, rating__lt=4)
        if val == "gte4":
            return queryset.filter(rating__gte=4)
        return queryset


class TransCountFilter(admin.SimpleListFilter):
    title = "Transaksiya soni"
    parameter_name = "trans_count_range"

    def lookups(self, request, model_admin):
        return [
            ("zero", "0"),
            ("1to10", "1 — 10"),
            ("gt10", "> 10"),
        ]

    def queryset(self, request, queryset):
        val = self.value()
        if val == "zero":
            return queryset.filter(trans_count=0)
        if val == "1to10":
            return queryset.filter(trans_count__gte=1, trans_count__lte=10)
        if val == "gt10":
            return queryset.filter(trans_count__gt=10)
        return queryset


# ---------- Helper: rasmlar preview ----------
def image_preview(obj, field_name, size=48):
    f = getattr(obj, field_name, None)
    if not f:
        return "—"
    try:
        url = f.url
    except Exception:
        return "—"
    return format_html(
        '<img src="{}" alt="{}" style="height:{}px;width:{}px;object-fit:cover;border-radius:6px;" />',
        url, getattr(obj, "name", "img"), size, size
    )


# ---------- User ----------

from django.contrib import admin
from .models import (
    User, PersonProfile, CompanyProfile, Vehicle, Trailer,
    CarrierPreference, Service, UserDoc, Consent, MembershipApplication
)

# ===============================
# USER bilan birga boshqa modellarni qulay boshqarish uchun InlineAdmin ishlatamiz
# ===============================

class PersonProfileInline(admin.StackedInline):
    model = PersonProfile
    extra = 0
    can_delete = False
    verbose_name = "Jismoniy shaxs profili"
    verbose_name_plural = "Jismoniy shaxs profili"


class CompanyProfileInline(admin.StackedInline):
    model = CompanyProfile
    extra = 0
    can_delete = False
    verbose_name = "Yuridik shaxs profili"
    verbose_name_plural = "Yuridik shaxs profili"


class VehicleInline(admin.TabularInline):
    model = Vehicle
    extra = 0
    verbose_name = "Transport vositasi"
    verbose_name_plural = "Transport vositalari"


class TrailerInline(admin.TabularInline):
    model = Trailer
    extra = 0
    verbose_name = "Tirkama"
    verbose_name_plural = "Tirkamalar"


class CarrierPreferenceInline(admin.StackedInline):
    model = CarrierPreference
    extra = 0
    verbose_name = "Yuk tashish preferensiyasi"
    verbose_name_plural = "Yuk tashish preferensiyalari"


class UserDocInline(admin.StackedInline):
    model = UserDoc
    extra = 0
    verbose_name = "Hujjat"
    verbose_name_plural = "Hujjatlar"


class ConsentInline(admin.StackedInline):
    model = Consent
    extra = 0
    verbose_name = "Rozilik"
    verbose_name_plural = "Rozilik"


class MembershipApplicationInline(admin.TabularInline):
    model = MembershipApplication
    extra = 0
    verbose_name = "A’zolik arizasi"
    verbose_name_plural = "A’zolik arizalari"




# ===============================
# ALOHIDA MODELLAR ADMINDA (agar kerak bo‘lsa alohida ko‘rsatish uchun)
# ===============================


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("owner", "plate_number", "brand", "model", "manufactured_year")
    search_fields = ("plate_number", "brand", "model")


# ===============================================
# ADMIN SOZLAMALARI (to'liq) – admin.py ichiga joylang
# ===============================================
from django.contrib import admin
from django import forms

# --- ModelFormlar: O'zbekcha yorliqlar, tartib va tekshiruvlar ---

class PersonProfileForm(forms.ModelForm):
    class Meta:
        model = PersonProfile
        fields = [
            # 1. Shaxsiy ma'lumotlar
            'birth_date', 'passport_number', 'passport_given_at', 'passport_issuer',
            # 2. Manzil
            'region', 'district', 'street', 'house',
            # 3. Ish joyi va tajriba
            'workplace_name', 'workplace_inn', 'years_of_experience', 'has_international_visa', 'extra_phone',
        ]
        labels = {
            'birth_date': "Tug'ilgan sana",
            'passport_number': "Pasport seriyasi va raqami",
            'passport_given_at': "Pasport berilgan sana",
            'passport_issuer': "Beruvchi organ",
            'region': "Viloyat",
            'district': "Tuman",
            'street': "Ko'cha",
            'house': "Uy",
            'workplace_name': "Ish joyi (tashkilot nomi)",
            'workplace_inn': "Ish joyi STIR",
            'years_of_experience': "Ish tajribasi (yil)",
            'has_international_visa': "Xalqaro viza mavjud",
            'extra_phone': "Qo'shimcha telefon",
        }


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            'name', 'registered_at', 'inn', 'legal_address',
            'director_full_name', 'responsible_full_name',
            'phone', 'email', 'website',
            'employees_total', 'drivers_total', 'stability_rating',
        ]
        labels = {
            'name': "Tashkilot nomi",
            'registered_at': "Ro'yxatdan o'tgan sana",
            'inn': "STIR",
            'legal_address': "Yuridik manzil",
            'director_full_name': "Rahbarning F.I.Sh.",
            'responsible_full_name': "Mas'ul vakil F.I.Sh.",
            'phone': "Telefon raqami",
            'email': "Elektron pochta",
            'website': "Veb-sayt",
            'employees_total': "Umumiy xodimlar soni",
            'drivers_total': "Haydovchilar soni",
            'stability_rating': "Barqarorlik reytingi (0–5)",
        }


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'brand', 'model', 'plate_number', 'manufactured_year', 'fuel',
            'tech_passport_number', 'insurance_policy_number', 'insurance_valid_until',
        ]
        labels = {
            'brand': "Avtomobil markasi",
            'model': "Modeli",
            'plate_number': "Davlat raqami",
            'manufactured_year': "Ishlab chiqarilgan yili",
            'fuel': "Yoqilg'i turi",
            'tech_passport_number': "Texnik pasport raqami",
            'insurance_policy_number': "Sug'urta polisi raqami",
            'insurance_valid_until': "Sug'urta amal qiladigan sana",
        }


class TrailerForm(forms.ModelForm):
    class Meta:
        model = Trailer
        fields = [
            'brand', 'model', 'plate_number', 'manufactured_year', 'capacity_tons', 'tech_passport_number',
        ]
        labels = {
            'brand': "Tirkama markasi",
            'model': "Modeli",
            'plate_number': "Davlat raqami",
            'manufactured_year': "Ishlab chiqarilgan yili",
            'capacity_tons': "Yuk ko'tarish sig'imi (t)",
            'tech_passport_number': "Texnik pasport raqami",
        }


class CarrierPreferenceForm(forms.ModelForm):
    class Meta:
        model = CarrierPreference
        fields = [
            'scope', 'primary_route_1', 'primary_route_2', 'primary_route_3', 'international_routes', 'cargo_types',
        ]
        labels = {
            'scope': "Yo'nalish turi",
            'primary_route_1': "Asosiy yo'nalish 1",
            'primary_route_2': "Asosiy yo'nalish 2",
            'primary_route_3': "Asosiy yo'nalish 3",
            'international_routes': "Xalqaro yo'nalishlar",
            'cargo_types': "Asosiy yuk turlari (ID ro'yxati)",
        }
        help_texts = {
            'cargo_types': "Masalan: [1,2,3] (CargoType qiymatlari)",
        }


class ConsentForm(forms.ModelForm):
    class Meta:
        model = Consent
        fields = ['charter_agreed', 'personal_data_processing', 'agreed_at']
        labels = {
            'charter_agreed': "\"Uyushma Ustavini o'qidim va roziman\"",
            'personal_data_processing': "\"Shaxsiy ma'lumotlarimni qayta ishlashga roziman\"",
            'agreed_at': "Tasdiqlangan vaqti",
        }


class MembershipApplicationForm(forms.ModelForm):
    class Meta:
        model = MembershipApplication
        fields = ['full_name', 'phone', 'email', 'address', 'note', 'attachment', 'status']
        labels = {
            'full_name': "To'liq ism-sharif",
            'phone': "Telefon raqami",
            'email': "Elektron pochta",
            'address': "Manzil",
            'note': "Izoh",
            'attachment': "Biriktirilgan fayl",
            'status': "Holat",
        }


# --- Inline-lar: User markazida hammasini bir joyda ko'rish/yaratish ---

class PersonProfileInline(admin.StackedInline):
    model = PersonProfile
    form = PersonProfileForm
    can_delete = False
    extra = 0
    fieldsets = (
        ("1. Shaxsiy ma'lumotlar", {
            'fields': ('birth_date', 'passport_number', 'passport_given_at', 'passport_issuer')
        }),
        ("2. Yashash manzili", {
            'fields': ('region', 'district', 'street', 'house')
        }),
        ("3. Ish joyi va tajriba", {
            'fields': ('workplace_name', 'workplace_inn', 'years_of_experience', 'has_international_visa', 'extra_phone')
        }),
    )


class CompanyProfileInline(admin.StackedInline):
    model = CompanyProfile
    form = CompanyProfileForm
    can_delete = False
    extra = 0
    fieldsets = (
        ("1. Tashkilot ma'lumotlari", {
            'fields': ('name', 'registered_at', 'inn', 'legal_address')
        }),
        ("2. Rahbar va mas'ul", {
            'fields': ('director_full_name', 'responsible_full_name')
        }),
        ("3. Aloqa", {
            'fields': ('phone', 'email', 'website')
        }),
        ("4. Statistika", {
            'fields': ('employees_total', 'drivers_total', 'stability_rating')
        }),
    )


class VehicleInline(admin.StackedInline):
    model = Vehicle
    form = VehicleForm
    extra = 0


class TrailerInline(admin.StackedInline):
    model = Trailer
    form = TrailerForm
    extra = 0


class CarrierPreferenceInline(admin.StackedInline):
    model = CarrierPreference
    form = CarrierPreferenceForm
    extra = 0


class UploadedDocumentInline(admin.TabularInline):
    model = UserDoc
    extra = 0
    fields = ('document_type', 'file',)


class ConsentInline(admin.StackedInline):
    model = Consent
    form = ConsentForm
    can_delete = False
    extra = 0
    readonly_fields = ('agreed_at',)


class MembershipApplicationInline(admin.TabularInline):
    model = MembershipApplication
    form = MembershipApplicationForm
    extra = 0


# --- User Admin: bir sahifada to'liq oqim ---

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "type", "is_active", "rating", "trans_count")
    list_filter = ("type", "is_active", "country")
    search_fields = ("full_name", "phone", "company", "inn")
    readonly_fields = ()

    fieldsets = (
        ("Asosiy ma'lumotlar", {
            'fields': ("full_name", "phone", "type", "company", "inn", "country", "rating", "trans_count", "is_active"),
            'description': "Foydalanuvchi tipi tanlangandan so'ng mos inline bloklar pastda ochiladi."
        }),
    )

    def get_inlines(self, request, obj=None):
        """
        Navbat/tartib: User.type ga qarab mos inlinelar ko'rsatiladi.
        DRIVER/Jismoniy uchun – PersonProfile, Vehicle, Trailer, CarrierPreference, UploadedDocument, Consent, MembershipApplication
        COMPANY (Yuridik) uchun – CompanyProfile, Vehicle, Trailer, CarrierPreference, UploadedDocument, Consent, MembershipApplication
        Boshqa – faqat Consent va UploadedDocument
        """
        base = [UploadedDocumentInline, ConsentInline, MembershipApplicationInline]
        if obj:
            if obj.type == User.UserTypes.DRIVER:
                return [PersonProfileInline, VehicleInline, TrailerInline, CarrierPreferenceInline] + base
            elif obj.type == User.UserTypes.PERSON:
                return [CompanyProfileInline, VehicleInline, TrailerInline, CarrierPreferenceInline] + base
            else:
                return base
        # Yangi yaratishda hali type aniq emas – minimal to'plam
        return base

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Yangi yaratilganda mos profilni avtomatik yaratib qo'yish (qulay oqim)
        if not change:
            if obj.type == User.UserTypes.DRIVER and not hasattr(obj, 'person'):
                PersonProfile.objects.create(user=obj)
            if obj.type == User.UserTypes.PERSON and not hasattr(obj, 'company_profile'):
                CompanyProfile.objects.create(user=obj, name=obj.company or obj.full_name, inn=obj.inn or '', legal_address='')
            if not hasattr(obj, 'consent'):
                Consent.objects.create(user=obj)


# --- Qolgan modellarning admini ---

@admin.register(PersonProfile)
class PersonProfileAdmin(admin.ModelAdmin):
    form = PersonProfileForm
    list_display = ("user", "birth_date", "passport_number", "region", "years_of_experience")
    list_filter = ("region", "has_international_visa")
    search_fields = ("user__full_name", "passport_number", "district", "street")
    fieldsets = (
        ("1. Shaxsiy ma'lumotlar", {'fields': ('user', 'birth_date', 'passport_number', 'passport_given_at', 'passport_issuer')}),
        ("2. Yashash manzili", {'fields': ('region', 'district', 'street', 'house')}),
        ("3. Ish joyi va tajriba", {'fields': ('workplace_name', 'workplace_inn', 'years_of_experience', 'has_international_visa', 'extra_phone')}),
    )


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    form = CompanyProfileForm
    list_display = ("name", "inn", "phone", "employees_total", "drivers_total", "stability_rating")
    list_filter = ("registered_at",)
    search_fields = ("name", "inn", "director_full_name")
    fieldsets = (
        ("1. Tashkilot ma'lumotlari", {'fields': ('user', 'name', 'registered_at', 'inn', 'legal_address')}),
        ("2. Rahbar va mas'ul", {'fields': ('director_full_name', 'responsible_full_name')}),
        ("3. Aloqa", {'fields': ('phone', 'email', 'website')}),
        ("4. Statistika", {'fields': ('employees_total', 'drivers_total', 'stability_rating')}),
    )


@admin.register(Trailer)
class TrailerAdmin(admin.ModelAdmin):
    form = TrailerForm
    list_display = ("vehicle", "plate_number", "brand", "model", "capacity_tons")
    search_fields = ("plate_number", "brand", "model", "vehicle__plate_number")


@admin.register(CarrierPreference)
class CarrierPreferenceAdmin(admin.ModelAdmin):
    form = CarrierPreferenceForm
    list_display = ("user", "scope", "primary_route_1")
    list_filter = ("scope",)


@admin.register(UserDoc)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ("user", "document_type", )
    list_filter = ("document_type",)
    autocomplete_fields = ("user",)


@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    form = ConsentForm
    list_display = ("user", "charter_agreed", "personal_data_processing", "agreed_at")
    readonly_fields = ("agreed_at",)


@admin.register(MembershipApplication)
class MembershipApplicationAdmin(admin.ModelAdmin):
    form = MembershipApplicationForm
    list_display = ("user", "full_name", "phone", "status")
    list_filter = ("status",)
    search_fields = ("full_name", "phone", "user__full_name")



# ---------- Service ----------
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    def icon_thumb(self, obj):
        return image_preview(obj, "icon", size=36)
    icon_thumb.short_description = "Icon"

    list_display = ("icon_thumb", "name", "status")
    list_filter = ("status",)
    search_fields = ("name", "des")
    ordering = ("status", "name")
    list_editable = ("status",)
    list_per_page = 25
    formfield_overrides = TEXTAREA_OVERRIDES
    readonly_fields = ("icon_preview",)

    def icon_preview(self, obj):
        return image_preview(obj, "icon", size=96)

    fieldsets = (
        ("Xizmat", {"fields": ("name", "status")}),
        ("Ikon", {"fields": ("icon", "icon_preview")}),
        ("Tavsif", {"fields": ("des",)}),
    )


# ---------- Docs ----------
@admin.register(Docs)
class DocsAdmin(admin.ModelAdmin):
    def file_link(self, obj):
        f = getattr(obj, "icon", None)
        if not f:
            return "—"
        try:
            url = f.url
        except Exception:
            return "—"
        return format_html('<a href="{}" target="_blank">Yuklab olish</a>', url)
    file_link.short_description = "Fayl"

    list_display = ("name", "size", "file_link")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 25
    readonly_fields = ("size",)


    # Fayl o‘lchamini qayta hisoblash (ixtiyoriy action)
    @admin.action(description="Fayl hajmini (bayt) `size` ga yozish")
    def recalc_size(self, request, queryset):
        updated = 0
        for obj in queryset:
            f = getattr(obj, "icon", None)
            try:
                obj.size = str(f.size)  # baytda
                obj.save(update_fields=["size"])
                updated += 1
            except Exception:
                pass
        self.message_user(request, f"Yangilandi: {updated} ta obyekt.")
    actions = ["recalc_size"]


# ---------- News ----------
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    def image_thumb(self, obj):
        return image_preview(obj, "image", size=56)
    image_thumb.short_description = "Rasm"

    list_display = ("image_thumb", "name", "short_des_trunc")
    search_fields = ("name", "short_des", "description")
    ordering = ("-id",)
    list_per_page = 25
    formfield_overrides = TEXTAREA_OVERRIDES
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        return image_preview(obj, "image", size=160)

    def short_des_trunc(self, obj):
        txt = (obj.short_des or "").strip()
        return (txt[:80] + "…") if len(txt) > 80 else txt
    short_des_trunc.short_description = "Qisqa tavsif"

    fieldsets = (
        ("Yangilik", {"fields": ("name", "short_des")}),
        ("Kontent", {"fields": ("description",)}),
        ("Rasm", {"fields": ("image", "image_preview")}),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    def file_link(self, obj):
        if obj.file:
            try:
                return format_html('<a href="{}" target="_blank">Faylni ochish</a>', obj.file.url)
            except Exception:
                return "—"
        return "—"
    file_link.short_description = "Fayl"

    list_display = ("full_name", "phone", "email", "address", "short_text", "file_link")
    search_fields = ("full_name", "phone", "email", "address", "text")
    list_filter = ("created_at",)  # BaseModel’da `created_at` bo‘lsa
    ordering = ("-id",)
    list_per_page = 25
    readonly_fields = ("file_preview",)

    def short_text(self, obj):
        if not obj.text:
            return "—"
        return (obj.text[:60] + "…") if len(obj.text) > 60 else obj.text
    short_text.short_description = "Matn"

    def file_preview(self, obj):
        if obj.file:
            try:
                url = obj.file.url
            except Exception:
                return "—"
            return format_html('<a href="{}" target="_blank">📎 Faylni ko‘rish</a>', url)
        return "—"

    fieldsets = (
        ("Ariza ma’lumotlari", {
            "fields": ("full_name", "phone", "email", "address")
        }),
        ("Qo‘shimcha", {
            "fields": ("text", "file", "file_preview")
        }),
    )




@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "image_thumb",
        "full_name",
        "degree",
        "email",
        "work_time_range",
        "total_hours",
    )
    search_fields = ("full_name", "degree", "email")
    ordering = ("full_name",)
    list_per_page = 25
    readonly_fields = ("image_preview_field",)

    @staticmethod
    def image_preview(obj, field_name, size=120):
        f = getattr(obj, field_name, None)
        if not f:
            return "—"
        try:
            url = f.url
        except Exception:
            return "—"
        return format_html(
            '<img src="{}" style="height:{}px;width:{}px;object-fit:cover;'
            'border-radius:8px;box-shadow:0 0 4px rgba(0,0,0,0.2);" />',
            url, size, size
        )

    # --- Rasm prevyu
    def image_thumb(self, obj):
        return self.image_preview(obj, "image", size=48)
    image_thumb.short_description = "Rasm"

    def image_preview_field(self, obj):
        return self.image_preview(obj, "image", size=160)
    image_preview_field.short_description = "Rasm (ko‘rish)"

    # --- Vaqtlar
    def work_time_range(self, obj):
        return f"{obj.work_time_from.strftime('%H:%M')} — {obj.work_time_to.strftime('%H:%M')}"
    work_time_range.short_description = "Ish vaqti"

    def total_hours(self, obj):
        today = datetime.date.today()
        start = datetime.datetime.combine(today, obj.work_time_from)
        end = datetime.datetime.combine(today, obj.work_time_to)
        if end <= start:
            end += datetime.timedelta(days=1)  # agar tunda kesib o‘tsa
        diff = end - start
        hours = diff.total_seconds() / 3600
        return f"{hours:.1f} soat"
    total_hours.short_description = "Umumiy soat"

    # --- Fieldset
    fieldsets = (
        ("Xodim ma’lumotlari", {
            "fields": ("image", "image_preview_field", "full_name", "degree", "email")
        }),
        ("Ish vaqti", {
            "fields": ("work_time_from", "work_time_to")
        }),
    )