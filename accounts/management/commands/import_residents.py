import json
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from django.conf import settings
from accounts.models import Stand, Resident


class Command(BaseCommand):
    help = "Import cleaned resident data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="accounts/data/residents_clean.json",
            help="Path to cleaned JSON file",
        )
        parser.add_argument(
            "--dry-run", action="store_true", help="Test without saving"
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs["file"]
        dry_run = kwargs["dry_run"]

        # Build full path if relative
        if not os.path.isabs(file_path):
            file_path = os.path.join(settings.BASE_DIR, file_path)

        # Load JSON
        with open(file_path, "r") as f:
            data = json.load(f)

        stats = {"created": 0, "skipped": 0, "errors": 0}

        with transaction.atomic():
            for item in data["residents"]:
                try:
                    stand = Stand.objects.get(stand_numb=item["stand_numb"])

                    # Check if resident exists
                    if Resident.objects.filter(stand=stand).exists():
                        stats["skipped"] += 1
                        continue

                    if not dry_run:
                        # Create user
                        user = User.objects.create_user(
                            username=item["user"]["username"],
                            email=item["user"]["email"],
                            first_name=item["user"]["first_name"],
                            last_name=item["user"]["last_name"],
                            password=item["user"]["password"],
                        )

                        # Create resident
                        Resident.objects.create(
                            user=user,
                            stand=stand,
                            phone=item["phone"],
                            monthly_fee=item["monthly_fee"],
                            current_balance=item["current_balance"],
                            last_payment_date=item["last_payment_date"],
                            account_status=item["account_status"],
                        )

                    stats["created"] += 1

                except Stand.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"Stand {item['stand_numb']} not found")
                    )
                    stats["errors"] += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error: {e}"))
                    stats["errors"] += 1

            if dry_run:
                transaction.set_rollback(True)

        # Summary
        self.stdout.write(f"\n✅ Created: {stats['created']}")
        self.stdout.write(f"⏭️ Skipped: {stats['skipped']}")
        self.stdout.write(f"❌ Errors: {stats['errors']}")
