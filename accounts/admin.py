from django.contrib import admin
from .models import Stand, Resident


# ==============================
# STAND
# ==============================
@admin.register(Stand)
class StandAdmin(admin.ModelAdmin):
    list_display = (
        "stand_numb",
        "street",
        "cluster",
        "cluster_na",
        "dev_status",
        "latitude",
        "longitude",
    )
    search_fields = ("stand_numb", "street", "cluster_na")
    list_filter = ("dev_status", "cluster")
    ordering = ("stand_numb",)


# ==============================
# RESIDENT
# ==============================
@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "stand",
        "phone",
        "alternative_phone",
        "email",
        "profile_photo",
    )
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "phone",
        "alternative_phone",
        "email",
    )
    list_filter = ("stand__cluster",)
