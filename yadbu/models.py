from django.db import models
from django.utils.translation import ugettext_lazy as _


class File(models.Model):
    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    filename = models.TextField(
        _('Filename'),
        help_text='Full filename or mask, like '
                  '`/path/to/file/my_backup.sql`, '
                  '`/path/to/folder/*` or '
                  '`/path/to/folder/*.jpeg`'
    )

    def __str__(self):
        return self.filename.strip()


class Backup(models.Model):
    STATUS_SUCCESS = 'success'
    STATUS_PARTIALLY = 'partially'
    STATUS_ERROR = 'error'
    STATUSES = (
        (STATUS_SUCCESS, _('Success')),
        (STATUS_PARTIALLY, _('Partially')),
        (STATUS_ERROR, _('Error')),
    )

    class Meta:
        verbose_name = _('Backup')
        verbose_name_plural = _('Backups')

    datetime = models.DateTimeField(_('Runned at'), auto_now_add=True)
    status = models.CharField(_('Status'), choices=STATUSES, max_length=20)


class BackupFile(models.Model):
    class Meta:
        verbose_name = _('Backuped File')
        verbose_name_plural = _('Backuped Files')

    backup = models.ForeignKey('yadbu.Backup', verbose_name=_('Backup'))
    file = models.ForeignKey('yadbu.File', verbose_name=_('File'))
    filename = models.TextField(_('Filename'))
