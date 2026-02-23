from django.urls import path
from . import views
from reporting import views as reporting_views

urlpatterns = [
    path("", views.report_list, name="report_list"),
    path("report/<uuid:report_id>/", views.report_detail, name="report_detail"),
    path("report/create/", views.create_report, name="create_report"),
    path("dashboard/", views.resident_dashboard, name="resident_dashboard"),
    path("main-dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("reports-map/", views.reports_map, name="reports_map"),
]
