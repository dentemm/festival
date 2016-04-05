# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-22 08:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0012_copy_image_permissions_to_collections'),
        ('home', '0026_auto_20160320_2029'),
    ]

    operations = [
        migrations.CreateModel(
            name='FestivalImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('festival', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='home.FestivalPage')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wagtailimages.Image')),
            ],
        ),
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'adres', 'verbose_name_plural': 'adressen'},
        ),
        migrations.AlterModelOptions(
            name='festivalpagerateableattribute',
            options={'verbose_name': 'Beoordeelbaar kenmerk', 'verbose_name_plural': 'Beoordeelbare kenmerken'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'locatie', 'verbose_name_plural': 'locaties'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['last_name'], 'verbose_name': 'persoon', 'verbose_name_plural': 'personen'},
        ),
        migrations.AlterField(
            model_name='festivalpageratebleattributevalue',
            name='rateable_attribute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='home.FestivalPageRateableAttribute'),
        ),
    ]