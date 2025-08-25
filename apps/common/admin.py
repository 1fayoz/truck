import datetime

from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.forms.widgets import Textarea

from .models import User, Service, Docs, News, Application, Employee

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
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "full_name", "company", "inn", "country", "phone",
        "trans_count", "rating",
    )
    list_filter = (
        "country",
        RatingRangeFilter,
        TransCountFilter,
        # Agar BaseModel’da created_at bo‘lsa, quyidagini oching:
        # ("created_at",)
    )
    search_fields = ("full_name", "company", "inn", "phone")
    ordering = ("-rating", "full_name")
    list_per_page = 25
    formfield_overrides = TEXTAREA_OVERRIDES
    # Tez tahrirlash uchun:
    list_editable = ("rating", )
    # Detal sahifada maydon tartibi:
    fieldsets = (
        ("Asosiy ma’lumot", {
            "fields": ("full_name", "company", "inn", "phone", "country")
        }),
        ("Statistika", {
            "fields": ("trans_count", "rating"),
        }),
    )


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

# ---- Forma: vaqtlar mantiqiyligini tekshirish
class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        t_from = cleaned.get("work_time_from")
        t_to = cleaned.get("work_time_to")
        # Agar tungi smena kerak bo'lmasa, oddiy tekshirish:
        if t_from and t_to and t_from >= t_to:
            raise forms.ValidationError(
                _("'work_time_from' 'work_time_to'dan kichik bo‘lishi kerak.")
            )
        return cleaned



@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeAdminForm

    # --- Ko‘rinishlar
    list_display = (
        "full_name",
        "degree",
        "email",
        "work_time_range",
        "total_hours",
    )
    search_fields = ("full_name", "degree", "email")
    ordering = ("full_name",)
    list_per_page = 25

    def work_time_range(self, obj):
        return f"{obj.work_time_from.strftime('%H:%M')} — {obj.work_time_to.strftime('%H:%M')}"
    work_time_range.short_description = "Ish vaqti"

    def total_hours(self, obj):
        dt = datetime.datetime
        today = datetime.date.today()
        start = dt.combine(today, obj.work_time_from)
        end = dt.combine(today, obj.work_time_to)
        diff = end - start
        hours = diff.total_seconds() / 3600
        return f"{hours:.1f} soat"
    total_hours.short_description = "Umumiy soat"

    fieldsets = (
        ("Xodim ma’lumotlari", {
            "fields": ("full_name", "degree", "email")
        }),
        ("Ish vaqti", {
            "fields": ("work_time_from", "work_time_to")
        }),
    )
