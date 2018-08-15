# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-15 08:57
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0037_auto_20180813_1957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arccomments',
            name='id',
        ),
        migrations.AddField(
            model_name='arccomments',
            name='application_id',
            field=models.UUIDField(blank=True, default=uuid.uuid4()),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='arccomments',
            name='review_id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='declaration',
            name='declaration_id',
            field=models.UUIDField(default=uuid.UUID('7276bc6b-a5bc-4538-af87-6762b4bd46b4'), primary_key=True, serialize=False),
        ),
    ]
