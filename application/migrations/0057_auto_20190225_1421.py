# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-02-25 14:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0056_auto_20190222_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nannyapplication',
            name='your_children_arc_flagged',
        ),
        migrations.RemoveField(
            model_name='nannyapplication',
            name='your_children_status',
        ),
    ]