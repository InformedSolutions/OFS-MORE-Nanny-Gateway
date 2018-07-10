# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-10 08:28
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0026_auto_20180709_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='declaration',
            name='declaration_id',
            field=models.UUIDField(default=uuid.UUID('dc615da9-1bbe-4c66-b1a0-bcf53be6a278'), primary_key=True, serialize=False),
        ),
    ]
