# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-10 16:15
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0034_auto_20180710_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='declaration',
            name='declaration_id',
            field=models.UUIDField(default=uuid.UUID('90415545-a9dc-4aff-ac7b-3db9a0d4297f'), primary_key=True, serialize=False),
        ),
    ]
