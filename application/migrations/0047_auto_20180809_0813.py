# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-09 08:13
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0046_auto_20180809_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='declaration',
            name='declaration_id',
            field=models.UUIDField(default=uuid.UUID('8d431da3-e628-42a4-aff0-27e53f3f5092'), primary_key=True, serialize=False),
        ),
    ]
