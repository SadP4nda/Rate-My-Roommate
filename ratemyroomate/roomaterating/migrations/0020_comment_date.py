# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-09 22:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomaterating', '0019_auto_20180109_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]