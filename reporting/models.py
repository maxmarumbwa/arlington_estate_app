from django.db import models
from django.contrib.auth.models import User
import uuid
from PIL import Image
import os


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
# VIOLATION TYPE
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

    # Field for filtering charts
    report_date = models.DateField(null=True, blank=True)

    # Single image (optional)
    image = models.ImageField(upload_to="reports/", null=True, blank=True)

    def save(self, *args, **kwargs):
        # Set fine_amount if not set
        if self.violation and not self.fine_amount:
            self.fine_amount = self.violation.fine_amount

        # Default report_date to created_at if not set
        if not self.report_date and self.created_at:
            self.report_date = self.created_at.date()

        super().save(*args, **kwargs)

        # Compress image if exists
        if self.image:
            self.compress_image()

    def compress_image(self):
        """Compress uploaded image to under 1MB."""
        try:
            img_path = self.image.path
            img = Image.open(img_path)

            # Convert to RGB for non-JPEG images
            if img.mode in ("RGBA", "P"):
                if img.mode == "RGBA":
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                else:
                    img = img.convert("RGB")

            # Resize
            img.thumbnail((1280, 1280), Image.Resampling.LANCZOS)

            # Compress to under 1MB
            quality = 85
            min_quality = 20
            while True:
                img.save(img_path, format="JPEG", quality=quality, optimize=True)
                size = os.path.getsize(img_path)
                if size <= 1024 * 1024 or quality <= min_quality:
                    break
                quality -= 5
        except Exception as e:
            print(f"Error compressing image for report {self.id}: {e}")

    def __str__(self):
        return f"{self.house_number} - {self.status}"


# ==============================
# REPORT IMAGES (Multiple)
# ==============================
class ReportImage(models.Model):
    report = models.ForeignKey(
        "PropertyReport", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="reports/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Image for {self.report.house_number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save first

        if self.image:
            self.compress_image()

    def compress_image(self):
        """Compress uploaded image to under 1MB."""
        try:
            img_path = self.image.path
            img = Image.open(img_path)

            if img.mode in ("RGBA", "P"):
                if img.mode == "RGBA":
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                else:
                    img = img.convert("RGB")

            img.thumbnail((1280, 1280), Image.Resampling.LANCZOS)

            quality = 85
            while True:
                img.save(img_path, format="JPEG", quality=quality, optimize=True)
                size = os.path.getsize(img_path)
                if size <= 1024 * 1024 or quality <= 20:
                    break
                quality -= 5
        except Exception as e:
            print(f"Error compressing image: {e}")


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
