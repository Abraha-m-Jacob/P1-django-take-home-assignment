import csv
import os

from datetime import datetime
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from ...models import FoodTruck

load_dotenv()


class Command(BaseCommand):
    help = 'Loads food truck data from a CSV file after deleting existing data'

    def handle(self, *args, **options):
        FoodTruck.objects.all().delete()
        print("Existing food truck data deleted")
        error_count = 0
        with open(os.environ.get('CSV_FILE_PATH'), 'rt', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader, None)
            latitude_index = headers.index('Latitude')
            longitude_index = headers.index('Longitude')
            locationid_index = headers.index('locationid')
            applicant_index = headers.index('Applicant')
            facility_type_index = headers.index('FacilityType')
            location_description_index = headers.index('LocationDescription')
            address_index = headers.index('Address')
            food_items_index = headers.index('FoodItems')
            status_index = headers.index('Status')
            schedule_index = headers.index('Schedule')
            expiration_date_index = headers.index('ExpirationDate')
            permit_index = headers.index('permit')
            print("reader______________________", headers.index('Latitude'), headers.index('Longitude'))
            for i, row in enumerate(reader, start=1):
                try:
                    latitude = float(row[latitude_index])
                    longitude = float(row[longitude_index])
                    expiration_date_str = row[expiration_date_index]
                    if expiration_date_str:
                        expiration_date = datetime.strptime(expiration_date_str, '%m/%d/%Y %I:%M:%S %p').date()
                    else:
                        expiration_date = None
                except (ValueError, IndexError):
                    error_count += 1
                    print(f"Skipping row with invalid data: {row}")
                    print(i, row[latitude_index], row[longitude_index], "row[expiration_date_index]",
                          row[expiration_date_index])
                    continue
                data = {
                    'locationid': row[locationid_index],
                    'applicant': row[applicant_index],
                    'facility_type': row[facility_type_index],
                    'location_description': row[location_description_index],
                    'address': row[address_index],
                    'food_items': row[food_items_index],
                    'latitude': latitude,
                    'longitude': longitude,
                    'status': row[status_index],
                    'schedule': row[schedule_index],
                    'expiration_date': expiration_date,
                    'permit': row[permit_index],
                }
                food_truck = FoodTruck.objects.create(**data)
                food_truck.save()
            print("error_count------------------", error_count)
        self.stdout.write(self.style.SUCCESS('Successfully loaded food truck data'))
