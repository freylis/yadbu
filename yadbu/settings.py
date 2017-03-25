from django.conf import settings as dj_settings


# https://tech.yandex.ru/oauth/
YADBU_TOKEN = getattr(dj_settings, 'YADBU_TOKEN', None)

# https://tech.yandex.ru/disk/api/concepts/app-folders-docpage/
YADBU_APP_NAME = getattr(dj_settings, 'YADBU_APP_NAME', 'yadbu')

# show each file, backuped from mask, like /path/to/folder/*
YADBU_SHOW_EACH_FILE_FROM_MASK = getattr(dj_settings, 'YADBU_SHOW_EACH_FILE_FROM_MASK', False)
