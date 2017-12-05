import datetime

from django.template import Context
from django.template import loader as template_loader
from django.core.mail import send_mail

from . import settings
from . import api_client


def send_report(backup, recipients):
    """
    Send report about backup result

    Args:
        backup (yadbu.models.Backup): Backup instance
        recipients (list[str]): Emails list to get report
    """
    tpl = template_loader.get_template('yadbu/mail_report.html')
    try:
        disk_info = api_client.get_disk_info()
    except Exception as exc:
        disk_info_error = exc
        disk_info = {}
    else:
        disk_info_error = None
    context = Context({
        'backup': backup,
        'disk_info': disk_info,
        'disk_info_error': disk_info_error,
    })
    mail_text = tpl.render(context)
    send_mail(
        subject='Yadbu backup {} report {}'.format(
            backup.status.upper(),
            datetime.datetime.today().strftime('%d.%m.%Y %H:%M'),
        ),
        from_email=settings.YADBU_REPORT_FROM_EMAIL,
        message=mail_text,
        html_message=mail_text,
        recipient_list=recipients,
    )
