# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_auto_20160329_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='customimage',
            name='test',
            field=models.CharField(max_length=16, null=True),
        ),
    ]