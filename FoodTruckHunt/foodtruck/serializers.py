from rest_framework import serializers

from .models import FoodTruck


class FoodTruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodTruck
        fields = (
            "locationid",
            "applicant",
            "facility_type",
            "location_description",
            "address",
            "food_items",
            "latitude",
            "longitude",
            "status",
            "schedule",
            "expiration_date",
            "permit",
        )
