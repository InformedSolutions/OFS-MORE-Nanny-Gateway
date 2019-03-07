# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-07 20:13
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0060_merge_20190301_1236'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ApplicationReference',
        ),
        migrations.AlterField(
            model_name='nannyapplication',
            name='application_reference',
            field=models.CharField(blank=True, max_length=7, null=True, validators=[django.core.validators.RegexValidator('([0-9]{7})')]),
        ),
    ]