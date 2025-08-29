import datetime

from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from .models import (
    Docs,
    News,
    Application,
    Employee,
    User,
    PersonProfile,
    CompanyProfile,
    Vehicle,
    Trailer,
    CarrierPreference,
    Service,
    UserDoc,
    Consent,
    MembershipApplication,
)

admin.site.site_header = "Admin Panel"
admin.site.site_title = "Admin"
admin.site.index_title = "Boshqaruv"
admin.site.enable_nav_sidebar = True

TEXTAREA_OVERRIDES = {
    models.TextField: {"widget": admin.widgets.AdminTextareaWidget(attrs={"rows": 4, "style": "width:95%;"})}
}


class RatingRangeFilter(admin.SimpleListFilter):
    title = "Reyting (oralig‘i)"
    parameter_name = "rating_range"

    def lookups(self, request, model_admin):
        return [("lt2", "0 — 2"), ("2to4", "2 — 4"), ("gte4", "4 — 5")]

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
        return [("zero", "0"), ("1to10", "1 — 10"), ("gt10", "> 10")]

    def queryset(self, request, queryset):
        val = self.value()
        if val == "zero":
            return queryset.filter(trans_count=0)
        if val == "1to10":
            return queryset.filter(trans_count__gte=1, trans_count__lte=10)
        if val == "gt10":
            return queryset.filter(trans_count__gt=10)
        return queryset


def image_preview(obj, field_name, size=48, rounded=6):
    f = getattr(obj, field_name, None)
    if not f:
        return "—"
    try:
        url = f.url
    except Exception:
        return "—"
    return format_html(
        '<img src="{}" alt="preview" style="height:{}px;width:{}px;object-fit:cover;border-radius:{}px;" />',
        url,
        size,
        size,
        rounded,
    )


class PersonProfileInline(admin.StackedInline):
    model = PersonProfile
    extra = 0
    can_delete = False


class CompanyProfileInline(admin.StackedInline):
    model = CompanyProfile
    extra = 0
    can_delete = False


class VehicleInline(admin.TabularInline):
    model = Vehicle
    extra = 0


class TrailerInline(admin.TabularInline):
    model = Trailer
    extra = 0


class CarrierPreferenceInline(admin.StackedInline):
    model = CarrierPreference
    extra = 0


class UploadedDocumentInline(admin.TabularInline):
    model = UserDoc
    extra = 0
    fields = ("document_type", "file")



class MembershipApplicationInline(admin.TabularInline):
    model = MembershipApplication
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "phone",
        "type",
        "country",
        "is_active",
        "rating",
        "trans_count",
    )
    list_filter = ("type", "is_active", "country", RatingRangeFilter, TransCountFilter)
    search_fields = ("full_name", "phone", "company", "inn")

    fieldsets = (
        (
            "Asosiy ma'lumotlar",
            {
                "fields": (
                    "full_name",
                    "phone",
                    "type",
                    "company",
                    "inn",
                    "country",
                    "rating",
                    "trans_count",
                    "is_active",
                )
            },
        ),
    )

    def get_inlines(self, request, obj=None):
        base = [UploadedDocumentInline, MembershipApplicationInline]
        if obj:
            if obj.type == User.UserTypes.DRIVER:
                return [PersonProfileInline, VehicleInline, TrailerInline, CarrierPreferenceInline] + base
            if obj.type == User.UserTypes.PERSON:
                return [CompanyProfileInline, VehicleInline, TrailerInline, CarrierPreferenceInline] + base
        return base

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            if obj.type == User.UserTypes.DRIVER and not hasattr(obj, "person"):
                PersonProfile.objects.create(user=obj)
            if obj.type == User.UserTypes.PERSON and not hasattr(obj, "company_profile"):
                CompanyProfile.objects.create(user=obj, name=obj.company or obj.full_name, inn=obj.inn or "", legal_address="")
            if not hasattr(obj, "consent"):
                Consent.objects.create(user=obj)


