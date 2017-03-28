from django.contrib import admin

from . import models


class BackupFileInline(admin.TabularInline):
    model = models.BackupFile
    extra = 0
    can_delete = False
    readonly_fields = [
        'file',
        'log',
    ]


class BackupAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'status',
        'datetime',
    ]
    list_filter = [
        'status',
        'datetime',
    ]
    inlines = [
        BackupFileInline,
    ]
    readonly_fields = [
        'log',
        'status',
    ]
    ordering = [
        '-datetime',
    ]
admin.site.register(models.Backup, BackupAdmin)


class FileAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.File, FileAdmin)
