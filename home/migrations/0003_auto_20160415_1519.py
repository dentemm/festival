# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-15 13:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20160415_1515'),
    ]

    operations = [

        migrations.AddField(
            model_name='addressorderable',
            name='address_ptr',
        ),
        migrations.AddField(
            model_name='addressorderable',
            name='page',
        ),
        migrations.AddField(
            model_name='orderabletest',
            name='location_ptr',
        ),
        migrations.AddField(
            model_name='orderabletest',
            name='page',
        ),
        migrations.AddModel(
            name='AddressOrderable',
        ),
        migrations.AddModel(
            name='OrderableTest',
        ),

        migrations.RemoveField(
            model_name='addressorderable',
            name='address_ptr',
        ),
        migrations.RemoveField(
            model_name='addressorderable',
            name='page',
        ),
        migrations.RemoveField(
            model_name='orderabletest',
            name='location_ptr',
        ),
        migrations.RemoveField(
            model_name='orderabletest',
            name='page',
        ),
        migrations.DeleteModel(
            name='AddressOrderable',
        ),
        migrations.DeleteModel(
            name='OrderableTest',
        ),
    ]
