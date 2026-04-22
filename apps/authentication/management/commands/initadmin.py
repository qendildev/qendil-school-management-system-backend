from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', 'superadmin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@qendil.com')
        password = os.environ.get('ADMIN_PASSWORD', 'Admin@1234')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                role='superadmin'
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {username} already exists'))
