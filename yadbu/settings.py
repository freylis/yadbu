from django.conf import settings as dj_settings


# https://tech.yandex.ru/oauth/
YADBU_TOKEN = getattr(dj_settings, 'YADBU_TOKEN', None)

# https://tech.yandex.ru/disk/api/concepts/app-folders-docpage/
YADBU_BACKUP_DIRECTORY = getattr(dj_settings, 'YADBU_BACKUP_DIRECTORY', 'yadbu')

YADBU_WRITE_TRACEBACK_ON_ERROR = getattr(dj_settings, 'YADBU_WRITE_TRACEBACK_ON_ERROR', True)
