# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-16 15:38
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0002_auto_20160416_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='score',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
