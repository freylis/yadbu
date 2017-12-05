from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from ... import models
from ... import settings


class Command(BaseCommand):
    help = 'Send report about backup results'

    def add_arguments(self, parser):
        parser.add_argument('backup_id', type=int)

    def handle(self, *args, **options):
        """
        Send report
        """
        if not settings.YADBU_REPORT_TO_EMAILS:
            raise CommandError('Emails list to report is empty. Please fill `YADBU_REPORT_TO_EMAILS` setting')

        try:
            backup = models.Backup.objects.get(id=options['backup_id'])
        except models.Backup.DoesNotExist:
            raise CommandError('Backup with pk={} not found'.format(options['backup_id']))

        backup.send_report()
