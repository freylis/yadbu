# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yadbu', '0002_auto_20170327_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='backup',
            name='yad_directory',
            field=models.CharField(editable=False, max_length=255, null=True, verbose_name='Directory at Yandex.Disk'),
        ),
    ]