# @admin.register(PersonProfile)
# class PersonProfileAdmin(admin.ModelAdmin):
#     list_display = ("user", "region", "district", "workplace_name", "years_of_experience", "has_international_visa")
#     list_filter = ("region", "has_international_visa")
#     search_fields = ("user__full_name", "district", "street", "workplace_name", "workplace_inn")
#
#
# @admin.register(CompanyProfile)
# class CompanyProfileAdmin(admin.ModelAdmin):
#     list_display = ("user", "name", "inn", "phone", "employees_total", "drivers_total", "stability_rating")
#     list_filter = ("stability_rating",)
#     search_fields = ("name", "inn", "phone", "director_full_name", "responsible_full_name")
#     formfield_overrides = TEXTAREA_OVERRIDES
#
#
# @admin.register(Vehicle)
# class VehicleAdmin(admin.ModelAdmin):
#     list_display = ("owner", "plate_number", "brand", "model", "manufactured_year", "fuel")
#     list_filter = ("fuel", "manufactured_year")
#     search_fields = ("plate_number", "brand", "model", "owner__full_name")
#
#
# @admin.register(Trailer)
# class TrailerAdmin(admin.ModelAdmin):
#     list_display = ("user", "vehicle", "plate_number", "brand", "model", "manufactured_year", "capacity_tons")
#     list_filter = ("manufactured_year",)
#     search_fields = ("plate_number", "brand", "model", "user__full_name", "vehicle__plate_number")
#
#
# @admin.register(CarrierPreference)
# class CarrierPreferenceAdmin(admin.ModelAdmin):
#     list_display = ("user", "scope", "primary_route_1", "primary_route_2", "primary_route_3")
#     list_filter = ("scope",)
#     search_fields = ("user__full_name", "primary_route_1", "primary_route_2", "primary_route_3", "international_routes")
#     formfield_overrides = TEXTAREA_OVERRIDES


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

    def icon_preview(self, obj):
        return image_preview(obj, "icon", size=120)

    icon_preview.short_description = "Icon"

    readonly_fields = ("icon_preview",)
    fieldsets = (("Xizmat", {"fields": ("name", "status")}), ("Ikon", {"fields": ("icon", "icon_preview")}), ("Tavsif", {"fields": ("des",)}))


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

    @admin.action(description="Fayl hajmini MB ga qayta hisoblash")
    def recalc_size_mb(self, request, queryset):
        updated = 0
        for obj in queryset:
            f = getattr(obj, "icon", None)
            try:
                obj.size = str(round(f.size / (1024 * 1024), 2))
                obj.save(update_fields=["size"])
                updated += 1
            except Exception:
                pass
        self.message_user(request, f"Yangilandi: {updated} ta obyekt.")

    actions = ["recalc_size_mb"]


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

    def image_preview_field(self, obj):
        return image_preview(obj, "image", size=160)

    image_preview_field.short_description = "Rasm"

    def short_des_trunc(self, obj):
        txt = (obj.short_des or "").strip()
        return (txt[:80] + "…") if len(txt) > 80 else txt

    short_des_trunc.short_description = "Qisqa tavsif"

    readonly_fields = ("image_preview_field",)
    fieldsets = (("Yangilik", {"fields": ("name", "short_des")}), ("Kontent", {"fields": ("description",)}), ("Rasm", {"fields": ("image", "image_preview_field")}))


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
    ordering = ("-id",)
    list_per_page = 25

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

    readonly_fields = ("file_preview",)
    fieldsets = (("Ariza ma’lumotlari", {"fields": ("full_name", "phone", "email", "address")}), ("Qo‘shimcha", {"fields": ("text", "file", "file_preview")}))


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("image_thumb", "full_name", "degree", "email", "work_time_range", "total_hours", 'created_at')
    search_fields = ("full_name", "degree", "email")
    ordering = ("full_name",)
    list_per_page = 25

    def image_thumb(self, obj):
        return image_preview(obj, "image", size=48)

    image_thumb.short_description = "Rasm"

    def image_preview_field(self, obj):
        return image_preview(obj, "image", size=160)

    image_preview_field.short_description = "Rasm"

    def work_time_range(self, obj):
        return f"{obj.work_time_from.strftime('%H:%M')} — {obj.work_time_to.strftime('%H:%M')}"

    work_time_range.short_description = "Ish vaqti"

    def total_hours(self, obj):
        today = datetime.date.today()
        start = datetime.datetime.combine(today, obj.work_time_from)
        end = datetime.datetime.combine(today, obj.work_time_to)
        if end <= start:
            end += datetime.timedelta(days=1)
        diff = end - start
        hours = diff.total_seconds() / 3600
        return f"{hours:.1f} soat"

    total_hours.short_description = "Umumiy soat"

    readonly_fields = ("image_preview_field",)
    fieldsets = (("Xodim ma’lumotlari", {"fields": ("image", "image_preview_field", "full_name", "degree", "email")}), ("Ish vaqti", {"fields": ("work_time_from", "work_time_to")}))
