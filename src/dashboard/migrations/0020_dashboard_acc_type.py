# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-24 09:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_auto_20170416_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='acc_type',
            field=models.CharField(choices=[('d', 'dynamo'), ('p', 'prime'), ('n', 'normal')], default='n', max_length=1),
        ),
    ]
