import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from django.contrib.auth.models import User
from reporting.models import PropertyReport, ViolationType  # replace with your app name


class Command(BaseCommand):
    help = "Generate dummy property reports for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=100,
            help="Number of dummy reports to create",
        )

    def handle(self, *args, **options):
        count = options["count"]

        # Create/get a test user
        user, _ = User.objects.get_or_create(
            username="testuser", defaults={"email": "test@example.com"}
        )

        # Get all active violations
        violations = list(ViolationType.objects.filter(is_active=True))
        if not violations:
            self.stdout.write(self.style.ERROR("No active violations found!"))
            return

        # Status options
        statuses = [
            "DRAFT",
            "SUBMITTED",
            "UNDER_REVIEW",
            "APPROVED",
            "FINED",
            "PAID",
            "CLOSED",
        ]

        # Date range
        start_date = datetime(2020, 1, 1)
        end_date = datetime.today()

        for i in range(count):
            delta_seconds = random.randint(
                0, int((end_date - start_date).total_seconds())
            )
            created_at = make_aware(start_date + timedelta(seconds=delta_seconds))
            violation = random.choice(violations)
            status = random.choice(statuses)
            house_number = f"H-{random.randint(1, 150)}"
            latitude = -17.82 + random.uniform(-0.02, 0.02)
            longitude = 31.05 + random.uniform(-0.02, 0.02)

            report = PropertyReport.objects.create(
                reported_by=user,
                house_number=house_number,
                violation=violation,
                description=f"Dummy report {i+1}",
                fine_amount=violation.fine_amount,
                status=status,
                latitude=latitude,
                longitude=longitude,
                created_at=created_at,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"[{i+1}/{count}] Created report {report.report_id} ({status}) on {created_at.date()}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {count} dummy reports!")
        )
