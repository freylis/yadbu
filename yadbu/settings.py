from django.conf import settings as dj_settings


# https://tech.yandex.ru/oauth/
YADBU_TOKEN = getattr(dj_settings, 'YADBU_TOKEN', None)

# https://tech.yandex.ru/disk/api/concepts/app-folders-docpage/
YADBU_BACKUP_DIRECTORY = getattr(dj_settings, 'YADBU_BACKUP_DIRECTORY', 'yadbu')

# timeout in seconds
YADBU_REQUEST_TIMEOUT = getattr(dj_settings, 'YADBU_REQUEST_TIMEOUT', 5)

YADBU_REPORT_TO_EMAILS = getattr(dj_settings, 'YADBU_REPORT_TO_EMAILS', [])
YADBU_REPORT_FROM_EMAIL = getattr(dj_settings, 'YADBU_REPORT_FROM_EMAIL', 'yadbu@localhost')
