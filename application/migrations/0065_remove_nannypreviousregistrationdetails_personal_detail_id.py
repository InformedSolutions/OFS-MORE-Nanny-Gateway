# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-11 16:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0064_auto_20190311_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nannypreviousregistrationdetails',
            name='personal_detail_id',
        ),
    ]
