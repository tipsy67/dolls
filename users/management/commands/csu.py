import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        newsu = User(username='negoro1', is_staff=True, is_superuser=True)
        newsu.set_password(os.environ.get('PGADMIN_DEFAULT_PASSWORD'))

        newsu.save()
