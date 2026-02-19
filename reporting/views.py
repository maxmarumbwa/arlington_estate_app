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

    return render(request, "reporting/create_report.html", {"form": form})


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
