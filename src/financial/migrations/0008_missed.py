# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-14 01:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financial', '0007_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='missed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('was_to', models.CharField(max_length=30)),
                ('missed_to', models.CharField(max_length=30)),
                ('trans_id', models.CharField(max_length=34)),
                ('amount', models.DecimalField(decimal_places=3, max_digits=4)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='missed', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
