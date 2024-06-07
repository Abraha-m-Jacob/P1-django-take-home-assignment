import logging

from django.utils import timezone
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FoodTruck
from .serializers import FoodTruckSerializer
from .utils import (
    CustomValidationException,
    find_distance_from_location,
    validate_latitude,
    validate_longitude,
    validate_pagination_params,
    validate_required_fields,
)

# Create your views here.

logger = logging.getLogger(__name__)


class FindFoodTruck(APIView):

    def get(self, request):
        logger.info("Request for finding closest food trucks started")
        paginator = LimitOffsetPagination()
        try:
            print("request____________", request.GET)
            validate_required_fields(request.GET, ["latitude", "longitude"])
            latitude = validate_latitude(request.GET.get("latitude"))
            longitude = validate_longitude(request.GET.get("longitude"))
            validate_pagination_params(request)
            print(latitude, longitude)
            food_trucks = FoodTruck.objects.filter(
                status="APPROVED",
                expiration_date__gt=timezone.now(),
                latitude__isnull=False,
                longitude__isnull=False,
            )
            food_trucks_with_distance = []
            for food_truck in food_trucks:
                distance = find_distance_from_location(latitude, longitude, food_truck)
                food_trucks_with_distance.append((food_truck, distance))
            food_trucks_with_distance.sort(key=lambda x: x[1])
            food_trucks = [
                food_truck for food_truck, distance in food_trucks_with_distance
            ]
            paginated_trucks = paginator.paginate_queryset(food_trucks, request)
            serializer = FoodTruckSerializer(paginated_trucks, many=True)
            logger.info(
                "Completed request for finding closest food trucks successfully"
            )
            return paginator.get_paginated_response(serializer.data)
        except CustomValidationException as cve:
            logger.error("Validation error occurred: {}".format(cve.to_dict()))
            return Response(cve.to_dict(), 400)
        except Exception as e:
            logger.exception(e)
