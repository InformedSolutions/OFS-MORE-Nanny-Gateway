# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-02-21 16:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0073_auto_20200221_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childcaretraining',
            name='application_id',
            field=models.OneToOneField(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.NannyApplication'),
        ),
        migrations.AlterField(
            model_name='dbscheck',
            name='application_id',
            field=models.OneToOneField(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.NannyApplication'),
        ),
        migrations.AlterField(
            model_name='declaration',
            name='application_id',
            field=models.OneToOneField(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.NannyApplication'),
        ),
        migrations.AlterField(
            model_name='firstaidtraining',
            name='application_id',
            field=models.OneToOneField(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.NannyApplication'),
        ),
        migrations.AlterField(
            model_name='insurancecover',
            name='application_id',
            field=models.OneToOneField(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.NannyApplication'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='application_id',
            field=models.OneToOneField(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.NannyApplication'),
        ),
    ]
