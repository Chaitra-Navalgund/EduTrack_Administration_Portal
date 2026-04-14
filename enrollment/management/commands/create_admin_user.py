from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from enrollment.models import Users
from enrollment.views import sha1_md5


class Command(BaseCommand):
    help = "Create or update an admin portal user in the custom users table."

    def add_arguments(self, parser):
        parser.add_argument("--name", required=True, help="Display name")
        parser.add_argument("--email", required=True, help="Email address")
        parser.add_argument("--username", required=True, help="Login username")
        parser.add_argument("--password", required=True, help="Login password")
        parser.add_argument(
            "--photo",
            default="default.png",
            help="Photo filename stored in the users table",
        )
        parser.add_argument(
            "--status",
            default="active",
            choices=["active", "inactive"],
            help="Whether the user can log in",
        )

    def handle(self, *args, **options):
        username = options["username"].strip()
        email = options["email"].strip()
        password = options["password"]

        if len(username) < 8:
            raise CommandError("Username must be at least 8 characters.")
        if len(password) < 8:
            raise CommandError("Password must be at least 8 characters.")

        defaults = {
            "name": options["name"].strip(),
            "email": email,
            "password": sha1_md5(password),
            "photo": options["photo"].strip(),
            "status": options["status"],
            "datetime": timezone.now(),
        }

        user, created = Users.objects.update_or_create(
            username=username,
            defaults=defaults,
        )

        action = "created" if created else "updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"Admin user {action} successfully for username '{user.username}'."
            )
        )
