# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-06 14:14
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0020_auto_20180706_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='declaration',
            name='declaration_id',
            field=models.UUIDField(default=uuid.UUID('74b610f6-b1b4-41b4-adae-37a70cdb67a4'), primary_key=True, serialize=False),
        ),
    ]
