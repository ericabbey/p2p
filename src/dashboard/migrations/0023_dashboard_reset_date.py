# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-11 10:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_auto_20170508_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='reset_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]