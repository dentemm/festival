# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-15 19:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0028_merge'),
        ('home', '0006_commentsnippet'),
    ]

    operations = [
        migrations.CreateModel(
            name='FestivalPageRelatedLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, verbose_name='Externe link')),
                ('title', models.CharField(help_text='Naam van link', max_length=63, verbose_name='titel')),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_links', to='home.FestivalPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
