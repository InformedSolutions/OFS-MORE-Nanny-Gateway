# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-02-19 11:19
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0051_merge_20181106_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nannyapplication',
            name='application_reference',
            field=models.CharField(blank=True, max_length=7, null=True, validators=[django.core.validators.RegexValidator('([0-9]{7})')]),
        ),
    ]