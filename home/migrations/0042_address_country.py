# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 14:42
from __future__ import unicode_literals

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_location_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True, verbose_name='land'),
        ),
    ]