# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-09 08:09
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0045_auto_20180809_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='declaration',
            name='declaration_id',
            field=models.UUIDField(default=uuid.UUID('50a811d1-b00a-4b08-b734-4f1ea7421488'), primary_key=True, serialize=False),
        ),
    ]
