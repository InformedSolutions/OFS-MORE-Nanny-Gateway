# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-10 14:35
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0031_auto_20180710_1132'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.IntegerField(validators=[django.core.validators.MaxValueValidator(9999999)])),
            ],
            options={
                'db_table': 'APPLICATION_REFERENCE',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('payment_reference', models.CharField(max_length=29)),
                ('payment_submitted', models.BooleanField(default=False)),
                ('payment_authorised', models.BooleanField(default=False)),
                ('application_id', models.ForeignKey(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.NannyApplication')),
            ],
            options={
                'db_table': 'PAYMENT',
            },
        ),
        migrations.AlterField(
            model_name='declaration',
            name='declaration_id',
            field=models.UUIDField(default=uuid.UUID('e20a7d28-3b8f-4f2c-805b-fa4ca7e2d2cb'), primary_key=True, serialize=False),
        ),
    ]
