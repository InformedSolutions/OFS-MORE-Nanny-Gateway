# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-09 15:16
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0024_auto_20180709_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='declaration',
            name='declaration_id',
            field=models.UUIDField(default=uuid.UUID('a7cf52fa-1c62-47b7-b860-e6028fb0dcc9'), primary_key=True, serialize=False),
        ),
    ]