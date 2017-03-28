## yadbu - Yandex.disk backup tool for Django
#### Quick start
Install `yadbu`

    pip install django-yadbu

Add `yadbu` to your `INSTALLED_APPS`

    INSTALLED_APPS = [
        ...,
        'yadbu',
    ]

[Register](https://oauth.yandex.ru/) your oauth application with rights:
* Yandex.Disk REST API
    - Access to information on Drive
    - Access to the application folder on Drive

Get oauth token and put to `YADBU_TOKEN` setting in your `settings.py` like this:

    # settings.py
    YADBU_TOKEN = '<your_access_token>`

Fill several files in your admin interface in `http://127.0.0.1:8000/admin/yadbu/file/` like this:
* /path/to/file.sql
* /path/to/several/files/*.jpg
* /path/to/all/files/*

Prepare files and run management command

    python manage.py yad_backup

Check backup result in your `Yandex.Disk` and in `http://127.0.0.1:8000/admin/yadbu/backup/`

Your can put call management command to crontab and forget about backup

#### Other possible settings

    # settings.py

    # subdirectory name in your yandex.disk like `application/project_slug`
    YADBU_BACKUP_DIRECTORY = 'project_slug'

    # Write traceback if something went wrong
    YADBU_WRITE_TRACEBACK_ON_ERROR = True

    # Send email after backup finished. Not send if emails list is empty
    YADBU_MAIL_AFTER_FINISH = [
        'dev@example.com',
        'noreply@example.com',
    ]
