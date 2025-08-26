from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create a superuser from environment variables'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        first_name = os.environ.get('DJANGO_SUPERUSER_FIRSTNAME')
        last_name = os.environ.get('DJANGO_SUPERUSER_LASTNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not first_name or not last_name or not email or not password:
            self.stderr.write("Missing superuser credentials in environment.")
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write("Superuser already exists.")
        else:
            User.objects.create_superuser(
                first_name=first_name, 
                last_name=last_name,
                email=email, 
                password=password
            )
            self.stdout.write(f"Superuser '{email}' created.")