# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 14:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0039_auto_20160404_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='address',
        ),
    ]