import glob
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from yadbu import settings
from . import api_client


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
        success_count = 0
        errors_count = 0
        backup_file = BackupFile()
        for filename in self._iter_files():
           api_client.upload_file(backup.directory_name, filename)

    def _iter_files(self):
        path_list = glob.glob(self.filename)
        for path in path_list:
            yield path


class Backup(models.Model):
    STATUS_NEW = 'new'
    STATUS_SUCCESS = 'success'
    STATUS_PARTIALLY = 'partially'
    STATUS_ERROR = 'error'
    STATUSES = (
        (STATUS_NEW, _('New')),
        (STATUS_SUCCESS, _('Success')),
        (STATUS_PARTIALLY, _('Partially')),
        (STATUS_ERROR, _('Error')),
    )

    class Meta:
        verbose_name = _('Backup')
        verbose_name_plural = _('Backups')

    datetime = models.DateTimeField(_('Runned at'), auto_now_add=True)
    status = models.CharField(_('Status'), choices=STATUSES, max_length=20, default=STATUS_NEW)
    log = models.TextField(_('Process log'), default='')
    yad_directory = models.CharField(_('Directory at Yandex.Disk'), max_length=255, null=True, editable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.directory_name = None

    @classmethod
    def run(cls):
        self = cls.objects.create(status=cls.STATUS_NEW)
        error = None
        self.create_backup_directory()
        file_items = File.objects.all()
        for file_item in file_items:
            file_item.backup(self)
        self.save()

    def create_backup_directory(self):
        today = datetime.datetime.today()
        self.directory_name = 'backups/{}/{}/{}/{}_{}'.format(
            settings.YADBU_BACKUP_DIRECTORY,
            today.year,
            today.strftime('%m'),
            today.strftime('%d'),
            self.pk,
        )
        self.yad_directory = api_client.create_folder(self.directory_name)['href']
        self.save()


class BackupFile(models.Model):
    class Meta:
        verbose_name = _('Backuped File')
        verbose_name_plural = _('Backuped Files')

    backup = models.ForeignKey('yadbu.Backup', verbose_name=_('Backup'))
    file = models.TextField(_('File path'))
    filename = models.TextField(_('Filename'))
