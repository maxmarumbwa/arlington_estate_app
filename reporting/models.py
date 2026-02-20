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

    class Meta:
        verbose_name_plural = "Communities"

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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
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

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} - ${self.fine_amount}"


# ==============================
# PROPERTY REPORT
# ==============================

from django.db import models
from django.contrib.auth.models import User
import uuid


class PropertyReport(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("RESOLVED", "Resolved"),
        ("APPROVED", "Approved"),
    ]

    report_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    reported_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="reports"
    )
    house_number = models.CharField(max_length=50)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    violation = models.ForeignKey(
        "ViolationType", on_delete=models.SET_NULL, null=True, related_name="reports"
    )
    description = models.TextField(blank=True)
    fine_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    fine_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")
    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 Add a single image field
    image = models.ImageField(upload_to="reports/", null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.violation and not self.fine_amount:
            self.fine_amount = self.violation.fine_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.house_number} - {self.status}"


# ==============================
# REPORT IMAGES
# ==============================


class ReportImage(models.Model):
    report = models.ForeignKey(
        PropertyReport,
        on_delete=models.CASCADE,
        related_name="images",  # 🔥 VERY IMPORTANT
    )
    image = models.ImageField(upload_to="reports/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Image for {self.report.house_number}"


# ==============================
# REPORT COMMENTS
# ==============================


class ReportComment(models.Model):
    report = models.ForeignKey(
        PropertyReport, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} on {self.report.house_number}"
