# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 14:48
from __future__ import unicode_literals

from django.db import migrations
import django_countries.fields
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0042_address_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='festivalpage',
            name='test',
            field=recurrence.fields.RecurrenceField(null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(default='BE', max_length=2, null=True, verbose_name='land'),
        ),
    ]
