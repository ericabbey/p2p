# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-06 23:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0012_btcaddr_changecount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='btcaddr',
            name='newAddr',
            field=models.CharField(blank=True, max_length=34, null=True),
        ),
    ]
