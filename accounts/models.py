from django.contrib.auth.models import User
from django.contrib.gis.db import models


class Stand(models.Model):
    # Stand Info
    stand_numb = models.CharField(max_length=10, unique=True)
    street = models.CharField(max_length=150, blank=True, null=True)
    cluster = models.BooleanField(null=True, blank=True)
    cluster_na = models.CharField(max_length=50, blank=True, null=True)

    # Coordinates
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.PointField(srid=4326, null=True, blank=True)

    # Status
    dev_status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
            from django.contrib.gis.geos import Point

            self.location = Point(self.longitude, self.latitude)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.street:
            return f"{self.stand_numb} - {self.street}"
        return self.stand_numb


class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stand = models.OneToOneField(Stand, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    alternative_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to="uploads/photos/", blank=True, null=True
    )

    def __str__(self):
        return self.user.get_full_name()
