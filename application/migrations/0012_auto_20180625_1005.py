# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-25 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0011_applicanthomeaddress_childcare_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicantpersonaldetails',
            name='lived_abroad',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='applicantpersonaldetails',
            name='post_certificate_declaration',
            field=models.NullBooleanField(),
        ),
    ]