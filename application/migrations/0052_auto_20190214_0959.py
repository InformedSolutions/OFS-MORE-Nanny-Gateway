# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-02-14 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0051_merge_20181106_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arccomments',
            name='comment',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
