# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-10-12 10:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0041_auto_20180817_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicantpersonaldetails',
            name='your_children',
            field=models.NullBooleanField(),
        ),
    ]