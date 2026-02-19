from django.urls import path
from . import views

urlpatterns = [
    path("", views.report_list, name="report_list"),
    path("report/<uuid:report_id>/", views.report_detail, name="report_detail"),
    path("report/create/", views.report_create, name="report_create"),
    path("dashboard/", views.resident_dashboard, name="resident_dashboard"),
]
