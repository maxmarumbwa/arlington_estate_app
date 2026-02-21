from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PropertyReport
from .forms import PropertyReportForm


# -----------------------------
# List all reports (admin or general view)
# -----------------------------
@login_required
def report_list(request):
    reports = PropertyReport.objects.all().order_by("-created_at")
    return render(request, "reporting/report_list.html", {"reports": reports})


# -----------------------------
# Detail view for a single report
# -----------------------------
@login_required
def report_detail(request, report_id):
    report = get_object_or_404(PropertyReport, report_id=report_id)
    return render(request, "reporting/report_detail.html", {"report": report})


# -----------------------------
# Create a new property report
# -----------------------------
@login_required
def create_report(request):
    if request.method == "POST":
        form = PropertyReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_by = request.user  # Link report to logged-in user
            report.save()
            return redirect("resident_dashboard")
    else:
        form = PropertyReportForm()

    return render(request, "reporting/create_report_geolocation.html", {"form": form})


# -----------------------------
# Resident dashboard (show reports by logged-in user)
# -----------------------------
@login_required
def resident_dashboard(request):
    # Only show reports created by this user
    reports = PropertyReport.objects.filter(reported_by=request.user).order_by(
        "-created_at"
    )

    total_reports = reports.count()
    open_reports = reports.filter(status="OPEN").count()
    resolved_reports = reports.filter(status="RESOLVED").count()

    context = {
        "reports": reports,
        "total_reports": total_reports,
        "open_reports": open_reports,
        "resolved_reports": resolved_reports,
    }

    return render(request, "reporting/resident_dashboard.html", context)


from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum
from datetime import datetime
from reporting.models import PropertyReport


def dashboard(request):
    selected_year = int(request.GET.get("year", datetime.now().year))
    reports = PropertyReport.objects.filter(report_date__year=selected_year)

    # Summary
    total_reports = reports.count()
    pending_reports = reports.filter(status="OPEN").count()
    resolved_reports = reports.filter(status="RESOLVED").count()
    total_fines = reports.aggregate(total=Sum("fine_amount"))["total"] or 0

    # Monthly counts
    monthly_data = (
        reports.annotate(month=TruncMonth("report_date"))
        .values("month")
        .annotate(count=Count("id"))
    )

    counts_dict = {entry["month"].month: entry["count"] for entry in monthly_data}

    months = []
    counts = []
    for m in range(1, 13):
        months.append(datetime(selected_year, m, 1).strftime("%b"))
        counts.append(counts_dict.get(m, 0))

    years_list = list(range(2020, datetime.now().year + 1))

    context = {
        "total_reports": total_reports,
        "pending_reports": pending_reports,
        "resolved_reports": resolved_reports,
        "total_fines": total_fines,
        "months": months,
        "counts": counts,
        "selected_year": selected_year,
        "years_list": years_list,
    }

    return render(request, "reporting/summary-dashboard.html", context)
