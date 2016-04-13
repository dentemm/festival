# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-13 06:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_orderabletest'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdresOrderable',
            fields=[
                ('address_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.Address')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='adresorderable', to='home.FestivalPage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=('home.address', models.Model),
        ),
    ]
