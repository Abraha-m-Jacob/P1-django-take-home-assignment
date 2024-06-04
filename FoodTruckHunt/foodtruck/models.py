from django.db import models

# Create your models here.


class FoodTruck(models.Model):
    locationid = models.CharField(max_length=20, unique=True)
    applicant = models.CharField(max_length=255)
    facility_type = models.CharField(max_length=50)
    location_description = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    food_items = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=50)
    schedule = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.applicant
