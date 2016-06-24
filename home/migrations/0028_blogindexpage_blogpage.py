# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 13:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import home.models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0028_merge'),
        ('home', '0027_auto_20160617_2041'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('date_posted', models.DateField(default=datetime.date.today, verbose_name='Publicatie datum')),
                ('author', models.CharField(max_length=40, null=True, verbose_name='Auteur')),
                ('blog_content', wagtail.wagtailcore.fields.StreamField((('blog_title', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(label='afbeelding', required=True)), ('title', wagtail.wagtailcore.blocks.CharBlock(label='Titel', required=True)), ('auteur', wagtail.wagtailcore.blocks.CharBlock(label='Auteur', required=True))), help_text='Dit is de titel van het artikel, voorzien van een afbeelding')), ('blogintro', wagtail.wagtailcore.blocks.StructBlock((('intro', wagtail.wagtailcore.blocks.TextBlock(label='Inleiding van het artikel', required=True)),), help_text='Hiermee kan je optioneel een korte inleiding voorzien')), ('subtitle', home.models.Heading2Block()), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock(help_text='Geef de afbeelding een korte beschrijving', max_length=180, required=True))))), ('quote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(help_text='Geef hier een citaat in', label='Citaat', max_length=150, required=True)), ('person', wagtail.wagtailcore.blocks.CharBlock(help_text='Van wie is dit citaat?', label='Auteur', max_length=28, required=True)))))), verbose_name='Blog inhoud')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
    ]
