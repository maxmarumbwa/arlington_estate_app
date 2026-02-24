import json
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from accounts.models import Stand


class Command(BaseCommand):
    help = "Import stands from GeoJSON"

    def add_arguments(self, parser):
        parser.add_argument("geojson_file", type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs["geojson_file"]

        with open(file_path) as f:
            data = json.load(f)

        for feature in data["features"]:
            props = feature["properties"]
            coords = feature["geometry"]["coordinates"]

            longitude = coords[0]
            latitude = coords[1]

            point = Point(longitude, latitude, srid=4326)

            Stand.objects.update_or_create(
                stand_numb=props.get("stand_numb"),
                defaults={
                    "street": props.get("street"),
                    "latitude": latitude,
                    "longitude": longitude,
                    "dev_status": props.get("dev_status", True),
                    "location": point,
                },
            )

        self.stdout.write(self.style.SUCCESS("Stands imported successfully"))
