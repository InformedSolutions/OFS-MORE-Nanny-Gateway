# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-11-01 10:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0047_auto_20181029_0933'),
    ]

    operations = [
        migrations.RenameField(
            model_name='arccomments',
            old_name='table_name',
            new_name='endpoint_name',
        ),
    ]
