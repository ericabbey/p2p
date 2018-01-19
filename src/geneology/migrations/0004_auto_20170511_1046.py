# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-11 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geneology', '0003_descendant'),
    ]

    operations = [
        migrations.AddField(
            model_name='descendant',
            name='last_login',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='tree',
            name='last_login',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
