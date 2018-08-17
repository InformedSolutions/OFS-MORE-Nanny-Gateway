# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-13 19:57
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0036_auto_20180809_1948'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nannyapplication',
            old_name='criminal_record_check_arc_flagged',
            new_name='dbs_arc_flagged',
        ),
        migrations.RenameField(
            model_name='nannyapplication',
            old_name='first_aid_training_arc_flagged',
            new_name='first_aid_arc_flagged',
        ),
        migrations.AlterField(
            model_name='declaration',
            name='declaration_id',
            field=models.UUIDField(default=uuid.UUID('859d2a8d-3ff4-4fc7-afc3-e6dccd7ecd16'), primary_key=True, serialize=False),
        ),
    ]