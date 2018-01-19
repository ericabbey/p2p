# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-14 08:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_support'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support',
            name='priority',
            field=models.CharField(choices=[('L', 'low'), ('M', 'medium'), ('H', 'high')], default='L', max_length=1),
        ),
    ]
