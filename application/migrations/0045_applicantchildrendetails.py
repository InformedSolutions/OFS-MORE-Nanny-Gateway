# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-10-18 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0044_merge_20181016_1230'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantChildrenDetails',
            fields=[
                ('child_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('child', models.IntegerField(blank=True, null=True)),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('middle_names', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('birth_day', models.IntegerField(blank=True)),
                ('birth_month', models.IntegerField(blank=True)),
                ('birth_year', models.IntegerField(blank=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('street_line1', models.CharField(blank=True, max_length=100, null=True)),
                ('street_line2', models.CharField(blank=True, max_length=100, null=True)),
                ('town', models.CharField(blank=True, max_length=100, null=True)),
                ('county', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('postcode', models.CharField(blank=True, max_length=100, null=True)),
                ('application_id', models.ForeignKey(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.NannyApplication')),
            ],
            options={
                'db_table': 'APPLICANT_CHILDREN_DETAILS',
            },
        ),
    ]