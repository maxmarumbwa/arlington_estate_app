from django.shortcuts import render, get_object_or_404, redirect
from .models import PropertyReport
from .forms import PropertyReportForm
from django.contrib.auth.decorators import login_required


def report_list(request):
    reports = PropertyReport.objects.all().order_by("-created_at")
    return render(request, "reporting/report_list.html", {"reports": reports})


def report_detail(request, report_id):
    report = get_object_or_404(PropertyReport, report_id=report_id)
    return render(request, "reporting/report_detail.html", {"report": report})


@login_required
def report_create(request):
    if request.method == "POST":
        form = PropertyReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_by = request.user
            report.save()
            return redirect("report_detail", report_id=report.report_id)
    else:
        form = PropertyReportForm()

    return render(request, "reporting/report_form.html", {"form": form})
