import os
import glob
import datetime
import traceback

from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import settings
from . import api_client
from . import utils


class File(models.Model):
    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    filename = models.TextField(
        _('Filename'),
        help_text=_(
            'Absolute path to file or mask, like '
            '`/path/to/file/my_backup.sql`, '
            '`/path/to/folder/*` or '
            '`/path/to/folder/*.jpeg`'
        ),
    )

    def __str__(self):
        return self.filename.strip()

    def backup(self, backup):
        """
        Run backup process for this files

        Args:
            backup (Backup): Backup instance
        """
        success_count = 0
        errors_count = 0

        # write in backup for history
        backup_file = BackupFile.objects.create(
            backup=backup,
            file=self.filename,
        )

        # recursively copy each file to y.d
        for filename in self._iter_files(self.filename):
            try:
                api_client.upload_file(backup.directory_name, filename)
            except Exception as exc:
                errors_count += 1
                backup_file.log_error(filename, exc)
            else:
                success_count += 1
                backup_file.log_success(filename)
        backup_file.log_total(
            success_count=success_count,
            errors_count=errors_count,
        )

    def _iter_files(self, path):
        """
        All files generator

        Args:
            path (str): path to find all files

        Yields:
            str: file path with name
        """
        path_list = glob.glob(path)
        for path_item in path_list:
            if os.path.isfile(path_item):
                yield path_item
            elif os.path.isdir(path_item):
                yield from self._iter_files(path_item + os.path.sep + '*')


class Backup(models.Model):
    STATUS_NEW = 'new'
    STATUS_SUCCESS = 'success'
    STATUS_ERROR = 'error'
    STATUS_ABORTED = 'aborted'
    STATUSES = (
        (STATUS_NEW, _('New')),
        (STATUS_SUCCESS, _('Success')),
        (STATUS_ERROR, _('Error')),
        (STATUS_ABORTED, _('Aborted')),
    )

    class Meta:
        verbose_name = _('Backup')
        verbose_name_plural = _('Backups')

    datetime = models.DateTimeField(_('Runned at'), auto_now_add=True)
    status = models.CharField(_('Status'), choices=STATUSES, max_length=20, default=STATUS_NEW)
    log = models.TextField(_('Process log'), default='')
    directory_name = models.CharField(_('Directory at Yandex.Disk'), max_length=255, null=True, editable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return 'Backup {} / {}'.format(
            self.datetime.strftime('%d.%m.%Y'),
            self.id,
        )

    def process(self):
        """
        Run backup process
        """
        self._create_backup_directory()
        file_items = File.objects.all()
        for file_item in file_items:
            try:
                file_item.backup(self)
            except Exception as exc:
                self._log_error(exc)
        self.save()

    def send_report(self):
        """
        Send report to email if it necessary
        """
        utils.send_report(self, recipients=settings.YADBU_REPORT_TO_EMAILS)

    def _log_error(self, exc):
        self.log = '{}\nBackup error: {}\n{}'.format(
            self.log,
            str(exc),
            traceback.format_exc(),
        )
        self.status = self.STATUS_ERROR
        self.save()

    def _create_backup_directory(self):
        """
        All copied files will be in this directory
        """
        today = datetime.datetime.today()
        self.directory_name = 'backups/{}/{}/{}/{}_{}'.format(
            settings.YADBU_BACKUP_DIRECTORY,
            today.year,
            today.strftime('%m'),
            today.strftime('%d'),
            self.pk,
        )
        self.save()


class BackupFile(models.Model):
    class Meta:
        verbose_name = _('Backuped File')
        verbose_name_plural = _('Backuped Files')

    backup = models.ForeignKey('yadbu.Backup', verbose_name=_('Backup'))
    file = models.TextField(_('File path'))
    log = models.TextField(_('Log'), default='')

    def log_error(self, filename, exc):
        self.log = '{}\n{!r} copied with error: {}\n{}'.format(
            self.log,
            filename,
            str(exc),
            traceback.format_exc(),
        )
        self.save()

    def log_success(self, filename):
        self.log = '{}\n{!r} successfully copied'.format(
            self.log,
            filename,
        )
        self.save()

    def log_total(self, success_count, errors_count):
        msg = 'Backup finished with {} success and {} errors'.format(
            success_count,
            errors_count,
        )
        self.log = '{}\n{}'.format(msg, self.log)
        self.save()
