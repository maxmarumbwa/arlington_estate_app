from datetime import datetime, timedelta
import random
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from reporting.models import PropertyReport, ViolationType


class Command(BaseCommand):
    help = "Generate dummy property reports for testing"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=500)

    def handle(self, *args, **options):
        count = options["count"]
        user, _ = User.objects.get_or_create(
            username="testuser", defaults={"email": "test@example.com"}
        )
        violations = list(ViolationType.objects.filter(is_active=True))
        statuses = [
            "DRAFT",
            "SUBMITTED",
            "UNDER_REVIEW",
            "APPROVED",
            "FINED",
            "PAID",
            "CLOSED",
        ]

        start_date = datetime(2020, 1, 1)
        end_date = datetime.today()

        for i in range(count):
            # Random full date for report_date
            delta_days = random.randint(0, (end_date - start_date).days)
            report_date = start_date + timedelta(days=delta_days)

            violation = random.choice(violations)
            status = random.choice(statuses)
            house_number = f"H-{random.randint(1,150)}"
            latitude = -17.82 + random.uniform(-0.02, 0.02)
            longitude = 31.05 + random.uniform(-0.02, 0.02)

            PropertyReport.objects.create(
                reported_by=user,
                house_number=house_number,
                violation=violation,
                description=f"Dummy report {i+1}",
                fine_amount=violation.fine_amount,
                status=status,
                latitude=latitude,
                longitude=longitude,
                report_date=report_date,
            )

        self.stdout.write(
            self.style.SUCCESS(f"Created {count} dummy reports from 2020 to today!")
        )
