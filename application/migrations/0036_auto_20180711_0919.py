# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-11 09:19
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0035_auto_20180710_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='declaration',
            name='declaration_id',
            field=models.UUIDField(default=uuid.UUID('74501fed-bb06-4022-903a-4b31baede40f'), primary_key=True, serialize=False),
        ),
    ]
