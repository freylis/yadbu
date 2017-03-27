from django.core.management.base import BaseCommand

from ... import models


class Command(BaseCommand):
    help = 'Backup all files to Yandex.Disk'

    def handle(self, *args, **options):
        models.Backup.run()
