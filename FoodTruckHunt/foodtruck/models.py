from django.db import models

# Create your models here.


class FoodTruck(models.Model):
    locationid = models.CharField(max_length=20, unique=True)
    applicant = models.CharField(max_length=500)
    facility_type = models.CharField(max_length=500)
    location_description = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    food_items = models.CharField(max_length=500)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=500)
    schedule = models.CharField(max_length=500, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    permit = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.applicant
