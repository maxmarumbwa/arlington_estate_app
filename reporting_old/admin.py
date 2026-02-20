from django.contrib import admin
from .models import (
    Community,
    Profile,
    ViolationType,
    PropertyReport,
    ReportImage,
    ReportComment,
)


# ==============================
# COMMUNITY
# ==============================


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_email", "contact_phone")
    search_fields = ("name", "contact_email")


# ==============================
# PROFILE
# ==============================


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_type", "house_number", "phone")
    list_filter = ("user_type",)
    search_fields = ("user__username", "house_number")


# ==============================
# VIOLATION TYPE
# ==============================


@admin.register(ViolationType)
class ViolationTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "fine_amount", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name",)


# ==============================
# INLINE IMAGES
# ==============================


class ReportImageInline(admin.TabularInline):
    model = ReportImage
    extra = 1


class ReportCommentInline(admin.TabularInline):
    model = ReportComment
    extra = 1


# ==============================
# PROPERTY REPORT
# ==============================


@admin.register(PropertyReport)
class PropertyReportAdmin(admin.ModelAdmin):
    list_display = (
        "report_id",
        "house_number",
        "violation",
        "status",
        "fine_amount",
        "fine_paid",
        "created_at",
    )
    list_filter = ("status", "fine_paid", "violation")
    search_fields = ("house_number", "report_id")
    readonly_fields = ("report_id", "created_at")

    inlines = [ReportImageInline, ReportCommentInline]


# ==============================
# REPORT IMAGE
# ==============================


@admin.register(ReportImage)
class ReportImageAdmin(admin.ModelAdmin):
    list_display = ("report", "uploaded_at")


# ==============================
# REPORT COMMENT
# ==============================


@admin.register(ReportComment)
class ReportCommentAdmin(admin.ModelAdmin):
    list_display = ("report", "user", "created_at")
    search_fields = ("user__username",)
