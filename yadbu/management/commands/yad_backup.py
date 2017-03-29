from django.core.management.base import BaseCommand

from ... import models


class Command(BaseCommand):
    help = 'Backup your files to Yandex.Disk'

    def handle(self, *args, **options):
        backup = models.Backup.objects.create(status=models.Backup.STATUS_NEW)
        try:
            backup.process()

        except Exception as exc:
            backup.log_error(exc)

        except KeyboardInterrupt:
            backup.status = backup.STATUS_ABORTED
            backup.save()
            return

        else:
            if backup.status != backup.STATUS_ERROR:
                backup.status = backup.STATUS_SUCCESS
                backup.log = 'Complete'
        backup.save()
