# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-15 12:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roomaterating', '0003_auto_20171215_0012'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]