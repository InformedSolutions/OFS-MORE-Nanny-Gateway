# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-17 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0040_auto_20180817_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nannyapplication',
            name='application_status',
            field=models.CharField(blank=True, choices=[('ACCEPTED', 'ACCEPTED'), ('ARC_REVIEW', 'ARC_REVIEW'), ('CANCELLED', 'CANCELLED'), ('CYGNUM_REVIEW', 'CYGNUM_REVIEW'), ('DRAFTING', 'DRAFTING'), ('FURTHER_INFORMATION', 'FURTHER_INFORMATION'), ('NOT_REGISTERED', 'NOT_REGISTERED'), ('REGISTERED', 'REGISTERED'), ('REJECTED', 'REJECTED'), ('SUBMITTED', 'SUBMITTED'), ('WITHDRAWN', 'WITHDRAWN')], max_length=50),
        ),
    ]