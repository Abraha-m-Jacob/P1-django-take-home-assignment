import os
from dotenv import load_dotenv
from . import error_messages
from typing import Union
from django.http import QueryDict
from geopy.distance import geodesic

load_dotenv()


class CustomValidationException(Exception):
    def __init__(self, error: dict):
        self.error_code = error['error_code']
        self.message = error['message']

    def to_dict(self):
        return {"error_code": self.error_code, "message": self.message}


def validate_pagination_params(request):
    try:
        offset = int(request.GET.get('offset'))
        limit = int(request.GET.get('limit'))
        if offset < 0:
            raise CustomValidationException(error_messages.ERR_1007_OFFSET_POSITIVE_NUMERIC)
        if limit < 0:
            raise CustomValidationException(error_messages.ERR_1008_LIMIT_POSITIVE_NUMERIC)
        return offset, limit
    except ValueError:
        raise CustomValidationException(error_messages.ERR_1006_PAGINATION_PARAMS_INVALID)


def validate_required_fields(request_data: Union[dict, QueryDict], required_fields: list):
    print("request_data-------------", request_data)
    missing_fields = [field for field in required_fields if field not in request_data]
    if missing_fields:
        error_message = f"{error_messages.ERR_1001_MISSING_FIELDS['message']}: {', '.join(missing_fields)}"
        raise CustomValidationException({'error_code': error_messages.ERR_1001_MISSING_FIELDS['error_code'],
                                         'message': error_message})


def validate_latitude(latitude: str):
    try:
        latitude_float = float(latitude)
        if -90 <= latitude_float <= 90:
            return latitude_float
        else:
            raise CustomValidationException(error_messages.ERR_1003_INVALID_LATITUDE)
    except ValueError:
        raise CustomValidationException(error_messages.ERR_1002_LATITUDE_NUMERIC)


def validate_longitude(longitude: str):
    try:
        longitude_float = float(longitude)
        if -180 <= longitude_float <= 180:
            return longitude_float
        else:
            raise CustomValidationException(error_messages.ERR_1005_INVALID_LONGITUDE)
    except ValueError:
        raise CustomValidationException(error_messages.ERR_1004_LONGITUDE_NUMERIC)


def find_distance_from_location(latitude, longitude, food_truck):
    return geodesic((latitude, longitude), (food_truck.latitude, food_truck.longitude)).miles

