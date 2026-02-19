from django.db import models
from django.contrib.auth.models import User
import uuid


# ==============================
# COMMUNITY
# ==============================


class Community(models.Model):
    name = models.CharField(max_length=200, default="Arlington Estate")
    address = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


# ==============================
# USER PROFILE
# ==============================


class Profile(models.Model):

    USER_TYPES = [
        ("RESIDENT", "Resident"),
        ("SECURITY", "Security"),
        ("MANAGER", "Manager"),
        ("ACCOUNTS", "Accounts"),
        ("ICT", "ICT"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    house_number = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"


# ==============================
# PREDEFINED VIOLATION TYPES
# ==============================


class ViolationType(models.Model):

    CATEGORY_CHOICES = [
        ("EXTERIOR", "Exterior Maintenance"),
        ("LANDSCAPE", "Landscaping / Tall Grass"),
        ("PARKING", "Parking Violation"),
        ("NOISE", "Noise Disturbance"),
        ("TRASH", "Improper Waste Disposal"),
        ("STRUCTURE", "Unauthorized Structure"),
        ("SECURITY", "Security Breach"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ${self.fine_amount}"


# ==============================
# PROPERTY REPORT
# ==============================


class PropertyReport(models.Model):

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("RESOLVED", "Resolved"),
    ]

    report_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    house_number = models.CharField(max_length=50)

    # 🗺 Location Fields (NEW)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )

    violation = models.ForeignKey(ViolationType, on_delete=models.SET_NULL, null=True)

    description = models.TextField(blank=True)

    fine_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    fine_paid = models.BooleanField(default=False)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically assign fine from predefined violation
        if self.violation and not self.fine_amount:
            self.fine_amount = self.violation.fine_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Report {self.report_id} - {self.house_number}"


# ==============================
# REPORT IMAGES
# ==============================


class ReportImage(models.Model):
    report = models.ForeignKey(PropertyReport, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="reports/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.report.house_number}"


# ==============================
# REPORT COMMENTS
# ==============================


class ReportComment(models.Model):
    report = models.ForeignKey(PropertyReport, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username}"
