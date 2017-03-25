from django.contrib import admin

from . import models


class BackupAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Backup, BackupAdmin)


class FileAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.File, FileAdmin)
