from django.urls import path

from .views import FindFoodTruck

urlpatterns = [
    path("nearest_foodtrucks/", FindFoodTruck.as_view(), name="nearest-foodtrucks")
]
