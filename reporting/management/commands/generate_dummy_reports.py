from datetime import datetime, timedelta
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from reporting.models import PropertyReport, ViolationType
from shapely.geometry import Point, shape
import json


class Command(BaseCommand):
    help = "Generate dummy property reports within Arlington boundary"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=500)

    def handle(self, *args, **options):
        count = options["count"]

        # ----------------------------------
        # 1️⃣ Load your GeoJSON boundary
        # ----------------------------------
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": [
                            [
                                [
                                    [31.072844583999419, -17.900947122786324],
                                    [31.077399827519841, -17.898723730115641],
                                    [31.078213263862775, -17.902194391845487],
                                    [31.081955071040266, -17.901109810054912],
                                    [31.081250092876388, -17.897639148325066],
                                    [31.085317274591052, -17.897096857429776],
                                    [31.088462561783725, -17.902194391845487],
                                    [31.0895471435743, -17.903875493620884],
                                    [31.079352074742879, -17.911087962528217],
                                    [31.076749078445495, -17.906749635365912],
                                    [31.072844583999419, -17.900947122786324],
                                ]
                            ]
                        ],
                    },
                }
            ],
        }

        polygon = shape(geojson["features"][0]["geometry"])

        # Bounding box (auto from polygon)
        minx, miny, maxx, maxy = polygon.bounds

        # ----------------------------------
        # 2️⃣ Setup DB Data
        # ----------------------------------
        user, _ = User.objects.get_or_create(
            username="testuser", defaults={"email": "test@example.com"}
        )

        violations = list(ViolationType.objects.filter(is_active=True))

        statuses = ["OPEN", "IN_PROGRESS", "RESOLVED", "APPROVED"]

        start_date = datetime(2020, 1, 1)
        end_date = datetime.today()

        created = 0

        while created < count:
            # Random date
            delta_days = random.randint(0, (end_date - start_date).days)
            report_date = start_date + timedelta(days=delta_days)

            # Generate random point inside bounding box
            lon = random.uniform(minx, maxx)
            lat = random.uniform(miny, maxy)

            point = Point(lon, lat)

            # Check if inside polygon
            if polygon.contains(point):

                violation = random.choice(violations)

                PropertyReport.objects.create(
                    reported_by=user,
                    house_number=f"H-{random.randint(1,150)}",
                    violation=violation,
                    description=f"Dummy report {created+1}",
                    fine_amount=violation.fine_amount,
                    status=random.choice(statuses),
                    latitude=lat,
                    longitude=lon,
                    report_date=report_date,
                )

                created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Created {count} reports inside boundary!")
        )
